import requests
import json
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
    #cast = [cast.text for cast in soup.find_all('a', {'class': 'text-slug tooltip'})]
    #directors = [directors.text for directors in soup.find_all('span', {'class': 'prettify'})]
    rating = soup.find('meta', {'name': 'twitter:data2'}).get('content')
    #genres = soup.find('div', {'class': 'text-sluglist capitalize'})
    #genres = [genres.text for genres in genres.find_all('a', {'class': 'text-slug'})]
    #producers = soup.find_all('div', {'class': 'text-sluglist'})[2]
    #producers = [producers.text for producers in producers.find_all('a')]
    #writers = soup.find_all('div', {'class': 'text-sluglist'})[3]
    #writers = [writers.text for writers in writers.find_all('a')]
    year = soup.find('small', {'class': 'number'}).text

    item['title'] = title
    item['release year'] = year
    #item['director(s)'] = directors
    #item['cast'] = cast
    item['rating'] = rating
    #item['genres'] = genres
    #item['producer(s)'] = producers
    #item['writer(s)'] = writers


    movie = url.split('/')[-2]

    """
    r = requests.get(f'https://letterboxd.com/esi/film/{movie}/stats/', headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')


    watched_by = soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'}).text
    listed_by = soup.find('a', {'class': 'has-icon icon-list icon-16 tooltip'}).text
    liked_by = soup.find('a', {'class': 'has-icon icon-like icon-liked icon-16 tooltip'}).text

    item['watched by'] = watched_by
    item['listed by'] = listed_by
    item['liked by'] = liked_by """

    r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/', headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    """ 
    NAIVE VERSION -- FASTER, WILL NOT SCRAPE LARGER REVIEWS
    
    i = 2
    all_reviews = []
    while(i < 6):

        #grab reviews for current page
        pop_reviews = soup.find_all('li', {'class': 'film-detail'})
        
        pop_reviews = [pr.text for pr in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]
        all_reviews.append(pop_reviews)

        #set up next page
        r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/page/{i}/', headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        i += 1

    item['popular reviews'] = all_reviews """
    
    #grab full review links
    full_rev_links = [("https://letterboxd.com" + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]
    #print(full_revs_links)
    
    rev_texts = []
    #parse full review links
    i = 2
    while (i < 6):
        #TODO - ability to scrape the actual rating of the review for pre-training and later general reference

        for link in full_rev_links:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'lxml')
            rev = soup.find('body').text
            rev_texts.append(rev)
        r = requests.get(f'https://letterboxd.com/film/{movie}/reviews/by/activity/page/{i}/', headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        full_rev_links = [("https://letterboxd.com" + link.get('data-full-text-url')) for link in soup.find_all('div', {'class': 'body-text -prose collapsible-text'})]
        i += 1

    #TODO - add review pre-processing to the scraper itself!

    item['popular reviews'] = rev_texts
    
    with open(f'{movie}.json', 'w') as f:
        json.dump(item, f,  indent=2)

letterboxd_scrape('https://letterboxd.com/film/the-matrix/')