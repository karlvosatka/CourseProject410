# Description: Function used to build sentiment analysis model
# Created by Rui Mao at 2022-11-15
# Reference: https://www.nltk.org ;https://www.cs.cornell.edu/people/pabo/movie-review-data/ ; https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3 ; https://joblib.readthedocs.io/en/latest/

import nltk
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC
from sklearn import model_selection
import joblib
import time


start_time = time.time()

# Get all the words used in movie review and ranked them according to their frequency
ranked_words = nltk.FreqDist(movie_reviews.words())

# Use top 20000 words as features, exculde first 20 words as stopwords.
features = list(ranked_words)[20:20020]

# Write features to a text file
try:
    file = open("features.txt","w")

    print("Creating features...")
    file.write(str(features))
    file.close()
    print("Feature vector created successfully and saved to features.txt")
except:
    print("Failed to create features file")

# docs which include all movie reviews
docs = []
for file in movie_reviews.fileids():
    for cat in movie_reviews.categories(file):
        docs.append((movie_reviews.words(file),cat))


def create_feature_map(review):
    """
    :param review: ['This','is','review','one']
    :return:   feature_map: {'This':False,'is':True,'review':False,'one':True}
    """

    feature_map = {}
    for feature in features:
        label = feature in review # label is either True or False
        feature_map[feature] = label
    return feature_map

print("Creating feature map, this may take hours...")

try:# creating feature map for all reviews
    all_feature_map = []
    for (review,cat) in docs:
        all_feature_map.append((create_feature_map(review),cat))

    print("Feature map created successfully.")
except:
    print("Failed to create feature map")


# Model training
train_set,test_set = model_selection.train_test_split(all_feature_map,test_size = 0.05)

model = SklearnClassifier(SVC(kernel = 'linear'))

print("Begin training the model...")
model.train(train_set)

print("Model training finished")

# Save the trained model
try:
    #model_file = open('model.pickle','wb')
    joblib.dump(model,'model.pkl')
    print("trained model saved as model.pkl ")
except:
    print("failed to save the model")

# Check the testing accuracy
acc = nltk.classify.accuracy(model, test_set)
print('The testing accuracy : {}'.format(acc))

print("---time lapsed %s seconds ---" % (time.time() - start_time))
