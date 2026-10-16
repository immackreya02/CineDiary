# 23CS11E - WEBFRAMEWORK USING PYTHON

## Micro Project Report On

# CineDiary — Movie Watchlist & Rating System

### *Submitted by*

### **REYA IMMACULATE X - 24104044**

*In partial fulfillment for the award of the degree of*

***BACHELOR OF ENGINEERING***
*in*
***COMPUTER SCIENCE AND ENGINEERING***

---

### **NATIONAL ENGINEERING COLLEGE**
**(An Autonomous Institution affiliated to Anna University, Chennai)**
**K.R.NAGAR, KOVILPATTI – 628503**

**OCTOBER – 2026**

---

<div page-break="always"></div>

# NATIONAL ENGINEERING COLLEGE
### K.R.NAGAR, KOVILPATTI – 628503

## **BONAFIDE CERTIFICATE**

This is to certify that this project report is a Bonafide record of **REYA IMMACULATE X (24104044)** work done for the course **23CS11E - WEBFRAMEWORK USING PYTHON** at the **NATIONAL ENGINEERING COLLEGE, K.R. NAGAR**, during the academic year 2025 – 2026 who carried out the project work under my supervision.

<br><br><br>

**Course Instructor/Guide**

---

<div page-break="always"></div>

## **TABLE OF CONTENTS**

| CHAPTER NO. | TITLE | PAGE NO |
| :---: | :--- | :---: |
| | **ABSTRACT** | 4 |
| **1** | **INTRODUCTION** | 5 |
| | 1.1 Introduction | 5 |
| | 1.2 Problem Statement | 6 |
| | 1.3 Objectives | 7 |
| **2** | **IMPLEMENTATION** | 8 |
| | 2.1 Project Structure | 8 |
| | 2.2 Project Code | 9 |
| **3** | **IMPLEMENTATION RESULTS** | 142 |
| **4** | **CONCLUSION** | 150 |

---

<div page-break="always"></div>

## **ABSTRACT**

The **CineDiary — Movie Watchlist & Rating System** is a full-stack web application designed to streamline personal film cataloging, rating tracking, custom list curation, and viewing analytics by providing an integrated platform where movie enthusiasts can efficiently log and monitor their cinema journal.

Through the system, users can securely sign up, receive 6-digit email OTP verification via SMTP delivery, search millions of global films live via **The Movie Database (TMDB) API**, assign 1–5 star ratings, write custom reviews, organize films into custom curated collections, and analyze viewing habits through interactive 12-month analytics.

The system's functionality is driven by key modules: **User & Auth Management** (JWT authentication & SMTP email OTP verification), **Global Cinema & Live Discover** (real-time TMDB global search & discover filters by genre, language, and release year), **Personal Movie Diary** (star ratings, watch dates, and review logs), **Curated Collections** (theme/director lists), and **Interactive 12-Month Analytics** (monthly watch counts, screen runtime calculation, average rating, and MoM trends). Built using **Python Flask**, **PyMongo**, **MongoDB (NoSQL)**, **Vanilla HTML5**, **CSS3 (Glassmorphism)**, and **JavaScript (ES6)**, the system provides a responsive, secure, and aesthetic cinema tracking experience.

By automating movie metadata retrieval, preventing duplicate database entries, providing instant search filtering, and generating interactive viewing analytics, **CineDiary** delivers a centralized, accurate, and user-friendly platform for personal film collection management.

---

<div page-break="always"></div>

# CHAPTER 1
# INTRODUCTION

### 1.1 INTRODUCTION

Cinema and film watching play a major role in modern entertainment and cultural appreciation. Traditionally, moviegoers track their watched films using physical notebooks, mobile notes, or spreadsheets, which can lead to disorganized logs, difficulty in searching past reviews, lack of visual poster presentation, and calculation errors when evaluating viewing habits over time.

To address these challenges, **CineDiary** has been developed as a centralized and automated web-based application. The system is designed to simplify the complete film logging process, starting from user authentication and 6-digit email OTP verification to live TMDB global film discovery, custom collection management, star rating logs, and interactive 12-month viewing trend analytics.

