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
    year = soup.find('small', {'class': 'number'}).text

    item['title'] = title
    item['release year'] = year
    item['rating'] = rating


    movie = url.split('/')[-2]

    r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/', headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')
    
    #grab full review links
    full_rev_links = [("https://letterboxd.com" + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]

    #find score for each review. if not given, set as -1
    review_scores = []
    review_scores_data = soup.find_all('div', {'class': 'attribution-block'})
    for j in range(len(review_scores_data)):
        score_data = review_scores_data[j].find('span')['class']
        if 'rating' in score_data:
            review_scores.append(int(score_data[2][6:]))
        else:
            review_scores.append(-1)
    
    #parse full review links
    rev_texts = []
    i = 2
    while (i < 6):

        for link in full_rev_links:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            rev = soup.find('body').text
            rev_texts.append(rev)
        r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/page/{i}/', headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        full_rev_links = [('https://letterboxd.com' + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]

        #pull review scores for each review
        review_scores_data = soup.find_all('div', {'class': 'attribution-block'})
        for j in range(len(review_scores_data)):
            score_data = review_scores_data[j].find('span')['class']
            if 'rating' in score_data:
                review_scores.append(int(score_data[2][6:]))
            else:
                review_scores.append(-1)
        
        i += 1

    #average review according to kaggle dataset is 6.488350645011941, so we consider pos as >= 6.5, neg as < 6.5. account for not given scores
    review_binary = ['not given' if s == -1 else 'neg' if s < 6.5 else 'pos' for s in review_scores]

    
    for i in range(len(rev_texts)):
        #remove all characters besides letters
        rev_texts[i] = re.sub(r'[^\w]', ' ', rev_texts[i])

        #make all chars lowercase
        rev_texts[i] = rev_texts[i].lower()

    item['popular reviews'] = rev_texts
    item['popular review scores'] = review_scores
    item['popular review score binary'] = review_binary
    
    #create json file with all data
    with open(f'{movie}.json', 'w') as f:
        json.dump(item, f,  indent=2)

    #create text file with just full text reviews
    with open(f'{movie}.txt', 'w') as fp:
        for item in rev_texts:
            fp.write("%s\n" % item)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s letterboxd_url", file=sys.stderr)
    elif sys.argv[1].find("https://letterboxed.com/film/") == None:
        print("Error: Incorrect URL format", file=sys.stderr)
    else:
        letterboxd_scrape(sys.argv[1])
