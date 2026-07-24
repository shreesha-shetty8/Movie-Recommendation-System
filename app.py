import streamlit as st

from recommendation_engine import recommend, get_all_movies
from tmdb import get_complete_movie
from utils import (
    generate_summary,
    ask_movie_ai,
    fun_fact,
    quick_review,
    explain_recommendation
)

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

/* Main App */
.main {
    background-color: #0E1117;
}

/* Headers */
h1 {
    color: #FFD700;
    text-align: center;
}

h2, h3 {
    color: white;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 2px solid #FFD700;
    background-color: #262730;
    color: white;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #FFD700;
    color: black;
}

/* Selectbox */
div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Images */
img {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<h1>🎬 AI Movie Recommendation System</h1>

<h4 style="text-align:center; color:#CFCFCF;">
Discover your next favorite movie using
<b>Machine Learning</b> + <b>Google Gemini AI</b>
</h4>
""", unsafe_allow_html=True)

st.divider()

movie_list = get_all_movies()

selected_movie = st.selectbox(
    "Select Movie",
    movie_list
)
if st.button("Recommend Movies", use_container_width=True):

    st.session_state["selected_movie"] = get_complete_movie(selected_movie)

    st.session_state["recommendations"] = recommend(selected_movie)

    st.success("🎉 Recommendations generated successfully!")

# -------------------------------
# Selected Movie
# -------------------------------

if "selected_movie" in st.session_state:

    movie = st.session_state["selected_movie"]

    st.divider()
    st.markdown("## 🎥 Selected Movie")

    col1, col2 = st.columns([1, 2])

    with col1:
        if movie.get("poster"):
            st.image(movie["poster"], width=350)

    with col2:
        st.subheader(f'{movie.get("title", "Unknown")} ({movie.get("release_date", "")[:4]})')

        st.write(f"⭐ **Rating:** {movie.get('rating', 'N/A')} / 10")
        st.write(f"🎬 **Director:** {movie.get('director', 'Unknown')}")
        st.write(f"🎭 **Genres:** {movie.get('genres', 'Unknown')}")

        cast = movie.get("cast", [])
        if cast:
            st.write("👥 **Cast:** " + ", ".join(cast[:5]))

        st.write("### Overview")
        st.write(movie.get("overview", "No overview available."))
        st.divider()

        st.subheader("🤖 AI Assistant")

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📝 Summary",
                "💬 Ask AI",
                "🎉 Fun Fact",
                "⭐ Review"
            ]
        )

# ---------------- SUMMARY ----------------

        with tab1:

            if st.button("Generate Summary", key="summary_btn"):

                with st.spinner("Generating summary..."):

                    st.success(generate_summary(movie["title"]))

        # ---------------- ASK AI ----------------

        with tab2:

            question = st.text_input(
                "Ask anything about this movie",
                key="ask_ai_question"
            )

            if st.button("Ask AI", key="ask_ai_btn"):

                if question.strip():

                    with st.spinner("Thinking..."):

                        answer = ask_movie_ai(
                            movie["title"],
                            question
                        )

                    st.info(answer)

                else:

                    st.warning("Please enter a question.")

        # ---------------- FUN FACT ----------------

        with tab3:

            if st.button("Show Fun Fact", key="fun_fact_btn"):

                with st.spinner("Finding an interesting fact..."):

                    st.success(fun_fact(movie["title"]))

        # ---------------- REVIEW ----------------

        with tab4:

            if st.button("Generate Review", key="review_btn"):

                with st.spinner("Writing review..."):

                    st.info(quick_review(movie["title"]))



# -------------------------------
# Recommended Movies
# -------------------------------

if "recommendations" in st.session_state:

    st.divider()
    st.markdown("## 🔥 Top 5 Recommended Movies")

    recommendations = st.session_state["recommendations"]

    cols = st.columns(5)

    for i, movie in enumerate(recommendations):

        info = get_complete_movie(movie["title"])

        with cols[i]:

            if info and info.get("poster"):
                st.image(info["poster"], use_container_width=True)

            st.markdown(
    f"""
    <div style="
        background:#1E1E1E;
        padding:12px;
        border-radius:12px;
        text-align:center;
        min-height:70px;
        margin-top:8px;
    ">
        <h4 style="color:white; margin:0;">
            {movie['title']}
        </h4>
    </div>
    """,
    unsafe_allow_html=True
)

            if info:
                year = info.get("release_date", "")[:4]
                st.markdown(
                     f"""
                     <div style="text-align:center;">
                         ⭐ <b>{round(info.get('rating',0),1)}</b>/10
                        <br>
                        📅 {year}
                    </div>
                     """,
                    unsafe_allow_html=True
                )
                

            if st.button("View Details", key=f"details_{i}"):

                st.session_state["recommended_movie"] = info

            if st.button("🤖 Why Recommended?", key=f"why_{i}"):

                with st.spinner("Analyzing recommendation..."):

                    explanation = explain_recommendation(
                        st.session_state["selected_movie"]["title"],
                        movie["title"]
                    )

                st.info(explanation)
# -------------------------------
# Recommended Movie Details
# -------------------------------

if "recommended_movie" in st.session_state:

    movie = st.session_state["recommended_movie"]

    st.divider()
    st.markdown("## 🎬 Recommended Movie Details")

    col1, col2 = st.columns([1, 2])

    with col1:
        if movie.get("poster"):
            st.image(movie["poster"], use_container_width=True)

    with col2:

        st.subheader(movie["title"])

        st.write(f"⭐ **Rating:** {round(movie.get('rating',0),1)} / 10")
        st.write(f"🎬 **Director:** {movie.get('director','Unknown')}")
        st.write(f"🎭 **Genres:** {movie.get('genres','Unknown')}")

        cast = movie.get("cast", [])

        if cast:
            st.write("👥 **Cast:** " + ", ".join(cast[:5]))

        st.write("### Overview")
        st.write(movie.get("overview", "No overview available."))

        st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:25px; color:#BFBFBF;">

<h3 style="color:#FFD700;">🎬 AI Movie Recommendation System</h3>

<p>
Developed by <b>Shreesha Shetty</b>
</p>

<p>
<a href="https://github.com/shreesha-shetty8" target="_blank" style="text-decoration:none;">
🐙 GitHub
</a>
&nbsp;&nbsp;|&nbsp;&nbsp;
<a href="https://www.linkedin.com/in/shreesha-shetty8/" target="_blank" style="text-decoration:none;">
💼 LinkedIn
</a>
</p>

<p>
<b>Tech Stack</b><br>
Python • Streamlit • Scikit-learn • Pandas • TMDB API • Google Gemini AI
</p>

<p style="font-size:13px;">
© 2026 • Built with Machine Learning & AI
</p>

</div>
""", unsafe_allow_html=True)