The system is developed using modern web technologies such as **Python Flask**, **PyMongo**, **MongoDB**, **Vanilla HTML5**, **CSS3 (Glassmorphism)**, and **JavaScript (ES6)**, providing a lightweight and efficient platform for storing and managing movie records. The system also supports real-time API integrations, custom confirmation dialogs, profile initial avatars, and automated runtime/score calculations.

By reducing manual record-keeping, eliminating disorganized notes, and providing instant access to personal viewing metrics, **CineDiary** improves the efficiency, accuracy, and aesthetic pleasure of film journal management for movie enthusiasts.

---

### 1.2 PROBLEM STATEMENT

The existing film logging process for many enthusiasts is fragmented and unorganized, relying on basic notes or static spreadsheets that lack live movie poster metadata, director/cast details, and interactive analytics. This creates significant difficulty for users in searching past watched movies, curating themed lists, and tracking monthly viewing habits.

The manual process of entering movie details, searching cast/crew information, and calculating average ratings across hundreds of films becomes a time-consuming burden. Furthermore, the lack of a centralized system for organizing films into custom curated collections (e.g., *"Mind-Bending Sci-Fi"* or *"Tamil Masterpieces"*) makes it hard to retrieve specific film recommendations.

The absence of real-time viewing analytics also prevents users from understanding their monthly screen time, average score distributions, and genre preferences over time. Therefore, there is a clear need for an automated, aesthetic system to manage movie watchlists and ratings in a structured, accurate, centralized, and visually captivating manner.

---

### 1.3 OBJECTIVES

The primary objective of **CineDiary** is to establish a centralized platform that efficiently manages all film cataloging and rating activities. It provides an intuitive, dark-glassmorphism interface for users to securely log in, verify via 6-digit email OTP, search global cinema, curate lists, and monitor personal viewing trends.

Key objectives include:
1. **Secure Email Authentication**: Implementing user signup, login, and 6-digit email OTP verification with SMTP delivery and instant auto-login.
2. **Global Movie Discovery**: Integrating live TMDB API search and discover filters (Genre, Language, Release Year) with live director/cast fetching.
3. **Personal Diary & Star Ratings**: Providing a diary interface for logging watched movies with 1–5 star ratings, watch dates, and custom review notes.
4. **Curated Collections**: Enabling users to group movies into custom themed lists with quick live search additions.
5. **Interactive 12-Month Analytics**: Calculating monthly watch counts, total screen time (hours/minutes), average ratings, top genres, and MoM trends visualized through an interactive 12-bar chart with hover tooltips.
6. **NoSQL Data Persistence**: Utilizing MongoDB document storage for flexible schema management and fast querying.

---

<div page-break="always"></div>

# CHAPTER 2
# IMPLEMENTATION

### 2.1 PROJECT STRUCTURE

```
NoSQL Database Project/
├── client/                     # Vanilla HTML5 / CSS3 / JS Frontend
│   ├── css/
│   │   └── styles.css          # Glassmorphism Cinema Theme Stylesheet
│   ├── js/
│   │   ├── api.js              # Fetch API Client Module
│   │   └── common.js           # Shared Navigation & Modal Utilities
│   ├── index.html              # Main Movie Catalogue & Live Search Page
│   ├── movie-details.html      # Movie Details, Review & Rating View
│   ├── diary.html              # Personal Movie Diary & Watchlist Page
│   ├── lists.html              # Curated Film Collections Page
│   ├── stats.html              # Interactive 12-Month Analytics Dashboard
│   ├── login.html              # User Authentication (Sign In & Sign Up)
│   ├── verify-otp.html         # 6-Digit Email OTP Verification Screen
│   └── profile.html            # User Profile & Stats Summary
├── server/                     # Python Flask API Backend
│   ├── routes/
│   │   ├── auth_routes.py      # Auth & OTP endpoints
│   │   ├── movie_routes.py     # Movie & TMDB API endpoints
│   │   ├── diary_routes.py     # Diary & Rating endpoints
│   │   ├── list_routes.py      # Curated Collections endpoints
│   │   └── stats_routes.py     # Monthly Analytics & Aggregations
│   ├── app.py                  # Main Flask Server Entrypoint
│   ├── db.py                   # PyMongo MongoDB connection & serializer
│   ├── utils.py                # JWT & SMTP Email OTP sender
│   └── .env                    # Environment secrets
├── .gitignore                  # Git tracking exclusion rules
└── README.md                   # Project documentation
```

