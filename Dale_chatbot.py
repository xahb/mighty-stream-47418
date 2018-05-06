# -*- coding: utf-8 -*-
"""
Created on Thu May  3 20:37:36 2018

@author: xahb
"""

import pandas as pd
good=pd.read_csv('/home/xahb/Py data/clahelpbot_sup/good.tsv', sep='\t')

print(good.sample(3))

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer=TfidfVectorizer()
vectorizer.fit(good.context_0)

matrix_big=vectorizer.transform(good.context_0)
print(matrix_big.shape)

from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=300)

svd.fit(matrix_big)

matrix_small = svd.transform(matrix_big)

print(matrix_small.shape)

print(svd.explained_variance_ratio_.sum())


import numpy as np
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator

def softmax(x):
    proba=np.exp(-x)
    return proba / sum(proba)

class NeighborSampler(BaseEstimator):
    def __init__(self, k=5, temperature=1.0):
        self.k=k
        self.temperature=temperature
    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)
    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p=softmax(distance * self.temperature)))
        return self.y_[result]
            

from sklearn.pipeline import make_pipeline

ns = NeighborSampler()
ns.fit(matrix_small, good.reply)
pipe = make_pipeline(vectorizer, svd, ns)

print(pipe.predict(['сколько тебе лет'])[0])


# dumps
import pickle
with open('dale_chatbot2.pickle', 'wb') as handle:
    pickle.dump(pipe, handle, protocol=2)

