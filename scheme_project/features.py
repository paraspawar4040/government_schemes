"""
features.py
Generates a synthetic citizen population + (citizen, scheme) training pairs
for the ML layer: an eligibility classifier and a match-score regressor
that ranks eligible schemes by relevance instead of just listing them.
"""
import random
import pandas as pd
import numpy as np

STATES = None  # filled from schemes.csv at runtime
GENDERS = ["Male", "Female", "Transgender"]
CASTES = ["General", "OBC", "SC", "ST", "Minority"]
OCCUPATIONS = ["Farmer", "Student", "Laborer", "Unemployed", "Self-employed",
               "Woman-headed household", "Senior Citizen", "Disabled", "All"]


def generate_citizens(n, states, seed=42):
    rng = random.Random(seed)
    citizens = []
    for i in range(n):
        age = rng.randint(0, 85)
        gender = rng.choice(GENDERS)
        caste = rng.choice(CASTES)
        income = rng.choice([0, 50000, 90000, 120000, 150000, 200000, 250000,
                              300000, 400000, 600000, 800000, 1200000])
        state = rng.choice(states)
        occupation = rng.choice(OCCUPATIONS)
        citizens.append({
            "citizen_id": i, "age": age, "gender": gender,
            "caste_category": caste, "income": income, "state": state,
            "occupation": occupation,
        })
    return pd.DataFrame(citizens)


def _matches(val_scheme, val_citizen):
    return val_scheme == "All" or val_scheme == val_citizen


def build_training_pairs(citizens_df, schemes_df):
    """
    For every citizen x scheme pair, compute:
      - eligible (0/1) using the same hard-filter rules as eligibility_engine
      - match_score (0-1): how strong a fit, for schemes that ARE eligible,
        based on how many soft-criteria (occupation match, income headroom,
        age centrality) align -- this is the regression target.
    """
    rows = []
    for _, c in citizens_df.iterrows():
        for _, s in schemes_df.iterrows():
            state_ok = (s["level"] != "State") or (s["state"] == c["state"])
            gender_ok = _matches(s["gender"], c["gender"])
            caste_ok = _matches(s["caste_category"], c["caste_category"])
            age_ok = s["min_age"] <= c["age"] <= s["max_age"]
            income_ok = (s["max_income"] == -1) or (c["income"] <= s["max_income"])
            occ_ok = _matches(s["occupation"], c["occupation"])

            eligible = int(state_ok and gender_ok and caste_ok and age_ok
                            and income_ok and occ_ok)

            if eligible:
                # soft match score: reward occupation specificity, income headroom,
                # age centrality within the scheme's band
                occ_bonus = 0.3 if s["occupation"] != "All" and s["occupation"] == c["occupation"] else 0.0
                if s["max_income"] == -1:
                    income_bonus = 0.2
                else:
                    headroom = max(0, (s["max_income"] - c["income"]) / max(s["max_income"], 1))
                    income_bonus = 0.2 * headroom
                age_span = max(s["max_age"] - s["min_age"], 1)
                age_center = (s["min_age"] + s["max_age"]) / 2
                age_bonus = 0.2 * (1 - min(abs(c["age"] - age_center) / age_span, 1))
                caste_bonus = 0.15 if s["caste_category"] != "All" and s["caste_category"] == c["caste_category"] else 0.0
                state_bonus = 0.15 if s["level"] == "State" else 0.05
                match_score = min(1.0, 0.0 + occ_bonus + income_bonus + age_bonus + caste_bonus + state_bonus)
            else:
                match_score = 0.0

            rows.append({
                "age": c["age"], "gender": c["gender"], "caste_category": c["caste_category"],
                "income": c["income"], "state": c["state"], "occupation": c["occupation"],
                "scheme_id": s["scheme_id"], "scheme_gender": s["gender"],
                "scheme_caste": s["caste_category"], "scheme_min_age": s["min_age"],
                "scheme_max_age": s["max_age"], "scheme_max_income": s["max_income"],
                "scheme_occupation": s["occupation"], "scheme_level": s["level"],
                "eligible": eligible, "match_score": match_score,
            })
    return pd.DataFrame(rows)


def encode_features(pairs_df):
    """One-hot / numeric encode the pairs dataframe for sklearn models."""
    df = pairs_df.copy()
    cat_cols = ["gender", "caste_category", "occupation", "scheme_gender",
                "scheme_caste", "scheme_occupation", "scheme_level"]
    df = pd.get_dummies(df, columns=cat_cols)
    df["income_gap"] = df["scheme_max_income"].replace(-1, 2_000_000) - df["income"]
    df["age_in_band"] = ((df["age"] >= df["scheme_min_age"]) & (df["age"] <= df["scheme_max_age"])).astype(int)
    drop_cols = ["state", "scheme_id"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


if __name__ == "__main__":
    schemes = pd.read_csv("data/schemes.csv")
    states = sorted(schemes.loc[schemes.level == "State", "state"].unique().tolist()) + ["All India"]
    citizens = generate_citizens(300, states)
    pairs = build_training_pairs(citizens, schemes)
    print("Citizens:", len(citizens), "| Training pairs:", len(pairs))
    print("Eligible rate:", pairs.eligible.mean().round(3))
    pairs.to_csv("data/training_pairs.csv", index=False)
    print("Saved data/training_pairs.csv")
