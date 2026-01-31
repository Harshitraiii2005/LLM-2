import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec

def bow_vectorizer(texts, max_features=1000):
    vectorizer = CountVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(texts).toarray()
    return pd.DataFrame(X, columns=vectorizer.get_feature_names_out())

def word2vec_vectorizer(texts, vector_size=100, sg=0):
    sentences = texts.apply(lambda x: x.split())
    model = Word2Vec(
        sentences,
        vector_size=vector_size,
        window=3,
        min_count=2,
        sg=sg,
        workers=4
    )

    def sentence_vector(tokens):
        vectors = [model.wv[w] for w in tokens if w in model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(vector_size)

    X = np.array([sentence_vector(tokens) for tokens in sentences])
    return pd.DataFrame(X)
