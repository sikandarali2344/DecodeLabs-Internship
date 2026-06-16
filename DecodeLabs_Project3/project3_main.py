# ============================================
# PROJECT 3: AI RECOMMENDATION LOGIC - PRODUCTION GRADE
# Batch: 2026 | DecodeLabs
# AI Engineer: Sikandar
# ============================================

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter
import random
import warnings
warnings.filterwarnings('ignore')

# Create folders
os.makedirs('outputs/project3', exist_ok=True)
os.makedirs('outputs/project3/charts', exist_ok=True)
os.makedirs('models/project3', exist_ok=True)
os.makedirs('reports/project3', exist_ok=True)

# Set style for beautiful plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 80)
print("🌟 DECODELABS - AI RECOMMENDATION ENGINE (PRODUCTION GRADE)")
print("=" * 80)
print("Batch 2026 | Project 3: Recommendation Logic")
print("AI Engineer: Sikandar")
print("=" * 80)

# ============================================
# PART 1: ENHANCED DATASET
# ============================================

class MovieDatabase:
    """Production-grade movie database with rich metadata"""
    
    def __init__(self):
        self.movies = []
        self.genres = []
        self.directors = []
        self.tags = []
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize with rich movie data"""
        
        movies_data = [
            # Action/Adventure
            {
                "id": 1,
                "title": "The Dark Knight",
                "year": 2008,
                "director": "Christopher Nolan",
                "genre": ["Action", "Crime", "Drama"],
                "rating": 4.9,
                "votes": 2345678,
                "duration": 152,
                "language": "English",
                "country": "USA",
                "tags": ["superhero", "dark", "psychological", "joker", "batman"],
                "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham..."
            },
            {
                "id": 2,
                "title": "Inception",
                "year": 2010,
                "director": "Christopher Nolan",
                "genre": ["Action", "Sci-Fi", "Thriller"],
                "rating": 4.7,
                "votes": 1987654,
                "duration": 148,
                "language": "English",
                "country": "USA",
                "tags": ["mind-bending", "dreams", "heist", "philosophical", "time"],
                "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
                "plot": "A thief who steals corporate secrets through the use of dream-sharing technology..."
            },
            {
                "id": 3,
                "title": "The Avengers",
                "year": 2012,
                "director": "Joss Whedon",
                "genre": ["Action", "Adventure", "Sci-Fi"],
                "rating": 4.5,
                "votes": 1567890,
                "duration": 143,
                "language": "English",
                "country": "USA",
                "tags": ["marvel", "superhero", "ensemble", "comic", "action-packed"],
                "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"],
                "plot": "Earth's mightiest heroes must come together and learn to fight as a team..."
            },
            {
                "id": 4,
                "title": "Mad Max: Fury Road",
                "year": 2015,
                "director": "George Miller",
                "genre": ["Action", "Adventure", "Sci-Fi"],
                "rating": 4.7,
                "votes": 1123456,
                "duration": 120,
                "language": "English",
                "country": "Australia",
                "tags": ["post-apocalyptic", "car-chase", "dystopian", "feminist", "epic"],
                "cast": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
                "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler..."
            },
            {
                "id": 5,
                "title": "The Matrix",
                "year": 1999,
                "director": "Lana Wachowski, Lilly Wachowski",
                "genre": ["Action", "Sci-Fi"],
                "rating": 4.8,
                "votes": 1987654,
                "duration": 136,
                "language": "English",
                "country": "USA",
                "tags": ["philosophical", "cyberpunk", "classic", "mind-bending", "futuristic"],
                "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                "plot": "A computer programmer discovers that reality is a simulation..."
            },
            
            # Sci-Fi
            {
                "id": 6,
                "title": "Interstellar",
                "year": 2014,
                "director": "Christopher Nolan",
                "genre": ["Sci-Fi", "Drama", "Adventure"],
                "rating": 4.6,
                "votes": 1765432,
                "duration": 169,
                "language": "English",
                "country": "USA",
                "tags": ["space", "time-travel", "emotional", "scientific", "gravity"],
                "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
                "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival..."
            },
            {
                "id": 7,
                "title": "Avatar",
                "year": 2009,
                "director": "James Cameron",
                "genre": ["Action", "Adventure", "Sci-Fi"],
                "rating": 4.3,
                "votes": 1345678,
                "duration": 162,
                "language": "English",
                "country": "USA",
                "tags": ["3d", "aliens", "visual-effects", "epic", "environmental"],
                "cast": ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver"],
                "plot": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders..."
            },
            {
                "id": 8,
                "title": "Arrival",
                "year": 2016,
                "director": "Denis Villeneuve",
                "genre": ["Sci-Fi", "Drama"],
                "rating": 4.5,
                "votes": 987654,
                "duration": 116,
                "language": "English",
                "country": "USA",
                "tags": ["intellectual", "linguistics", "emotional", "philosophical", "alien"],
                "cast": ["Amy Adams", "Jeremy Renner", "Forest Whitaker"],
                "plot": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world..."
            },
            
            # Drama
            {
                "id": 9,
                "title": "The Shawshank Redemption",
                "year": 1994,
                "director": "Frank Darabont",
                "genre": ["Drama"],
                "rating": 4.9,
                "votes": 2789012,
                "duration": 142,
                "language": "English",
                "country": "USA",
                "tags": ["hope", "prison", "friendship", "classic", "inspirational"],
                "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
                "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency..."
            },
            {
                "id": 10,
                "title": "The Godfather",
                "year": 1972,
                "director": "Francis Ford Coppola",
                "genre": ["Crime", "Drama"],
                "rating": 4.9,
                "votes": 2345678,
                "duration": 175,
                "language": "English",
                "country": "USA",
                "tags": ["mafia", "classic", "masterpiece", "family", "crime"],
                "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
                "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son..."
            },
            {
                "id": 11,
                "title": "The Social Network",
                "year": 2010,
                "director": "David Fincher",
                "genre": ["Drama", "Biography"],
                "rating": 4.4,
                "votes": 876543,
                "duration": 120,
                "language": "English",
                "country": "USA",
                "tags": ["tech", "entrepreneurship", "facebook", "legal-drama", "modern"],
                "cast": ["Jesse Eisenberg", "Andrew Garfield", "Justin Timberlake"],
                "plot": "The story of the founding of Facebook and the resulting legal battles..."
            },
            
            # Comedy/Romance
            {
                "id": 12,
                "title": "The Grand Budapest Hotel",
                "year": 2014,
                "director": "Wes Anderson",
                "genre": ["Comedy", "Adventure", "Drama"],
                "rating": 4.4,
                "votes": 765432,
                "duration": 99,
                "language": "English",
                "country": "USA",
                "tags": ["quirky", "visual", "nostalgic", "whimsical", "artistic"],
                "cast": ["Ralph Fiennes", "Tony Revolori", "Saoirse Ronan"],
                "plot": "A writer encounters the owner of an aging grand hotel who tells him of his early days as a lobby boy..."
            },
            {
                "id": 13,
                "title": "Titanic",
                "year": 1997,
                "director": "James Cameron",
                "genre": ["Romance", "Drama"],
                "rating": 4.5,
                "votes": 1987654,
                "duration": 195,
                "language": "English",
                "country": "USA",
                "tags": ["love", "tragedy", "historical", "epic", "emotional"],
                "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
                "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic..."
            },
            
            # Thriller/Horror
            {
                "id": 14,
                "title": "The Silence of the Lambs",
                "year": 1991,
                "director": "Jonathan Demme",
                "genre": ["Thriller", "Crime", "Drama"],
                "rating": 4.8,
                "votes": 1543210,
                "duration": 118,
                "language": "English",
                "country": "USA",
                "tags": ["psychological", "serial-killer", "classic", "suspense", "fbi"],
                "cast": ["Jodie Foster", "Anthony Hopkins", "Scott Glenn"],
                "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer..."
            },
            {
                "id": 15,
                "title": "Get Out",
                "year": 2017,
                "director": "Jordan Peele",
                "genre": ["Horror", "Mystery", "Thriller"],
                "rating": 4.5,
                "votes": 987654,
                "duration": 104,
                "language": "English",
                "country": "USA",
                "tags": ["social-thriller", "psychological", "horror", "mind-bending", "twist"],
                "cast": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
                "plot": "A young African-American man visits his white girlfriend's family estate where he learns disturbing secrets..."
            }
        ]
        
        self.movies = movies_data
        
        # Extract metadata
        self.genres = sorted(set([g for movie in self.movies for g in movie['genre']]))
        self.directors = sorted(set([m['director'] for m in self.movies]))
        self.tags = sorted(set([t for movie in self.movies for t in movie['tags']]))
        
        print(f"✅ Loaded {len(self.movies)} movies")
        print(f"   🎭 {len(self.genres)} genres")
        print(f"   🎬 {len(self.directors)} directors")
        print(f"   🏷️ {len(self.tags)} tags")

# ============================================
# PART 2: ADVANCED RECOMMENDATION ENGINE
# ============================================

class AdvancedRecommendationEngine:
    """Advanced recommendation engine with multiple algorithms"""
    
    def __init__(self, database):
        self.db = database
        self.user_history = []
        self.user_preferences = {}
        self.similarity_threshold = 0.3
        self.algorithm = "weighted"  # Options: weighted, cosine, hybrid
    
    def calculate_similarity_weighted(self, user_prefs, movie):
        """Weighted similarity calculation"""
        score = 0
        weights = {
            'genre': 2.0,
            'director': 1.5,
            'tags': 1.0,
            'year': 0.5,
            'rating': 0.3,
            'cast': 0.5
        }
        
        # Genre matching (HIGHEST WEIGHT)
        if 'genres' in user_prefs and user_prefs['genres']:
            matched_genres = set(user_prefs['genres']).intersection(set(movie['genre']))
            if matched_genres:
                score += weights['genre'] * (len(matched_genres) / len(user_prefs['genres']))
        
        # Director matching
        if 'director' in user_prefs and user_prefs['director']:
            if user_prefs['director'].lower() in movie['director'].lower():
                score += weights['director']
        
        # Tags matching
        if 'tags' in user_prefs and user_prefs['tags']:
            matched_tags = set(user_prefs['tags']).intersection(set(movie['tags']))
            if matched_tags:
                score += weights['tags'] * (len(matched_tags) / len(user_prefs['tags']))
        
        # Year preference
        if 'year_range' in user_prefs:
            year_range = user_prefs['year_range']
            if year_range[0] <= movie['year'] <= year_range[1]:
                score += weights['year']
        
        # Rating preference
        if 'min_rating' in user_prefs:
            if movie['rating'] >= user_prefs['min_rating']:
                score += weights['rating'] * (movie['rating'] / 5.0)
        
        # Cast matching
        if 'cast' in user_prefs and user_prefs['cast']:
            matched_cast = set(user_prefs['cast']).intersection(set(movie['cast']))
            if matched_cast:
                score += weights['cast'] * (len(matched_cast) / len(user_prefs['cast']))
        
        return score
    
    def calculate_similarity_cosine(self, user_prefs, movie):
        """Cosine similarity between user preferences and movie features"""
        # Create feature vectors
        user_vector = []
        movie_vector = []
        
        # Genre features
        for genre in self.db.genres:
            user_vector.append(1 if genre in user_prefs.get('genres', []) else 0)
            movie_vector.append(1 if genre in movie['genre'] else 0)
        
        # Tag features
        for tag in self.db.tags:
            user_vector.append(1 if tag in user_prefs.get('tags', []) else 0)
            movie_vector.append(1 if tag in movie['tags'] else 0)
        
        # Director feature
        user_vector.append(1 if 'director' in user_prefs and user_prefs['director'].lower() in movie['director'].lower() else 0)
        movie_vector.append(1)
        
        # Convert to numpy arrays
        user_vector = np.array(user_vector)
        movie_vector = np.array(movie_vector)
        
        # Calculate cosine similarity
        if np.linalg.norm(user_vector) == 0 or np.linalg.norm(movie_vector) == 0:
            return 0
        
        similarity = np.dot(user_vector, movie_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(movie_vector))
        return similarity * 100  # Convert to percentage
    
    def calculate_similarity_hybrid(self, user_prefs, movie):
        """Hybrid approach combining weighted and cosine similarity"""
        weighted_score = self.calculate_similarity_weighted(user_prefs, movie)
        cosine_score = self.calculate_similarity_cosine(user_prefs, movie)
        
        # Normalize weighted score
        max_weighted = 5.0  # Maximum possible weighted score
        weighted_normalized = (weighted_score / max_weighted) * 100
        
        # Hybrid: 60% weighted, 40% cosine
        hybrid_score = (0.6 * weighted_normalized) + (0.4 * cosine_score)
        return min(hybrid_score, 100)  # Cap at 100%
    
    def get_recommendations(self, user_preferences, algorithm="weighted", top_n=5):
        """Get top N recommendations using specified algorithm"""
        self.user_preferences = user_preferences
        self.algorithm = algorithm
        
        recommendations = []
        
        for movie in self.db.movies:
            if algorithm == "weighted":
                score = self.calculate_similarity_weighted(user_preferences, movie)
                # Normalize to percentage
                max_score = 5.0
                score_percent = min((score / max_score) * 100, 100)
            elif algorithm == "cosine":
                score_percent = self.calculate_similarity_cosine(user_preferences, movie)
            else:  # hybrid
                score_percent = self.calculate_similarity_hybrid(user_preferences, movie)
            
            # Apply user history penalty
            if movie['title'] in self.user_history:
                score_percent *= 0.7  # 30% penalty for already watched
            
            recommendations.append({
                'movie': movie,
                'similarity': round(score_percent, 1),
                'score': score_percent
            })
        
        # Sort by similarity score
        recommendations.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top N
        return recommendations[:top_n]
    
    def get_diverse_recommendations(self, user_preferences, top_n=5):
        """Get diverse recommendations (different genres/directors)"""
        recommendations = self.get_recommendations(user_preferences, "hybrid", top_n*2)
        
        # Ensure diversity
        diverse_list = []
        used_genres = set()
        used_directors = set()
        
        for rec in recommendations:
            movie = rec['movie']
            movie_genres = set(movie['genre'])
            
            # Check if this adds diversity
            if not movie_genres.intersection(used_genres) or len(used_genres) < 2:
                diverse_list.append(rec)
                used_genres.update(movie_genres)
                used_directors.add(movie['director'])
            
            if len(diverse_list) >= top_n:
                break
        
        return diverse_list
    
    def add_to_history(self, movie_title):
        """Track user's watched history"""
        if movie_title not in self.user_history:
            self.user_history.append(movie_title)

