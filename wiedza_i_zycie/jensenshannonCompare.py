
class jensenshannonCompare:

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

    def analyze_articles(self):

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