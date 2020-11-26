
import numpy as np
from scipy.spatial import distance


class JensenshannonCompare:

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

    def get_similar(self, t_df, lda, corpus, dictionary, article_index):

        t_df['documents_distributions'] = [
            [tup[1] for tup in lst] for lst in lda[corpus]]

        docDistribution = self.getDocDistribution(
            article_index,
            t_df,
            dictionary,
            lda)

        sorted_sim_items = self.get_list_of_similar(
            docDistribution, np.array(t_df['documents_distributions']))

        # print(t_df['title'][int(list(sorted_sim_items.keys())[1])])
        # print(t_df['title'][int(list(sorted_sim_items.keys())[0])])

        return t_df['title'][int(list(sorted_sim_items.keys())[1])]
