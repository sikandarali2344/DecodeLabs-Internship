# ============================================
# PROJECT 3: AI RECOMMENDATION ENGINE - WEB APP
# Batch: 2026 | DecodeLabs
# AI Engineer: Sikandar
# ============================================

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'decodelabs_2026_secret_key_sikandar'

# ============================================
# MOVIE DATABASE (15 Movies with Rich Data)
# ============================================

MOVIES = [
    {"id": 1, "title": "The Dark Knight", "year": 2008, "director": "Christopher Nolan", 
     "genre": ["Action", "Crime", "Drama"], "rating": 4.9, "votes": "2.3M",
     "tags": ["superhero", "dark", "psychological", "joker", "batman"],
     "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
     "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
     "duration": "152 min", "language": "English", "country": "USA"},
     
    {"id": 2, "title": "Inception", "year": 2010, "director": "Christopher Nolan", 
     "genre": ["Action", "Sci-Fi", "Thriller"], "rating": 4.7, "votes": "2.0M",
     "tags": ["mind-bending", "dreams", "heist", "philosophical", "time"],
     "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
     "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
     "duration": "148 min", "language": "English", "country": "USA"},
     
    {"id": 3, "title": "The Avengers", "year": 2012, "director": "Joss Whedon", 
     "genre": ["Action", "Adventure", "Sci-Fi"], "rating": 4.5, "votes": "1.6M",
     "tags": ["marvel", "superhero", "ensemble", "comic", "action-packed"],
     "plot": "Earth's mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity.",
     "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"],
     "duration": "143 min", "language": "English", "country": "USA"},
     
    {"id": 4, "title": "Mad Max: Fury Road", "year": 2015, "director": "George Miller", 
     "genre": ["Action", "Adventure", "Sci-Fi"], "rating": 4.7, "votes": "1.1M",
     "tags": ["post-apocalyptic", "car-chase", "dystopian", "feminist", "epic"],
     "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshipper, and a drifter named Max.",
     "cast": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
     "duration": "120 min", "language": "English", "country": "Australia"},
     
    {"id": 5, "title": "The Matrix", "year": 1999, "director": "Lana Wachowski, Lilly Wachowski", 
     "genre": ["Action", "Sci-Fi"], "rating": 4.8, "votes": "2.0M",
     "tags": ["philosophical", "cyberpunk", "classic", "mind-bending", "futuristic"],
     "plot": "A computer programmer discovers that reality as he knows it is a sophisticated simulation created by machines to subjugate humanity, and joins a rebellion to break free.",
     "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
     "duration": "136 min", "language": "English", "country": "USA"},
     
    {"id": 6, "title": "Interstellar", "year": 2014, "director": "Christopher Nolan", 
     "genre": ["Sci-Fi", "Drama", "Adventure"], "rating": 4.6, "votes": "1.8M",
     "tags": ["space", "time-travel", "emotional", "scientific", "gravity"],
     "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. As they face the unknown, they must confront the limits of human endurance and love.",
     "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
     "duration": "169 min", "language": "English", "country": "USA"},
     
    {"id": 7, "title": "Avatar", "year": 2009, "director": "James Cameron", 
     "genre": ["Action", "Adventure", "Sci-Fi"], "rating": 4.3, "votes": "1.3M",
     "tags": ["3d", "aliens", "visual-effects", "epic", "environmental"],
     "plot": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
     "cast": ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver"],
     "duration": "162 min", "language": "English", "country": "USA"},
     
    {"id": 8, "title": "Arrival", "year": 2016, "director": "Denis Villeneuve", 
     "genre": ["Sci-Fi", "Drama"], "rating": 4.5, "votes": "987K",
     "tags": ["intellectual", "linguistics", "emotional", "philosophical", "alien"],
     "plot": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world. She must find a way to understand them before conflict erupts.",
     "cast": ["Amy Adams", "Jeremy Renner", "Forest Whitaker"],
     "duration": "116 min", "language": "English", "country": "USA"},
     
    {"id": 9, "title": "The Shawshank Redemption", "year": 1994, "director": "Frank Darabont", 
     "genre": ["Drama"], "rating": 4.9, "votes": "2.8M",
     "tags": ["hope", "prison", "friendship", "classic", "inspirational"],
     "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency. The film explores the power of hope and friendship.",
     "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
     "duration": "142 min", "language": "English", "country": "USA"},
     
    {"id": 10, "title": "The Godfather", "year": 1972, "director": "Francis Ford Coppola", 
     "genre": ["Crime", "Drama"], "rating": 4.9, "votes": "2.3M",
     "tags": ["mafia", "classic", "masterpiece", "family", "crime"],
     "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son. A powerful story of family, power, and corruption.",
     "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
     "duration": "175 min", "language": "English", "country": "USA"},
     
    {"id": 11, "title": "The Social Network", "year": 2010, "director": "David Fincher", 
     "genre": ["Drama", "Biography"], "rating": 4.4, "votes": "876K",
     "tags": ["tech", "entrepreneurship", "facebook", "legal-drama", "modern"],
     "plot": "The story of the founding of Facebook and the resulting legal battles. A compelling drama about ambition, betrayal, and the creation of a revolutionary platform.",
     "cast": ["Jesse Eisenberg", "Andrew Garfield", "Justin Timberlake"],
     "duration": "120 min", "language": "English", "country": "USA"},
     
    {"id": 12, "title": "The Grand Budapest Hotel", "year": 2014, "director": "Wes Anderson", 
     "genre": ["Comedy", "Adventure", "Drama"], "rating": 4.4, "votes": "765K",
     "tags": ["quirky", "visual", "nostalgic", "whimsical", "artistic"],
     "plot": "A writer encounters the owner of an aging grand hotel who tells him of his early days as a lobby boy. A story of friendship, loyalty, and the changing world of Europe.",
     "cast": ["Ralph Fiennes", "Tony Revolori", "Saoirse Ronan"],
     "duration": "99 min", "language": "English", "country": "USA"},
     
    {"id": 13, "title": "Titanic", "year": 1997, "director": "James Cameron", 
     "genre": ["Romance", "Drama"], "rating": 4.5, "votes": "2.0M",
     "tags": ["love", "tragedy", "historical", "epic", "emotional"],
     "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic. Their romance blossoms amidst the tragedy of the ship's sinking.",
     "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
     "duration": "195 min", "language": "English", "country": "USA"},
     
    {"id": 14, "title": "The Silence of the Lambs", "year": 1991, "director": "Jonathan Demme", 
     "genre": ["Thriller", "Crime", "Drama"], "rating": 4.8, "votes": "1.5M",
     "tags": ["psychological", "serial-killer", "classic", "suspense", "fbi"],
     "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.",
     "cast": ["Jodie Foster", "Anthony Hopkins", "Scott Glenn"],
     "duration": "118 min", "language": "English", "country": "USA"},
     
    {"id": 15, "title": "Get Out", "year": 2017, "director": "Jordan Peele", 
     "genre": ["Horror", "Mystery", "Thriller"], "rating": 4.5, "votes": "987K",
     "tags": ["social-thriller", "psychological", "horror", "mind-bending", "twist"],
     "plot": "A young African-American man visits his white girlfriend's family estate where he learns disturbing secrets about the family and the town. A brilliant social thriller.",
     "cast": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
     "duration": "104 min", "language": "English", "country": "USA"}
]

