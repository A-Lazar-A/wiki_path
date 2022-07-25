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
    links = html.select('#mw-content-text')[0].find_all(href=href_wiki_not_jpg)
    print(f'{title.text}\n{link}\n')
    try:
        recursive_following(main_url + choice(links)['href'], steps, main_url)
    except:
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
    This is the program that shows one a path made in required amount of steps from the provided Wikipedia article
    to a random one
    Two or more words write separated by _ (World_War)
    """
    print(text2art('Wiki Path'))
    url = 'https://en.wikipedia.org/wiki/'

    if language == 'ru':
        url = 'https://ru.wikipedia.org/wiki/'
    try:
        recursive_following(url + request, steps, url[:-6])
    except:
        print('OOOPS, try again')


if __name__ == '__main__':
    wiki_path()
