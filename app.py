import os
import random
import smtplib
import requests
import jwt
import bcrypt
import json
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. APPLICATION SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
load_dotenv()
                             
app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'cinediary_secret_key_2026_reya')

# Database Setup (NoSQL MongoDB via PyMongo)
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cinediary')
client = MongoClient(MONGODB_URI)
db = client.get_database('cinediary')

users_collection = db['users']
movies_collection = db['movies']
diary_collection = db['diaryentries']
lists_collection = db['lists']

# Environmental & API Config
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'
TMDB_BACKDROP_BASE = 'https://image.tmdb.org/t/p/w1280'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

MONTH_NAMES = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

TMDB_GENRES = {
    'action': 28, 'adventure': 12, 'animation': 16, 'comedy': 35,
    'crime': 80, 'documentary': 99, 'drama': 18, 'family': 10751,
    'fantasy': 14, 'history': 36, 'horror': 27, 'music': 10402,
    'mystery': 9648, 'romance': 10749, 'sci-fi': 878, 'science fiction': 878,
    'thriller': 53, 'war': 10752, 'western': 37
}

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS & SERIALIZATION
# -----------------------------------------------------------------------------
def serialize_doc(doc):
    """Recursively converts ObjectId to string and formats dates for HTML template use."""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            if key == '_id':
                new_doc['_id'] = str(value)
            elif isinstance(value, ObjectId):
                new_doc[key] = str(value)
            elif isinstance(value, datetime):
                new_doc[key] = value.strftime('%b %d, %Y')
            elif isinstance(value, (dict, list)):
                new_doc[key] = serialize_doc(value)
            else:
                new_doc[key] = value

        if 'posterUrl' in new_doc or 'poster' in new_doc:
            p_val = new_doc.get('posterUrl') or new_doc.get('poster') or 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=400'
            new_doc['posterUrl'] = p_val
            new_doc['poster'] = p_val

        if 'backdropUrl' in new_doc or 'backdrop' in new_doc:
            b_val = new_doc.get('backdropUrl') or new_doc.get('backdrop') or new_doc.get('posterUrl') or new_doc.get('poster') or 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&q=80&w=1200'
            new_doc['backdropUrl'] = b_val
            new_doc['backdrop'] = b_val

        if 'releaseYear' in new_doc or 'year' in new_doc:
            y_val = new_doc.get('releaseYear') or new_doc.get('year') or 2024
            new_doc['releaseYear'] = y_val
            new_doc['year'] = y_val

        return new_doc
    if isinstance(doc, ObjectId):
        return str(doc)
    if isinstance(doc, datetime):
        return doc.strftime('%b %d, %Y')
    return doc

def serialize_docs(cursor):
    return [serialize_doc(doc) for doc in cursor]

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed_password):
    if not hashed_password:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp_code):
    smtp_user = os.getenv('SMTP_USER', '').strip()
    smtp_pass = os.getenv('SMTP_PASS', '').replace(' ', '').strip()

    if not smtp_user or not smtp_pass:
        print(f"==================================================")
        print(f" [DEV MODE OTP] Verification Code for {to_email}: {otp_code}")
        print(f"==================================================")
        return True, "Dev Mode: OTP generated successfully"

    try:
        msg = MIMEMultipart()
        msg['From'] = f"CineDiary <{smtp_user}>"
        msg['To'] = to_email
        msg['Subject'] = f"{otp_code} is your CineDiary Verification Code"

        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #140A0D; color: #F3E9DC; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: #1F0E15; border: 1px solid #3A2029; padding: 30px; border-radius: 20px; text-align: center;">
              <h1 style="color: #D4A94C; font-family: Georgia, serif;">CineDiary</h1>
              <p style="color: #B39A9E; font-size: 14px;">Welcome! Enter the code below to verify your email address:</p>
              <div style="font-size: 36px; font-weight: bold; color: #D4A94C; letter-spacing: 6px; padding: 15px; margin: 20px 0; background: #140A0D; border: 1px solid #3A2029; border-radius: 12px;">
                {otp_code}
              </div>
              <p style="color: #B39A9E; font-size: 12px;">This verification code expires in 10 minutes.</p>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True, "OTP email sent successfully"
    except Exception as e:
        print(f"[SMTP ERROR] Failed to send email via {smtp_user}: {e}")
        return False, f"Email delivery error: {str(e)}"

