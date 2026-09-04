"""
eligibility_engine.py
Rule-based hard-filter engine. Given a citizen profile, returns the subset
of schemes from schemes.csv the citizen is eligible for, checked against
gender, caste category, age, state, income and occupation constraints.
"""
import pandas as pd


def load_schemes(path="data/schemes.csv"):
    df = pd.read_csv(path)
    return df


def is_eligible(citizen: dict, scheme: pd.Series) -> bool:
    """citizen keys: age, gender, caste_category, income, state, occupation"""

    # State check: scheme must be Central (All India) or match citizen's state
    if scheme["level"] == "State" and scheme["state"] != citizen["state"]:
        return False

    # Gender check
    if scheme["gender"] != "All" and scheme["gender"] != citizen["gender"]:
        return False

    # Caste category check
    if scheme["caste_category"] != "All" and scheme["caste_category"] != citizen["caste_category"]:
        return False

    # Age check
    if not (scheme["min_age"] <= citizen["age"] <= scheme["max_age"]):
        return False

    # Income ceiling check (-1 means no limit)
    if scheme["max_income"] != -1 and citizen["income"] > scheme["max_income"]:
        return False

    # Occupation check
    if scheme["occupation"] != "All" and scheme["occupation"] != citizen["occupation"]:
        return False

    return True


def filter_eligible_schemes(citizen: dict, df: pd.DataFrame) -> pd.DataFrame:
    mask = df.apply(lambda row: is_eligible(citizen, row), axis=1)
    return df[mask].copy()


if __name__ == "__main__":
    df = load_schemes()
    sample_citizen = {
        "age": 24, "gender": "Female", "caste_category": "SC",
        "income": 150000, "state": "Maharashtra", "occupation": "Student",
    }
    result = filter_eligible_schemes(sample_citizen, df)
    print(f"Eligible schemes for sample citizen: {len(result)}")
    print(result[["scheme_name", "state", "benefits"]].to_string(index=False))
