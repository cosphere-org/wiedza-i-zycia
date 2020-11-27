
import gensim
import numpy as np
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel

# from scipy.spatial import distance


class LdaModels:

    def __init__(
            self,
            mallet_path,
    ):

        self.mallet_path = mallet_path

    #
    # MALLET_MODEL
    #

    def train_mallet(self, **kwargs):

        num_topics = 20

        articles = kwargs['data']['tokenized_articles']
        dictionary = corpora.Dictionary(articles)
        corpus = [dictionary.doc2bow(doc) for doc in articles]

        ldamallet = gensim.models.wrappers.LdaMallet(
            self.mallet_path,
            corpus=corpus,
            num_topics=num_topics,
            id2word=dictionary,
        )

        model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(
            ldamallet)

        return dictionary, corpus, model

    #
    # COMBINE_AND_CHOSE_BEST_MODEL
    #

    def model_create(self, model_params, articles, dictionary):

        mod = []

        # print(model_params['num_topics'])
        # print(model_params['chunksize'])
        # print(model_params['minimum_probability'])
        model = LdaModel(**model_params)

        coherencemodel = CoherenceModel(
            model=model,
            texts=articles,
            dictionary=dictionary,
            coherence='c_v'
        )
        mod = {
            'coherence': coherencemodel.get_coherence(),
            'model': model,
            # 'params': model_params,
            'minimum_probability': model_params['minimum_probability'],
            'num_topics': model_params['num_topics'],
        }

        return mod

    def model_iterate(self, model_params, params, articles, dictionary, par):

        for val in np.arange(
                params[par]['start'],
                params[par]['limit'],
                params[par]['step'],
        ):
            model_params[par] = val
            yield self.model_create(model_params, articles, dictionary)

    def combine_models(self, **kwargs):

        dictionary = kwargs['dictionary']
        corpus = kwargs['corpus']
        articles = kwargs['wiz_df']['tokenized_articles']

        params = {
            'num_topics': {
                'start': 2,
                'limit': 80,
                'step': 4,
            },
            'minimum_probability': {
                'start': 0.1,
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

        for model in self.model_iterate(
            model_params,
            params,
            articles,
            dictionary,
            'minimum_probability',
        ):
            models.append(model)

        mod = sorted(models, key=lambda k: k['coherence'])[-1]
        model_params['minimum_probability'] = mod['minimum_probability']

        for model in self.model_iterate(
            model_params,
            params,
            articles,
            dictionary,
            'num_topics',
        ):
            models.append(model)

        return models
