class tfModel():
    '''
    Usage:
        import pandas as pd
        import gensim
        ...
        m = tfModel('questions_with_tags.csv')
        query = 'Programming languages supporting functional programming'
        similar_documents = m.get_similar_documents(query, num_results=10)
    '''
    def __init__(self, question_file):
        qs = pd.read_csv(question_file)
        qs = qs.fillna(value={'new_tags': ''})
        raw_documents = qs['title'] + qs['new_tags']
        # sample to smaller number of documents
        raw_documents = raw_documents[0:10000]
        qs = qs[0:10000]
        self.questions = qs
        tokenized_docs = [[w.lower() for w in word_tokenize(text)] 
                            for text in raw_documents]
        self.dictionary = gensim.corpora.Dictionary(tokenized_docs)
        corpus = [self.dictionary.doc2bow(tokenized_doc) for tokenized_doc in tokenized_docs]
        tf_idf = gensim.models.TfidfModel(corpus)
        self.tf_idf = tf_idf
        self.similarity_checker = gensim.similarities.Similarity("",self.tf_idf[corpus],num_features=len(self.dictionary))
    
    def get_similar_documents(self, query, num_results=5, threshold=0.10):
        tokenized_query = [w.lower() for w in word_tokenize(query)]
        query_bag_of_words = self.dictionary.doc2bow(tokenized_query)
        query_tf_idf = self.tf_idf[query_bag_of_words]
        question_similarities = self.similarity_checker[query_tf_idf]
        print("Q Similarities", len(question_similarities), question_similarities)

        # Display similar questions from the past:

        questions_copy = self.questions.copy()
        questions_copy['similarity'] = question_similarities
        questions_above_threshold_similarity = questions_copy[questions_copy['similarity'] >= threshold]
        questions_above_threshold_similarity = questions_above_threshold_similarity.sort_values('similarity',ascending=False)
        
        return questions_above_threshold_similarity['title'].head(num_results)