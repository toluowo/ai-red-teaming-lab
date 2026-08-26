"""Risk classification for the lab's documented scoring scale."""


def classify_risk(score: int) -> str:
    """Return a risk label for a numeric triage score."""
    if score < 0:
        raise ValueError("score cannot be negative")
    if score == 0:
        return "Safe"
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 14:
        return "High"
    return "Critical"
