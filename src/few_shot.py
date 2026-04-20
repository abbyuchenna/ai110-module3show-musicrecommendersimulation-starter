"""
few-shot examples for specialized gemma prompting.

these curated examples teach gemma how to map activity and vibe descriptions
to precise genre, mood, and energy values — reducing guessing and improving
consistency compared to zero-shot (no examples) baseline prompting.
"""

import json

EXAMPLES = [
    {
        "input": "something relaxing for bedtime",
        "output": {
            "genre": "ambient",
            "mood": "relaxed",
            "energy": 0.12,
            "likes_acoustic": True,
            "preferred_decade": None,
            "mood_tags": ["relaxed"],
        },
    },
    {
        "input": "hype music for a basketball warmup",
        "output": {
            "genre": "hip-hop",
            "mood": "energetic",
            "energy": 0.88,
            "likes_acoustic": False,
            "preferred_decade": None,
            "mood_tags": ["energetic"],
        },
    },
    {
        "input": "chill lo-fi beats for studying late at night",
        "output": {
            "genre": "lofi",
            "mood": "focused",
            "energy": 0.32,
            "likes_acoustic": False,
            "preferred_decade": "2020s",
            "mood_tags": ["focused", "chill"],
        },
    },
    {
        "input": "i'm driving on the highway and need something upbeat",
        "output": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.75,
            "likes_acoustic": False,
            "preferred_decade": None,
            "mood_tags": ["happy", "energetic"],
        },
    },
    {
        "input": "sad breakup songs, something emotional and acoustic",
        "output": {
            "genre": "acoustic",
            "mood": "moody",
            "energy": 0.22,
            "likes_acoustic": True,
            "preferred_decade": None,
            "mood_tags": ["moody"],
        },
    },
    {
        "input": "i want to feel pumped up at the gym",
        "output": {
            "genre": "rock",
            "mood": "aggressive",
            "energy": 0.92,
            "likes_acoustic": False,
            "preferred_decade": None,
            "mood_tags": ["aggressive", "energetic"],
        },
    },
    {
        "input": "background music for a coffee shop, nothing too loud",
        "output": {
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.38,
            "likes_acoustic": True,
            "preferred_decade": None,
            "mood_tags": ["relaxed", "chill"],
        },
    },
    {
        "input": "deep focus, no distractions, just code",
        "output": {
            "genre": "synthwave",
            "mood": "focused",
            "energy": 0.5,
            "likes_acoustic": False,
            "preferred_decade": "2020s",
            "mood_tags": ["focused"],
        },
    },
]


def build_few_shot_block() -> str:
    """format examples as a demonstration block to inject into the gemma prompt."""
    lines = ["here are examples of correct preference parsing:\n"]
    for ex in EXAMPLES:
        lines.append(f'input: "{ex["input"]}"')
        lines.append(f'output: {json.dumps(ex["output"])}')
        lines.append("")
    return "\n".join(lines)
