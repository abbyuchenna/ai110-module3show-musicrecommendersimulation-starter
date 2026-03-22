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

`## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

BetterthanSpotify

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

BetterthanSpotify suggests the top 3–5 songs from a small catalog based on what a user says they like — including genre, mood, energy level, acoustic preference, favorite era, and specific mood tags.

it’s mainly for classroom use to show how recommendation systems work behind the scenes. it’s not meant for real-world deployment or large-scale users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

here’s what it looks at:

genre: if the song matches the user’s favorite genre, it gets +1.0
mood: if the mood matches, +1.0
energy: the closer the song’s energy is to what the user wants, the more points it gets (up to +2.0)
danceability bonus: if the user likes high-energy music and the song is very danceable, +0.3
acousticness bonus: if the user prefers acoustic songs and the track is acoustic, +0.5
popularity bonus: songs with popularity ≥75 get +0.4
era bonus: if the song is from the user’s preferred decade, +0.5
mood tag bonus: matching detailed mood tags (like “nostalgic” or “euphoric”) can add up to +0.6

all these points get added together, and the highest-scoring songs are recommended. the system also explains why each song was picked, which makes it really transparent.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

the dataset (data/songs.csv) has 26 songs total. it started with 10 songs and was expanded by adding 16 more to make it more diverse.

each song includes 13 attributes:
id, title, artist, genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release decade, and mood tags.

genres included: pop, lofi, rock, jazz, metal, electronic, acoustic, classical, reggae, hip-hop, country, indie pop, synthwave, ambient

moods included: happy, chill, intense, relaxed, focused, moody, energetic, aggressive

overall, the dataset leans toward mainstream western music. pop, lofi, and rock are the most represented, while genres like classical, reggae, and country only have one song each. also, there are no “sad” songs, which is a noticeable gap.

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

this recommender works best when the user has clear preferences.

for example, a lofi + chill user consistently gets really accurate results — everything lines up across genre, mood, and energy
a rock + intense energy user gets strong matches like “storm runner,” which fits almost perfectly
the system is very transparent — it shows exactly how each score was built, so nothing feels random
energy matching works really well as a tiebreaker when songs are otherwise similar

overall, it’s simple but predictable, which actually makes it feel reliable in the right situations.
---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

there are definitely some weaknesses:

small catalog: with only 26 songs, some genres barely have representation, so those users get weaker recommendations
missing moods: there are no “sad” songs, so those users basically can’t be served properly
same weights for everyone: the model treats all users the same, even though people value things like mood or genre differently
artist repetition: the same artist can show up multiple times in top results, which limits variety
strict genre matching: “pop” and “indie pop” are treated as completely different, which feels unrealistic
bias in practice: if this were a real product, fans of popular genres (like pop or lofi) would consistently get better recommendations than others

so while it works, it’s not equally fair across all user types.

i tested the system in a few different ways:

user profiles:
i ran six profiles — three normal (pop/happy, lofi/chill, rock/intense) and three edge cases (like high-energy sad). the normal ones worked really well, but the edge cases exposed gaps, especially with missing moods.
automated tests:
there are 17 pytest cases, all passing. they check scoring, ranking, edge cases, and overall functionality.
sensitivity testing:
i adjusted the weights (like lowering genre importance and increasing energy). this showed that small changes in weights can completely shift what gets recommended, which highlights how subjective these systems really are.
---
##8. future work

if i had more time, i’d improve it by:

expanding the dataset to 100+ songs with better balance across genres and moods
adding genre similarity (so related genres get partial credit)
letting users customize weights based on what they care about most
incorporating collaborative filtering (using patterns from multiple users)
actually using the valence score to better capture emotional tone

these changes would make it feel a lot more realistic and personalized.

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

this project made me realize how far a simple scoring system can go — but also how limited it is without the right data.

what surprised me most was how often certain songs (like “gym hero”) showed up across completely different users. it made me realize that in a small dataset, a few “well-rounded” songs can dominate everything, even if they’re not the best fit.

it also changed how i think about platforms like spotify. they’re probably doing something similar at a basic level, just with way more data and smarter weighting. scale is really what makes their recommendations feel personal.

at the end of the day, human judgment still matters a lot. the algorithm only reflects what you choose to include — if you leave out something like “sad” music, the system literally can’t fix that on its own. someone has to recognize those gaps and design around them.


`
![Terminal window displaying Python test output with green checkmarks indicating all tests passed, showing test file names and execution summary in a dark command-line interface](data/image%203-21-26.jpg)

![Terminal Output](data/Image%203-21-26%20at%208.08%20PM.jpg)

![Terminal Output](data/Image%203-21-26%20at%208.58%20PM.jpg)

![Terminal Output](data/Image%203-21-26%20at%208.59%20PM.jpg)


