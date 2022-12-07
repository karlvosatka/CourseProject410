
# Description: Function used to build trigram model with multiple training algorithms.
# Created by Rui Mao at 2022-11-15
# Reference and code snippets from below links：
# https://www.nltk.org ;https://www.cs.cornell.edu/people/pabo/movie-review-data/ ;
# https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3 ;
# https://joblib.readthedocs.io/en/latest/
# https://realpython.com/python-nltk-sentiment-analysis/

import nltk
from nltk.corpus import movie_reviews
from sklearn import model_selection
import time




from sklearn.naive_bayes import (
    BernoulliNB,
    ComplementNB,
    MultinomialNB,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier



start_time = time.time()



positive_trigram_finder = nltk.collocations.TrigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["pos"])
    if w.isalpha()
])
negative_trigram_finder = nltk.collocations.TrigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["neg"])
    if w.isalpha()
])



#common_set = set(pos_trigram_list).intersection(neg_trigram_list)
common_set2 = set(positive_trigram_finder.ngram_fd).intersection((negative_trigram_finder.ngram_fd))
print (len(common_set2))
#print(bigram_features)

for trigram in common_set2:
    del positive_trigram_finder.ngram_fd[trigram]
    del negative_trigram_finder.ngram_fd[trigram]

top_N_pos_bigram = {trigram for trigram, freq in positive_trigram_finder.ngram_fd.most_common(2500)}
top_N_neg_bigram = {trigram for trigram, freq in negative_trigram_finder.ngram_fd.most_common(2500)}

print(top_N_pos_bigram)
print("**************************")
#print(top_250_neg_bigram)

features = top_N_pos_bigram.union(top_N_neg_bigram)

docs = []
for file in movie_reviews.fileids():
    for cat in movie_reviews.categories(file):
        docs.append((movie_reviews.words(file),cat))


def create_feature_map(review):
    """
    :param review: ['This','is','review','one']
    :return:   feature_map: {'This':False,'is':True,'review':False,'one':True}
    """
    trigram = nltk.collocations.TrigramCollocationFinder.from_words(review)



    feature_map = {}
    for feature in features:
        label = feature in trigram.ngram_fd # label is either True or False
        feature_map[feature] = label
    return feature_map
#
print("Creating feature map, this may take hours...")

try:# creating feature map for all reviews
    all_feature_map = []
    for (review,cat) in docs:
        all_feature_map.append((create_feature_map(review),cat))

    print("Feature map created successfully.")
except:
    print("Failed to create feature map")

# Below Code snippet from https://realpython.com/python-nltk-sentiment-analysis/
classifiers = {
    "BernoulliNB": BernoulliNB(),
    "ComplementNB": ComplementNB(),
    "MultinomialNB": MultinomialNB(),
    "KNeighborsClassifier": KNeighborsClassifier(),
    "DecisionTreeClassifier": DecisionTreeClassifier(),
    "RandomForestClassifier": RandomForestClassifier(),
    "LogisticRegression": LogisticRegression(),
    "MLPClassifier": MLPClassifier(max_iter=1000),
    "AdaBoostClassifier": AdaBoostClassifier(),
}
#Model training
train_set,test_set = model_selection.train_test_split(all_feature_map,test_size = 0.2)



for name, sklearn_classifier in classifiers.items():
    classifier = nltk.classify.SklearnClassifier(sklearn_classifier)
    classifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print(F"{accuracy:.2%} - {name}")