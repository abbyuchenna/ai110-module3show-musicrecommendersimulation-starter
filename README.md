# 🎵 Music Recommender Simulation

## Project Summary

This project implements a **weighted scoring music recommender system** that takes user music taste preferences (genre, mood, energy level, acousticness) and returns personalized song recommendations from a 18-song catalog. The system resembles real-world recommenders like Spotify or YouTube Music by using preference matching and feature similarity to rank songs. The recommender also explains *why* each song was selected, improving transparency and user trust.

---

## How The System Works

The recommender uses a **weighted point-scoring algorithm**:

### Song Features (9 attributes per song):
- **Categorical**: ID, Title, Artist, Genre, Mood
- **Numerical (0.0-1.0 scale)**: Energy, Valence, Danceability, Acousticness
- **Numeric**: Tempo (BPM)

### User Preferences:
- `favorite_genre` (string): e.g., "pop", "lofi", "rock"
- `favorite_mood` (string): e.g., "happy", "chill", "intense"
- `target_energy` (float): 0.0-1.0 scale (0.0 = mellow, 1.0 = intense)
- `high_energy` (bool): Bonus danceability scoring
- `likes_acoustic` (bool): Bonus for acoustic songs

### Scoring Formula:
Each song receives a total score of:
- **Genre match**: +2.0 (highest priority)
- **Mood match**: +1.0
- **Energy similarity**: 1.0 × (1 - |target_energy - song_energy|) [range: 0-1]
- **Danceability bonus**: +0.3 (if high_energy=True and danceability > 0.7)
- **Acousticness bonus**: +0.5 (if likes_acoustic=True and acousticness > 0.5)

### Selection & Explanation:
1. Score all 18 songs using the above weights
2. Sort by descending score
3. Return top K recommendations (default K=3)
4. Generate human-readable explanation for each (e.g., "matches your favorite genre and has good acousticness")

---

## Dataset

The catalog contains **18 diverse songs** across 10 genres:
- Pop, Lofi, Rock, Indie Pop, Metal, Jazz, Electronic, Acoustic, Classical, Reggae, Hip-Hop, Country

**Genre Distribution:**
- High representation: Pop (2), Lofi (3), Rock (1), Jazz (1)
- Medium representation: Electronic, Hip-Hop, Country, Indie Pop (1 each)
- Lower representation: Metal, Acoustic, Classical, Reggae (1 each)

All attributes are realistic and Spotify-like (refer to `data/songs.csv`).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

3. Run the recommender:

   ```bash
   cd src
   python3 main.py
   ```

### Running Tests

Run the test suite with:

```bash
pytest tests/
```

---

## Experiments & Results

### Test Profile 1: Pop & Happy Lover
```
Preferences: Pop genre, Happy mood, Energy 0.8, High danceability
Top Recommendation: "Sunrise City" by Neon Echo (Score: 4.28)
Reason: Matches genre + mood + close energy + very danceable
```

### Test Profile 2: Lofi & Chill Listener
```
Preferences: Lofi genre, Chill mood, Energy 0.4, Acoustic preference
Top Recommendation: "Midnight Coding" by LoRoom (Score: 4.48)
Reason: Matches genre + mood + close energy + good acousticness
```

### Test Profile 3: Rock & Intense Energy Seeker
```
Preferences: Rock genre, Intense mood, Energy 0.9, High danceability
Top Recommendation: "Storm Runner" by Voltline (Score: 3.99)
Reason: Matches genre + mood + exact energy match
```

**Key Observation:** The system effectively differentiates between opposite user types. A chill lofi listener gets very different recommendations (low energy, high acoustic) than a rock/intense listener, demonstrating that the weighting strategy creates meaningful preference separation.

---

## Limitations and Risks

1. **Small catalog (18 songs)**: Limited diversity; real systems have millions
2. **No collaborative filtering**: Doesn't learn from other users' preferences
3. **No temporal dynamics**: Ignores mood changes throughout the day/week
4. **Genre imbalance**: Some genres (Metal, Classical) are underrepresented
5. **Fixed weights**: All users get same 2.0/1.0/1.0 weights regardless of importance
6. **No lyrical analysis**: Only uses audio features, not content
7. **Cold start problem**: New users have no history to inform recommendations
8. **Popularity bias**: No mechanism to discover underrated songs

---

## Reflection

This project revealed that **even simple weighting systems can create surprisingly effective recommendations** when features are chosen carefully. The key insight is that real-world recommenders like Spotify likely use similar logic under the hood—categorical matching (genre/mood) with fine-grained similarity scoring (energy/acousticness)—but with vastly more data and ML optimization.

The main takeaway is the importance of **transparency and explainability**. By showing users *why* a song was recommended, we build trust and understanding. Real recommenders that hide their logic can feel "magical" but also mysterious or unfair. This project demonstrates that simple, transparent algorithms can be both effective and understandable.



- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

![Terminal window displaying Python test output with green checkmarks indicating all tests passed, showing test file names and execution summary in a dark command-line interface](data/image%203-21-26.jpg)

![Terminal Output](data/Image%203-21-26%20at%208.08%20PM.jpg)


