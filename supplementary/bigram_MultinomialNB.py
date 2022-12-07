
# Description: Bigram model + MultinomialNB, output: model file and feature file
# Created by Rui Mao at 2022-11-15
# Reference and code snippets from below links：
# https://www.nltk.org ;https://www.cs.cornell.edu/people/pabo/movie-review-data/ ; 
# https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3 ; 
# https://joblib.readthedocs.io/en/latest/
# https://realpython.com/python-nltk-sentiment-analysis/



import nltk
from nltk.corpus import movie_reviews
from sklearn import model_selection
import joblib
import time




from sklearn.naive_bayes import (

    MultinomialNB,
)



start_time = time.time()

# Get all the words used in movie review and ranked them according to their frequency
ranked_words = nltk.FreqDist(movie_reviews.words())


positive_bigram_finder = nltk.collocations.BigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["pos"])
    if w.isalpha() 
])
negative_bigram_finder = nltk.collocations.BigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["neg"])
    if w.isalpha() 
])


common_set2 = set(positive_bigram_finder.ngram_fd).intersection((negative_bigram_finder.ngram_fd))
print (len(common_set2))


for bigram in common_set2:
    del positive_bigram_finder.ngram_fd[bigram]
    del negative_bigram_finder.ngram_fd[bigram]

top_250_pos_bigram = {bigram for bigram, freq in positive_bigram_finder.ngram_fd.most_common(4000)}
top_250_neg_bigram = {bigram for bigram, freq in negative_bigram_finder.ngram_fd.most_common(4000)}



print(top_250_pos_bigram)
print("**************************")


features = top_250_pos_bigram.union(top_250_neg_bigram)
#print(features)
# Write features to a text file
try:
    file = open("saved_features/MNB_Bigram_features2.txt","w")

    print("Creating features...")
    file.write(str(features))
    file.close()
    print("Features created successfully and saved to MNB_Bigram_features.txt")
except:
    print("Failed to create features file")

#docs which include all movie reviews
docs = []
for file in movie_reviews.fileids():
    for cat in movie_reviews.categories(file):
        docs.append((movie_reviews.words(file),cat))


def create_feature_map(review):
    """
    :param review: ['This','is','review','one']
    :return:   feature_map: {('This','is'):False,('is','review'):True,('review','one'):False}
    """
    bigram = nltk.collocations.BigramCollocationFinder.from_words(review)



    feature_map = {}
    for feature in features:
        label = feature in bigram.ngram_fd # label is either True or False
        feature_map[feature] = label
    return feature_map
#
print("Creating feature map, this may take some time...")

try:# creating feature map for all reviews
    all_feature_map = []
    for (review,cat) in docs:
        all_feature_map.append((create_feature_map(review),cat))

    print("Feature map created successfully.")
except:
    print("Failed to create feature map")



#Model training
train_set,test_set = model_selection.train_test_split(all_feature_map,test_size = 0.2)


classifier = nltk.classify.SklearnClassifier(MultinomialNB())
classifier.train(train_set)

# Save the trained model
try:

    joblib.dump(classifier,'saved_model/MultinomialNB2.pkl')
    print("trained model saved to /saved_model as MultinomialNB2.pkl ")
except:
    print("failed to save the model")
accuracy = nltk.classify.accuracy(classifier, test_set)
print(F"{accuracy:.2%} - MultinomialNB")