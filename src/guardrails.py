"""
Input and output guardrails for the Music Recommender System.

validate_preferences  — checks user preference dicts before scoring
validate_output       — checks recommendation results are well-formed
check_text_input      — validates natural language input before AI parsing
"""

VALID_GENRES = {
    "pop", "lofi", "jazz", "rock", "electronic", "indie",
    "synthwave", "acoustic", "metal", "classical", "reggae",
    "hip-hop", "country", "ambient",
}
VALID_MOODS = {
    "happy", "chill", "intense", "relaxed", "focused",
    "moody", "energetic", "aggressive",
}
VALID_DECADES = {"1980s", "1990s", "2000s", "2010s", "2020s", None}


def validate_preferences(prefs: dict) -> tuple:
    """
    Validate a user preference dict.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    if not isinstance(prefs, dict):
        return False, ["Preferences must be a dictionary"]

    if prefs.get("genre") not in VALID_GENRES:
        errors.append(
            f"Invalid genre '{prefs.get('genre')}' — valid options: {sorted(VALID_GENRES)}"
        )

    if prefs.get("mood") not in VALID_MOODS:
        errors.append(
            f"Invalid mood '{prefs.get('mood')}' — valid options: {sorted(VALID_MOODS)}"
        )

    energy = prefs.get("energy")
    if not isinstance(energy, (int, float)) or not (0.0 <= energy <= 1.0):
        errors.append(f"energy must be a float between 0.0 and 1.0, got {energy!r}")

    if not isinstance(prefs.get("likes_acoustic"), bool):
        errors.append("likes_acoustic must be True or False")

    if prefs.get("preferred_decade") not in VALID_DECADES:
        errors.append(
            f"preferred_decade must be one of {sorted(d for d in VALID_DECADES if d)}, or null"
        )

    return len(errors) == 0, errors


def validate_output(recs: list, k: int) -> tuple:
    """
    Validate recommendation output list.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    if not isinstance(recs, list):
        return False, ["Output must be a list"]

    if len(recs) > k:
        errors.append(f"Too many results: got {len(recs)}, expected at most {k}")

    scores = [score for _, score, _ in recs]
    if scores != sorted(scores, reverse=True):
        errors.append("Results are not sorted by score (descending)")

    for i, (song, score, reason) in enumerate(recs):
        if not isinstance(score, (int, float)):
            errors.append(f"Item {i}: score must be numeric, got {type(score).__name__}")
        if not isinstance(reason, str) or len(reason.strip()) == 0:
            errors.append(f"Item {i}: reason must be a non-empty string")

    return len(errors) == 0, errors


def check_text_input(text: str) -> tuple:
    """
    Validate natural language input before sending to the AI pipeline.
    Returns (is_valid: bool, error_message: str).
    """
    if not isinstance(text, str):
        return False, "Input must be a string"
    if len(text.strip()) < 3:
        return False, "Input too short — please describe what music you want"
    if len(text) > 500:
        return False, "Input too long — please keep your request under 500 characters"
    return True, ""
