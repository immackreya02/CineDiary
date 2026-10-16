# CineDiary 🎬 — Personal Movie Watchlist & Rating System

> A sleek, high-performance web application for film enthusiasts to curate custom movie collections, track watched films with ratings and reviews, discover global cinema live via TMDB, and inspect personal viewing habits with interactive 12-month analytics.

---

## 🛠️ Technology Stack (Python Web Frameworks Project)

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3, Flask (`app.py`, URL Routing, Jinja2 Templates) |
| **Database** | MongoDB (NoSQL) via PyMongo driver |
| **Template Engine** | Flask Jinja2 (`templates/` directory, `url_for('static', ...)` static files) |
| **Styling & Presentation** | Vanilla CSS3 (`static/css/styles.css`), Glassmorphism UI, Light/Dark Theme |
| **External API** | The Movie Database (TMDB Live API) |

---

## 📁 Project Structure

```
NoSQL Database Project/
│
├── app.py                  # Main Flask application, URL Routing & Jinja2 Templates
├── db.py                   # PyMongo database connection & serialization helpers
├── utils.py                # Password hashing & email verification helpers
├── requirements.txt        # Python package dependencies (Flask, PyMongo, Werkzeug)
├── .env                    # Environment variables configuration
│
├── static/                 # Flask Static Files Directory
│   ├── css/
│   │   └── styles.css      # Core stylesheet & Light/Dark theme engine
│   └── js/
│       ├── api.js          # REST API communication helpers
│       └── common.js       # Toast notifications & Theme switcher
│
└── templates/              # Flask Jinja2 Templates Directory
    ├── index.html          # Movie Search & Catalogue Grid
    ├── movie_details.html  # Movie Info, Interactive 5-Star Rating & Reviews
    ├── diary.html          # Personal Movie Diary & Watchlist Filters
    ├── lists.html          # Curated Film Collections & Add/Remove Film Modals
    ├── stats.html          # Personal Cinema Analytics Dashboard
    ├── profile.html        # User Profile, Bio Editor & Activity Shelf
    ├── login.html          # Sign In & Registration Forms
    └── verify_otp.html     # Email OTP Verification
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/)
- [MongoDB Community Server](https://www.mongodb.com/try/download/community) running locally on port `27017`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Server
```bash
python app.py
```
*(Open your web browser at `http://localhost:5001` to view the application)*
