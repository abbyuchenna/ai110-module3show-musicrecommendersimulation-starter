import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Recommend top k songs for a user profile."""
        scored_songs = []
        for song in self.songs:
            score = self._score_song(user, song)
            explanation = self.explain_recommendation(user, song)
            scored_songs.append((song, score, explanation))
        
        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _, _ in scored_songs[:k]]

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Calculate a score for a song given user preferences."""
        score = 0.0
        
        # Genre match: +2.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        
        # Mood match: +1.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        
        # Energy similarity: 1.0 * (1 - |distance|)
        energy_distance = abs(song.energy - user.target_energy)
        energy_sim = 1.0 * (1.0 - energy_distance)
        score += energy_sim
        
        # Acoustic preference bonus
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness < 0.5:
            score += 0.3
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate an explanation for why a song was recommended."""
        reasons = []
        
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"matches your favorite genre ({song.genre})")
        
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"matches your favorite mood ({song.mood})")
        
        energy_match = abs(song.energy - user.target_energy)
        if energy_match < 0.15:
            reasons.append(f"energy level ({song.energy:.2f}) matches your target ({user.target_energy:.2f})")
        
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append(f"high acousticness ({song.acousticness:.2f})")
        
        if not reasons:
            reasons.append(f"good overall fit for your preferences")
        
        return "because it " + " and ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to floats
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, list]:
    """
    Score a single song based on user preferences.
    
    SENSITIVITY TEST VERSION:
    - Genre match HALVED: +1.0 (was +2.0)
    - Energy similarity DOUBLED: 2.0 * (1 - distance) (was 1.0 * (1 - distance))
    
    Returns a tuple: (total_score, reasons_list)
    
    Scoring breakdown:
    - Genre match: +1.0 (MODIFIED from +2.0)
    - Mood match: +1.0
    - Energy similarity: 2.0 * (1 - |distance|) (MODIFIED from 1.0 *)
    - Danceability bonus (if high energy): +0.3
    - Acousticness bonus (if preferred): +0.5
    """
    score = 0.0
    reasons = []
    
    # Genre match (HALVED from +2.0 to +1.0)
    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 1.0
        reasons.append('Genre match (+1.0)')
    
    # Mood match
    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 1.0
        reasons.append('Mood match (+1.0)')
    
    # Energy similarity (DOUBLED from 1.0* to 2.0*)
    target_energy = user_prefs.get('energy', 0.5)
    energy_distance = abs(song['energy'] - target_energy)
    energy_sim = 2.0 * (1.0 - energy_distance)  # Changed multiplier from 1.0 to 2.0
    score += energy_sim
    reasons.append(f'Energy similarity ({energy_sim:.2f})')
    
    # Danceability bonus
    if user_prefs.get('high_energy', False) and song['danceability'] > 0.7:
        score += 0.3
        reasons.append('Danceability bonus (+0.3)')
    
    # Acousticness preference
    if user_prefs.get('likes_acoustic', False) and song['acousticness'] > 0.5:
        score += 0.5
        reasons.append('Acousticness bonus (+0.5)')
    
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    
    Args:
        user_prefs: Dictionary with keys {genre, mood, energy, high_energy, likes_acoustic}
        songs: List of song dictionaries
        k: Number of recommendations to return
    
    Returns:
        List of tuples (song_dict, score, explanation)
    """
    scored_songs = []
    
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = explain_recommendation(user_prefs, song, score, reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]

def explain_recommendation(user_prefs: Dict, song: Dict, score: float, reasons: list = None) -> str:
    """
    Generate a human-readable explanation for why a song was recommended.
    
    Args:
        user_prefs: User preferences dictionary
        song: Song dictionary
        score: Total score for the song
        reasons: List of reason strings (if not provided, will be re-scored internally)
    """
    if reasons is None:
        _, reasons = score_song(user_prefs, song)
    
    if not reasons:
        return "good overall match for your taste profile"
    
    return "because it " + " and ".join(reasons)
