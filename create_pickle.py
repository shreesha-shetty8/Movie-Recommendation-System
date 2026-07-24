import pandas as pd
import pickle
import ast
import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download once
nltk.download("punkt", quiet=True)

ps = PorterStemmer()


# -----------------------------
# Helper Functions
# -----------------------------

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])


def convert(text):
    items = []

    try:
        for i in ast.literal_eval(text):
            items.append(i["name"])
    except:
        pass

    return items


def fetch_cast(text):
    cast = []

    try:
        counter = 0

        for i in ast.literal_eval(text):
            if counter != 3:
                cast.append(i["name"])
                counter += 1
            else:
                break
    except:
        pass

    return cast


def fetch_director(text):

    director = []

    try:
        for i in ast.literal_eval(text):

            if i["job"] == "Director":
                director.append(i["name"])
                break
    except:
        pass

    return director


# -----------------------------
# Load Dataset
# -----------------------------

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")
movies = movies.head(1000)
# -----------------------------
# Keep Useful Columns
# -----------------------------

movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
    ]
]

movies.dropna(inplace=True)

# -----------------------------
# Feature Engineering
# -----------------------------

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(fetch_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces

movies["genres"] = movies["genres"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["cast"] = movies["cast"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies["crew"] = movies["crew"].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# Create Tags

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

new_movies = movies[["movie_id", "title", "tags"]]

new_movies["tags"] = new_movies["tags"].apply(lambda x: " ".join(x))
new_movies["tags"] = new_movies["tags"].apply(lambda x: x.lower())

# -----------------------------
# Text Processing
# -----------------------------

new_movies["tags"] = new_movies["tags"].apply(stem)

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(new_movies["tags"]).toarray()

import numpy as np

similarity = cosine_similarity(vectors).astype(np.float32)


# -----------------------------
# Save Pickle Files
# -----------------------------

pickle.dump(
    new_movies,
    open("movies.pkl", "wb")
)

pickle.dump(
    similarity,
    open("similarity.pkl", "wb")
)

print("=" * 50)
print("movies.pkl created successfully")
print("similarity.pkl created successfully")
print("=" * 50)