def get_current_user():
    user_id = session.get('user_id')
    if user_id and ObjectId.is_valid(user_id):
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            return serialize_doc(user)
    return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated

def fetch_tmdb_credits(tmdb_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={TMDB_API_KEY}'
        resp = requests.get(url, headers=HEADERS, timeout=3)
        if resp.status_code == 200:
            credits_data = resp.json()
            director = 'Unknown Director'
            for crew_member in credits_data.get('crew', []):
                if crew_member.get('job') == 'Director':
                    director = crew_member.get('name')
                    break
            cast_list = [c.get('name') for c in credits_data.get('cast', [])[:5] if c.get('name')]
            return director, cast_list
    except Exception:
        pass
    return 'Acclaimed Director', ['Lead Actor', 'Co-Star']

@app.context_processor
def inject_user():
    return {'current_user': get_current_user()}

# -----------------------------------------------------------------------------
# 3. AUTHENTICATION & USER CONTROLLERS
# -----------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        action = request.form.get('action', 'login')

        if action == 'login':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            user = users_collection.find_one({'email': email})
            if not user or not check_password(password, user.get('password', '')):
                return render_template('login.html', error='Invalid email or password', active_tab='login')

            if not user.get('isVerified', True):
                otp_code = generate_otp()
                otp_expires = datetime.now() + timedelta(minutes=10)
                users_collection.update_one({'_id': user['_id']}, {'$set': {'otpCode': otp_code, 'otpExpiresAt': otp_expires}})
                send_otp_email(email, otp_code)
                session['unverified_email'] = email
                return redirect(url_for('verify_otp_page'))

            session['user_id'] = str(user['_id'])
            session['user_name'] = user.get('name', 'Film Lover')
            session['user_email'] = user.get('email', '')
            return redirect(url_for('index_page'))

        elif action == 'register':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            if not name or not email or not password:
                return render_template('login.html', error='Please provide name, email, and password', active_tab='signup')

            existing = users_collection.find_one({'email': email})
            if existing:
                if existing.get('isVerified', True):
                    return render_template('login.html', error='User with this email already exists', active_tab='signup')
                else:
                    otp_code = generate_otp()
                    otp_expires = datetime.now() + timedelta(minutes=10)
                    users_collection.update_one(
                        {'_id': existing['_id']},
                        {'$set': {'name': name, 'password': hash_password(password), 'otpCode': otp_code, 'otpExpiresAt': otp_expires, 'updatedAt': datetime.now()}}
                    )
                    send_otp_email(email, otp_code)
                    session['unverified_email'] = email
                    return redirect(url_for('verify_otp_page'))

            hashed = hash_password(password)
            otp_code = generate_otp()
            otp_expires = datetime.now() + timedelta(minutes=10)

            new_user = {
                'name': name,
                'email': email,
                'password': hashed,
                'avatar': '',
                'bio': 'Film lover & CineDiary member',
                'favoriteMovies': [],
                'isVerified': False,
                'otpCode': otp_code,
                'otpExpiresAt': otp_expires,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            }
            users_collection.insert_one(new_user)
            send_otp_email(email, otp_code)
            session['unverified_email'] = email
            return redirect(url_for('verify_otp_page'))

    return render_template('login.html', active_tab=request.args.get('tab', 'login'))

@app.route('/verify-otp', methods=['GET', 'POST'])
@app.route('/verify-otp.html', methods=['GET', 'POST'])
def verify_otp_page():
    email = session.get('unverified_email', '')
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        email_submitted = request.form.get('email', email).strip().lower()

        user = users_collection.find_one({'email': email_submitted})
        if not user:
            return render_template('verify_otp.html', email=email_submitted, error='Account not found for email')

        stored_otp = user.get('otpCode')
        otp_expires = user.get('otpExpiresAt')

        if not stored_otp or str(stored_otp).strip() != str(otp).strip():
            return render_template('verify_otp.html', email=email_submitted, error='Invalid 6-digit OTP code')

        if otp_expires and datetime.now() > otp_expires:
            return render_template('verify_otp.html', email=email_submitted, error='OTP code has expired. Please request a new one.')

        users_collection.update_one(
            {'_id': user['_id']},
            {
                '$set': {'isVerified': True, 'updatedAt': datetime.now()},
                '$unset': {'otpCode': '', 'otpExpiresAt': ''}
            }
        )

        session.pop('unverified_email', None)
        session['user_id'] = str(user['_id'])
        session['user_name'] = user.get('name', 'Film Lover')
        session['user_email'] = user.get('email', '')
        return redirect(url_for('index_page'))

    return render_template('verify_otp.html', email=email)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/profile.html', methods=['GET', 'POST'])
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user_id = session.get('user_id')
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        bio = request.form.get('bio', '').strip()
        avatar = request.form.get('avatar', '').strip()
        
        update_fields = {'updatedAt': datetime.now()}
        if name:
            update_fields['name'] = name
            session['user_name'] = name
        if bio:
            update_fields['bio'] = bio
        if avatar:
            update_fields['avatar'] = avatar

        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
        return redirect(url_for('profile_page'))

    user_data = serialize_doc(user)
    fav_ids = user_data.get('favoriteMovies', [])
    populated_favs = []
    for fid in fav_ids:
        try:
            m_obj = ObjectId(fid) if isinstance(fid, str) else fid
            movie = movies_collection.find_one({'_id': m_obj})
            if movie:
                populated_favs.append(serialize_doc(movie))
        except Exception:
            continue
    user_data['favoriteMovies'] = populated_favs

    diary_cursor = diary_collection.find({'userId': ObjectId(user_id)}).sort('updatedAt', -1).limit(6)
    recent_diary = []
    for entry in serialize_docs(diary_cursor):
        m_id = entry.get('movieId')
        movie = movies_collection.find_one({'_id': ObjectId(m_id)}) if m_id and ObjectId.is_valid(m_id) else None
        entry['movie'] = serialize_doc(movie) if movie else {'title': 'Unknown Movie'}
        recent_diary.append(entry)

    return render_template('profile.html', user=user_data, recent_diary=recent_diary)

# -----------------------------------------------------------------------------
# 4. MOVIE CATALOGUE & SEARCH CONTROLLERS (TMDB DISCOVER ENHANCED)
# -----------------------------------------------------------------------------
@app.route('/')
@app.route('/index.html')
def index_page():
    search = request.args.get('search', '').strip()
    genre = request.args.get('genre', '').strip()
    year = request.args.get('year', '').strip()

    query = {}
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'director': {'$regex': search, '$options': 'i'}},
            {'cast': {'$regex': search, '$options': 'i'}},
        ]
    if genre and genre != 'All':
        query['genres'] = genre
    if year and year != 'All' and year.isdigit():
        query['releaseYear'] = int(year)

    cursor = movies_collection.find(query).sort('releaseYear', -1).limit(24)
    movies = serialize_docs(cursor)

    # TMDB Live API Integration (Using Discover API for Genre & Year filtering)
    tmdb_movies = []
    if TMDB_API_KEY:
        try:
            if search:
                url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(search)}&include_adult=false'
            else:
                params = [f'api_key={TMDB_API_KEY}', 'include_adult=false', 'sort_by=popularity.desc']
                if genre and genre != 'All' and genre.lower() in TMDB_GENRES:
                    params.append(f'with_genres={TMDB_GENRES[genre.lower()]}')
                if year and year != 'All' and year.isdigit():
                    params.append(f'primary_release_year={int(year)}')
                url = f'https://api.themoviedb.org/3/discover/movie?{"&".join(params)}'

            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                tmdb_data = resp.json()
                for item in tmdb_data.get('results', [])[:12]:
                    poster_path = item.get('poster_path')
                    backdrop_path = item.get('backdrop_path')
                    rel_date = item.get('release_date', '')
                    rel_yr = int(rel_date.split('-')[0]) if rel_date and len(rel_date.split('-')[0]) == 4 else 2024
                    tmdb_movies.append({
                        'tmdbId': item.get('id'),
                        'title': item.get('title'),
                        'posterUrl': f'{TMDB_IMAGE_BASE}{poster_path}' if poster_path else 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=400',
                        'backdropUrl': f'{TMDB_BACKDROP_BASE}{backdrop_path}' if backdrop_path else 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&q=80&w=1200',
                        'releaseYear': rel_yr,
                        'overallRating': round(float(item.get('vote_average') or 7.5) / 2.0, 1),
                        'genres': [genre.title() if genre and genre != 'All' else 'Feature']
                    })
        except Exception as e:
            print(f"TMDB fetch error: {e}")

    # Standard genre options including all TMDB genre categories
    standard_genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    db_genres = [g for g in movies_collection.distinct('genres') if g]
    all_genres = sorted(list(set(standard_genres + db_genres)))
    
    current_yr = datetime.now().year
    all_years = list(range(current_yr, 1970, -1))

    return render_template(
        'index.html',
        movies=movies,
        tmdb_movies=tmdb_movies,
        search=search,
        selected_genre=genre,
        selected_year=year,
        genres=all_genres,
        years=all_years
    )

