"""
chatbot_parser.py
Lightweight regex/keyword parser that extracts a citizen profile
(age, gender, caste_category, income, state, occupation) from a
free-text sentence, e.g.:
  "I am a 24 year old SC woman from Maharashtra, student, family
   income 1.5 lakh"
"""
import re

GENDER_KEYWORDS = {
    "woman": "Female", "women": "Female", "female": "Female", "girl": "Female",
    "man": "Male", "men": "Male", "male": "Male", "boy": "Male",
    "transgender": "Transgender", "trans": "Transgender",
}

CASTE_KEYWORDS = ["SC", "ST", "OBC", "General", "Minority"]

OCCUPATION_KEYWORDS = {
    "farmer": "Farmer", "farming": "Farmer", "agriculture": "Farmer",
    "student": "Student", "studying": "Student",
    "laborer": "Laborer", "labourer": "Laborer", "labour": "Laborer", "worker": "Laborer",
    "unemployed": "Unemployed", "jobless": "Unemployed",
    "self-employed": "Self-employed", "self employed": "Self-employed",
    "business": "Self-employed", "entrepreneur": "Self-employed",
    "widow": "Woman-headed household", "single mother": "Woman-headed household",
    "senior citizen": "Senior Citizen", "elderly": "Senior Citizen", "retired": "Senior Citizen",
    "disabled": "Disabled", "disability": "Disabled", "divyang": "Disabled",
}

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry",
    "Chandigarh", "Andaman and Nicobar Islands", "Lakshadweep",
    "Dadra and Nagar Haveli and Daman and Diu",
]


def _parse_income(text):
    text_l = text.lower()
    # e.g. "1.5 lakh", "150000", "2 lakhs", "3 crore"
    m = re.search(r"(\d+(?:\.\d+)?)\s*lakh", text_l)
    if m:
        return int(float(m.group(1)) * 100000)
    m = re.search(r"(\d+(?:\.\d+)?)\s*crore", text_l)
    if m:
        return int(float(m.group(1)) * 10000000)
    m = re.search(r"income[^\d]{0,15}(\d{4,9})", text_l)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{5,9})\s*(?:rs|rupees|inr)?\s*(?:per year|/year|annually)?", text_l)
    if m:
        return int(m.group(1))
    return None


def _parse_age(text):
    m = re.search(r"(\d{1,3})\s*(?:years?|yrs?)[\s-]*old", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"\bage[d]?\s*[:\-]?\s*(\d{1,3})\b", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{1,2})\s*year old\b", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


def _parse_gender(text):
    text_l = text.lower()
    for kw, val in GENDER_KEYWORDS.items():
        if re.search(rf"\b{re.escape(kw)}\b", text_l):
            return val
    return None


def _parse_caste(text):
    for c in CASTE_KEYWORDS:
        if re.search(rf"\b{c}\b", text, re.IGNORECASE if c != "SC" else 0):
            return c if c != "General" else "General"
    return None


def _parse_occupation(text):
    text_l = text.lower()
    for kw, val in OCCUPATION_KEYWORDS.items():
        if kw in text_l:
            return val
    return None


def _parse_state(text):
    for state in INDIAN_STATES:
        if re.search(rf"\b{re.escape(state)}\b", text, re.IGNORECASE):
            return state
    return None


def parse_profile(text: str) -> dict:
    """Extracts as much of a citizen profile as possible from free text.
    Missing fields are returned as None so the UI can prompt for them."""
    return {
        "age": _parse_age(text),
        "gender": _parse_gender(text),
        "caste_category": _parse_caste(text),
        "income": _parse_income(text),
        "state": _parse_state(text),
        "occupation": _parse_occupation(text),
    }


if __name__ == "__main__":
    samples = [
        "I am a 24 year old SC woman from Maharashtra, student, family income 1.5 lakh",
        "62 years old farmer in Punjab, general category, income around 90000",
        "My son is 16, ST, studying in Odisha, no income",
    ]
    for s in samples:
        print(s)
        print(" ->", parse_profile(s))
        print()
