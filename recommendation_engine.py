import pickle
import pandas as pd

# =====================================================
# LOAD DATA
# =====================================================

with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# =====================================================
# PREPARE DATA
# =====================================================

movies = movies.reset_index(drop=True)

movies["title_lower"] = movies["title"].str.lower()

# =====================================================
# GET ALL MOVIES
# =====================================================

def get_all_movies():

    return sorted(
        movies["title"].tolist()
    )

# =====================================================
# GET MOVIE ID
# =====================================================

def get_movie_id(title):

    movie = movies[
        movies["title_lower"] == title.lower()
    ]

    if movie.empty:

        return None

    return int(movie.iloc[0]["movie_id"])

# =====================================================
# GET MOVIE TITLE
# =====================================================

def get_movie_title(movie_id):

    movie = movies[
        movies["movie_id"] == movie_id
    ]

    if movie.empty:

        return None

    return movie.iloc[0]["title"]
# =====================================================
# RECOMMEND MOVIES
# =====================================================

def recommend(movie_name, top_n=5):

    movie_name = movie_name.lower()

    movie = movies[
        movies["title_lower"] == movie_name
    ]

    if movie.empty:

        return []

    movie_index = movie.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        enumerate(distances),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i in movie_list[1:top_n + 1]:

        index = i[0]

        recommendations.append({

            "movie_id": int(
                movies.iloc[index]["movie_id"]
            ),

            "title": movies.iloc[index]["title"],

            "similarity": round(
                float(i[1]),
                4
            )
        })

    return recommendations


# =====================================================
# SEARCH MOVIES
# =====================================================

def search_movies(query):

    query = query.lower()

    result = movies[
        movies["title_lower"].str.contains(
            query,
            na=False
        )
    ]

    return result["title"].tolist()


# =====================================================
# TOTAL MOVIES
# =====================================================

def total_movies():

    return len(movies)


# =====================================================
# OPTIONAL TEST
# =====================================================

if __name__ == "__main__":

    print("Total Movies :", total_movies())

    print()

    recommendations = recommend("Avatar")

    for movie in recommendations:

        print(movie)