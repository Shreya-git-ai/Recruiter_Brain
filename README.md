Recruiter Brain

Explainable AI-powered candidate ranking system

Recruiter Brain ranks candidates against a job description using semantic search instead of keyword matching — combining transformer-based embeddings, hiring-signal analysis, profile-quality screening, and explainable scoring to surface genuinely relevant candidates from large applicant pools.

🔗 Live demo: recruiterbrain-u5hmq6tp5jnpafboh3ke5x.streamlit.app


The Problem

Keyword-based hiring fails in a specific, predictable way. A candidate who lists "RAG, Pinecone, LLM" in their skills section beats someone who actually shipped a recommendation system but described it in plain English. Most ATS and recruiter tools reward keyword density, not actual fit — and they're trivially gamed by keyword-stuffed profiles.

The Solution

Recruiter Brain ranks candidates on meaning, not vocabulary. Semantic embeddings capture what a candidate actually did, not just which words they used. This is combined with rule-based honeypot detection, red-flag penalties (title-chasing, non-coding roles dressed up as technical ones), and behavioral/availability signals — so the system surfaces candidates who are genuinely relevant, not just well-optimized for keyword search.


Key Features


Semantic candidate–job matching using transformer embeddings (sentence-transformers/all-MiniLM-L6-v2) and cosine similarity
Explainable ranking — every candidate gets a human-readable reasoning summary (matching experience, strengths, concerns)
Profile-quality and honeypot detection — flags skill inflation, keyword stuffing, and deliberately fake/inconsistent profiles
Hard requirement filtering before ranking begins
Career fit & hiring signal scoring — relevant titles, AI/ML production experience, search/retrieval/recommendation system exposure
Scales to 100k+ candidate profiles while staying fully CPU-friendly
Reproducible pipeline — embeddings precomputed once, ranking runs in under 2 minutes



System Architecture

Job Description
      │
      ▼
Embedding Generation
      │
      ▼
Candidate Loading
      │
      ▼
Hard Filters
      │
      ▼
Profile Quality Checks
      │
      ▼
Semantic Matching
      │
      ▼
Career Fit Scoring
      │
      ▼
Hiring Signal Analysis
      │
      ▼
Score Aggregation
      │
      ▼
Reasoning Generation
      │
      ▼
Top Ranked Candidates

Ranking Pipeline

1. Candidate Loading — Profiles are loaded from structured datasets and normalized for downstream processing.

2. Hard Filtering — Candidates that fail mandatory job requirements are removed before ranking.

3. Profile Quality Analysis — Heuristic checks catch skill inflation, profile inconsistencies, keyword stuffing, and honeypot indicators.

4. Semantic Matching — The job description is embedded and compared against precomputed candidate embeddings using cosine similarity.

5. Career Fit Scoring — Additional weight given to relevant titles, AI/ML experience, search/retrieval experience, recommendation systems exposure, and production ML background.

6. Hiring Signal Analysis — Professional signals are factored into final ranking.

7. Explainable Recommendations — Every ranked candidate gets a concise, recruiter-readable explanation of why they were ranked where they were.


Compute Strategy

CPU-only, no external API calls during ranking. The full 100K-candidate embedding set is precomputed once (~3.5 hrs) and cached to disk in .npy format. The ranking step loads precomputed vectors and completes in under 2 minutes.

StageRuntimeCandidate Loading~15sFiltering~20sEmbedding Lookup~5sSemantic Scoring<1sFinal Ranking & Reasoning~44sTotal Runtime~98s


Project Structure

Recruiter-Brain/
│
├── app/                          # Streamlit application
│   ├── pages/
│   │   ├── About.py
│   │   ├── Analytics.py
│   │   ├── Candidate_ranking.py
│   │   └── Job_Description.py
│   ├── ui/
│   │   ├── components.py
│   │   ├── styles.py
│   │   └── utils.py
│   ├── home_demo.py
│   └── HOME.py
│
├── data/
│   ├── candidates.jsonl
│   ├── candidate_embeddings.npy
│   ├── candidate_ids.npy
│   └── sample_candidates.json
│
├── src/
│   ├── pipeline.py
│   ├── precompute_embeddings.py
│   ├── semantic_score.py
│   ├── signal_score.py
│   ├── career_fit_score.py
│   ├── hard_filters.py
│   ├── honeypot_detector.py
│   ├── reasoning.py
│   ├── combine.py
│   └── data_loader.py
│
├── tests/
├── output/                       # Pipeline-generated rankings
├── outputs/                      # Streamlit app outputs (UI read path)
├── run.py
├── validate_submission.py
├── requirements.txt
└── submission_metadata.yaml


Getting Started

Install dependencies

bashpip install -r requirements.txt

Precompute embeddings (one-time)

bashpython src/precompute_embeddings.py

Generates data/candidate_embeddings.npy and data/candidate_ids.npy. This step is run once and reused across all ranking runs.

Run the ranker

bashpython run.py

Outputs output/final_ranked_candidates.csv.

Validate output

bashpython validate_submission.py output/final_ranked_candidates.csv


Tech Stack

Python · NumPy · Pandas · Sentence Transformers · Hugging Face Transformers · scikit-learn · Streamlit


Future Improvements


Learning-to-rank models
Recruiter feedback loops
Vector database integration
Real-time recommendation APIs
Personalized ranking strategies



About

Built by Shreya Chaturvedi, 1st-year CS (AI/ML) student. Originally developed for an AI hiring and talent-matching challenge, then refined into a generalized, scalable candidate-ranking system.