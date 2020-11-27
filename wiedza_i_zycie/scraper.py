
import json
import os
import re
import time
import pandas as pd

from bs4 import BeautifulSoup
import click
import requests

from .image import Image


class WiedzaIZycieScraper:

    def __init__(self, main_url, editions_url, request_lag_seconds):
        self.main_url = main_url
        self.editions_url = editions_url
        self.request_lag_seconds = request_lag_seconds

    #
    # ENTRYPOINT
    #
    def scrape_and_save(self):

        click.secho('[STARTING SCRAPER]', fg='green')

        self.save_editions(self.get_editions_data())

        click.secho('[SCRAPER DONE]', fg='green')

    def get_editions_data(self):

        edition_urls = self.get_urls_by_pattern(
            self.get_page(self.editions_url), '(10,.+html)$')

        return [
            self.get_edition_data(url)
            for url in edition_urls
        ]

    def save_editions(self, editions):

        path = os.path.join(
            os.path.dirname(__file__), 'data', 'editions.js')

        with open(path, 'w') as f:
            f.write(
                'data = ' + json.dumps(
                    editions,
                    indent=4,
                    sort_keys=True))

    def get_articles_df(self):
        path = os.path.join(
            os.path.dirname(__file__), 'data', 'editions.json')

        if(os.path.isfile(path)):
            with open(path) as json_file:
                data = json.load(json_file)
            return pd.DataFrame(data)
        else:
            click.secho('[JSON NOT FOUND, RUN SCRAPER]', fg='red')

    #
    # EDITION
    #
    def get_edition_data(self, url):

        click.secho('\n\n[EDITION]', fg='yellow')

        edition_summary = self.get_page(
            re.sub(r'\/(\d{2}),', '/19,', url, flags=re.IGNORECASE))
        date = self.get_edition_date(edition_summary)

        click.secho(f'url: {url}', fg='yellow')
        click.secho(f'date: {date}', fg='yellow')

        return {
            'url': url,
            'table_of_contents': (
                self.get_edition_table_of_contents(edition_summary)),
            'date': date,
            'image': (
                Image(self.main_url, edition_summary, 'maxi-pokaz-cz')
                .download()),
            'articles': self.get_articles_data(url),
        }

    def get_edition_table_of_contents(self, edition):

        toc = []
        summary_div = edition.find('div', class_='box-czasopisma-pokaz')
        if summary_div:
            table = summary_div.find(
                'div', attrs={'style': 'margin-bottom: 15px'})

            if table:
                pretty_table = BeautifulSoup(
                    re.sub(r'<br\/>|<\/em>|<em>|\n', '', str(table)),
                    'html.parser')

            for strong in pretty_table.find_all('strong'):
                toc.append({
                    'title': str(strong.text),
                    'sub_title': str(strong.next_sibling)
                })

        return toc

    def get_edition_date(self, edition):

        edition_title_date = edition.find(
            'div',
            attrs={'style': 'margin-top: 0px;'})

        if edition_title_date:
            edition_date = re.findall(
                r'\d{2}/[12]\d{3}', str(edition_title_date.get_text()))

            return edition_date[0]

    #
    # ARTICLE
    #
    def get_articles_data(self, edition_url):

        articles_urls = self.get_urls_by_pattern(
            self.get_page(edition_url), '8,.+html')

        return [
            self.get_article_data(article_url)
            for article_url in articles_urls
        ]

    def get_article_data(self, url):

        click.secho('\n[ARTICLE]', fg='blue')

        article = self.get_page(url)
        author, date, paragraphs = self.get_article_elements(article)
        title = self.get_article_title(article)

        click.secho(f'url: {url}', fg='blue')
        click.secho(f'title: {title}', fg='blue')
        click.secho(f'author: {author}', fg='blue')
        click.secho(f'date: {date}', fg='blue')

        return {
            'url': url,
            'title': title,
            'author': author,
            'date': date,
            'paragraphs': paragraphs,
            'image': (
                Image(self.main_url, article, 'maxi-pokaz')
                .download()),
        }

    def get_article_title(self, article):

        try:
            return article.title.get_text()

        except AttributeError:
            return None

    def get_article_elements(self, article):

        paragraphs = []
        author = None
        date = None

        try:
            article_div = article.find('div', class_='box-teksty-pokaz')

        except AttributeError:
            return author, date, paragraphs

        else:

            added = article_div.find('div', class_='dodano-2').get_text()
            if added:

                # -- author
                author_match = re.search(
                    r'(Autor: (?P<author>(\w+[\s-])+\w+))', added)
                if author_match:
                    author = author_match.group('author')

                # -- date
                date_match = re.search(
                    r'(dodano: (?P<date>(\d+[,-:\.\s]){3}))', added)
                if date_match:
                    date = date_match.group('date')

            # -- paragraphs
            for paragraph_text in article_div.find_all('p'):
                paragraphs.append(paragraph_text.get_text())

        return author, date, paragraphs

    #
    # GENERAL
    #
    def get_urls_by_pattern(self, page, pattern):

        pattern = re.compile(pattern)

        return set([
            os.path.join(self.main_url, a.attrs['href'])
            for a in page.find_all('a', href=pattern)
            if 'href' in a.attrs
        ])

    def get_page(self, url):

        time.sleep(self.request_lag_seconds)
        return BeautifulSoup(requests.get(url).content, 'html.parser')
