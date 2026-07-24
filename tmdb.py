import streamlit as st
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =====================================================
# TMDB CONFIG
# =====================================================

API_KEY = st.secrets["TMDB_API_KEY"]

BASE_URL = "https://api.themoviedb.org/3"

POSTER_URL = "https://image.tmdb.org/t/p/w500"

# =====================================================
# REQUEST SESSION
# =====================================================

session = requests.Session()

retry = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry)

session.mount("https://", adapter)
session.mount("http://", adapter)

session.headers.update({
    "User-Agent": "MovieRecommendationSystem/1.0"
})

# =====================================================
# SEARCH MOVIE
# =====================================================

@st.cache_data(ttl=86400)
# =====================================================
# SEARCH MOVIE
# =====================================================

@st.cache_data(ttl=86400)
def search_movie(title):

    try:

        url = f"{BASE_URL}/search/movie"

        params = {
            "api_key": API_KEY,
            "query": title
        }

        response = session.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        # ------------------------------------------------
        # 1. Exact title match
        # ------------------------------------------------

        for movie in results:

            if movie.get("title", "").strip().lower() == title.strip().lower():

                return movie

        # ------------------------------------------------
        # 2. Original title match
        # ------------------------------------------------

        for movie in results:

            if movie.get("original_title", "").strip().lower() == title.strip().lower():

                return movie

        # ------------------------------------------------
        # 3. Choose the oldest release (helps for Avatar,
        #    Batman, etc. instead of newest sequels)
        # ------------------------------------------------

        results.sort(
            key=lambda x: x.get("release_date", "9999-12-31")
        )

        return results[0]

    except Exception as e:

        print("TMDB Search Error:", e)

        return None
# =====================================================
# GET MOVIE DETAILS
# =====================================================

@st.cache_data(ttl=86400)
def get_movie_details(movie_id):

    try:

        url = f"{BASE_URL}/movie/{movie_id}"

        params = {
            "api_key": API_KEY
        }

        response = session.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print("Movie Details Error:", e)

        return None
# =====================================================
# GET MOVIE CREDITS
# =====================================================

@st.cache_data(ttl=86400)
def get_movie_credits(movie_id):

    try:

        url = f"{BASE_URL}/movie/{movie_id}/credits"

        params = {
            "api_key": API_KEY
        }

        response = session.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print("Credits Error:", e)

        return None


# =====================================================
# COMPLETE MOVIE INFORMATION
# =====================================================

@st.cache_data(ttl=86400)
def get_complete_movie(movie_title):

    search = search_movie(movie_title)

    if search is None:
        return None

    movie_id = search["id"]

    details = get_movie_details(movie_id)

    credits = get_movie_credits(movie_id)

    if details is None:
        return None

    poster = None

    if details.get("poster_path"):

        poster = POSTER_URL + details["poster_path"]

    # -------------------------
    # Director
    # -------------------------

    director = "Not Available"

    if credits:

        for person in credits.get("crew", []):

            if person.get("job") == "Director":

                director = person.get("name")

                break

    # -------------------------
    # Cast
    # -------------------------

    cast = []

    if credits:

        for actor in credits.get("cast", [])[:5]:

            cast.append(actor.get("name"))

    # -------------------------
    # Genres
    # -------------------------

    genres = []

    for genre in details.get("genres", []):

        genres.append(genre["name"])
    # =====================================================
    # RETURN COMPLETE MOVIE DATA
    # =====================================================

    return {

        "id": movie_id,

        "title": details.get("title", "Unknown"),

        "poster": poster,

        "rating": details.get("vote_average", "N/A"),

        "release_date": details.get("release_date", "N/A"),

        "overview": details.get(
            "overview",
            "No overview available."
        ),

        "runtime": details.get("runtime", "N/A"),

        "language": details.get(
            "original_language",
            "N/A"
        ).upper(),

        "genres": ", ".join(genres),

        "director": director,

        "cast": cast,

        "vote_count": details.get("vote_count", 0),

        "popularity": details.get("popularity", 0),

        "homepage": details.get("homepage", ""),

        "tagline": details.get("tagline", "")
    }


# =====================================================
# OPTIONAL TEST
# =====================================================

if __name__ == "__main__":

    movie = get_complete_movie("Avatar")

    from pprint import pprint

    pprint(movie)