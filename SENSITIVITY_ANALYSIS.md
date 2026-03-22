# Sensitivity Analysis: Weight Modification Experiment

## Changes Applied
- **Genre match**: Halved from +2.0 → +1.0
- **Energy similarity**: Doubled from 1.0× → 2.0×

---

## Impact on Algorithm Priorities

### BEFORE (Original Weights)
```
Priority Hierarchy:
1. Genre match (+2.0) ← HIGHEST
2. Mood match (+1.0)
3. Energy similarity (0-1.0, max +1.0)
4. Danceability/Acousticness bonuses (+0.3/+0.5)

Max possible score: 2.0 + 1.0 + 1.0 + 0.3 + 0.5 = 5.3
```

### AFTER (Modified Weights)
```
Priority Hierarchy:
1. Energy similarity (0-2.0, max +2.0) ← NOW HIGHEST!
2. Genre match (+1.0) ← DEMOTED
2. Mood match (+1.0) ← TIE
4. Danceability/Acousticness bonuses (+0.3/+0.5)

Max possible score: 1.0 + 1.0 + 2.0 + 0.3 + 0.5 = 5.3 (same max)
```

---

## Key Behavioral Changes

### 1. **Genre Barrier Weakened**
**BEFORE:** Genre match was worth +2.0 (40% of typical score)
**AFTER:** Genre match worth only +1.0 (17% of typical score)

**Effect:** Songs from wrong genres now rank higher if they match energy perfectly
- Pop fan gets rock recommendations if rock matches their energy
- Less strict genre lockdown

---

### 2. **Energy Becomes the Dominant Factor**
**BEFORE:** Energy similarity max +1.0 (20% of score)
**AFTER:** Energy similarity max +2.0 (38% of score)

**Effect:** Energy matching can now override genre/mood preferences
- A song with perfect energy (2.0) beats a perfect genre match (1.0)
- System values "feels right" over "expected category"

---

## Concrete Example: Pop & Happy Lover

### BEFORE (Original)
```
Profile: genre=pop, mood=happy, energy=0.8

Ranking #1: Sunrise City (Pop • Happy • 0.82 energy)
Score: 2.0 + 1.0 + 0.98 + 0.3 = 4.28
Reason: Perfect genre + mood + close energy

Ranking #2: Rooftop Lights (Indie Pop • Happy • 0.76 energy)  
Score: 0.0 + 1.0 + 0.96 + 0.3 = 2.26
Reason: Wrong genre, but mood matches → 2.26
```

### AFTER (Modified)
```
Profile: genre=pop, mood=happy, energy=0.8

Ranking #1: Sunrise City (Pop • Happy • 0.82 energy)
Score: 1.0 + 1.0 + 1.96 + 0.3 = 4.26
Reason: Genre + mood + close energy (still #1)

Ranking #2: Rooftop Lights (Indie Pop • Happy • 0.76 energy)
Score: 0.0 + 1.0 + 1.92 + 0.3 = 3.22
Reason: Wrong genre BUT closer energy → 3.22 (ranks higher!)
```

**Result:** Rooftop Lights jumped from 3rd place to 2nd place (+0.96 points from energy doubling)

---

## Profile-by-Profile Impact Analysis

### Rock & Intense Energy Seeker

| Song | Before | After | Change | Reason |
|------|--------|-------|--------|--------|
| Storm Runner (Rock, Intense, 0.91 E) | 3.99 | 3.98 | -0.01 | Genre now worth 1.0 instead of 2.0 |
| Gym Hero (Pop, Intense, 0.93 E) | 2.27 | 3.24 | +0.97 | Energy doubled; now beats weak genre match |
| Urban Hustle (Hip-Hop, Intense, 0.87 E) | 2.27 | 3.24 | +0.97 | Same boost as Gym Hero |

**KEY INSIGHT:** The gap between "correct genre" and "wrong genre" narrowed from 1.72 points to 0.74 points. **Genre is no longer a hard barrier.**

---

## Adversarial Edge Case: High-Energy Sad Indie Fan

### BEFORE
```
Best match: Metal Rage (Energy 0.96)
Score: 0 + 0 + 0.99 + 0.3 = 1.29
Problem: No genre/mood matches → very weak score
```

### AFTER
```
Best match: Metal Rage (Energy 0.96)
Score: 0 + 0 + 1.98 + 0.3 = 2.28
Benefit: Energy doubling lifted floor score from 1.29 to 2.28 (+0.99)
```

**Effect on edge cases:** Conflicting preferences are LESS punishing because energy can compensate.

---

## Mathematical Validation: Negative Score Check

**Can scores go negative? NO.**

Minimum components:
- Genre match: 0.0 (only triggers on match)
- Mood match: 0.0 (only triggers on match)
- Energy similarity: 0.0 (minimum when distance = 1.0: 2.0 × (1 - 1.0) = 0.0)
- Bonuses: 0.0 (only trigger on conditions)

**Minimum possible score: 0.0 ✓**
**Maximum possible score: 1.0 + 1.0 + 2.0 + 0.3 + 0.5 = 5.3 ✓**

---

## Recommendations for Production Use

### Original Weights (Genre-First) Best For:
- Strict categorization (strict jazz purist, not interested in adjacent genres)
- Discovery within user's preferred genre
- Strong preference signals

### Modified Weights (Energy-First) Best For:
- Vibe-based recommendations (user cares MORE about the *feeling* than the label)
- Cross-genre discovery (willing to try rock if energy matches their chill preference)
- Mood-adaptive playlists (time of day matters more than genre)

---

## Conclusion

The sensitivity test reveals that **weighting is fundamentally about priority trade-offs**:

| Dimension | Impact |
|-----------|--------|
| **Categorical matching (genre/mood)** | Ensures recommendations feel "on brand" |
| **Continuous similarity (energy)** | Ensures recommendations feel "right now" |

**Original (2.0 genre):** Trusts user's stated genre preference absolutely.  
**Modified (2.0 energy):** Trusts user's stated energy/vibe more than their genre claim.

Real recommenders often use **personalization** to adjust these weights per user type, which is an important future improvement!