# ============================================
# PART 3: USER INTERFACE & VISUALIZATIONS
# ============================================

class RecommendationUI:
    """Interactive UI for recommendation engine"""
    
    def __init__(self, engine):
        self.engine = engine
        self.user_prefs = {}
    
    def collect_preferences(self):
        """Collect user preferences with rich input"""
        print("\n" + "=" * 80)
        print("🎯 STEP 1: TELL US WHAT YOU LIKE")
        print("=" * 80)
        
        print(f"\n📌 Available Genres: {', '.join(self.engine.db.genres[:10])}...")
        genres_input = input("\n   What genres do you enjoy? (comma separated): ")
        if genres_input.strip():
            self.user_prefs['genres'] = [g.strip() for g in genres_input.split(',') if g.strip()]
        
        print(f"\n📌 Favorite Directors: {', '.join(self.engine.db.directors[:8])}...")
        director = input("   Who's your favorite director? (press Enter to skip): ")
        if director.strip():
            self.user_prefs['director'] = director.strip()
        
        print("\n📌 Preferred Year Range:")
        start_year = input("   Start year (e.g., 1990, press Enter to skip): ")
        if start_year.strip():
            try:
                start = int(start_year)
                end = input("   End year (e.g., 2020): ")
                end = int(end) if end else start + 10
                self.user_prefs['year_range'] = [start, end]
            except:
                print("   ⚠️ Invalid year range, skipping...")
        
        print("\n📌 Minimum Rating (1-5):")
        min_rating = input("   What's the minimum rating you'd accept? (press Enter to skip): ")
        if min_rating.strip():
            try:
                self.user_prefs['min_rating'] = float(min_rating)
            except:
                print("   ⚠️ Invalid rating, skipping...")
        
        print(f"\n📌 Available Tags (sample): {', '.join(self.engine.db.tags[:10])}...")
        tags_input = input("   What themes/tags do you like? (comma separated): ")
        if tags_input.strip():
            self.user_prefs['tags'] = [t.strip() for t in tags_input.split(',') if t.strip()]
        
        print("\n📌 Favorite Actors:")
        cast_input = input("   Who are your favorite actors? (comma separated): ")
        if cast_input.strip():
            self.user_prefs['cast'] = [c.strip() for c in cast_input.split(',') if c.strip()]
        
        print("\n📌 Algorithm Selection:")
        print("   1. Weighted (Fast, accurate for explicit preferences)")
        print("   2. Cosine (Better for multi-dimensional matching)")
        print("   3. Hybrid (Best overall - combines both)")
        algo_choice = input("   Select algorithm (1-3, default=3): ")
        
        algo_map = {'1': 'weighted', '2': 'cosine', '3': 'hybrid'}
        self.user_prefs['algorithm'] = algo_map.get(algo_choice, 'hybrid')
        
        return self.user_prefs
    
    def display_recommendations(self, recommendations, method="recommendations"):
        """Display recommendations with rich formatting"""
        print("\n" + "=" * 80)
        print(f"🎬 YOUR TOP {len(recommendations)} RECOMMENDATIONS")
        print("=" * 80)
        
        # Summary stats
        avg_similarity = np.mean([r['similarity'] for r in recommendations])
        max_similarity = max([r['similarity'] for r in recommendations])
        
        print(f"\n📊 Match Stats: Average: {avg_similarity:.1f}% | Best: {max_similarity:.1f}%")
        print("-" * 80)
        
        for i, rec in enumerate(recommendations, 1):
            movie = rec['movie']
            similarity = rec['similarity']
            
            # Create visual bar
            bar_length = 30
            filled = int((similarity / 100) * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Rating stars
            stars = '⭐' * int(movie['rating']) + '☆' * (5 - int(movie['rating']))
            
            print(f"\n{i:2}. 🎥 {movie['title']} ({movie['year']})")
            print(f"    Match: {similarity:5.1f}% [{bar}]")
            print(f"    Rating: {movie['rating']}/5.0 {stars} ({movie['votes']:,} votes)")
            print(f"    Director: {movie['director']}")
            print(f"    Genre: {', '.join(movie['genre'])}")
            print(f"    Duration: {movie['duration']} min | Language: {movie['language']}")
            print(f"    Tags: {', '.join(movie['tags'][:5])}")
            print(f"    Plot: {movie['plot'][:150]}...")
            print(f"    Cast: {', '.join(movie['cast'][:3])}")
            
            # Match explanation
            reason = self._get_match_reason(movie, similarity)
            print(f"    💡 {reason}")
    
    def _get_match_reason(self, movie, similarity):
        """Generate detailed match reason"""
        reasons = []
        
        # Genre match
        if 'genres' in self.user_prefs:
            matched = set(self.user_prefs['genres']).intersection(set(movie['genre']))
            if matched:
                reasons.append(f"✓ Genre matches: {', '.join(matched)}")
        
        # Director match
        if 'director' in self.user_prefs:
            if self.user_prefs['director'].lower() in movie['director'].lower():
                reasons.append(f"✓ Director matches: {self.user_prefs['director']}")
        
        # Tag match
        if 'tags' in self.user_prefs:
            matched = set(self.user_prefs['tags']).intersection(set(movie['tags']))
            if matched:
                reasons.append(f"✓ Tags match: {', '.join(list(matched)[:3])}")
        
        # Rating match
        if 'min_rating' in self.user_prefs:
            if movie['rating'] >= self.user_prefs['min_rating']:
                reasons.append(f"✓ Meets rating requirement")
        
        if not reasons:
            return "📌 Based on your general preferences"
        
        return " | ".join(reasons[:3])
    
    def show_visualizations(self, recommendations):
        """Generate and display visualizations"""
        print("\n" + "=" * 80)
        print("📊 GENERATING VISUALIZATIONS")
        print("=" * 80)
        
        # Create DataFrame for analysis
        data = []
        for rec in recommendations:
            movie = rec['movie']
            data.append({
                'Movie': movie['title'],
                'Year': movie['year'],
                'Rating': movie['rating'],
                'Similarity': rec['similarity'],
                'Duration': movie['duration'],
                'Genres': movie['genre']
            })
        
        df = pd.DataFrame(data)
        
        # FIGURE 1: Recommendation Scores
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Similarity Scores
        ax1 = axes[0, 0]
        colors = plt.cm.viridis(np.linspace(0.3, 1, len(df)))
        bars = ax1.barh(df['Movie'], df['Similarity'], color=colors, edgecolor='black')
        ax1.set_xlabel('Similarity Score (%)', fontsize=12, fontweight='bold')
        ax1.set_title('🎯 Recommendation Match Scores', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 100)
        for bar, val in zip(bars, df['Similarity']):
            ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=9)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. Movie Ratings vs Similarity
        ax2 = axes[0, 1]
        scatter = ax2.scatter(df['Rating'], df['Similarity'], s=200, c=df['Year'], 
                              cmap='coolwarm', alpha=0.7, edgecolors='black')
        ax2.set_xlabel('Rating', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Similarity (%)', fontsize=12, fontweight='bold')
        ax2.set_title('⭐ Rating vs Match Score', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax2, label='Year')
        for idx, row in df.iterrows():
            ax2.annotate(row['Movie'], (row['Rating']+0.02, row['Similarity']), 
                        fontsize=8, alpha=0.8)
        ax2.grid(True, alpha=0.3)
        
        # 3. Year Distribution
        ax3 = axes[1, 0]
        years = df['Year'].value_counts().sort_index()
        ax3.bar(years.index, years.values, color='#2E86AB', edgecolor='black')
        ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax3.set_title('📅 Year Distribution of Recommendations', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Top Tags
        ax4 = axes[1, 1]
        all_tags = []
        for movie in self.engine.db.movies:
            all_tags.extend(movie['tags'])
        tag_counts = Counter(all_tags).most_common(10)
        tags, counts = zip(*tag_counts)
        ax4.barh(tags, counts, color='#A23B72', edgecolor='black')
        ax4.set_xlabel('Frequency', fontsize=12, fontweight='bold')
        ax4.set_title('🏷️ Most Popular Tags', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('outputs/project3/charts/recommendation_analysis.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✅ Visualization saved: 'outputs/project3/charts/recommendation_analysis.png'")
        
        # FIGURE 2: Genre Distribution
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Genre count in recommendations
        ax1 = axes[0]
        genre_counts = Counter()
        for rec in recommendations:
            genre_counts.update(rec['movie']['genre'])
        
        genres, counts = zip(*genre_counts.most_common())
        ax1.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90,
                colors=plt.cm.Set3(np.linspace(0, 1, len(genres))))
        ax1.set_title('🎭 Genre Distribution in Recommendations', fontsize=14, fontweight='bold')
        
        # Similarity by genre
        ax2 = axes[1]
        genre_scores = {}
        for rec in recommendations:
            for genre in rec['movie']['genre']:
                if genre not in genre_scores:
                    genre_scores[genre] = []
                genre_scores[genre].append(rec['similarity'])
        
        avg_scores = {genre: np.mean(scores) for genre, scores in genre_scores.items()}
        genres, scores = zip(*sorted(avg_scores.items(), key=lambda x: x[1], reverse=True))
        
        ax2.bar(genres, scores, color=plt.cm.viridis(np.linspace(0.3, 1, len(genres))))
        ax2.set_xlabel('Genre', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average Similarity (%)', fontsize=12, fontweight='bold')
        ax2.set_title('📊 Genre Match Strength', fontsize=14, fontweight='bold')
        ax2.tick_params(axis='x', rotation=15)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('outputs/project3/charts/genre_analysis.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✅ Visualization saved: 'outputs/project3/charts/genre_analysis.png'")
        
        # FIGURE 3: Recommendation Dashboard
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Summary table as heatmap
        summary_data = []
        for rec in recommendations[:5]:
            movie = rec['movie']
            summary_data.append([
                movie['title'],
                movie['year'],
                movie['rating'],
                rec['similarity'],
                len(movie['genre']),
                movie['duration']
            ])
        
        columns = ['Movie', 'Year', '⭐ Rating', 'Match %', 'Genres', 'Duration']
        df_summary = pd.DataFrame(summary_data, columns=columns)
        
        # Hide axes and create table
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df_summary.values, colLabels=df_summary.columns,
                        cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.5, 1.8)
        
        # Color code the cells
        for i, row in enumerate(df_summary.values):
            for j, val in enumerate(row):
                if j == 4:  # Match column
                    color = plt.cm.RdYlGn(val/100)
                    table[(i+1, j)].set_facecolor(color)
        
        ax.set_title('🎬 RECOMMENDATION DASHBOARD', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('outputs/project3/charts/dashboard.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✅ Visualization saved: 'outputs/project3/charts/dashboard.png'")
        
        return 'outputs/project3/charts/'

# ============================================
# PART 4: MAIN PROGRAM
# ============================================

def main():
    """Main program execution"""
    
    # Initialize
    print("\n🚀 INITIALIZING RECOMMENDATION ENGINE...")
    print("-" * 50)
    
    db = MovieDatabase()
    engine = AdvancedRecommendationEngine(db)
    ui = RecommendationUI(engine)
    
    # Display welcome
    print("\n" + "=" * 80)
    print("🌟 AI RECOMMENDATION ENGINE - PRODUCTION GRADE")
    print("=" * 80)
    print(f"📅 Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Database: {len(db.movies)} movies, {len(db.genres)} genres, {len(db.tags)} tags")
    print("=" * 80)
    
    # Collect user preferences
    user_prefs = ui.collect_preferences()
    
    print("\n" + "=" * 80)
    print("📊 YOUR PREFERENCES SUMMARY")
    print("=" * 80)
    
    for key, value in user_prefs.items():
        if key == 'algorithm':
            print(f"   • Algorithm: {value.upper()}")
        else:
            print(f"   • {key}: {value}")
    
    # Get recommendations
    print("\n🔍 FINDING YOUR PERFECT MOVIE MATCHES...")
    print("-" * 50)
    
    algorithm = user_prefs.get('algorithm', 'hybrid')
    recommendations = engine.get_recommendations(user_prefs, algorithm=algorithm, top_n=5)
    
    # Display
    ui.display_recommendations(recommendations)
    
    # Show visualizations
    charts_dir = ui.show_visualizations(recommendations)
    
    # Save results
    save_results(user_prefs, recommendations)
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ RECOMMENDATION COMPLETE!")
    print("=" * 80)
    print("\n📁 OUTPUTS GENERATED:")
    print(f"   • {charts_dir}")
    print("   • outputs/project3/recommendations.json")
    print("   • outputs/project3/recommendations.txt")
    print("   • outputs/project3/recommendations_detailed.json")
    print("\n📊 VISUALIZATIONS:")
    print("   • recommendation_analysis.png")
    print("   • genre_analysis.png")
    print("   • dashboard.png")
    
    # Ask for more
    print("\n" + "-" * 50)
    while True:
        choice = input("\n🔄 OPTIONS:\n  [1] Try another search\n  [2] Get diverse recommendations\n  [3] Exit\n\nSelect option: ")
        
        if choice == '1':
            main()
            return
        elif choice == '2':
            diverse = engine.get_diverse_recommendations(user_prefs, top_n=5)
            ui.display_recommendations(diverse, "diverse")
        elif choice == '3':
            print("\n" + "=" * 80)
            print("🌟 THANK YOU FOR USING AI RECOMMENDATION ENGINE!")
            print("=" * 80)
            print("🏆 Created by Sikandar 2026 | DecodeLabs")
            print("📧 decodelabs.tech@gmail.com")
            print("🌎 www.decodelabs.tech")
            print("=" * 80)
            break
        else:
            print("❌ Invalid option, please try again")

def save_results(user_prefs, recommendations):
    """Save results to multiple formats"""
    
    # JSON format
    with open('outputs/project3/recommendations.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'user_preferences': user_prefs,
            'recommendations': [
                {
                    'title': rec['movie']['title'],
                    'year': rec['movie']['year'],
                    'director': rec['movie']['director'],
                    'genre': rec['movie']['genre'],
                    'rating': rec['movie']['rating'],
                    'tags': rec['movie']['tags'],
                    'similarity_score': rec['similarity'],
                    'plot': rec['movie']['plot'][:200],
                    'cast': rec['movie']['cast'][:3]
                }
                for rec in recommendations
            ]
        }, f, indent=2)
    
    # Text format
    with open('outputs/project3/recommendations.txt', 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("AI RECOMMENDATION ENGINE - RESULTS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("USER PREFERENCES:\n")
        for key, value in user_prefs.items():
            f.write(f"  • {key}: {value}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("TOP RECOMMENDATIONS:\n")
        f.write("=" * 80 + "\n\n")
        
        for i, rec in enumerate(recommendations, 1):
            movie = rec['movie']
            f.write(f"{i}. {movie['title']} ({movie['year']})\n")
            f.write(f"   Match: {rec['similarity']:.1f}%\n")
            f.write(f"   Director: {movie['director']}\n")
            f.write(f"   Genre: {', '.join(movie['genre'])}\n")
            f.write(f"   Rating: {movie['rating']}/5.0\n")
            f.write(f"   Tags: {', '.join(movie['tags'])}\n")
            f.write(f"   Plot: {movie['plot'][:150]}...\n\n")
    
    # Detailed format (for data analysis)
    with open('outputs/project3/recommendations_detailed.json', 'w') as f:
        detailed_data = {
            'timestamp': datetime.now().isoformat(),
            'user_preferences': user_prefs,
            'analysis': {
                'total_recommendations': len(recommendations),
                'average_similarity': np.mean([r['similarity'] for r in recommendations]),
                'max_similarity': max([r['similarity'] for r in recommendations]),
                'min_similarity': min([r['similarity'] for r in recommendations]),
                'genre_distribution': dict(Counter([g for rec in recommendations for g in rec['movie']['genre']])),
                'director_distribution': dict(Counter([rec['movie']['director'] for rec in recommendations])),
                'year_range': {
                    'min': min([rec['movie']['year'] for rec in recommendations]),
                    'max': max([rec['movie']['year'] for rec in recommendations])
                }
            },
            'recommendations': [
                {
                    'movie': rec['movie'],
                    'similarity': rec['similarity']
                }
                for rec in recommendations
            ]
        }
        json.dump(detailed_data, f, indent=2)
    
    print("✅ Results saved successfully!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session ended by user")
        print("🌟 Thank you for using AI Recommendation Engine!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your inputs and try again.")