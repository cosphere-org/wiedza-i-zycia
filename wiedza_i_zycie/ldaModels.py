
import gensim
import numpy as np
from gensim.models import CoherenceModel, LdaModel
from scipy.spatial import distance

from .prepareAndTokenize import PrepareAndTokenize


class LdaModels:

    def __init__(
            self,
            mallet_path,
    ):

        self.mallet_path = mallet_path

    def train_mallet(self, **kwargs):

        num_topics = 20

        articles = kwargs['data']['tokenized_articles']
        # articles = [[t for t in a if t is not None] for a in articles]
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

    def combine_models(self, **kwargs):

        dictionary = kwargs['dictionary']
        corpus = kwargs['corpus']
        articles = kwargs['wiz_df']['tokenized_articles']

        params = {
            'num_topics': {
                'start': 2,
                'limit': 50,
                'step': 4,
            },
            'chunksize': {
                'start': 10,
                'limit': 500,
                'step': 50,
            },
            'minimum_probability': {
                'start': 0.0,
                'limit': 0.5,
                'step': 0.1,
            },
        }

        model_params = {
            'corpus': corpus,
            'num_topics': 20,
            'id2word': dictionary,
            'alpha': 'auto',
            'eta': 'auto',
            'chunksize': 300,
            'minimum_probability': 0.0,
        }
        
        models = []

        for param in params:
            for param in params.values():
                for value in range(
                    param['start'], param['limit'], param['step']):

                    model_params[param] = value
                    model = LdaModel(**model_params)

                    coherencemodel = CoherenceModel(
                        model=model,
                        texts=texts,
                        dictionary=dictionary,
                        coherence='c_v'
                    )
                    models.append(
                        {
                            'coherence': coherencemodel.get_coherence(),
                            'model': model,
                            'params': model_params,
                        }
                    )
        return models

    def choes_best_model(self, **kwargs):
        models = kwargs['models']
        return sorted(models, key=lambda k: k['coherence'])[0]
