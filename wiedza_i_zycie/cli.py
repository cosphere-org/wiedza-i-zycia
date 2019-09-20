
import json
import os

import click

from .scraper import WiedzaIZycieScraper


def get_scraper():
    return WiedzaIZycieScraper(
        main_url=os.environ['MAIN_URL'],
        editions_url=os.environ['EDITION_LIST_PAGE'],
        request_lag_seconds=float(os.environ['REQUEST_LAG_SECONDS']))


@click.command()
def scrape_all_and_save():
    get_scraper().scrape_and_save()


@click.command()
@click.argument('url')
def scrape_edition(url):
    click.secho(
        json.dumps(
            get_scraper().get_edition_data(url),
            indent=4,
            sort_keys=True),
        fg='white')


@click.command()
@click.argument('url')
def scrape_article(url):
    click.secho(
        json.dumps(
            get_scraper().get_article_data(url),
            indent=4,
            sort_keys=True),
        fg='white')


@click.group()
def cli():
    """Expose multiple commands allowing one to work with lily_assistant."""

    pass


cli.add_command(scrape_all_and_save)
cli.add_command(scrape_edition)
cli.add_command(scrape_article)
