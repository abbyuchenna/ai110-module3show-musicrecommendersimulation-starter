# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Primary Name: VibeFinder 1.0**

**Alternative Names** (choose one):
- **MoodMatcher**: Emphasizes mood + energy matching capabilities
- **GenreGenius**: Highlights strong genre-matching algorithm
- **FeelGood Music Suggester**: Fun, accessible name for casual users

**Description**: VibeFinder 1.0 is a weighted-scoring music recommender system designed to demonstrate how playlist algorithms work in classroom or hobby applications.

---

## 2. Goal / Task

**What This Recommender Tries to Do:**

VibeFinder takes a user's music preferences (favorite genre, favorite mood, desired energy level, and acoustic preference) and returns the top 3-5 songs from a catalog that *best match* those preferences. 

**In one sentence**: "Given what you like, find the songs that make you the happiest."

**What It Does:**
- Reads user preferences (e.g., "I like pop music, I'm happy, and I want high energy")
- Scores every song in the dataset based on how well it matches
- Ranks songs from best to worst match
- Shows the user top recommendations with explanations

**What It Does NOT Do:**
- It doesn't learn from your behavior (no "machine learning" in the AI sense)
- It doesn't know what went viral or what's trendy
- It doesn't understand lyrics or artist collaborations
- It doesn't predict what you'll like based on what others liked

---

## 3. Data Used

**Dataset Size**: 18 songs (perfect for learning; tiny for real use)

**Song Features**:
- **ID & Metadata**: Song title, artist name, genre, mood
- **Audio Features**:
  - **Genre**: Pop, Lofi, Rock, Jazz, Metal, Electronic, Acoustic, Classical, Reggae, Hip-Hop, Country, Indie Pop, Synthwave, Ambient
  - **Mood**: Happy, Chill, Intense, Relaxed, Focused, Moody, Energetic
  - **Energy** (0.0-1.0): How intense/active the song is (0.0 = silence, 1.0 = max intensity)
  - **Tempo (BPM)**: Beats per minute (60-170)
  - **Valence** (0.0-1.0): Musical happiness/brightness (0.0 = sad, 1.0 = happy)
  - **Danceability** (0.0-1.0): How dance-able the song is
  - **Acousticness** (0.0-1.0): How acoustic vs. electric (0.0 = fully electric, 1.0 = fully acoustic)

**Dataset Balance**:
- ✅ Good variety of genres and moods
- ⚠️ Lofi songs over-represented (3/18) vs. Metal (1/18)
- ⚠️ No "sad" songs (all sad moods missing)
- ✅ Energy ranges from 0.28 to 0.96 (fairly complete spectrum)

---

## 4. Algorithm Summary (In Plain English)

**How the Scoring Works** (what happens behind the scenes):

When you tell VibeFinder your preferences, it grades every song like a teacher grading a test:

**Category 1: Exact Match (Genre)**
- Does the song match your favorite genre? YES = +1.0 point, NO = 0 points
- Example: You like Pop music → Pop songs get +1.0, Rock songs get 0

**Category 2: Mood Match**
- Does the song fit your mood? YES = +1.0 point, NO = 0 points
- Example: You want "happy" music → Happy songs get +1.0, Intense songs get 0

**Category 3: Energy Match (The Smart Part)**
- How close is the song's energy to what you want?
- If you want energy 0.5 (medium) and the song is 0.5 → Perfect! Get 2.0 points (maximum)
- If you want energy 0.5 and the song is 0.7 (too energetic) → Lose 0.4 points (get 1.6)
- If you want energy 0.5 and the song is 0.1 (too quiet) → Lose 0.8 points (get 1.2)
- Simple rule: **The closer the energy, the more points you get** (0.0 to 2.0 points max)

**Bonus Categories** (the extras):
- If you love danceability AND the song is very danceable (>0.7): +0.3 bonus points
- If you love acoustic music AND the song is acoustic (>0.5): +0.5 bonus points

**Final Score = Genre + Mood + Energy + Bonuses**

**Example**: You want Pop + Happy + Energy 0.8
- Pop song with Happy mood and Energy 0.82:
  - Genre match: +1.0
  - Mood match: +1.0
  - Energy match: 1.96 (very close!)
  - Danceability bonus: +0.3
  - **TOTAL: 4.26 / 5.3 possible** → This gets recommended!

---

## 5. Intended Use Cases ✅

