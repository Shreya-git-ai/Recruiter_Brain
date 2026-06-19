# Recruiter Brain

### Explainable AI-Powered Talent Matching System

Recruiter Brain is a candidate ranking and talent-matching system that combines semantic search, hiring-signal analysis, profile-quality screening, and explainable AI to identify the most relevant candidates for a given job description.

The system is designed to process large candidate datasets efficiently while maintaining transparency in ranking decisions through recruiter-friendly explanations.

---

## Overview

Modern recruitment pipelines often struggle with:

* Large volumes of candidate profiles
* Keyword stuffing and profile manipulation
* Difficulty identifying genuine role fit
* Lack of transparency in ranking decisions

Recruiter Brain addresses these challenges through a hybrid ranking architecture that combines semantic relevance, professional experience signals, quality filters, and explainable scoring.

---

## Key Features

* Semantic candidate-job matching using transformer embeddings
* Explainable ranking with human-readable reasoning
* Profile-quality and anomaly detection
* Hard requirement filtering
* Hiring signal analysis
* Efficient ranking for 100k+ candidate profiles
* CPU-friendly inference through embedding precomputation
* Fully reproducible ranking pipeline

---

## System Architecture

```text
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
```

---

## Ranking Pipeline

### Candidate Loading

Candidate profiles are loaded from structured datasets and normalized for downstream processing.

### Hard Filtering

Candidates that do not satisfy mandatory job requirements are filtered before ranking.

### Profile Quality Analysis

The system identifies suspicious or low-quality profiles using heuristic checks such as:

* Skill inflation
* Profile inconsistencies
* Keyword stuffing
* Honeypot indicators

### Semantic Matching

The job description is embedded using a transformer model and compared against candidate embeddings using cosine similarity.

Model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Career Fit Scoring

Additional scoring considers:

* Relevant titles
* AI/ML experience
* Search and retrieval experience
* Recommendation systems exposure
* Production ML background

### Hiring Signal Analysis

Professional signals are incorporated into ranking decisions to improve candidate quality assessment.

### Explainable Recommendations

For every ranked candidate, the system generates a concise explanation describing:

* Why the candidate is relevant
* Matching experience
* Relevant strengths
* Potential concerns

---

## Project Structure

```text
Recruiter-Brain/
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
├── output/
├── run.py
├── validate_submission.py
├── requirements.txt
└── submission_metadata.yaml
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Precomputation

Generate candidate embeddings:

```bash
python src/precompute_embeddings.py
```

Generated artifacts:

```text
data/candidate_embeddings.npy
data/candidate_ids.npy
```

Embedding generation is performed once and reused across ranking runs.

---

## Running the Ranker

```bash
python run.py
```

Generated output:

```text
output/final_ranked_candidates.csv
```

---

## Validation

```bash
python validate_submission.py output/final_ranked_candidates.csv
```

Expected result:

```text
Submission is valid.
```

---

## Performance

Observed runtime on CPU:

| Stage                     | Runtime |
| ------------------------- | ------- |
| Candidate Loading         | ~15s    |
| Filtering                 | ~20s    |
| Embedding Lookup          | ~5s     |
| Semantic Scoring          | <1s     |
| Final Ranking & Reasoning | ~44s    |
| Total Runtime             | ~98s    |

---

## Future Improvements

* Learning-to-rank models
* Recruiter feedback loops
* Vector database integration
* Real-time recommendation APIs
* Interactive recruiter dashboard
* Personalized ranking strategies

---

## Tech Stack

* Python
* NumPy
* Pandas
* Sentence Transformers
* Hugging Face Transformers
* Scikit-learn

---

## Acknowledgements

This project was originally developed during an AI hiring and talent-matching challenge and later refined into a generalized candidate-ranking system focused on scalable and explainable recruitment intelligence.
