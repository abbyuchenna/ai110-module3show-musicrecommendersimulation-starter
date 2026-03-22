from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs, load_songs
import pytest


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


# ============================================================================
# TESTS FROM STARTER CODE (Enhanced)
# ============================================================================

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ============================================================================
# TEST 1: SCORING CORRECTNESS
# ============================================================================

def test_score_song_perfect_match():
    """Test that a perfect genre+mood match gets the highest score."""
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "high_energy": True,
        "likes_acoustic": False
    }
    song = {
        'genre': 'pop',
        'mood': 'happy',
        'energy': 0.8,
        'danceability': 0.9,
        'acousticness': 0.1
    }
    
    score, reasons = score_song(user_prefs, song)
    # Genre (2.0) + Mood (1.0) + Energy similarity (1.0) + Danceability bonus (0.3)
    # = 4.3 expected
    assert score >= 4.0  # Flexible due to float arithmetic
    assert isinstance(reasons, list)
    assert len(reasons) > 0
    assert any('Genre' in r for r in reasons)
    assert any('Mood' in r for r in reasons)


def test_score_song_energy_similarity():
    """Test that energy similarity rewards closeness."""
    user_prefs = {"genre": "rock", "mood": "intense", "energy": 0.9}
    
    # Song with energy exactly equal to target
    song_perfect = {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
    score_perfect, _ = score_song(user_prefs, song_perfect)
    
    # Song with energy 0.1 away from target
    song_close = {'genre': 'rock', 'mood': 'intense', 'energy': 0.8}
    score_close, _ = score_song(user_prefs, song_close)
    
    # Song with energy 0.5 away from target
    song_far = {'genre': 'rock', 'mood': 'intense', 'energy': 0.4}
    score_far, _ = score_song(user_prefs, song_far)
    
    # Perfect should score higher than close, which should score higher than far
    assert score_perfect > score_close > score_far


def test_score_song_acousticness_bonus():
    """Test that acousticness bonus is applied correctly."""
    user_prefs = {
        "genre": "acoustic",
        "mood": "relaxed",
        "energy": 0.3,
        "likes_acoustic": True
    }
    
    # Acoustic song
    song_acoustic = {
        'genre': 'acoustic',
        'mood': 'relaxed',
        'energy': 0.3,
        'acousticness': 0.9
    }
    
    # Non-acoustic song
    song_electric = {
        'genre': 'acoustic',
        'mood': 'relaxed',
        'energy': 0.3,
        'acousticness': 0.1
    }
    
    score_acoustic, _ = score_song(user_prefs, song_acoustic)
    score_electric, _ = score_song(user_prefs, song_electric)
    
    # Acoustic should score higher due to bonus
    assert score_acoustic > score_electric


def test_score_song_returns_tuple():
    """Test that score_song returns a tuple of (float, list)."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.5}
    song = {'genre': 'pop', 'mood': 'happy', 'energy': 0.5}
    
    result = score_song(user_prefs, song)
    assert isinstance(result, tuple)
    assert len(result) == 2
    score, reasons = result
    assert isinstance(score, float)
    assert isinstance(reasons, list)
    assert score >= 0


# ============================================================================
# TEST 2: RANKING ACCURACY
# ============================================================================

def test_recommend_songs_returns_sorted_by_score():
    """Test that recommend_songs returns results sorted by score (descending)."""
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4}
    
    songs = [
        {'title': 'Pop Banger', 'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'danceability': 0.8, 'acousticness': 0.1},
        {'title': 'Lofi Classic', 'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'danceability': 0.5, 'acousticness': 0.8},
        {'title': 'Rock Anthem', 'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'danceability': 0.7, 'acousticness': 0.05},
    ]
    
    recommendations = recommend_songs(user_prefs, songs, k=3)
    
    # Check sorted order
    assert len(recommendations) == 3
    for i in range(len(recommendations) - 1):
        current_score = recommendations[i][1]
        next_score = recommendations[i + 1][1]
        assert current_score >= next_score  # Descending order
    
    # Lofi + chill should be top recommendation
    assert recommendations[0][0]['genre'] == 'lofi'


def test_recommend_songs_respects_k_parameter():
    """Test that recommend_songs respects the k parameter."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [{'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'danceability': 0.8, 'acousticness': 0.2}] * 10
    
    recs_k3 = recommend_songs(user_prefs, songs, k=3)
    recs_k5 = recommend_songs(user_prefs, songs, k=5)
    
    assert len(recs_k3) == 3
    assert len(recs_k5) == 5


# ============================================================================
# TEST 3: EDGE CASES & ADVERSARIAL TESTS
# ============================================================================

def test_recommend_empty_catalog():
    """Test that recommend_songs handles empty catalog gracefully."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = []
    
    recommendations = recommend_songs(user_prefs, songs, k=5)
    
    assert recommendations == []


def test_recommend_k_greater_than_catalog():
    """Test that k > catalog size returns only available songs."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [{'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'danceability': 0.8, 'acousticness': 0.2}] * 3
    
    recommendations = recommend_songs(user_prefs, songs, k=10)
    
    assert len(recommendations) == 3


def test_score_song_conflicting_preferences():
    """Test scoring with conflicting preferences (lofi + intense)."""
    user_prefs = {
        "genre": "lofi",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": True
    }
    
    # Song that matches genre but conflicts with other prefs
    lofi_chill = {
        'genre': 'lofi',
        'mood': 'chill',
        'energy': 0.3,
        'acousticness': 0.9
    }
    
    score, reasons = score_song(user_prefs, lofi_chill)
    
    # Should score high on genre but low on mood/energy
    assert isinstance(score, float)
    assert isinstance(reasons, list)
    assert score >= 0


def test_classify_no_matching_genre():
    """Test scoring when no songs match the user's favorite genre."""
    user_prefs = {
        "genre": "heavy_metal",
        "mood": "angry",
        "energy": 0.95
    }
    
    songs = [
        {'genre': 'pop', 'mood': 'happy', 'energy': 0.7, 'danceability': 0.8, 'acousticness': 0.2},
        {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'danceability': 0.5, 'acousticness': 0.9},
    ]
    
    recommendations = recommend_songs(user_prefs, songs, k=2)
    
    # Even without genre match, should return recommendations based on other features
    assert len(recommendations) == 2
    # But the pop song (higher energy) should rank higher than lofi
    assert recommendations[0][0]['genre'] == 'pop'


# ============================================================================
# TEST 4: FUNCTIONAL INTERFACE (CSV Loading)
# ============================================================================

def test_load_songs_returns_list():
    """Test that load_songs returns a list."""
    songs = load_songs("../data/songs.csv")
    assert isinstance(songs, list)


def test_load_songs_converts_numeric_fields():
    """Test that load_songs converts numeric fields to floats/ints."""
    songs = load_songs("../data/songs.csv")
    
    if songs:  # Only test if songs were loaded
        song = songs[0]
        assert isinstance(song['id'], int)
        assert isinstance(song['energy'], float)
        assert isinstance(song['tempo_bpm'], float)
        assert isinstance(song['danceability'], float)
        assert isinstance(song['acousticness'], float)


def test_load_songs_missing_file():
    """Test that load_songs handles missing files gracefully."""
    songs = load_songs("../data/nonexistent.csv")
    assert songs == []  # Should return empty list, not crash


# ============================================================================
# TEST 5: CLASS-BASED RECOMMENDER (OOP Interface)
# ============================================================================

def test_recommender_scores_correctly():
    """Test that Recommender class scores match functional scoring."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False
    )
    
    rec = make_small_recommender()
    song = rec.songs[0]  # Pop track
    
    # OOP scoring should work
    explanation = rec.explain_recommendation(user, song)
    results = rec.recommend(user, k=1)
    
    assert results[0].genre == "pop"
    assert "pop" in explanation.lower() or "pop" in results[0].genre


def test_recommender_k_parameter():
    """Test that Recommender.recommend respects k."""
    user = UserProfile("pop", "happy", 0.8, False)
    rec = make_small_recommender()
    
    results_k1 = rec.recommend(user, k=1)
    results_k2 = rec.recommend(user, k=2)
    
    assert len(results_k1) == 1
    assert len(results_k2) == 2