**This recommender is GOOD for:**

1. **Educational Projects** (like this one): Learning how recommendation algorithms work without complex math
2. **Hobby Apps**: Small personal music playlists, friend group recommendations, themed playlists
3. **Demonstrating Concepts**: Teaching students about weighting, scoring, and ranking algorithms
4. **Prototyping**: Testing ideas before building a real system
5. **Music Café / Small Venue**: A tiny coffee shop with 20 curated songs that needs a simple "what should we play?" system

---

## 6. Non-Intended Use Cases ❌

**This recommender is BAD for (do NOT use for):**

1. **Production Music Streaming** (Don't use for Spotify, Apple Music, YouTube Music):
   - Only has 18 songs (needs millions)
   - No collaborative filtering (can't learn from user behavior)
   - No machine learning (too simplistic for real users)

2. **High-Stakes Commercial Apps**:
   - Artist/label royalty distributions depend on recommendations
   - Users expect personalized, smart suggestions
   - Bias toward low-acoustic genres would create fairness issues

3. **Medical/Therapeutic Music Selection**:
   - Mood-matching is too simplistic for mental health
   - Missing important features like "healing" or "therapeutic"
   - Could recommend wrong songs to vulnerable users

4. **Real-Time DJ Systems**:
   - No consideration of what played last (doesn't prevent repetition)
   - No transition logic (loud song → quiet song can be jarring)
   - No audience feedback

5. **Multi-User Household Systems**:
   - No way to identify different users
   - Can't learn family preferences
   - Can't handle conflicting taste profiles

---

## 7. How the Model Works  

**In Plain Language:**

Imagine you tell a friend: *"I love pop music, I'm in a happy mood, and I want something energetic."*

VibeFinder does exactly this:
1. It reads the user's preferences (pop genre, happy mood, energy 0.8, likes danceability)
2. It looks at each song in the catalog and asks: "How well does this match their taste?"
3. It gives each song a score using the system described above
4. It ranks all songs by score (highest first)
5. It returns the top 3-5 recommendations
6. It explains why each song was picked

**Why This Works for Learning:**
- Simple enough to understand the logic
- Complex enough to see real weighting trade-offs
- Shows how bias enters even "fair" algorithms



## 4. Data  

**Dataset Size**: 18 songs (expanded from starter 10)

**Genres Represented**:
- Pop (2 songs): Sunrise City, Gym Hero
- Lofi (3 songs): Midnight Coding, Library Rain, Focus Flow
- Rock (1 song): Storm Runner
- Ambient (1 song): Spacewalk Thoughts
- Jazz (2 songs): Coffee Shop Stories, Jazz Nights
- Synthwave (1 song): Night Drive Loop
- Indie Pop (1 song): Rooftop Lights
- Metal (1 song): Metal Rage
- Electronic (1 song): Electric Dreams
- Acoustic (1 song): Acoustic Soul
- Classical (1 song): Classical Peace
- Reggae (1 song): Reggae Vibes
- Hip-Hop (1 song): Urban Hustle
- Country (1 song): Country Roads

**Moods Represented**: happy, chill, intense, moody, relaxed, focused, energetic

**Attributes (Per Song)**:
- ID, Title, Artist, Genre, Mood (categorical)
- Energy, Tempo, Valence, Danceability, Acousticness (0.0-1.0 scale)

**Changes Made**: Expanded original 10 songs to 18 by adding 8 diverse songs (Metal, Jazz, Electronic, Acoustic, Classical, Reggae, Hip-Hop, Country) to increase genre coverage.

**What's Missing**:
- Language/lyrical content
- Artist popularity or collaborations
- Song explicit content flags
- Recency (all songs treated equally, no "new" or "old" bias)
- User demographics (age, location, language)

---

## 5. Strengths  

The system **works well for**:

1. **Clear genre/mood matching**: When a user strongly prefers a specific genre (e.g., "lofi + chill"), the system consistently recommends songs of that type. Users get exactly what they ask for.

2. **Energy preference separation**: The system effectively differentiates between high-energy (pop fans: energy 0.8) and low-energy (lofi fans: energy 0.4) users. A rock fan won't get lofi recommendations and vice versa.

3. **Transparency**: The explanations clearly show *why* a recommendation was made, making the algorithm feel fair and understandable rather than a "black box."

4. **Reasonable top-3 selections**: For all three test profiles (Pop & Happy, Lofi & Chill, Rock & Intense), the #1 recommendation was intuitively correct.

5. **Balanced weighting**: Genre (+2) > Mood (+1) > Energy (+1) reflects real music preference hierarchy (people usually care most about genre).

---

## 6. Limitations and Biases 

**The "Small Playlist" Problem:**
This system has only 18 songs to work with—like a jukebox with 18 songs instead of a music streaming service with millions. Because the catalog is so small, the same few songs (like "Gym Hero" and "Midnight Coding") will show up in recommendations for many different user types. This makes the system feel repetitive. A user testing it might think "Why do I keep seeing the same 4 songs?" The honest answer: because there are only 18 to choose from. Real music apps (Spotify, Apple Music) solve this by having millions of songs, so everyone gets unique recommendations.

**Genre Imbalance—Some Music Styles Get Shortchanged:**
The song collection has 3 Lofi songs, 2 Pop songs, and 2 Jazz songs. But it has only 1 Metal song, 1 Classical song, and 1 Reggae song. This creates an uneven playing field:
- A Lofi fan says "I love Lofi music" and gets 3 great genre-matched options
- A Classical fan says "I love Classical music" and gets... 1 song

This means Classical fans are more likely to be recommended non-Classical songs, just to fill up a top-5 list. They might think the system "doesn't understand" classical music, when really it's just that the dataset is imbalanced. In the real world, if Spotify had only 1 classical song, they'd have the same problem.

**The Acoustic Music "Silent Trap":**
The system has a hidden rule: if a user says they like acoustic music, the algorithm gives a +0.5 point bonus to highly acoustic songs (and nothing to electric songs). This sounds helpful, but it's actually a filter bubble. Imagine a user says "I like acoustic music" and then the system acts like ONLY acoustic songs can match them well. An electric song that's perfect in every other way (right genre, mood, energy) will lose by 0.5 points just because it's not acoustic. The user never sees this penalty explained; it just happens silently in the scoring. This is a subtle but real form of bias.

**Extreme Music Preferences Get Penalized:**
The algorithm assumes most people want music with "medium" energy. Someone who wants very, very quiet music (energy = 0.05, almost silent like ambient sounds) will be frustrated because:
- The quietest song in our collection is 0.28 energy (still fairly active)
- This mismatch costs them 0.46 points in scoring—equivalent to losing BOTH a genre match AND a mood match combined
The system mathematically disadvantages people with extreme tastes because the dataset doesn't support those extremes. This is a dataset problem, not an algorithm problem, but it's a real limitation.

**Missing Moods Create Forced Redirects:**
The system has no "sad" songs. Zero. So if a user says "I want sad music," the system can't deliver—it redirects them to "intense" (the closest available mood) and hopes they're satisfied. Similarly, the dataset is missing moods like "romantic," "angry," "dreamy," or "peaceful." This means the system will never truly understand users wanting these moods.

---

## 7. Evaluation  

**How We Tested It:**

We ran the system through three realistic user profiles to check if recommendations made sense:

1. **Pop & Happy Lover** (wants upbeat pop music): Got "Sunrise City" as #1. Correct! ✅
2. **Lofi & Chill Listener** (wants relaxing, acoustic music): Got "Midnight Coding" as #1. Correct! ✅
3. **Rock & Intense Energy Seeker** (wants loud, energetic rock): Got "Storm Runner" as #1. Correct! ✅

**The "Gym Hero" Problem—Why One Song Keeps Winning:**

One interesting thing happened during testing: a song called "Gym Hero" by Max Pulse kept appearing in top recommendations for very different user types:
- Pop fans got it (because it's labeled "pop")
- Intense mood fans got it (because it's labeled "intense")
- High-energy fans got it (because energy = 0.93)

Why does it keep showing up? Because with only 18 songs, this song hits multiple bullseyes. It's like having a restaurant with 20 menu items—the "crowd-pleaser" dish shows up on most people's recommendation lists. In Spotify (200 million songs), "Gym Hero" would be 1 among thousands of equally good options.

**Stress Tests: What Happens When Users Want Impossible Things?**

We tested three "adversarial" scenarios to break the system:

1. **High-Energy Sad Indie Fan**: Wants very energetic (0.95) + sad mood. Result: Very weak recommendations (scores around 1.2). Why? There are NO sad songs in the dataset, and sad songs tend to be low-energy anyway. The system can't satisfy both. **Learning:** When user preferences conflict with what's in the dataset, the algorithm suffers.

2. **Acoustic Metal Fan**: Wants metal genre + acoustic preference. Result: Metal Rage won (genre match!), but never got the acoustic bonus because metal songs are 92% electric. **Learning:** Some preference combinations are mathematically impossible to satisfy together.

3. **Neutral Jazz Listener** (energy = 0.5, right in the middle): Got correct jazz recommendations. **Learning:** When users are vague/neutral, the algorithm relies 100% on genre/mood. Energy similarity becomes less useful.

**What Surprised Us:**

- The energy matching worked better than expected as a "tiebreaker." When two songs have identical genre and mood, the one with closer energy wins by tiny margins (0.03 points). This is good because it's predictable—users can understand why Midnight Coding beat Library Rain.
- Artist repetition is a real issue: Lofi fans got songs by LoRoom in positions #1 AND #3. With 18 songs, artist diversity is nearly impossible.
- The system is 100% deterministic (always gives the same answer for the same input). Real systems add randomness so users don't get bored.



---

## 8. Future Work & Improvements  

**High Priority**:

1. **Diversity Bonus**: Penalize recommending same artist twice in top-K. Implement: if song.artist appeared in previous recommendation, subtract 0.5 points.

2. **Collaborative Filtering**: Track which songs multiple users click/like, then recommend based on "people who liked X also liked Y."

3. **Dynamic Weighting**: Let users adjust genre/mood/energy weights. Some users care 90% about mood, others 90% about energy.

4. **Subgenre Support**: Instead of just "pop," support "indie pop" and "synthwave pop" and implement similarity between related subgenres.

5. **Expanded Dataset**: Add 100+ real songs across all genres for better coverage and reduced bias.

**Medium Priority**:

6. **Novelty/Recency**: Track which songs were recently recommended and deprioritize them. Add "freshness" bonus to unrecommended songs.

7. **Mood/Time-of-Day**: Return different recommendations depending on time of day (morning = energetic, evening = chill).

8. **Explanation Ranking**: Some reasons are stronger than others. Genre match is most important; prioritize that in the explanation.

9. **Adversarial Testing**: Test edge cases:
   - What if user inputs conflicting preferences? (happy + intense)
   - What if no songs match any preference?
   - What if K > catalog size?

**Nice-to-Have**:

10. **Visual Dashboard**: Display recommendations in a web UI with scatter plots (energy vs. danceability) showing recommended vs. all songs.

11. **A/B Testing**: Compare weighted scoring vs. random recommendations vs. simple genre matching on user satisfaction.

12. **Playlist Diversity**: Generate entire setlist recommendations, not just individual songs, optimizing for variety and transition.

---

## 9. AI Model / Prompt Comparison

**Prompts Used in Development**:

1. **"Design a weighting strategy for musical attributes"** → Suggested linear decay for continuous features; exponential would be too harsh.
   - Feedback: Linear worked better than expected for energy; exponential Gaussian was overkill.

2. **"Generate a Mermaid flowchart for the data pipeline"** → Provided clear visualization of scoring → ranking → output flow.
   - Impact: Helped validate system architecture before coding.

3. **"Create 8 new diverse songs for the dataset"** → Introduced Metal, Jazz, Electronic, Classical, Reggae, Hip-Hop, Country genres.
   - Impact: Expanded genre coverage and enabled testing for different user profiles.

**Decision Rationale**:
- Chose linear over exponential: Simpler, more interpretable, fewer hyperparameters
- Chose point-weighting over distance metrics (L2 norm): Easy to explain to non-technical stakeholders
- Chose functional + OOP hybrid: main.py uses functions (simple), tests use classes (structured)

---

**End of Model Card**---

## 9. Personal Reflection  

Building this project taught me that recommender systems are essentially scoring engines — they don't "understand" music, they just match numbers against user preferences. The most unexpected discovery was the critique → refine loop: when Gemma flags results as a poor match, the system flips the energy value and reruns the recommender, and that simple fix actually works because most mismatches come down to energy being off. This changed the way I think about apps like Spotify — what feels like personalization is really pattern matching at scale, and the catalog and data matter more than the algorithm. A perfect scoring formula still fails if the data is thin or unbalanced, which reinforces the importance of diverse, well-represented data in any recommendation system.


