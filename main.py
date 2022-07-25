import click
from art import text2art
from bs4 import BeautifulSoup
import requests
import re
from random import choice

def href_wiki_not_jpg(href):
    return href and re.compile('wiki').search(href) and not re.compile('.jpg').search(href)

def recursive_following(link, steps, main_url):
    if steps == 0:
        return
    steps -= 1

    response = requests.get(link)

    if response.status_code != 200:
        print(f'Something went wrong or there isn\'t any article, try again')
        return

    html = BeautifulSoup(response.content, 'lxml')

    title = html.find(id='firstHeading')
    links = html.find(id='bodyContent').find_all(href=href_wiki_not_jpg)
    print(f'{title.text}\n{link}\n')

    recursive_following(main_url + choice(links)['href'], steps, main_url)


@click.command('Wiki Path')
@click.argument('request')
@click.option('--language', '-l',
              type=click.Choice(['eng', 'ru']),
              help='Choose wiki language',
              default='eng')
@click.option('--steps', '-s', type=int, default=10, help='Choose number os steps')
def wiki_path(request, language, steps):
    """
    This is the program that shows to you what way you can go from provided article to another only with links in the
    articles

    """
    print(text2art('Wiki Path'))
    url = 'https://en.wikipedia.org/wiki/'

    if language == 'ru':
        url = 'https://ru.wikipedia.org/wiki/'

    recursive_following(url + request, steps, url[:-6])


if __name__ == '__main__':
    wiki_path()
