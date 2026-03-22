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
                    'popularity': int(row.get('popularity', 50)),
                    'release_decade': row.get('release_decade', '2010s'),
                    'mood_tags': row.get('mood_tags', '').split(';'),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
    
    return songs

# =============================================================================
# SCORING STRATEGIES (Strategy Pattern)
# Each strategy function takes (user_prefs, song) and returns (score, reasons).
# Switch modes by passing mode= to score_song() or recommend_songs().
# =============================================================================

def _score_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, list]:
    """Genre-First mode: genre is weighted 3x, mood 1x, energy 1x."""
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 3.0
        reasons.append('Genre match (+3.0) [Genre-First]')

    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 1.0
        reasons.append('Mood match (+1.0)')

    target_energy = user_prefs.get('energy', 0.5)
    energy_sim = 1.0 * (1.0 - abs(song['energy'] - target_energy))
    score += energy_sim
    reasons.append(f'Energy similarity ({energy_sim:.2f})')

    return (score, reasons)


def _score_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, list]:
    """Mood-First mode: mood is weighted 3x, genre 1x, energy 1x."""
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 1.0
        reasons.append('Genre match (+1.0)')

    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 3.0
        reasons.append('Mood match (+3.0) [Mood-First]')

    target_energy = user_prefs.get('energy', 0.5)
    energy_sim = 1.0 * (1.0 - abs(song['energy'] - target_energy))
    score += energy_sim
    reasons.append(f'Energy similarity ({energy_sim:.2f})')

    return (score, reasons)


def _score_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, list]:
    """Energy-Focused mode: energy similarity weighted 4x, genre 1x, mood 1x."""
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 1.0
        reasons.append('Genre match (+1.0)')

    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 1.0
        reasons.append('Mood match (+1.0)')

    target_energy = user_prefs.get('energy', 0.5)
    energy_sim = 4.0 * (1.0 - abs(song['energy'] - target_energy))
    score += energy_sim
    reasons.append(f'Energy similarity ({energy_sim:.2f}) [Energy-Focused]')

    return (score, reasons)


# Map mode names to strategy functions
SCORING_MODES = {
    'genre_first':     _score_genre_first,
    'mood_first':      _score_mood_first,
    'energy_focused':  _score_energy_focused,
}


def score_song(user_prefs: Dict, song: Dict, mode: str = 'default') -> Tuple[float, list]:
    """
    Score a single song based on user preferences.

    mode options:
      'default'        — original weighted scoring (genre +1.0, energy x2, bonuses)
      'genre_first'    — genre weighted 3x
      'mood_first'     — mood weighted 3x
      'energy_focused' — energy similarity weighted 4x

    Returns a tuple: (total_score, reasons_list)
    """
    # Delegate to a named strategy if one is requested
    if mode in SCORING_MODES:
        return SCORING_MODES[mode](user_prefs, song)

    # ---- Default scoring (original logic) ----
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

    # Energy similarity (2x multiplier)
    target_energy = user_prefs.get('energy', 0.5)
    energy_distance = abs(song['energy'] - target_energy)
    energy_sim = 2.0 * (1.0 - energy_distance)
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

    # Popularity bonus
    popularity = song.get('popularity', 50)
    if popularity >= 75:
        score += 0.4
        reasons.append(f'High popularity bonus (+0.4, popularity={popularity})')

    # Release decade bonus
    preferred_decade = user_prefs.get('preferred_decade', None)
    if preferred_decade and song.get('release_decade') == preferred_decade:
        score += 0.5
        reasons.append(f'Era match bonus (+0.5, {preferred_decade})')

    # Mood tags bonus: +0.3 per matching tag (max +0.6)
    preferred_tags = user_prefs.get('mood_tags', [])
    song_tags = song.get('mood_tags', [])
    tag_matches = [t for t in preferred_tags if t in song_tags]
    if tag_matches:
        tag_bonus = min(0.3 * len(tag_matches), 0.6)
        score += tag_bonus
        reasons.append(f'Mood tag match ({", ".join(tag_matches)}) (+{tag_bonus:.1f})')

    return (score, reasons)

def recommend_songs_diverse(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = 'default',
                            artist_penalty: float = 1.0, genre_penalty: float = 0.5) -> List[Tuple[Dict, float, str]]:
    """
    Greedy recommendation with Diversity Penalty.

    After each song is selected, any remaining song sharing the same artist
    gets its score reduced by artist_penalty, and any song sharing the same
    genre gets its score reduced by genre_penalty. This prevents the top-k
    list from being dominated by one artist or genre.

    Args:
        user_prefs:     User preference dictionary
        songs:          Full song catalog
        k:              Number of recommendations to return
        mode:           Scoring strategy (default / genre_first / mood_first / energy_focused)
        artist_penalty: Score deduction per repeated artist (+1.0 default)
        genre_penalty:  Score deduction per repeated genre  (+0.5 default)

    Returns:
        List of (song_dict, adjusted_score, explanation) tuples
    """
    # Step 1 — compute base scores for every song
    candidates = []
    for song in songs:
        base_score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = explain_recommendation(user_prefs, song, base_score, reasons, mode=mode)
        candidates.append([song, base_score, explanation])  # mutable list so we can update score

    selected = []
    selected_artists = []
    selected_genres = []

    for _ in range(k):
        if not candidates:
            break

        # Step 2 — apply accumulated penalties and pick highest adjusted score
        best_idx = max(range(len(candidates)), key=lambda i: candidates[i][1])
        best = candidates.pop(best_idx)
        selected.append(tuple(best))

        artist = best[0]['artist']
        genre  = best[0]['genre'].lower()

        # Step 3 — penalise remaining candidates that share artist or genre
        for candidate in candidates:
            if candidate[0]['artist'] == artist:
                candidate[1] -= artist_penalty
                if 'Diversity penalty: same artist' not in candidate[2]:
                    candidate[2] += f' | Diversity penalty: same artist (-{artist_penalty})'
            if candidate[0]['genre'].lower() == genre:
                candidate[1] -= genre_penalty
                if 'Diversity penalty: same genre' not in candidate[2]:
                    candidate[2] += f' | Diversity penalty: same genre (-{genre_penalty})'

        selected_artists.append(artist)
        selected_genres.append(genre)

    return selected


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = 'default') -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.

    Args:
        user_prefs: Dictionary with keys {genre, mood, energy, high_energy, likes_acoustic, ...}
        songs: List of song dictionaries
        k: Number of recommendations to return
        mode: Scoring strategy — 'default', 'genre_first', 'mood_first', 'energy_focused'

    Returns:
        List of tuples (song_dict, score, explanation)
    """
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = explain_recommendation(user_prefs, song, score, reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda x: x[1], reverse=True)

    return scored_songs[:k]

def explain_recommendation(user_prefs: Dict, song: Dict, score: float, reasons: list = None, mode: str = 'default') -> str:
    """
    Generate a human-readable explanation for why a song was recommended.

    Args:
        user_prefs: User preferences dictionary
        song: Song dictionary
        score: Total score for the song
        reasons: List of reason strings (if not provided, will be re-scored internally)
        mode: Scoring mode used (passed to score_song if re-scoring)
    """
    if reasons is None:
        _, reasons = score_song(user_prefs, song, mode=mode)

    if not reasons:
        return "good overall match for your taste profile"

    return "because it " + " and ".join(reasons)
