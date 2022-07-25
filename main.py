import click
from art import text2art
from bs4 import BeautifulSoup
import requests
from random import choice


@click.command('Wiki Path')
@click.argument('request')
@click.option('--language', '-l',
              type=click.Choice(['eng', 'ru']),
              help='Choose wiki language (ru and eng are required)',
              default='eng')
@click.option('--steps', '-s', type=int, default=10, help='Choose number os steps')
def wiki_path(request, language, steps):
    """
    This is the program that shows to you what way you can go from provided article to another only with links in the
    articles
    :param request: Wiki article
    :param language: Provided language (ru or eng)
    """
    print(text2art('Wiki Path'))
    url_en = 'https://en.wikipedia.org/wiki/'
    url_ru = 'https://ru.wikipedia.org/wiki/'
    response = None
    if language == 'eng':
        response = requests.get(url_en + request)
    if language == 'ru':
        response = requests.get(url_ru + request)
    if response.status_code != 200:
        print('Something went wrong, try again')
        return
    else:
        print('Success', steps)

if __name__ == '__main__':
    wiki_path()
