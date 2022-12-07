# Description: Function used to running sentiment analysis for new reviews
# Created by Rui Mao at 2022-11-29
# Modified by Karl Vosatka: (Add accuracy function, support JSON, finallize output)
# Reference and code snippets from below links:
# https://www.nltk.org ;https://www.cs.cornell.edu/people/pabo/movie-review-data/ ;
# https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3 ;
# https://realpython.com/python-nltk-sentiment-analysis/
# https://joblib.readthedocs.io/en/latest/

import sys
import json
import nltk
import joblib
import ast
from nltk.sentiment import SentimentIntensityAnalyzer


def analyzer(threshold):
    """
    The analyzer used to perform sentiment analysis.

    :param threshold: reviews longer than threshold will be processed by pretrained bigram model, otherwise by NLTK VADER
    :Output: Review Statistics
    """

    vader = SentimentIntensityAnalyzer()
    short_review_list = []
    reviews_list = []  # [['This','is','review','one'],['This','is','review','two']]
    review_threshold = threshold
    vader_pos_counter = 0
    vader_neg_counter = 0
    max_pos_score = 0
    max_neg_score = 0
    neu = 0

    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.extend([word.lower() for word in nltk.corpus.names.words()])

    print("Start Sentiment Analysis...")
    try:
        with open("MNB_Bigram_features.txt","r") as feature_file:
            content = feature_file.read().splitlines()
    except:
        print("Can't find the file.")


    features = ast.literal_eval(content[0])

    try:
        review_file = open(sys.argv[1] + ".json")
        movie_data = json.load(review_file)
    except:
        print("fetching movie data, please wait")

    #fetch data from scaper json file
    movie_title = movie_data["title"]
    overall_rating = movie_data["rating"]
    fetched_reviews = movie_data["reviews"]
    rating_sentiment = movie_data["rating sentiment"]
    review_score_sentiments = movie_data["review sentiments"]
    reviews_list_indices = []
    analyzer_sentiments = ["init"] * len(fetched_reviews)

    #score short reviews (i.e. less than 200 words) using VADER
    review_counter = 0
    for review in fetched_reviews:
        res = review.split()
        if len(res) < review_threshold:
            short_review_list.append(res)
            score = vader.polarity_scores(' '.join(res))

            if score['pos'] > max_pos_score:
                max_pos_score = score['pos']
                most_pos_short_review = ' '.join(res)
            if score['neg'] > max_neg_score:
                max_neg_score = score['neg']
                most_neg_short_review = ' '.join(res)

            if score['pos'] == score['neg']:
                vader_pos_counter += 0
                vader_neg_counter += 0
                neu += 1
                analyzer_sentiments[review_counter] = "not given"
            elif score['pos'] > score['neg']:
                analyzer_sentiments[review_counter] = "pos"
                vader_pos_counter += 1
            else:
                analyzer_sentiments[review_counter] = "neg"
                vader_neg_counter += 1

        else:
            analyzer_sentiments[review_counter] = "binom"
            reviews_list_indices.append(review_counter)
            reviews_list.append(res)
        
        review_counter += 1
        

    try:  # creating feature map for all reviews
        all_feature_map = []
        for review in reviews_list:


            bigram = nltk.collocations.BigramCollocationFinder.from_words(word for word in review if word not in stopwords)
            feature_map = {}
            for feature in features:
                label = feature in bigram.ngram_fd  # label is either True or False
                feature_map[feature] = label
            all_feature_map.append(feature_map)

        print("Feature map created successfully.")
    except:
        print("Failed to create feature map")

    model = joblib.load('MultinomialNB.pkl')

    # make mass predictions
    prediction = model.classify_many(all_feature_map)
    for i in range(len(prediction)):
        rev_index = reviews_list_indices[i]
        analyzer_sentiments[rev_index] = prediction[i]
    bi_pos_counter = prediction.count('pos')
    bi_neg_counter = prediction.count('neg')

    total_pos = vader_pos_counter + bi_pos_counter
    total_neg = vader_neg_counter + bi_neg_counter
    total = total_neg + total_pos

    #check accuracy per review by comparing per-review model results to review score sentiment indication as compared to average for letterboxd.com
    if len(analyzer_sentiments) != len(review_score_sentiments):
        print("Error: mismatch in reviews")
        accuracy_per_review = -1
    else:
        matching_score = 0
        matching_total = 0
        for i in range(len(analyzer_sentiments)):
            if analyzer_sentiments[i] == "not given" or review_score_sentiments[i] == "not given":
                continue
            else:
                if analyzer_sentiments[i] == review_score_sentiments[i]:
                    matching_score += 1
                matching_total += 1
        accuracy_per_review = matching_score / matching_total

    #compare overall sentiment of model to average user rating score for movie
    if total_pos > total_neg:
        overall_sentiment = "pos"
    else:
        overall_sentiment = "neg"
    overall_accuracy = overall_sentiment == rating_sentiment

    #write results to output txt file
    with open(f'{sys.argv[1]}.txt', 'w') as f:
        print("Movie: ", movie_title, file=f)
        print("Average User Rating", overall_rating, file=f)
        print("Total Analyzed Reviews:", total + neu,
          "Positive Reviews:", total_pos,
          "Negative Reviews:", total_neg, sep='\n', file=f)

        if total_pos > total_neg:
            print("Overall Sentiment: Positive", file=f)
        else:
            print("Overall Sentiment: Negative", file=f)

        print("Max Positive Score:", max_pos_score,
                "Most Positive Short Reviews: ", most_pos_short_review,
                "Max Negative Score:", max_neg_score,
                "Most Negative Short Reviews: ", most_neg_short_review, sep="\n", file=f)
        if overall_accuracy:
            print("The model accurately predicted the overall user rating", file=f)
        else:
            print("The model DID NOT accurately predict the average rating", file=f)
        print("Per-Review Accuracy:", accuracy_per_review, sep="\n", file=f)


if __name__ == "__main__":
    review_threshold = 200 # reviews longer than 200 words will be processed by bigram model, otherwise by vader
    analyzer(review_threshold)


