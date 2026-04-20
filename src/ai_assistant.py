"""
AI-powered layer for the Music Recommender System.
Uses Google's Gemma 3 1B (gemma-3-1b-it) via the google-generativeai SDK.

4-step agentic pipeline:
  Step 1 — Parse:     Gemma converts natural language → structured preferences JSON
  Step 2 — Recommend: existing scoring engine runs
  Step 3 — Critique:  Gemma self-evaluates whether results match the request
  Step 3b — Refine:   if critique flags issues, preferences are adjusted and retried
  Step 4 — Explain:   Gemma writes a friendly natural language summary
"""

import json
import re
import google.generativeai as genai
from rag import get_context

genai.configure(api_key="AIzaSyBzVJ1MS0MzPqGizjUKcBZrOpE-CoUIYeM")
_model = genai.GenerativeModel("gemma-3-1b-it")

VALID_GENRES = {
    "pop", "lofi", "jazz", "rock", "electronic", "indie",
    "synthwave", "acoustic", "metal", "classical", "reggae",
    "hip-hop", "country", "ambient",
}
VALID_MOODS = {
    "happy", "chill", "intense", "relaxed", "focused",
    "moody", "energetic", "aggressive",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a string (handles extra prose from the model)."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model response:\n{text}")
    return json.loads(match.group())


def _validate_and_fix(prefs: dict) -> dict:
    """Guardrail: clamp and correct all preference fields after parsing."""
    if prefs.get("genre") not in VALID_GENRES:
        print(f"  [Guardrail] Unknown genre '{prefs.get('genre')}' → defaulting to 'pop'")
        prefs["genre"] = "pop"

    if prefs.get("mood") not in VALID_MOODS:
        print(f"  [Guardrail] Unknown mood '{prefs.get('mood')}' → defaulting to 'chill'")
        prefs["mood"] = "chill"

    energy = float(prefs.get("energy", 0.5))
    prefs["energy"] = round(max(0.0, min(1.0, energy)), 2)

    if not isinstance(prefs.get("likes_acoustic"), bool):
        prefs["likes_acoustic"] = False

    if not isinstance(prefs.get("mood_tags"), list):
        prefs["mood_tags"] = []

    prefs.setdefault("preferred_decade", None)
    prefs["high_energy"] = prefs["energy"] > 0.7

    return prefs


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def parse_user_input(user_text: str) -> dict:
    """Step 1 — Gemma converts natural language to structured preferences, with RAG context."""
    print(f"\n  [Step 1: Parse] Input: '{user_text}'")

    # RAG: retrieve relevant knowledge chunks for this query
    context = get_context(user_text, top_k=3)
    context_section = f"\nrelevant music knowledge:\n{context}\n" if context else ""
    print(f"  [RAG] Retrieved {len(context.splitlines()) if context else 0} lines of context")

    prompt = f"""You are a music preference parser. Convert the request below into JSON.
{context_section}
Return ONLY a JSON object with these exact fields:
{{
  "genre": <one of: pop, lofi, jazz, rock, electronic, indie, synthwave, acoustic, metal, classical, reggae, hip-hop, country, ambient>,
  "mood": <one of: happy, chill, intense, relaxed, focused, moody, energetic, aggressive>,
  "energy": <float 0.0 to 1.0>,
  "likes_acoustic": <true or false>,
  "preferred_decade": <"1990s", "2000s", "2010s", "2020s", or null>,
  "mood_tags": <list of mood strings from the valid moods above>
}}

User request: "{user_text}"

JSON:"""

    response = _model.generate_content(prompt)
    prefs = _extract_json(response.text)
    prefs = _validate_and_fix(prefs)

    print(f"  [Step 1: Parse] → genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']}, acoustic={prefs['likes_acoustic']}")
    return prefs


