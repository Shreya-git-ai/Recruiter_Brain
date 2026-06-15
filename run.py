import argparse
from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Redrob Hackathon - Candidate Ranking Pipeline")
    parser.add_argument("--candidates", default="data/candidates.jsonl", help="Path to candidates file")
    parser.add_argument("--output", default="outputs/ranked_candidates.csv", help="Output CSV path")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of candidates loaded (for testing)")
    parser.add_argument("--top_n", type=int, default=100, help="Number of top candidates to output")

    args = parser.parse_args()

    run_pipeline(
        candidates_path=args.candidates,
        output_path=args.output,
        limit=args.limit,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()