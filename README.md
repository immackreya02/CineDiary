# CineDiary 🎬 — Personal Movie Watchlist & Rating System

> A sleek, high-performance web application for film enthusiasts to curate custom movie collections, track watched films with ratings and reviews, discover global cinema live via TMDB, and inspect personal viewing habits with interactive 12-month analytics.

🌐 **Live Application:** [https://cinediary.onrender.com](https://cinediary.onrender.com)  

---

## 🛠️ Technology Stack (Python Web Frameworks Project)

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3, Flask (`app.py`, URL Routing, Jinja2 Templates) |
| **Database** | MongoDB (NoSQL) via PyMongo driver / MongoDB Atlas |
| **Production Server** | Gunicorn WSGI (`Procfile`) |
| **Template Engine** | Flask Jinja2 (`templates/` directory) |
| **Styling & Presentation** | Vanilla CSS3, Glassmorphism UI, Responsive Design |
| **External API** | The Movie Database (TMDB Live API) |
| **Deployment** | Render Cloud Platform |

---

## 📁 Project Structure

```
CineDiary/
├── app.py                  # Main Flask application, URL Routing & Jinja2 Templates
├── requirements.txt        # Python package dependencies (Flask, PyMongo, Gunicorn)
├── Procfile                # Web worker process configuration for Render
├── .env                    # Environment variables configuration (ignored by git)
├── .gitignore              # Git ignore rules protecting secrets
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

## 🚀 Live Application & Quick Start Guide

### 🌐 Access Live Website
The application is deployed live on the cloud:
👉 **[https://cinediary.onrender.com](https://cinediary.onrender.com)**
