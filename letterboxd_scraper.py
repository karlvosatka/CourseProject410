import sys
import requests
import json
import re
from bs4 import BeautifulSoup

def letterboxd_scrape(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'referer': 'https://google.com',
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    item = {}

    title = soup.find('meta', {'property': 'og:title'}).get('content')
    rating = soup.find('meta', {'name': 'twitter:data2'}).get('content')
    rating = float(rating.split(" ")[0])*2
    if rating > 6.488350645011941: #derived from Kaggle dataset (https://www.kaggle.com/datasets/samlearner/letterboxd-movie-ratings-data?select=ratings_export.csv)
        rating_sentiment = "pos"
    else:
        rating_sentiment = "neg"
    year = soup.find('small', {'class': 'number'}).text

    item['title'] = title
    item['release year'] = year
    item['rating'] = rating
    item['rating sentiment'] = rating_sentiment


    movie = url.split('/')[-2]

    r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/', headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    #find score for each review. if not given, set as -1
    review_scores = []
    review_scores_data = soup.find_all('div', {'class': 'attribution-block'})
    for j in range(len(review_scores_data)):
        score_data = review_scores_data[j].find('span')['class']
        if 'rating' in score_data:
            review_scores.append(int(score_data[2][6:]))
        else:
            review_scores.append(-1)
    
    #grab full review links
    full_rev_links = [("https://letterboxd.com" + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]
    
    #scrape first page of reviews
    rev_texts = []
    for link in full_rev_links:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        rev = soup.find('body').text
        rev_texts.append(rev)
    
    
    #repeat for 10 total pages
    i = 2
    while (i <= 10):
        #change page
        r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/page/{i}/', headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')

        #pull review scores for each review
        review_scores_data = soup.find_all('div', {'class': 'attribution-block'})
        for j in range(len(review_scores_data)):
            score_data = review_scores_data[j].find('span')['class']
            if 'rating' in score_data:
                review_scores.append(int(score_data[2][6:]))
            else:
                review_scores.append(-1)

        full_rev_links = [('https://letterboxd.com' + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]

        for link in full_rev_links:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            rev = soup.find('body').text
            rev_texts.append(rev)
        
        i += 1

    #average review according to kaggle dataset is 6.488350645011941, so we consider pos as >= 6.5, neg as < 6.5. account for not given scores
    review_sentiments = ['not given' if s == -1 else 'neg' if s < 6.5 else 'pos' for s in review_scores]

    
    for i in range(len(rev_texts)):
        #remove all characters besides letters
        rev_texts[i] = re.sub(r'[^\w]', ' ', rev_texts[i])

        #make all chars lowercase
        rev_texts[i] = rev_texts[i].lower()

    item['reviews'] = rev_texts
    item['review scores'] = review_scores
    item['review sentiments'] = review_sentiments
    
    #create json file with all data
    with open(f'{movie}.json', 'w') as f:
        json.dump(item, f,  indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s letterboxd_url", file=sys.stderr)
    elif sys.argv[1].find("https://letterboxd.com/film/") == None:
        print("Error: Incorrect URL format", file=sys.stderr)
    else:
        letterboxd_scrape(sys.argv[1])
