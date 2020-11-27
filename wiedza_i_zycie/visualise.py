
import numpy as np

import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim
from gensim.models import CoherenceModel


class Visualise:

    def __init__(
            self,
            dictionary,
            corpus,
            lda,
            wiz_df,
            histogram_path,
            pydavis_path,
    ):

        self.dictionary = dictionary
        self.corpus = corpus
        self.lda = lda
        self.wiz_df = wiz_df
        self.histogram_path = histogram_path
        self.pydavis_path = pydavis_path

    def show_topics(self, lda):
        print(lda.show_topics(num_topics=10, num_words=20))
        # print(printlda.show_topic(topicid=4, topn=20))

    def print_document_lengths(self):
        self.wiz_df['doc_len'] = self.wiz_df[
            'tokenized_articles'].apply(lambda x: len(x))
        doc_lengths = list(self.wiz_df['doc_len'])

        print(
            "length of list:", len(doc_lengths),
            "\naverage document length", np.average(self.wiz_df['doc_len']),
            "\nminimum document length", min(self.wiz_df['doc_len']),
            "\nmaximum document length", max(self.wiz_df['doc_len']))

    def plot_histogram_of_lengths(self):
        self.wiz_df['doc_len'] = self.wiz_df[
            'tokenized_articles'].apply(lambda x: len(x))
        doc_lengths = list(self.wiz_df['doc_len'])
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

        print('\nPerplexity: ', self.lda.log_perplexity(self.corpus))

        coherence_model = CoherenceModel(
            model=self.lda,
            texts=self.wiz_df['tokenized_articles'],
            dictionary=self.dictionary,
            coherence='c_v'
        )
        coherence = coherence_model.get_coherence()
        print('\nCoherence Score: ', coherence)

    def make_pyDavis_visualization(self):

        vis = pyLDAvis.gensim.prepare(self.lda, self.corpus, self.dictionary)
        pyLDAvis.save_html(vis, self.pydavis_path)

    def choes_best_model(self, models):
        sorted_mods = sorted(models, key=lambda k: k['coherence'])

        print(sorted_mods[-1]['coherence'])
        # for mod in models:
        #     print(mod['coherence'])