def parse_user_input_few_shot(user_text: str) -> dict:
    """
    Step 1 variant — uses few-shot examples + RAG for specialized parsing.
    compare against parse_user_input() to see measurable output differences.
    """
    from few_shot import build_few_shot_block

    context = get_context(user_text, top_k=2)
    context_section = f"\nrelevant music knowledge:\n{context}\n" if context else ""
    few_shot_block = build_few_shot_block()

    prompt = f"""You are a music preference parser.

{few_shot_block}
{context_section}
now parse this new request using the exact same format. return ONLY a JSON object:
{{
  "genre": <one of: pop, lofi, jazz, rock, electronic, indie, synthwave, acoustic, metal, classical, reggae, hip-hop, country, ambient>,
  "mood": <one of: happy, chill, intense, relaxed, focused, moody, energetic, aggressive>,
  "energy": <float 0.0 to 1.0>,
  "likes_acoustic": <true or false>,
  "preferred_decade": <"1990s", "2000s", "2010s", "2020s", or null>,
  "mood_tags": <list of mood strings>
}}

User request: "{user_text}"

JSON:"""

    response = _model.generate_content(prompt)
    prefs = _extract_json(response.text)
    prefs = _validate_and_fix(prefs)
    return prefs


def critique_recommendations(recs: list, user_text: str) -> tuple:
    """Step 3 — Gemma reviews whether results match what the user asked for."""
    print(f"\n  [Step 3: Critique] Evaluating {len(recs)} recommendations...")

    songs_text = "\n".join(
        f"- {s['title']} by {s['artist']} (genre={s['genre']}, mood={s['mood']}, energy={s['energy']})"
        for s, _, _ in recs
    )

    prompt = f"""A user asked for: "{user_text}"

The music recommender returned these songs:
{songs_text}

Do these recommendations match what the user asked for?
Reply with exactly:
VERDICT: GOOD or POOR
REASON: one sentence explaining why"""

    response = _model.generate_content(prompt)
    reply = response.text.strip()
    is_good = "GOOD" in reply.upper()
    print(f"  [Step 3: Critique] {reply}")
    return is_good, reply


def explain_recommendations(recs: list, user_text: str) -> str:
    """Step 4 — Gemma writes a friendly 2-3 sentence explanation of the results."""
    print(f"\n  [Step 4: Explain] Generating summary...")

    songs_text = "\n".join(
        f"- {s['title']} by {s['artist']} ({s['genre']}, {s['mood']})"
        for s, _, _ in recs
    )

    prompt = f"""A user asked for: "{user_text}"

The music recommender suggested:
{songs_text}

Write 2-3 friendly sentences explaining why these songs are a good match for what the user wanted."""

    response = _model.generate_content(prompt)
    return response.text.strip()


# ---------------------------------------------------------------------------
# Full agentic pipeline
# ---------------------------------------------------------------------------

def run_ai_pipeline(user_text: str, songs: list) -> list:
    """
    Full 4-step agentic pipeline.
    Returns the final list of (song, score, explanation) tuples.
    All intermediate steps are printed so they are observable.
    """
    from recommender import recommend_songs

    print("\n" + "=" * 70)
    print("AI-POWERED RECOMMENDATION PIPELINE  (Gemma 3 1B)")
    print("=" * 70)

    # Step 1: Parse natural language → structured preferences
    prefs = parse_user_input(user_text)

    # Step 2: Run the existing scoring engine
    print(f"\n  [Step 2: Recommend] Running scoring engine...")
    recs = recommend_songs(prefs, songs, k=5)
    print(f"  [Step 2: Recommend] Returned {len(recs)} results")

    # Step 3: Self-critique
    is_good, _ = critique_recommendations(recs, user_text)

    # Step 3b: Refine if critique flagged poor results
    if not is_good:
        print(f"\n  [Step 3b: Refine] Adjusting energy and retrying...")
        prefs["energy"] = round(1.0 - prefs["energy"], 2)
        prefs["high_energy"] = prefs["energy"] > 0.7
        recs = recommend_songs(prefs, songs, k=5)
        print(f"  [Step 3b: Refine] Retried with adjusted energy={prefs['energy']}")

    # Step 4: Natural language explanation
    explanation = explain_recommendations(recs, user_text)
    print(f"\n  [Step 4: Explain]\n  {explanation}")
    print("=" * 70)

    return recs
