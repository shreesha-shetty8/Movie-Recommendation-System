# 🎬 AI Movie Recommendation System

An AI-powered Movie Recommendation System built using **Machine Learning**, **Streamlit**, **TMDB API**, and **Google Gemini AI**.

The application recommends similar movies based on content similarity and provides AI-powered insights such as movie summaries, reviews, fun facts, recommendation explanations, and interactive movie Q&A.

---

# ✨ Features

- 🎬 Content-Based Movie Recommendation
- 🤖 AI Movie Summary
- 💬 Ask AI about any movie
- 🎉 AI Fun Facts
- ⭐ AI Movie Reviews
- 🧠 Why Recommended? (AI Explanation)
- 🎥 Movie Details (Poster, Cast, Director, Genres & Rating)
- 🔥 Top 5 Similar Movie Recommendations
- 🌐 Real-time TMDB API Integration
- 🎨 Modern Dark UI with Streamlit

---

# 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- TMDB API
- Google Gemini AI

---

# 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py
├── recommendation_engine.py
├── tmdb.py
├── utils.py
├── create_pickle.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── README.md
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
└── .streamlit/
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/shreesha-shetty8/Movie-Recommendation-System.git
```

### Go to the project folder

```bash
cd Movie-Recommendation-System
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add API Keys

Create the following file:

```text
.streamlit/secrets.toml
```

Add your API keys:

```toml
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

### Run the application

```bash
streamlit run app.py
```

---

# 📸 Screenshots

> Add screenshots of the application here after deployment.

---

# 🚀 Future Enhancements

- 👤 User Authentication
- ❤️ Favorite Movies
- 📺 Watchlist
- 🎞️ Movie Trailer Integration
- 🤝 Hybrid Recommendation System
- 📈 Personalized Recommendations

---

# 👨‍💻 Author

**Shreesha Shetty**

- 🐙 GitHub: https://github.com/shreesha-shetty8
- 💼 LinkedIn: https://www.linkedin.com/in/shreesha-shetty8/

---

⭐ If you like this project, consider giving it a **Star** on GitHub!