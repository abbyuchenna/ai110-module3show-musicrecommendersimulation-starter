"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_song


def print_recommendations_clean(profile_name: str, user_prefs: dict, songs: list, recommendations: list) -> None:
    """
    Print recommendations in a clean, readable format.
    
    Args:
        profile_name: Name of the user profile
        user_prefs: Dictionary of user preferences
        songs: Full song list (for re-scoring to get reasons)
        recommendations: List of (song, score, explanation) tuples
    """
    print("=" * 90)
    print(f"🎵 {profile_name.upper()}")
    print("=" * 90)
    print(f"Preferences: {user_prefs['genre'].title()} • {user_prefs['mood'].title()} • Energy: {user_prefs['energy']}")
    print()
    
    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        
        # Main line: [Rank] Title by Artist - Score: X.XX
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        
        # Get reasons from re-scoring
        _, reasons = score_song(user_prefs, song)
        
        # Print reasons indented below
        print("   Reasons:")
        for reason in reasons:
            print(f"     • {reason}")
        
        # Print additional song details indented
        print(f"   Details: {song['genre'].title()} • {song['mood'].title()} • Energy: {song['energy']:.2f}")
        print()


def main() -> None:
    songs = load_songs("../data/songs.csv")
    
    if not songs:
        print("No songs loaded. Exiting.")
        return

    # Test Profile 1: Pop & Happy Lover
    user_prefs_1 = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "high_energy": True,
        "likes_acoustic": False
    }
    recommendations_1 = recommend_songs(user_prefs_1, songs, k=3)
    print_recommendations_clean("Pop & Happy Lover", user_prefs_1, songs, recommendations_1)

    # Test Profile 2: Lofi & Chill Listener
    user_prefs_2 = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "high_energy": False,
        "likes_acoustic": True
    }
    recommendations_2 = recommend_songs(user_prefs_2, songs, k=3)
    print_recommendations_clean("Lofi & Chill Listener", user_prefs_2, songs, recommendations_2)

    # Test Profile 3: Rock & Intense Energy Seeker
    user_prefs_3 = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "high_energy": True,
        "likes_acoustic": False
    }
    recommendations_3 = recommend_songs(user_prefs_3, songs, k=3)
    print_recommendations_clean("Rock & Intense Energy Seeker", user_prefs_3, songs, recommendations_3)

    # ============================================================================
    # ADVERSARIAL / EDGE CASE PROFILES
    # ============================================================================
    
    # Adversarial Profile 1: Conflicting Preferences
    # High energy (0.95) + Sad mood = rare combination
    # System must choose: match mood or match energy
    print("\n" + "=" * 90)
    print("⚠️  ADVERSARIAL TEST 1: CONFLICTING PREFERENCES (High Energy + Sad Mood)")
    print("=" * 90)
    print("Challenge: Most sad songs have LOW energy. User wants high-energy sadness (oxymoron).")
    print("Expected: Weak recommendations; low total scores.\n")
    
    adversarial_conflicting = {
        "genre": "indie",
        "mood": "sad",
        "energy": 0.95,
        "high_energy": True,
        "likes_acoustic": False
    }
    recommendations_adv1 = recommend_songs(adversarial_conflicting, songs, k=3)
    print_recommendations_clean("High-Energy Sad Indie Fan", adversarial_conflicting, songs, recommendations_adv1)

    # Adversarial Profile 2: Incompatible Feature Combo
    # Acoustic + Metal = contradictory (metal is almost never acoustic)
    print("\n" + "=" * 90)
    print("⚠️  ADVERSARIAL TEST 2: INCOMPATIBLE FEATURES (Acoustic + Metal)")
    print("=" * 90)
    print("Challenge: Metal songs are rarely acoustic (<15% acousticness).")
    print("Expected: Genre match (+2.0) but no acousticness bonus; conflicted ranking.\n")
    
    adversarial_acoustic_metal = {
        "genre": "metal",
        "mood": "intense",
        "energy": 0.92,
        "high_energy": True,
        "likes_acoustic": True
    }
    recommendations_adv2 = recommend_songs(adversarial_acoustic_metal, songs, k=3)
    print_recommendations_clean("Acoustic Metal Enthusiast", adversarial_acoustic_metal, songs, recommendations_adv2)

    # Adversarial Profile 3: Neutral/Minimal Preferences
    # Energy 0.5 (middle) = no strong energy preference
    # Only genre/mood drive ranking; many songs tie
    print("\n" + "=" * 90)
    print("⚠️  ADVERSARIAL TEST 3: NEUTRAL PREFERENCES (No Signal)")
    print("=" * 90)
    print("Challenge: Energy 0.5 (middle) gives similar scores to all songs.")
    print("Expected: Ranking becomes arbitrary; many songs score identically.\n")
    
    adversarial_neutral = {
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.5,
        "high_energy": False,
        "likes_acoustic": False
    }
    recommendations_adv3 = recommend_songs(adversarial_neutral, songs, k=3)
    print_recommendations_clean("Neutral Jazz Listener (Minimal Signal)", adversarial_neutral, songs, recommendations_adv3)


if __name__ == "__main__":
    main()
