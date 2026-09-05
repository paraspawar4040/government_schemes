# AI Government Schemes Recommendation System

An AI-based system that recommends Indian government welfare schemes to
citizens based on **gender, caste category, income, state, age, and
occupation**, using a two-stage design: a rule-based eligibility filter
followed by a machine-learned relevance ranking.

## Coverage
- **115 schemes** total
- **28 states + 8 Union Territories** all represented (3 schemes/state avg)
- **24 Central / All-India schemes**
- Scheme names/departments reflect well-known, publicly documented Central
  and State welfare programs. Benefit amounts change with each budget cycle
  — verify current figures on the official portal (linked per scheme)
  before citing exact numbers in your report or viva.

## Architecture
```
data/schemes.csv         -> master scheme dataset (15 columns)
data/build_dataset.py    -> regenerates schemes.csv
eligibility_engine.py    -> Stage 1: rule-based hard filter
features.py               -> synthetic citizen population + training pairs
train_model.py            -> Stage 2: trains + benchmarks ML models
recommender.py             -> full pipeline: filter -> rank -> explain
chatbot_parser.py         -> free-text -> structured profile (regex/NLP)
app.py                    -> Streamlit UI (Form / Chatbot / Analytics)
models/                   -> trained models + metrics.json
```

### Stage 1 — Eligibility Engine (rule-based)
Hard filters on: state (Central schemes always pass), gender, caste
category, age range, income ceiling, occupation. This guarantees no
ineligible scheme is ever shown, regardless of what the ML layer predicts.

### Stage 2 — ML Ranking
- **Eligibility classifier**: Random Forest benchmarked against Logistic
  Regression, Decision Tree, KNN, and Gradient Boosting on a synthetic
  population of citizen×scheme pairs (`features.py`). Metrics saved to
  `models/metrics.json` for your report.
- **Match-score regressor**: Random Forest Regressor scores each *eligible*
  scheme 0–100 by relevance (occupation specificity, income headroom, age
  centrality, caste/state specificity), so results aren't just a flat list
  — they're ranked by fit.
- **Explainability**: each recommendation includes an auto-generated
  "Matched because…" string listing the specific eligibility factors that
  applied.

### Chatbot
`chatbot_parser.py` extracts age, gender, caste, income, state and
occupation from a free-text sentence via regex/keyword matching (no
external LLM dependency, runs offline).

## Running it
```bash
pip install -r requirements.txt
python3 data/build_dataset.py   # (re)generate the dataset
python3 train_model.py          # train + benchmark models (~30s)
streamlit run app.py            # launch the app
```

## Extending the dataset
Add rows to the `STATE_SCHEMES` / `UT_SCHEMES` lists in
`data/build_dataset.py` and re-run it — the eligibility engine, ML
pipeline and app all read `data/schemes.csv` directly, so no other code
needs to change.

## Suggested report sections
1. Problem statement & motivation (scheme awareness gap in India)
2. Literature survey (NSAP, myScheme portal, prior recommender systems)
3. System architecture (2-stage: rule engine + ML ranking)
4. Dataset description (115 schemes, 15 attributes, 28 states + 8 UTs)
5. ML model comparison table (from `models/metrics.json`)
6. UI screenshots (Form tab, Chatbot tab, Analytics tab)
7. Limitations & future scope (verified live scraping, Aadhaar-based
   auto-fill, multilingual chatbot, state DBT integration)
