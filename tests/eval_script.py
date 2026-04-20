"""
Evaluation harness for the Music Recommender System.
Runs predefined test cases and prints a pass/fail summary.

Usage (from project root):
    python tests/eval_script.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from recommender import load_songs, recommend_songs
from guardrails import validate_preferences, validate_output

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

TEST_CASES = [
    {
        "name": "Pop/Happy user gets at least one pop song",
        "prefs": {
            "genre": "pop", "mood": "happy", "energy": 0.8, "high_energy": True,
            "likes_acoustic": False, "preferred_decade": "2020s", "mood_tags": ["happy"],
        },
        "check": lambda recs: any(s["genre"] == "pop" for s, _, _ in recs),
        "desc": "Top 5 includes at least one pop song",
    },
    {
        "name": "Lofi/Chill user gets low-energy top result",
        "prefs": {
            "genre": "lofi", "mood": "chill", "energy": 0.3, "high_energy": False,
            "likes_acoustic": True, "preferred_decade": None, "mood_tags": ["chill"],
        },
        "check": lambda recs: recs[0][0]["energy"] < 0.6,
        "desc": "Top result has energy below 0.6",
    },
    {
        "name": "High-energy user gets high-energy top result",
        "prefs": {
            "genre": "rock", "mood": "intense", "energy": 0.9, "high_energy": True,
            "likes_acoustic": False, "preferred_decade": None, "mood_tags": ["intense"],
        },
        "check": lambda recs: recs[0][0]["energy"] > 0.7,
        "desc": "Top result has energy above 0.7",
    },
    {
        "name": "Returns exactly K results",
        "prefs": {
            "genre": "jazz", "mood": "relaxed", "energy": 0.4, "high_energy": False,
            "likes_acoustic": True, "preferred_decade": None, "mood_tags": [],
        },
        "check": lambda recs: len(recs) == 3,
        "desc": "Returns exactly 3 results when k=3",
        "k": 3,
    },
    {
        "name": "Scores in descending order",
        "prefs": {
            "genre": "electronic", "mood": "energetic", "energy": 0.8, "high_energy": True,
            "likes_acoustic": False, "preferred_decade": None, "mood_tags": [],
        },
        "check": lambda recs: all(recs[i][1] >= recs[i + 1][1] for i in range(len(recs) - 1)),
        "desc": "All scores sorted highest to lowest",
    },
    {
        "name": "Valid preferences pass guardrail",
        "prefs": {
            "genre": "pop", "mood": "happy", "energy": 0.7, "high_energy": True,
            "likes_acoustic": False, "preferred_decade": "2020s", "mood_tags": [],
        },
        "check": lambda _: validate_preferences({
            "genre": "pop", "mood": "happy", "energy": 0.7,
            "likes_acoustic": False, "preferred_decade": "2020s",
        })[0],
        "desc": "Valid preference dict returns is_valid=True from guardrail",
    },
    {
        "name": "Invalid genre caught by guardrail",
        "prefs": None,
        "skip_recommend": True,
        "check": lambda _: not validate_preferences({
            "genre": "dubstep", "mood": "happy", "energy": 0.7,
            "likes_acoustic": False, "preferred_decade": None,
        })[0],
        "desc": "Invalid genre 'dubstep' is flagged as invalid by guardrail",
    },
    {
        "name": "Invalid energy range caught by guardrail",
        "prefs": None,
        "skip_recommend": True,
        "check": lambda _: not validate_preferences({
            "genre": "pop", "mood": "happy", "energy": 1.5,
            "likes_acoustic": False, "preferred_decade": None,
        })[0],
        "desc": "Energy value 1.5 (out of range) is flagged by guardrail",
    },
    {
        "name": "Output guardrail validates sorted results",
        "prefs": {
            "genre": "pop", "mood": "happy", "energy": 0.8, "high_energy": True,
            "likes_acoustic": False, "preferred_decade": None, "mood_tags": [],
        },
        "check": lambda recs: validate_output(recs, 5)[0],
        "desc": "Output passes guardrail: sorted, correct types, at most k results",
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_eval() -> bool:
    passed = 0
    failed = 0

    print("=" * 60)
    print("EVALUATION HARNESS — Music Recommender System")
    print("=" * 60)

    for test in TEST_CASES:
        try:
            recs = []
            if not test.get("skip_recommend"):
                k = test.get("k", 5)
                recs = recommend_songs(test["prefs"], SONGS, k=k)
            result = test["check"](recs)
        except Exception as e:
            result = False
            print(f"\n[ERROR] {test['name']}: {e}")

        status = "PASS ✓" if result else "FAIL ✗"
        if result:
            passed += 1
        else:
            failed += 1

        print(f"\n[{status}] {test['name']}")
        print(f"        {test['desc']}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{passed + failed} passed")
    if failed == 0:
        print("All tests passed!")
    else:
        print(f"{failed} test(s) failed.")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_eval()
    sys.exit(0 if success else 1)
