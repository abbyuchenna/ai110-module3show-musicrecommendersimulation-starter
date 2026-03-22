"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs, recommend_songs_diverse, score_song


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
        tags = ", ".join(song.get('mood_tags', []))
        print(f"   Details: {song['genre'].title()} • {song['mood'].title()} • Energy: {song['energy']:.2f} • Popularity: {song.get('popularity', '?')} • {song.get('release_decade', '?')} • Tags: {tags}")
        print()


def print_recommendations_table(profile_name: str, user_prefs: dict, songs: list, recommendations: list) -> None:
    """
    Print recommendations as a formatted table using tabulate.
    Columns: Rank, Title, Artist, Genre, Score, Reasons
    """
    print("=" * 90)
    print(f"🎵 {profile_name.upper()} — TABLE VIEW")
    print(f"Preferences: {user_prefs['genre'].title()} • {user_prefs['mood'].title()} • Energy: {user_prefs['energy']}")
    print("=" * 90)

    rows = []
    for rank, rec in enumerate(recommendations, 1):
        song, score, _ = rec
        _, reasons = score_song(user_prefs, song)
        reasons_str = "\n".join(f"• {r}" for r in reasons)
        rows.append([rank, song['title'], song['artist'], song['genre'].title(), f"{score:.2f}", reasons_str])

    headers = ["#", "Title", "Artist", "Genre", "Score", "Reasons"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
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
        "likes_acoustic": False,
        "preferred_decade": "2020s",
        "mood_tags": ["euphoric", "uplifting"]
    }
    recommendations_1 = recommend_songs(user_prefs_1, songs, k=3)
    print_recommendations_clean("Pop & Happy Lover", user_prefs_1, songs, recommendations_1)

    # Test Profile 2: Lofi & Chill Listener
    user_prefs_2 = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "high_energy": False,
        "likes_acoustic": True,
        "preferred_decade": "2020s",
        "mood_tags": ["nostalgic", "calm", "dreamy"]
    }
    recommendations_2 = recommend_songs(user_prefs_2, songs, k=3)
    print_recommendations_clean("Lofi & Chill Listener", user_prefs_2, songs, recommendations_2)

    # Test Profile 3: Rock & Intense Energy Seeker
    user_prefs_3 = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "high_energy": True,
        "likes_acoustic": False,
        "preferred_decade": "2010s",
        "mood_tags": ["aggressive", "powerful", "driving"]
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
        "likes_acoustic": False,
        "preferred_decade": "2010s",
        "mood_tags": ["dark", "powerful"]
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
        "likes_acoustic": True,
        "preferred_decade": "2010s",
        "mood_tags": ["aggressive", "dark"]
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
        "likes_acoustic": False,
        "preferred_decade": "2000s",
        "mood_tags": ["nostalgic", "romantic"]
    }
    recommendations_adv3 = recommend_songs(adversarial_neutral, songs, k=3)
    print_recommendations_clean("Neutral Jazz Listener (Minimal Signal)", adversarial_neutral, songs, recommendations_adv3)

    # ============================================================================
    # CHALLENGE 2: MULTIPLE SCORING MODES (Strategy Pattern)
    # The same user profile is run through 3 different scoring strategies to show
    # how changing the ranking logic changes the results.
    # ============================================================================

    demo_user = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "high_energy": True,
        "likes_acoustic": False,
        "preferred_decade": "2020s",
        "mood_tags": ["euphoric", "uplifting"]
    }

    print("\n" + "=" * 90)
    print("🎛️  CHALLENGE 2: SCORING MODES COMPARISON (same user, different strategies)")
    print("=" * 90)
    print("User: Pop • Happy • Energy 0.8\n")

    for mode_name, label in [
        ("genre_first",    "MODE 1 — Genre-First    (genre weighted 3x)"),
        ("mood_first",     "MODE 2 — Mood-First     (mood weighted 3x)"),
        ("energy_focused", "MODE 3 — Energy-Focused (energy similarity weighted 4x)"),
    ]:
        print(f"--- {label} ---")
        results = recommend_songs(demo_user, songs, k=3, mode=mode_name)
        for rank, (song, score, _) in enumerate(results, 1):
            _, reasons = score_song(demo_user, song, mode=mode_name)
            print(f"  {rank}. {song['title']} by {song['artist']} — Score: {score:.2f}")
            for r in reasons:
                print(f"       • {r}")
        print()

    # ============================================================================
    # CHALLENGE 3: DIVERSITY AND FAIRNESS LOGIC
    # A Diversity Penalty deducts points from songs whose artist or genre
    # already appears in the selected list, preventing artist/genre dominance.
    # ============================================================================

    diversity_user = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "high_energy": False,
        "likes_acoustic": True,
        "preferred_decade": "2020s",
        "mood_tags": ["calm", "dreamy", "nostalgic"]
    }

    print("\n" + "=" * 90)
    print("🌈  CHALLENGE 3: DIVERSITY PENALTY COMPARISON")
    print("=" * 90)
    print("User: Lofi • Chill • Energy 0.4  |  Artist penalty: -1.0  |  Genre penalty: -0.5\n")

    print("--- WITHOUT Diversity Penalty (standard recommend_songs) ---")
    standard = recommend_songs(diversity_user, songs, k=5)
    for rank, (song, score, _) in enumerate(standard, 1):
        print(f"  {rank}. {song['title']} by {song['artist']} [{song['genre']}] — Score: {score:.2f}")

    print()
    print("--- WITH Diversity Penalty (recommend_songs_diverse) ---")
    diverse = recommend_songs_diverse(diversity_user, songs, k=5, artist_penalty=1.0, genre_penalty=0.5)
    for rank, (song, score, explanation) in enumerate(diverse, 1):
        print(f"  {rank}. {song['title']} by {song['artist']} [{song['genre']}] — Score: {score:.2f}")
        if 'Diversity penalty' in explanation:
            for part in explanation.split(' | '):
                if 'Diversity penalty' in part:
                    print(f"       ⚠ {part}")
    print()

    # ============================================================================
    # CHALLENGE 4: VISUAL SUMMARY TABLE
    # Uses tabulate to display top recommendations as a formatted grid table
    # with columns for Rank, Title, Artist, Genre, Score, and Reasons.
    # ============================================================================

    print("\n" + "=" * 90)
    print("📊  CHALLENGE 4: VISUAL SUMMARY TABLES")
    print("=" * 90)

    table_profiles = [
        ("Pop & Happy Lover",        {"genre": "pop",  "mood": "happy",   "energy": 0.8, "high_energy": True,  "likes_acoustic": False, "preferred_decade": "2020s", "mood_tags": ["euphoric", "uplifting"]}),
        ("Lofi & Chill Listener",    {"genre": "lofi", "mood": "chill",   "energy": 0.4, "high_energy": False, "likes_acoustic": True,  "preferred_decade": "2020s", "mood_tags": ["nostalgic", "calm", "dreamy"]}),
        ("Rock & Intense Seeker",    {"genre": "rock", "mood": "intense", "energy": 0.9, "high_energy": True,  "likes_acoustic": False, "preferred_decade": "2010s", "mood_tags": ["aggressive", "powerful", "driving"]}),
    ]

    for name, prefs in table_profiles:
        recs = recommend_songs(prefs, songs, k=3)
        print_recommendations_table(name, prefs, songs, recs)


if __name__ == "__main__":
    main()
