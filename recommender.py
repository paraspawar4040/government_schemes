"""
recommender.py
End-to-end pipeline: eligibility hard-filter -> ML match-score ranking ->
auto-generated "why recommended" explanation string per scheme.
"""
import joblib
import pandas as pd

from eligibility_engine import load_schemes, filter_eligible_schemes
from features import encode_features


def _score_row(citizen, scheme):
    return {
        "age": citizen["age"], "gender": citizen["gender"],
        "caste_category": citizen["caste_category"], "income": citizen["income"],
        "state": citizen["state"], "occupation": citizen["occupation"],
        "scheme_id": scheme["scheme_id"], "scheme_gender": scheme["gender"],
        "scheme_caste": scheme["caste_category"], "scheme_min_age": scheme["min_age"],
        "scheme_max_age": scheme["max_age"], "scheme_max_income": scheme["max_income"],
        "scheme_occupation": scheme["occupation"], "scheme_level": scheme["level"],
    }


def explain(citizen, scheme):
    reasons = []
    if scheme["level"] == "State":
        reasons.append(f"resident of {scheme['state']}")
    else:
        reasons.append("Central / All-India scheme")
    if scheme["gender"] != "All":
        reasons.append(f"{scheme['gender'].lower()} applicant")
    if scheme["caste_category"] != "All":
        reasons.append(f"{scheme['caste_category']} category")
    if scheme["max_income"] != -1:
        reasons.append(f"income within Rs {int(scheme['max_income']):,} limit")
    if scheme["occupation"] != "All":
        reasons.append(f"matches occupation: {scheme['occupation']}")
    reasons.append(f"age {citizen['age']} within {int(scheme['min_age'])}-{int(scheme['max_age'])} band")
    return "Matched because: " + "; ".join(reasons) + "."


def recommend(citizen: dict, schemes_path="data/schemes.csv",
              reg_path="models/match_score_regressor.joblib", top_n=10):
    schemes = load_schemes(schemes_path)
    eligible = filter_eligible_schemes(citizen, schemes)

    if eligible.empty:
        return eligible.assign(match_score=[])

    bundle = joblib.load(reg_path)
    reg_model, columns = bundle["model"], bundle["columns"]

    rows = [_score_row(citizen, s) for _, s in eligible.iterrows()]
    pairs_df = pd.DataFrame(rows)
    encoded = encode_features(pairs_df.assign(eligible=1, match_score=0))
    encoded = encoded.drop(columns=["eligible", "match_score"], errors="ignore")
    # align columns with training-time schema
    for col in columns:
        if col not in encoded.columns:
            encoded[col] = 0
    encoded = encoded[columns]

    scores = reg_model.predict(encoded)
    eligible = eligible.copy()
    eligible["match_score"] = (scores * 100).round(1)
    eligible["why_recommended"] = [explain(citizen, s) for _, s in eligible.iterrows()]

    eligible = eligible.sort_values("match_score", ascending=False).head(top_n)
    return eligible.reset_index(drop=True)


if __name__ == "__main__":
    citizen = {
        "age": 24, "gender": "Female", "caste_category": "SC",
        "income": 150000, "state": "Maharashtra", "occupation": "Student",
    }
    results = recommend(citizen)
    for _, r in results.iterrows():
        print(f"[{r['match_score']:5.1f}] {r['scheme_name']} ({r['state']})")
        print("        ", r["why_recommended"])
