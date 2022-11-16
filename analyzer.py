# Description: Function used to running sentiment analysis for new reviews
# Created by Rui Mao at 2022-11-15
# Reference: https://www.nltk.org ;https://www.cs.cornell.edu/people/pabo/movie-review-data/ ; https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3 ; https://joblib.readthedocs.io/en/latest/


import nltk
import joblib
import ast
from nltk.classify.scikitlearn import SklearnClassifier


# Read feature_vector from generated feature_vector.txt

try:
    with open("features.txt","r") as feature_file:
        content = feature_file.read().splitlines()
except:
    print("Can't find the file.")

features = ast.literal_eval(content[0])

#print('bad' in features)


# Read fetched movie reviews and put into reviews_list:
try:
    reviews_file = open("reviews.txt",'r')
    fetched_reviews = reviews_file.readlines()
except:
    print("fetching reviews, please wait")

reviews_list = []  # [['This','is','review','one'],['This','is','review','two']]
for review in fetched_reviews:
    res = review.split()
    reviews_list.append(res)


# Function to create feature_map for each review
def create_feature_map(review):
    """
    :param review: ['This','is','review','one']
    :return:   feature_map: {'This':False,'is':True,'review':False,'one':True}
    """

    feature_map = {}
    for feature in features:
        label = feature in review
        feature_map[feature] = label
    return feature_map


# Create feature map for all fetched reviews
try:
    all_feature_map = []
    for review in reviews_list:
        all_feature_map.append((create_feature_map(review)))
except:
    print("failed to create feature map")

# load the pre-trained model
model = joblib.load('model.pkl')

# make prediction
prediction = model.classify_many(all_feature_map)
print(prediction)