# Extract all metadata
ALL_GENRES = sorted(set([g for movie in MOVIES for g in movie['genre']]))
ALL_DIRECTORS = sorted(set([m['director'] for m in MOVIES]))
ALL_TAGS = sorted(set([t for movie in MOVIES for t in movie['tags']]))
ALL_YEARS = sorted(set([m['year'] for m in MOVIES]))

# ============================================
# RECOMMENDATION ENGINE
# ============================================

def calculate_similarity(user_prefs, movie):
    """Calculate similarity score with weighted criteria"""
    score = 0
    total = 0
    
    # Genre matching (Highest Weight: 2.0)
    if 'genres' in user_prefs and user_prefs['genres']:
        matched = set(user_prefs['genres']).intersection(set(movie['genre']))
        total += len(user_prefs['genres']) * 2
        score += len(matched) * 2
    
    # Director matching (Weight: 1.5)
    if 'director' in user_prefs and user_prefs['director']:
        if user_prefs['director'].lower() in movie['director'].lower():
            score += 1.5
            total += 1.5
    
    # Tag matching (Weight: 1.0)
    if 'tags' in user_prefs and user_prefs['tags']:
        matched = set(user_prefs['tags']).intersection(set(movie['tags']))
        total += len(user_prefs['tags']) * 1.0
        score += len(matched) * 1.0
    
    # Year preference (Weight: 0.5)
    if 'year_range' in user_prefs:
        if user_prefs['year_range'][0] <= movie['year'] <= user_prefs['year_range'][1]:
            score += 0.5
            total += 0.5
    
    # Rating preference (Weight: 0.5)
    if 'min_rating' in user_prefs:
        if movie['rating'] >= user_prefs['min_rating']:
            score += 0.5
            total += 0.5
    
    if total == 0:
        return 50
    
    similarity = (score / total) * 100
    return min(similarity, 100)

