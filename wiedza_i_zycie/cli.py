
import json
import os

import click
import numpy as np

from .fileOperations import FileOperations
from .jensenshannonCompare import JensenshannonCompare
from .ldaModels import LdaModels
from .prepareAndTokenize import PrepareAndTokenize
from .scraper import WiedzaIZycieScraper
from .visualise import Visualise


def get_scraper():
    return WiedzaIZycieScraper(
        main_url=os.environ['MAIN_URL'],
        editions_url=os.environ['EDITION_LIST_PAGE'],
        request_lag_seconds=float(os.environ['REQUEST_LAG_SECONDS'])
    )


def get_prepare_and_tokenize():
    return PrepareAndTokenize(
        text_df=get_scraper().get_articles_df()
    )


def get_models():

    return LdaModels(
        mallet_path=os.environ['MALLET_PATH'],
    )


def get_visualize():

    dictionary, corpus, lda, wiz_df = run_analisys()

    return Visualise(
        dictionary, corpus, lda, wiz_df,
        os.environ['HISTOGRAM_PATH'],
        os.environ['PYDAVIS_VIS_FILE'],
    )


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


@click.command()
def make_pyDavis_visualization():
    get_visualize().make_pyDavis_visualization()


@click.command()
def print_document_lengths():
    get_visualize().print_document_lengths()


@click.command()
def plot_histogram_of_lengths():
    get_visualize().plot_histogram_of_lengths()


@click.command()
def reset_model():
    files = [
        os.environ['CORPUS_PATH'],
        os.environ['DICTIONARY_PATH'],
        os.environ['LDA_PATH'],
        os.environ['TRAINED_DF_PATH'],
    ]
    FileOperations(
        files,
        None,
    ).remove_files(files)


@click.command()
def reset_df():
    FileOperations(
        [os.environ['TOKENIZED_PATH']],
        None,
    ).remove_files([os.environ['TOKENIZED_PATH']])


@click.command()
def model_perplexity_and_coherence():
    get_visualize().model_perplexity_and_coherence()


@click.command()
def get_similar_article():

    dictionary, corpus, lda, wiz_df = run_analisys()
    random_article_index = np.random.randint(len(wiz_df))

    JensenshannonCompare().get_similar(
        wiz_df, lda, corpus, dictionary, random_article_index)


@click.command()
def run_analisys():

    [w_df, ] = FileOperations(
        path_list=[os.environ['TOKENIZED_PATH']],
        file_list=None,
    ).extract_resources(
        get_prepare_and_tokenize().prepare_and_tokenize
    )()

    [t_df, ] = FileOperations(
        path_list=[os.environ['TRAINED_DF_PATH']],
        file_list=None,
    ).extract_resources(
        get_prepare_and_tokenize().get_train_df
    )(wiz_df=w_df)

    files = [
        os.environ['CORPUS_PATH'],
        os.environ['DICTIONARY_PATH'],
    ]

    dic, cor = FileOperations(
        path_list=files,
        file_list=None,
    ).extract_resources(
        get_prepare_and_tokenize().get_corpus_and_dictionary
    )(wiz_df=t_df)

    [mods, ] = FileOperations(
        path_list=[os.environ['MODEL_LIST_PATH']],
        file_list=None,
    ).extract_resources(
        get_models().combine_models
    )(dictionary=dic, corpus=cor, wiz_df=t_df)

    model = FileOperations(
        path_list=[os.environ['LDA_PATH']],
        file_list=None,
    ).extract_resources(
        get_models().choes_best_model
    )(models=mods)

    return dic, cor, model, t_df


cli.add_command(scrape_all_and_save)
cli.add_command(scrape_edition)
cli.add_command(scrape_article)
cli.add_command(make_pyDavis_visualization)
cli.add_command(print_document_lengths)
cli.add_command(plot_histogram_of_lengths)
cli.add_command(reset_model)
cli.add_command(reset_df)
cli.add_command(model_perplexity_and_coherence)
cli.add_command(run_analisys)
