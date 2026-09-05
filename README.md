# \# AI Government Schemes Recommendation System



An AI-based system that recommends Indian government welfare schemes to citizens based on gender, caste category, income, state, age, and occupation, using a two-stage design: a rule-based eligibility filter followed by a machine-learned relevance ranking.



\## **Coverage**



\- 3,488 schemes total

\- 560 Central / All-India schemes

\- 2,928 State schemes

\- 223 scheme categories



Scheme names/departments reflect well-known, publicly documented Central and State welfare programs. Benefit amounts change with each budget cycle — verify current figures on the official portal (linked per scheme) before citing exact numbers in your report or viva.



\## **Dataset Scope**



This project includes 3,488 schemes (560 Central + 2,928 across states/UTs) covering major welfare categories — education, health, agriculture, housing, women \& child welfare, pension, and more. It is a large curated sample for demonstrating the recommendation pipeline, not an exhaustive list — India's official myScheme portal lists additional schemes at the district level not yet represented here. Contributions to expand or verify coverage are welcome.



\## **Architecture**







**### Stage 1 — Eligibility Engine (rule-based)**



Hard filters on: state (Central schemes always pass), gender, caste category, age range, income ceiling, occupation. This guarantees no ineligible scheme is ever shown, regardless of what the ML layer predicts.



\### Stage 2 — ML Ranking



\- Eligibility classifier: Random Forest benchmarked against Logistic Regression, Decision Tree, KNN, and Gradient Boosting on a synthetic population of citizen×scheme pairs (`features.py`). Metrics saved to `models/metrics.json` for your report.

\- Match-score regressor: Random Forest Regressor scores each eligible scheme 0–100 by relevance (occupation specificity, income headroom, age centrality, caste/state specificity), so results aren't just a flat list — they're ranked by fit.

\- Explainability: each recommendation includes an auto-generated "Matched because…" string listing the specific eligibility factors that applied.



\## Chatbot



`chatbot\_parser.py` extracts age, gender, caste, income, state and occupation from a free-text sentence via regex/keyword matching (no external LLM dependency, runs offline).



\## Running It



```bash

pip install -r requirements.txt

python3 data/build\_dataset.py   # (re)generate the dataset

python3 train\_model.py          # train + benchmark models

streamlit run app.py            # launch the app

```



\## Extending the Dataset



Add rows to the `STATE\_SCHEMES` / `UT\_SCHEMES` lists in `data/build\_dataset.py` and re-run it — the eligibility engine, ML pipeline and app all read `data/schemes.csv` directly, so no other code needs to change.



\## Suggested Report Sections



1\. Problem statement \& motivation (scheme awareness gap in India)

2\. Literature survey (NSAP, myScheme portal, prior recommender systems)

3\. System architecture (2-stage: rule engine + ML ranking)

4\. Dataset description (3,488 schemes, 15 attributes, 560 Central + 2,928 State)

5\. ML model comparison table (from `models/metrics.json`)

6\. UI screenshots (Form tab, Chatbot tab, Analytics tab)

7\. Limitations \& future scope (verified live scraping, Aadhaar-based auto-fill, multilingual chatbot, state DBT integration)