---

### 2.2 PROJECT CODE

#### **`server/app.py`**
```python
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from seed import seed_database
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp
from routes.diary_routes import diary_bp
from routes.list_routes import list_bp
from routes.stats_routes import stats_bp

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register API Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/users')
app.register_blueprint(movie_bp, url_prefix='/api/movies')
app.register_blueprint(diary_bp, url_prefix='/api/diary')
app.register_blueprint(list_bp, url_prefix='/api/lists')
app.register_blueprint(stats_bp, url_prefix='/api/stats')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'app': 'CineDiary Flask API',
        'engine': 'Python Flask + PyMongo'
    }), 200

if __name__ == '__main__':
    seed_database()
    port = int(os.getenv('PORT', 5001))
    print(f"=================================")
    print(f" CineDiary Flask API Server running on port {port}")
    print(f" Health check: http://localhost:{port}/api/health")
    print(f"=================================")
    app.run(host='0.0.0.0', port=port, debug=True)
```

#### **`server/db.py`**
```python
import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cinediary')
client = MongoClient(MONGO_URI)
db = client.get_database()

users_collection = db['users']
movies_collection = db['movies']
diary_collection = db['diaryentries']
lists_collection = db['lists']

def serialize_doc(doc):
    if not doc:
        return None
    doc['_id'] = str(doc['_id'])
    if 'userId' in doc and isinstance(doc['userId'], ObjectId):
        doc['userId'] = str(doc['userId'])
    if 'movieId' in doc and isinstance(doc['movieId'], ObjectId):
        doc['movieId'] = str(doc['movieId'])
    if 'movies' in doc and isinstance(doc['movies'], list):
        doc['movies'] = [str(m) if isinstance(m, ObjectId) else m for m in doc['movies']]
    return doc

def serialize_docs(cursor):
    return [serialize_doc(doc) for doc in cursor]
```

#### **`server/routes/stats_routes.py`**
```python
from flask import Blueprint, jsonify
from bson import ObjectId
from collections import Counter
from db import diary_collection, movies_collection

stats_bp = Blueprint('stats', __name__)
MONTH_NAMES = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

@stats_bp.route('/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({'success': False, 'message': 'Invalid user ID'}), 400

        u_obj = ObjectId(user_id)

        # Monthly Viewing Trends Pipeline with Runtime & MoM Calculations
        monthly_pipeline = [
            { '$match': { 'userId': u_obj, 'status': 'watched' } },
            { '$lookup': {
                'from': 'movies',
                'localField': 'movieId',
                'foreignField': '_id',
                'as': 'movieDetails'
            }},
            { '$unwind': { 'path': '$movieDetails', 'preserveNullAndEmptyArrays': True } },
            { '$group': {
                '_id': {
                    'year': { '$year': { '$ifNull': ['$watchedDate', '$updatedAt'] } },
                    'month': { '$month': { '$ifNull': ['$watchedDate', '$updatedAt'] } }
                },
                'count': { '$sum': 1 },
                'totalMinutes': { '$sum': { '$ifNull': ['$movieDetails.duration', 120] } },
                'ratings': { '$push': '$rating' },
                'genresList': { '$push': '$movieDetails.genres' }
            }},
            { '$sort': { '_id.year': 1, '_id.month': 1 } }
        ]

        monthly_results = list(diary_collection.aggregate(monthly_pipeline))
        monthly_watch_count = []
        
        for idx, item in enumerate(monthly_results):
            y = item['_id'].get('year', 2026)
            m = item['_id'].get('month', 10)
            month_name = MONTH_NAMES[m] if 1 <= m <= 12 else 'Oct'
            month_str = f"{month_name} {y}"
            
            total_mins = item.get('totalMinutes', 0)
            hours = total_mins // 60
            mins = total_mins % 60
            runtime_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

            valid_ratings = [r for r in item.get('ratings', []) if r and r > 0]
            month_avg_rating = round(sum(valid_ratings) / len(valid_ratings), 1) if valid_ratings else 0.0

            all_genres = []
            for g_item in item.get('genresList', []):
                if isinstance(g_item, list):
                    all_genres.extend(g_item)
                elif isinstance(g_item, str):
                    all_genres.append(g_item)
            
            top_genre = 'Drama'
            if all_genres:
                genre_counts = Counter(all_genres)
                top_genre = genre_counts.most_common(1)[0][0]

            if idx == 0:
                mom_trend = "Initial Month"
            else:
                prev_count = monthly_results[idx - 1]['count']
                curr_count = item['count']
                prev_m_name = MONTH_NAMES[monthly_results[idx-1]['_id'].get('month', 1)]
                diff = curr_count - prev_count
                mom_perc = round((diff / prev_count) * 100) if prev_count > 0 else 100
                sign = "+" if mom_perc > 0 else ""
                mom_trend = f"{sign}{mom_perc}% vs {prev_m_name}"

            monthly_watch_count.append({
                'month': month_str,
                'shortMonth': month_name,
                'year': y,
                'count': item['count'],
                'totalMinutes': total_mins,
                'runtimeStr': runtime_str,
                'avgRating': month_avg_rating,
                'topGenre': top_genre,
                'momTrend': mom_trend
            })

        return jsonify({
            'success': True,
            'data': {
                'monthlyWatchCount': monthly_watch_count
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
```

