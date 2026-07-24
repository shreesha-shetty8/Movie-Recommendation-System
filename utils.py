import streamlit as st
import google.generativeai as genai

# -------------------------------------------------------
# GEMINI CONFIG
# -------------------------------------------------------

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ GEMINI_API_KEY not found in .streamlit/secrets.toml")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")


# -------------------------------------------------------
# AI SUMMARY
# -------------------------------------------------------

@st.cache_data(show_spinner=False)
def generate_summary(movie_name):

    prompt = f"""
You are a professional movie reviewer.

Write a spoiler-free summary of the movie "{movie_name}".

Include:
1. Genre
2. Story
3. Why people like it

Keep it under 150 words.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No response received from Gemini."

    except Exception as e:
        return f"❌ Gemini Error:\n{str(e)}"


# -------------------------------------------------------
# WHY RECOMMENDED
# -------------------------------------------------------

@st.cache_data(show_spinner=False)
def explain_recommendation(selected_movie, recommended_movie):

    prompt = f"""
The user selected:

{selected_movie}

Recommended Movie:

{recommended_movie}

Explain in 3-5 lines why this movie is recommended.

Do not spoil either movie.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No explanation generated."

    except Exception as e:
        return f"❌ Gemini Error:\n{str(e)}"


# -------------------------------------------------------
# ASK AI
# -------------------------------------------------------

def ask_movie_ai(movie_name, question):

    prompt = f"""
Movie:
{movie_name}

Question:
{question}

Rules:
- Do not spoil the movie.
- Keep answer under 120 words.
- Answer naturally.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No answer generated."

    except Exception as e:
        return f"❌ Gemini Error:\n{str(e)}"


# -------------------------------------------------------
# MOVIE FACT
# -------------------------------------------------------

@st.cache_data(show_spinner=False)
def fun_fact(movie_name):

    prompt = f"""
Tell one interesting fact about the movie "{movie_name}".

Only one paragraph.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No fact generated."

    except Exception as e:
        return f"❌ Gemini Error:\n{str(e)}"


# -------------------------------------------------------
# QUICK REVIEW
# -------------------------------------------------------

@st.cache_data(show_spinner=False)
def quick_review(movie_name):

    prompt = f"""
Write a short review of "{movie_name}".

Maximum 80 words.

No spoilers.
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No review generated."

    except Exception as e:
        return f"❌ Gemini Error:\n{str(e)}"