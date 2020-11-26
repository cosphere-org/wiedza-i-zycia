
import re

import nltk
import numpy as np
import pandas as pd
from gensim import corpora
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from stempel import StempelStemmer
from stop_words import get_stop_words


class PrepareAndTokenize:

    def __init__(self, text_df):

        self.text_df = text_df
        self.stemmer = StempelStemmer.default()

    #
    # CLEAN_TEXT
    #

    def clean_and_lowercase(self, text):
        ts = '''
        ((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)
        '''
        text = re.sub(ts, " ", text)
        text = re.sub("[^a-zA-Z ]", "", text)
        text = text.lower()
        return text

    def remove_stop_words(self, text):
        stop_words = get_stop_words('pl')
        return [w for w in text if not w in stop_words]

    def steam_text(self, text):
        text = [self.stemmer.stem(word) for word in text]
        return text

    def prepare_text(self, text):
        text = self.clean_and_lowercase(text)
        text = word_tokenize(text)
        text = self.remove_stop_words(text)
        return self.steam_text(text)
    
    #
    # GET_DATAFRAME_WITH_CLEANED_TEXT
    #

    def get_prepared_paragraphs(self):
        articles_texts = []
        articles_titles = []
        for _, edition in self.text_df.iterrows():
            for article in edition['articles']:
                article_paragraphs = ''.join(article['paragraphs'])
                articles_texts.append(self.prepare_text(article_paragraphs))
                articles_titles.append(article['title'])
        return pd.DataFrame(
            {'title': articles_titles, 'tokenized_articles': articles_texts})

    def get_num_of_words(self, df):
        all_words = [word for item in list(
            df['tokenized_articles']) for word in item]
        return FreqDist(all_words)

    #
    # GET_DATAFRAME_PREPARED_FOR_LDA_MODEL
    #

    def keep_50_words(self, text, freq_dist):
        num_of_worlds = len(freq_dist)
        top_5 = int(0.05 * num_of_worlds)
        bottom_10 = int(0.1 * num_of_worlds)
        if (num_of_worlds > 100000):
            num_of_worlds = num_of_worlds - int(
                num_of_worlds * (num_of_worlds / 100000))

        top_5_worlds, _ = zip(*freq_dist.most_common(top_5))
        top_5_worlds = list(top_5_worlds)
        bottom_10_worlds, _ = zip(*freq_dist.most_common(bottom_10))
        bottom_10_worlds = list(bottom_10_worlds)

        words, _ = zip(*freq_dist.most_common(num_of_worlds))
        words = list(words)

        worlds = [word for word in text if word not in (
            top_5_worlds or bottom_10_worlds)]
        return [word for word in worlds if word in words]

    def keep_only_long_articles(self, wiz_df):
        df = wiz_df[wiz_df['tokenized_articles'].map(len) >= 40]
        df = wiz_df[wiz_df['tokenized_articles'].map(type) == list]
        df.reset_index(drop=True, inplace=True)
        df['tokenized_articles'] = [
            [t for t in a if t is not None] for a in wiz_df[
                'tokenized_articles']]

        return df

    def prepare_and_tokenize(self, **kwargs):

        wiz_df = kwargs['wiz_df']
        nltk.download('punkt')
        wiz_df = self.get_prepared_paragraphs()
        freq_d = self.get_num_of_words(wiz_df)

        wiz_df['tokenized_articles'] = wiz_df[
            'tokenized_articles'].apply(self.keep_50_words, freq_dist=freq_d)

        return self.keep_only_long_articles(wiz_df)

    #
    # GET_RANDOMIZED_TRAINING_DATAFRAME
    #

    def get_train_df(self, **kwargs):

        wiz_df = kwargs['wiz_df']

        train_df = None
        msk = np.random.rand(len([wiz_df])) < 0.9
        msk[0] = True
        train_df = wiz_df[msk]
        train_df.reset_index(drop=True, inplace=True)
        return train_df

    #
    # GET_MODEL_PARTS
    #

    def get_corpus_and_dictionary(self, **kwargs):

        wiz_df = kwargs['wiz_df']

        articles = wiz_df['tokenized_articles']
        dictionary = corpora.Dictionary(articles)
        corpus = [dictionary.doc2bow(doc) for doc in articles]

        return dictionary, corpus