---

<div page-break="always"></div>

# CHAPTER 3
# IMPLEMENTATION RESULTS

### **Figure 3.1: CineDiary Homepage & Database Catalogue**
The main landing page displaying the movie database collection with poster image fallback handling, year/language tags, star ratings, and clean navigation header.

### **Figure 3.2: Live TMDB Global Search & Filter Interface**
Real-time global cinema discovery enabling users to type any film from India, Hollywood, Japan, Korea, or France, filter by Genre, Language, and Release Year, and import official metadata into the database.

### **Figure 3.3: Curated Film Collections Management**
Custom theme lists (e.g., *"Tamil Masterpieces"*, *"Mind-Bending Sci-Fi"*) with stacked poster previews and quick live search additions.

### **Figure 3.4: Personal Movie Diary & Star Rating View**
Personal diary interface allowing users to log watched films with 1–5 star ratings, watch dates, custom review notes, and watchlist filtering.

### **Figure 3.5: Interactive 12-Month Viewing Activity & 4-Metric Pill Bar**
Interactive analytics dashboard featuring a 4-metric monthly focus bar (*Movies Watched*, *Total Runtime*, *Avg Rating*, *MoM Trend*) alongside a 12-month bar chart (Jan – Dec) with hover tooltips.

### **Figure 3.6: Email OTP Verification & User Profile Interface**
6-digit email OTP verification screen with auto-advancing input fields, resend countdown timer, and automatic login redirection upon verification.

---

<div page-break="always"></div>

# CHAPTER 4
# CONCLUSION

The **CineDiary — Movie Watchlist & Rating System** has been successfully designed and developed to automate and simplify the traditional manual process of tracking watched films, ratings, and viewing analytics. The system provides a centralized platform for film enthusiasts, enabling efficient management of movie watchlists, custom curated collections, and viewing trends. By utilizing technologies such as **Python Flask** for the web API, **PyMongo** and **MongoDB** for flexible document data storage, and **Vanilla HTML5, CSS3, and JavaScript** for a dark-glassmorphism user interface, the system provides a responsive and aesthetic environment for personal cinema management.

The implementation of separate authentication, diary, collection, and analytics modules has improved the organization and accessibility of personal film logs. Users can securely register with 6-digit email OTP verification, search global cinema live via TMDB API, log watched movies with 1–5 star ratings, write custom reviews, create curated lists, and inspect monthly screen time and rating trends.

The system also incorporates real-time API integrations, automated runtime calculation, and MoM trend evaluation, which helps reduce manual calculation effort and ensures consistent assessment records. The centralized NoSQL database minimizes duplicate entries and provides a structured approach for storing user, movie, diary, and collection documents.

In conclusion, **CineDiary** provides a reliable, secure, and visually stunning solution for transforming conventional movie logging into a centralized, technology-driven journal. Overall, this project demonstrates that the adoption of modern web technologies and database-driven automation can significantly improve personal movie management, providing a simple, accurate, transparent, and efficient platform for all film lovers.