@app.route('/movie-details.html')
@app.route('/movie/<movie_id>')
def movie_details_page(movie_id=None):
    m_id = movie_id or request.args.get('id')
    tmdb_id = request.args.get('tmdbId')

    movie = None
    if m_id and ObjectId.is_valid(m_id):
        movie = movies_collection.find_one({'_id': ObjectId(m_id)})

    if not movie and tmdb_id:
        try:
            detail_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}'
            resp = requests.get(detail_url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                detail = resp.json()
                rel_date = detail.get('release_date', '')
                rel_yr = int(rel_date.split('-')[0]) if rel_date and len(rel_date.split('-')[0]) == 4 else 2024
                director, cast_list = fetch_tmdb_credits(tmdb_id)

                new_movie = {
                    'title': detail.get('title'),
                    'posterUrl': f"{TMDB_IMAGE_BASE}{detail.get('poster_path')}" if detail.get('poster_path') else 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=400',
                    'backdropUrl': f"{TMDB_BACKDROP_BASE}{detail.get('backdrop_path')}" if detail.get('backdrop_path') else 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&q=80&w=1200',
                    'tagline': detail.get('tagline', ''),
                    'description': detail.get('overview', ''),
                    'genres': [g.get('name') for g in detail.get('genres', []) if g.get('name')],
                    'language': (detail.get('original_language') or 'en').upper(),
                    'releaseYear': rel_yr,
                    'durationMinutes': detail.get('runtime', 120),
                    'director': director,
                    'cast': cast_list,
                    'overallRating': round(float(detail.get('vote_average') or 7.5) / 2.0, 1),
                    'tmdbId': int(tmdb_id),
                    'createdAt': datetime.now(),
                    'updatedAt': datetime.now()
                }
                res = movies_collection.insert_one(new_movie)
                movie = movies_collection.find_one({'_id': res.inserted_id})
        except Exception as e:
            print(f"Error caching TMDB movie: {e}")

    if not movie:
        movie = movies_collection.find_one()

    movie_doc = serialize_doc(movie)

    user_entry = None
    user_id = session.get('user_id')
    if user_id and movie_doc:
        entry = diary_collection.find_one({
            'userId': ObjectId(user_id),
            'movieId': ObjectId(movie_doc['_id'])
        })
        if entry:
            user_entry = serialize_doc(entry)

    user_lists = []
    if user_id:
        user_lists = serialize_docs(lists_collection.find({'userId': ObjectId(user_id)}))

    return render_template('movie_details.html', movie=movie_doc, user_entry=user_entry, user_lists=user_lists)

# -----------------------------------------------------------------------------
# 5. DIARY & RATINGS CONTROLLERS
# -----------------------------------------------------------------------------
@app.route('/diary.html')
@app.route('/diary')
@login_required
def diary_page():
    user_id = session.get('user_id')
    status_filter = request.args.get('status', 'all')
    rating_filter = request.args.get('rating', 'all')

    query = {'userId': ObjectId(user_id)}
    if status_filter != 'all':
        query['status'] = status_filter
    if rating_filter != 'all':
        try:
            query['rating'] = float(rating_filter)
        except ValueError:
            pass

    cursor = diary_collection.find(query).sort('updatedAt', -1)
    raw_entries = serialize_docs(cursor)

    entries = []
    for entry in raw_entries:
        m_id = entry.get('movieId')
        movie = movies_collection.find_one({'_id': ObjectId(m_id)}) if m_id and ObjectId.is_valid(m_id) else None
        entry['movie'] = serialize_doc(movie) if movie else {'title': 'Unknown Movie'}
        entries.append(entry)

    return render_template('diary.html', entries=entries, selected_status=status_filter, selected_rating=rating_filter)

@app.route('/diary/add', methods=['POST'])
@login_required
def add_diary_entry():
    user_id = session.get('user_id')
    movie_id = request.form.get('movieId')
    rating = float(request.form.get('rating', 0))
    review = request.form.get('review', '').strip()
    status = request.form.get('status', 'watched')
    is_favorite = request.form.get('isFavorite') == 'on' or request.form.get('isFavorite') == 'true'

    if not movie_id or not ObjectId.is_valid(movie_id):
        return redirect(url_for('index_page'))

    u_obj = ObjectId(user_id)
    m_obj = ObjectId(movie_id)

    existing = diary_collection.find_one({'userId': u_obj, 'movieId': m_obj})
    entry_data = {
        'userId': u_obj,
        'movieId': m_obj,
        'status': status,
        'rating': rating,
        'review': review,
        'watchedDate': datetime.now(),
        'isFavorite': is_favorite,
        'updatedAt': datetime.now()
    }

    if existing:
        diary_collection.update_one({'_id': existing['_id']}, {'$set': entry_data})
    else:
        entry_data['createdAt'] = datetime.now()
        diary_collection.insert_one(entry_data)

    return redirect(url_for('diary_page'))

@app.route('/diary/delete/<entry_id>', methods=['POST', 'DELETE'])
@login_required
def delete_diary_entry(entry_id):
    if ObjectId.is_valid(entry_id):
        diary_collection.delete_one({'_id': ObjectId(entry_id)})
    return redirect(url_for('diary_page'))

# -----------------------------------------------------------------------------
# 6. FILM COLLECTIONS / LISTS CONTROLLERS
# -----------------------------------------------------------------------------
@app.route('/lists.html')
@app.route('/lists')
@login_required
def lists_page():
    user_id = session.get('user_id')
    cursor = lists_collection.find({'userId': ObjectId(user_id)}).sort('updatedAt', -1)
    raw_lists = serialize_docs(cursor)

    user_lists = []
    for lst in raw_lists:
        m_ids = lst.get('movies', [])
        populated_movies = []
        for mid in m_ids:
            if ObjectId.is_valid(mid):
                m = movies_collection.find_one({'_id': ObjectId(mid)})
                if m:
                    populated_movies.append(serialize_doc(m))
        lst['movies'] = populated_movies
        user_lists.append(lst)

    return render_template('lists.html', lists=user_lists)

@app.route('/lists/create', methods=['POST'])
@login_required
def create_list():
    user_id = session.get('user_id')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if title:
        new_list = {
            'userId': ObjectId(user_id),
            'name': title,
            'title': title,
            'description': description,
            'isPublic': True,
            'movies': [],
            'createdAt': datetime.now(),
            'updatedAt': datetime.now()
        }
        lists_collection.insert_one(new_list)

    return redirect(url_for('lists_page'))

@app.route('/lists/add-movie', methods=['POST'])
@login_required
def add_to_list():
    list_id = request.form.get('listId')
    movie_id = request.form.get('movieId')

    if ObjectId.is_valid(list_id) and ObjectId.is_valid(movie_id):
        lists_collection.update_one(
            {'_id': ObjectId(list_id)},
            {
                '$addToSet': {'movies': ObjectId(movie_id)},
                '$set': {'updatedAt': datetime.now()}
            }
        )
    return redirect(url_for('lists_page'))

@app.route('/lists/remove-movie', methods=['POST'])
@login_required
def remove_from_list():
    list_id = request.form.get('listId')
    movie_id = request.form.get('movieId')

    if ObjectId.is_valid(list_id) and ObjectId.is_valid(movie_id):
        lists_collection.update_one(
            {'_id': ObjectId(list_id)},
            {
                '$pull': {'movies': ObjectId(movie_id)},
                '$set': {'updatedAt': datetime.now()}
            }
        )
    return redirect(url_for('lists_page'))

# -----------------------------------------------------------------------------
# 7. CINEMA ANALYTICS & STATS CONTROLLERS
# -----------------------------------------------------------------------------
@app.route('/stats.html')
@app.route('/stats')
@login_required
def stats_page():
    user_id = session.get('user_id')
    u_obj = ObjectId(user_id)

    genre_pipeline = [
        { '$match': { 'userId': u_obj, 'status': 'watched' } },
        { '$lookup': {
            'from': 'movies',
            'localField': 'movieId',
            'foreignField': '_id',
            'as': 'movieDetails'
        }},
        { '$unwind': '$movieDetails' },
        { '$unwind': '$movieDetails.genres' },
        { '$group': {
            '_id': '$movieDetails.genres',
            'count': { '$sum': 1 }
        }},
        { '$sort': { 'count': -1 } }
    ]
    genre_results = list(diary_collection.aggregate(genre_pipeline))
    genre_breakdown = [{'genre': item['_id'], 'count': item['count']} for item in genre_results]

    rating_pipeline = [
        { '$match': { 'userId': u_obj, 'status': 'watched', 'rating': { '$gt': 0 } } },
        { '$group': {
            '_id': '$rating',
            'count': { '$sum': 1 }
        }},
        { '$sort': { '_id': 1 } }
    ]
    rating_results = list(diary_collection.aggregate(rating_pipeline))
    rating_distribution = [{'rating': item['_id'], 'count': item['count']} for item in rating_results]

    status_pipeline = [
        { '$match': { 'userId': u_obj } },
        { '$group': { '_id': '$status', 'count': { '$sum': 1 } } }
    ]
    status_results = list(diary_collection.aggregate(status_pipeline))
    status_map = {item['_id']: item['count'] for item in status_results}
    
    total_watched = status_map.get('watched', 0)
    watchlist_count = status_map.get('watchlist', 0)

    avg_rating = 0.0
    if rating_results:
        total_sum = sum(r['_id'] * r['count'] for r in rating_results)
        total_count = sum(r['count'] for r in rating_results)
        avg_rating = round(total_sum / total_count, 1) if total_count > 0 else 0.0

    stats = {
        'totalWatched': total_watched,
        'watchlistCount': watchlist_count,
        'avgRating': avg_rating,
        'favoriteGenre': genre_breakdown[0]['genre'] if genre_breakdown else 'Drama',
        'genreBreakdown': genre_breakdown,
        'ratingDistribution': rating_distribution
    }

    return render_template('stats.html', stats=stats)

# -----------------------------------------------------------------------------
# 8. APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"==================================================")
    print(f" CineDiary Pure Flask HTML Server running on http://localhost:{port}")
    print(f" Single app.py + Jinja2 Server-Side Form Architecture")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
