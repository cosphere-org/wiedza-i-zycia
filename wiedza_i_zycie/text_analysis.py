
import os
import pickle
import re

import gensim
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel
# from gensim.models.wrappers import LdaMallet
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from scipy.spatial import distance
from stempel import StempelStemmer
from stop_words import get_stop_words


from functools import wraps


class TextAnalyzer:

    def __init__(
            self,
            text_df,
            corpus_path,
            dictionary_path,
            lda_path,
            tokenized_text_df_path,
            trained_df_path,
            mallet_path,
            pydavis_file,
            histogram_path,
            coherence_values_path,
            model_list_path,
        ):

        self.text_df = text_df
        self.stemmer = StempelStemmer.default()
        self.corpus_path = corpus_path
        self.dictionary_path = dictionary_path
        self.lda_path = lda_path
        self.tokenized_text_df_path = tokenized_text_df_path
        self.trained_df_path = trained_df_path
        self.mallet_path = mallet_path
        self.pydavis_file = pydavis_file
        self.histogram_path = histogram_path
        self.coherence_values_path = coherence_values_path
        self.model_list_path = model_list_path

    #
    # TOKENIZATION
    #

    def clean_and_lowercase(self, text):
        text = re.sub(
            "((\S+)?(http(s)?)(\S+))|((\S+)"\
            "?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
        text = re.sub("[^a-zA-Z ]", "", text)
        text = text.lower()
        return text

    def tokenize_text(self, text):
        return word_tokenize(text)

    def remove_stop_words(self, text):
        stop_words = get_stop_words('pl')
        return [w for w in text if not w in stop_words]

    def steam_text(self, text):
        text = [self.stemmer.stem(word) for word in text]
        return text

    def prepare_text(self, text):
        text = self.clean_and_lowercase(text)
        text = self.tokenize_text(text)
        text = self.remove_stop_words(text)
        return self.steam_text(text)

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
        return df

    def prepare_and_tokenize(self, **kwargs):

        nltk.download('punkt')
        wiz_df = self.get_prepared_paragraphs()
        freq_d = self.get_num_of_words(wiz_df)

        wiz_df['tokenized_articles'] = wiz_df[
            'tokenized_articles'].apply(self.keep_50_words, freq_dist=freq_d)

        return self.keep_only_long_articles(wiz_df)

    #
    # TRAIN_FUNCTIONS
    #

    def train_lda(self, **kwargs):

        num_topics = 10
        chunksize = 300

        articles = kwargs['data']['tokenized_articles']
        articles = [[t for t in a if t is not None] for a in articles]
        dictionary = corpora.Dictionary(articles)
        corpus = [dictionary.doc2bow(doc) for doc in articles]

        # low alpha means each document is only
        # represented by a small number of topics
        # low eta means each topic is only
        # represented by a small number of words
        lda = LdaModel(
            corpus=corpus,
            num_topics=num_topics,
            id2word=dictionary,
            alpha=1e-2,
            eta=0.5e-2,
            chunksize=chunksize,
            minimum_probability=0.0,
            passes=2)
        return dictionary, corpus, lda

    def train_mallet(self, **kwargs):

        num_topics = 20

        articles = kwargs['data']['tokenized_articles']
        articles = [[t for t in a if t is not None] for a in articles]
        dictionary = corpora.Dictionary(articles)
        corpus = [dictionary.doc2bow(doc) for doc in articles]

        ldamallet = gensim.models.wrappers.LdaMallet(
            self.mallet_path,
            corpus=corpus,
            num_topics=num_topics,
            id2word=dictionary,
        )
        ## todo default-jdk
        model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(ldamallet)

        return dictionary, corpus, model

    
    #
    # GET_FUNCTIONS
    #

    def getDocDistribution(self, article_index, train_df, dictionary, lda):
        bow = dictionary.doc2bow(
            [world for world in
                train_df.iloc[article_index, 1] if world is not None])
        return np.array([tup[1] for tup in lda.get_document_topics(bow=bow)])

    def get_list_of_similar(self, query, matrix):

        sim_items = dict()
        for count, value in enumerate(
                [distance.jensenshannon(data, query) for data in matrix]):
            sim_items[f'{count}'] = value
        return {k: v for k, v in sorted(
            sim_items.items(), key=lambda item: item[1])}

    def get_train_df(self, **kwargs):

        train_df = None
        msk = np.random.rand(len(kwargs['wiz_df'])) < 0.9
        msk[0] = True
        train_df = kwargs['wiz_df'][msk]
        train_df.reset_index(drop=True, inplace=True)
        return train_df

    def load_from_files(self, path_list):

        files_list = []
        for path in path_list:
            entity = None
            if(os.path.isfile(path)):
                with open(path, 'rb') as file:
                    entity = pickle.load(file)
            files_list.append(entity)
        return files_list

    #
    # SAVE_FUNCTIONS
    #

    def save_files(self, file_list, path_list):

        for entity, path in zip(file_list, path_list):
            with open(path, 'wb') as file:
                pickle.dump(entity, file)    

    #
    # REMOVE_FUNCTIONS
    #

    def reset_model(self):

        files = [
            self.corpus_path,
            self.dictionary_path,
            self.lda_path,
            self.trained_df_path
        ]
        self.remove_files(files)

    def reset_df(self):
        self.remove_files(self.tokenized_text_df_path)

    def remove_files(self, files):

        for file in files:
            if os.path.isfile(file):
                os.remove(file)

    def analyze_articles(self):

        '''
        decorator function:
            arguments:
            list of files to load from
            function to run if files dont exist
            dataframe to train model if files dont exist
        '''
        [w_df,] = self.extract_resources([self.tokenized_text_df_path])(self.prepare_and_tokenize)(some='')
        [t_df,] = self.extract_resources([self.trained_df_path])(self.get_train_df)(wiz_df=w_df)
        files = [self.corpus_path, self.dictionary_path, self.lda_path]
        dictionary, corpus, lda = self.extract_resources(files)(self.train_lda)(data=t_df)

        
        t_df['documents_distributions'] = [
            [tup[1] for tup in lst] for lst in lda[corpus]]

        random_article_index = np.random.randint(len(t_df))
        docDistribution = self.getDocDistribution(
            random_article_index,
            t_df,
            dictionary,
            lda)

        sorted_sim_items = self.get_list_of_similar(
            docDistribution, np.array(t_df['documents_distributions']))

        print(t_df['title'][int(list(sorted_sim_items.keys())[1])])
        print(t_df['title'][int(list(sorted_sim_items.keys())[0])])

    #
    # SHOW_FUNCTIONS
    #

   

    def show_topics(self, lda):
        print(lda.show_topics(num_topics=10, num_words=20))
        # print(printlda.show_topic(topicid=4, topn=20))

    def print_document_lengths(self):
        wiz_df = self.get_tokenized_text_df()
        wiz_df['doc_len'] = wiz_df[
            'tokenized_articles'].apply(lambda x: len(x))
        doc_lengths = list(wiz_df['doc_len'])

        print(
            "length of list:", len(doc_lengths),
            "\naverage document length", np.average(wiz_df['doc_len']),
            "\nminimum document length", min(wiz_df['doc_len']),
            "\nmaximum document length", max(wiz_df['doc_len']))

    def plot_histogram_of_lengths(self):
        wiz_df = self.get_tokenized_text_df()
        wiz_df['doc_len'] = wiz_df[
            'tokenized_articles'].apply(lambda x: len(x))
        doc_lengths = list(wiz_df['doc_len'])
        num_bins = 1000
        fig, ax = plt.subplots(figsize=(12, 6))
        n, bins, patches = ax.hist(doc_lengths, num_bins)
        ax.set_xlabel('Document Length (tokens)', fontsize=15)
        ax.set_ylabel('Normed Frequency', fontsize=15)
        ax.grid()
        ax.set_xticks(np.logspace(
            start=np.log10(50), stop=np.log10(1000), num=8, base=10.0))
        plt.xlim(0, 1000)
        ax.plot(
            [np.average(doc_lengths) for i in np.linspace(
                0.0, 0.0035, 100)], np.linspace(0.0, 0.0035, 100), '-',
            label='average doc length')
        ax.legend()
        ax.grid()
        fig.tight_layout()
        plt.savefig(self.histogram_path)

    def model_perplexity_and_coherence(self):

        [w_df,] = self.extract_resources([self.tokenized_text_df_path])(self.prepare_and_tokenize)(some='')
        [t_df,] = self.extract_resources([self.trained_df_path])(self.get_train_df)(wiz_df=w_df)
        files = [self.corpus_path, self.dictionary_path, self.lda_path]
        dictionary, corpus, lda = self.extract_resources(files)(self.train_lda)(data=t_df)
        # Compute Perplexity
        print('\nPerplexity: ', lda.log_perplexity(corpus)) 

        articles = wiz_df['tokenized_articles']
        articles = [[t for t in a if t is not None] for a in articles]

        # Compute Coherence Score
        coherence_model_lda = CoherenceModel(
            model=lda, texts=articles, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)

    def model_perplexity_and_coherence(self):

        [w_df,] = self.extract_resources([self.tokenized_text_df_path])(self.prepare_and_tokenize)(some='')
        [t_df,] = self.extract_resources([self.trained_df_path])(self.get_train_df)(wiz_df=w_df)
        files = [self.corpus_path, self.dictionary_path, self.lda_path]
        dictionary, corpus, lda = self.extract_resources(files)(self.train_lda)(data=t_df)

        print('\nPerplexity: ', lda.log_perplexity(corpus))

        articles = wiz_df['tokenized_articles']
        articles = [[t for t in a if t is not None] for a in articles]

        coherence_model = CoherenceModel(
            model=lda,
            texts=articles,
            dictionary=dictionary,
            coherence='c_v'
            )
        coherence = coherence_model.get_coherence()
        print('\nCoherence Score: ', coherence)


    def compute_coherence_values(
        self, 
        dictionary, 
        corpus, 
        texts, 
        limit=30, 
        start=2, 
        step=3):

        coherence_values = []
        model_list = []

        for num_topics in range(start, limit, step):
            # model = gensim.models.wrappers.LdaMallet(
            # # model = LdaModel(
            #     self.mallet_path,
            #     corpus=corpus,
            #     num_topics=num_topics,
            #     id2word=dictionary,
            # )
            model = LdaModel(
                corpus=corpus,
                num_topics=num_topics,
                id2word=dictionary,
                alpha=1e-2,
                eta=0.5e-2,
                chunksize=300,
                minimum_probability=0.0,
                passes=2)
            model_list.append(model)
            coherencemodel = CoherenceModel(
                model=model,
                texts=texts,
                dictionary=dictionary,
                coherence='c_v'
            )
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values

    def run_coh(self):

        [w_df,] = self.extract_resources([self.tokenized_text_df_path])(self.prepare_and_tokenize)(some='')
        [t_df,] = self.extract_resources([self.trained_df_path])(self.get_train_df)(wiz_df=w_df)

        articles = t_df['tokenized_articles']
        articles = [[t for t in a if t is not None] for a in articles]

        dictionary = corpora.Dictionary(articles)
        corpus = [dictionary.doc2bow(doc) for doc in articles]

        model_list, coherence_values = self.compute_coherence_values(
            dictionary,
            corpus,
            articles,
            )

        self.save_coh(coherence_values, model_list)
        print(coherence_values)

    def save_coh(self, coherence_values, model_list):

        with open(self.coherence_values_path, 'wb') as file:
            pickle.dump(coherence_values, file)
        with open(self.model_list_path, 'wb') as file:
            pickle.dump(model_list, file)

    def choes_model(self, coherence_values, model_list):
        return model_list[max(coherence_values)]



    def make_pyDavis_visualization(self):

        [w_df,] = self.extract_resources([self.tokenized_text_df_path])(self.prepare_and_tokenize)(some='')
        [t_df,] = self.extract_resources([self.trained_df_path])(self.get_train_df)(wiz_df=w_df)
        files = [self.corpus_path, self.dictionary_path, self.lda_path]
        dictionary, corpus, lda = self.extract_resources(files)(self.train_lda)(data=t_df)

        vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
        pyLDAvis.save_html(vis, self.pydavis_file)
    
    def extract_resources(self, resources_paths): 
    
        def Inner(func): 
            def wrapper(**kwargs): 
                resources_list = self.load_from_files(resources_paths)

                empty = False
                for resource in resources_list:
                    if resource is None:
                        empty = True
                ## todo can not use in list, becouse data frame
                if empty is True:
                    resources_list = func(**kwargs)
                    if(len(resources_paths)==1):
                        resources_list = [resources_list]
                    self.save_files(resources_list, resources_paths)
                return resources_list
            return wrapper 
        return Inner 
