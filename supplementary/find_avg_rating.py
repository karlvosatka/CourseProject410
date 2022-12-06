#the "ratings_export.csv" file referenced below is from a kaggle dataset of letterboxd reviews site wide. This file calculates the average rating sitewide for each movie,
#which we reference as the cutoff point for labelling a rating score as positive of negative throughout the software.
#Kaggle link: https://www.kaggle.com/datasets/samlearner/letterboxd-movie-ratings-data?select=ratings_export.csv
import pandas as pd

ratings = pd.read_csv("ratings_export.csv")
mean_rev_score = ratings["rating_val"].mean()
print(mean_rev_score)
