import pandas as pd

ratings = pd.read_csv("ratings_export.csv")
mean_rev_score = ratings["rating_val"].mean()
print(mean_rev_score)