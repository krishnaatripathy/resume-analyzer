import re


def is_resume_text(text):
    """Check if extracted text actually looks like a resume."""
    if len(text.strip()) < 100:
        return False, "The PDF seems empty or has very little text."

    resume_keywords = [
        "experience", "education", "skills", "project", "work",
        "university", "college", "degree", "intern", "developer",
        "engineer", "analyst", "github", "linkedin", "email"
    ]

    text_lower = text.lower()
    found = sum(1 for kw in resume_keywords if kw in text_lower)

    if found < 3:
        return False, "This doesn't look like a resume. Please upload a proper resume PDF."

    return True, "OK"


def extract_score_from_text(text, label):
    """Pull a numeric score like '85' from text like 'Overall Score: 85/100'."""
    pattern = rf"{label}[:\s]*(\d{{1,3}})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def get_score_color(score):
    """Return a CSS class name based on score range."""
    if score is None:
        return "gray"
    if score >= 75:
        return "green"
    elif score >= 50:
        return "orange"
    else:
        return "red"


def get_strength_label(score):
    """Return a human-readable strength label."""
    if score is None:
        return "Unknown"
    if score >= 80:
        return "Strong 💪"
    elif score >= 65:
        return "Good 👍"
    elif score >= 45:
        return "Average 😐"
    else:
        return "Weak ⚠️"


def word_count(text):
    return len(text.split())