def get_recommendations(user_prefs, top_n=6):
    """Get top N recommendations"""
    recommendations = []
    for movie in MOVIES:
        similarity = calculate_similarity(user_prefs, movie)
        recommendations.append({
            'movie': movie,
            'similarity': round(similarity, 1)
        })
    
    recommendations.sort(key=lambda x: x['similarity'], reverse=True)
    return recommendations[:top_n]

# ============================================
# FLASK ROUTES
# ============================================

@app.route('/')
def index():
    """Home page with preference form"""
    return render_template('index.html', 
                         genres=ALL_GENRES,
                         directors=ALL_DIRECTORS,
                         tags=ALL_TAGS,
                         years=ALL_YEARS)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Get recommendations based on user preferences"""
    try:
        user_prefs = {}
        
        genres = request.form.getlist('genres')
        if genres:
            user_prefs['genres'] = genres
        
        director = request.form.get('director')
        if director:
            user_prefs['director'] = director
        
        year_start = request.form.get('year_start')
        year_end = request.form.get('year_end')
        if year_start and year_end and year_start.isdigit() and year_end.isdigit():
            user_prefs['year_range'] = [int(year_start), int(year_end)]
        elif year_start and year_start.isdigit():
            user_prefs['year_range'] = [int(year_start), int(year_start) + 10]
        
        min_rating = request.form.get('min_rating')
        if min_rating and min_rating.replace('.', '').isdigit():
            user_prefs['min_rating'] = float(min_rating)
        
        tags = request.form.getlist('tags')
        if tags:
            user_prefs['tags'] = tags
        
        recommendations = get_recommendations(user_prefs)
        
        return render_template('recommendations.html',
                             recommendations=recommendations,
                             preferences=user_prefs,
                             count=len(recommendations))
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', 
                         movie_count=len(MOVIES),
                         genre_count=len(ALL_GENRES),
                         tag_count=len(ALL_TAGS))

@app.route('/api/movies')
def api_movies():
    """API endpoint: Get all movies"""
    return jsonify(MOVIES)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint: Get recommendations"""
    data = request.get_json()
    recommendations = get_recommendations(data)
    return jsonify([{
        'id': r['movie']['id'],
        'title': r['movie']['title'],
        'year': r['movie']['year'],
        'director': r['movie']['director'],
        'genre': r['movie']['genre'],
        'rating': r['movie']['rating'],
        'similarity': r['similarity']
    } for r in recommendations])

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Server error occurred"), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🌟 AI RECOMMENDATION ENGINE - WEBSITE")
    print("=" * 70)
    print(f"📊 Database: {len(MOVIES)} movies loaded")
    print(f"🎭 {len(ALL_GENRES)} genres, {len(ALL_TAGS)} tags")
    print("=" * 70)
    print("🚀 Server running at: http://localhost:5000")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)