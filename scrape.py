import requests
from bs4 import BeautifulSoup
import pprint

'''
Scrapping data from websites. In this project, we access the "Hacker News" website and use BeautifulSoup
to parse the website content in order to filter the news with most votes.
'''

LINK_TO_HN = 'https://news.ycombinator.com/news'

def get_hn_pages(num_pages:str, main_link:str):
    mega_titles = []
    mega_subtxts = []
    for i in range(int(num_pages)):
        res = requests.get(f'{main_link}?p={i+1}')
        print(f'We\'ve got page {i+1} data. Processing...')
        soup = BeautifulSoup(res.text, 'html.parser')
        titles_list = soup.select('.titleline > a') ## catches all titles from each news and its vote scores
        subtexts_list = soup.select('.subtext')

        mega_titles+=titles_list
        mega_subtxts+=subtexts_list
    return mega_titles, mega_subtxts


def sort_stories_by_votes(news_list:list):
    return sorted(news_list, key= lambda k: k['votes'], reverse=True)

def create_custom_hn(titles:list, subtexts:list):
    hn = []
    for idx, item in enumerate(titles):
        title = item.getText()
        href = item.get('href', None)

        vote = subtexts[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


if __name__ == '__main__':
    num_pages = input('Welcome to Hacker News filtered!!! Insert the number of pages that you want us to scrape on: \t')
    try:
        mega_titles, mega_subtxts = get_hn_pages(num_pages, LINK_TO_HN)
        pprint.pprint(create_custom_hn(mega_titles, mega_subtxts))
    except TypeError as e:
        print('Could not execute. Insert a integer number!!!', e)
