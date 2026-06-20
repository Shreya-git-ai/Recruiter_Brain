"""Quick diagnostic for precomputed embedding files."""

import argparse
import os
import sys

from src.embedding_store import expected_file_size, repair_oversized_npy, validate_npy_files


def main():
    parser = argparse.ArgumentParser(description="Validate or repair precomputed embedding files")
    parser.add_argument("--repair", action="store_true", help="Truncate oversized .npy files to header size")
    args = parser.parse_args()

    embeddings_path = "data/candidate_embeddings.npy"
    ids_path = "data/candidate_ids.npy"
    candidates_path = "data/candidates.jsonl"

    print("=== NPY diagnostics ===\n")

    for label, path in [("embeddings", embeddings_path), ("ids", ids_path)]:
        if not os.path.isfile(path):
            print(f"[FAIL] {label}: file missing at {path}")
            continue

        size = os.path.getsize(path)
        try:
            expected = expected_file_size(path)
            status = "OK" if abs(size - expected) <= 1024 else "SUSPECT"
            print(f"[{status}] {label}: {size:,} bytes on disk, header expects {expected:,}")

            if args.repair and status == "SUSPECT" and size > expected:
                if repair_oversized_npy(path):
                    new_size = os.path.getsize(path)
                    print(f"  -> repaired: truncated to {new_size:,} bytes")
        except Exception as exc:
            print(f"[FAIL] {label}: {exc}")

    if os.path.isfile(candidates_path):
        print(f"\nCandidates file present: {os.path.getsize(candidates_path):,} bytes")
        try:
            with open(candidates_path, "rb") as f:
                line_count = sum(1 for _ in f)
            print(f"Candidates line count: {line_count:,}")
        except OSError as exc:
            print(f"Could not count candidate lines: {exc}")
    else:
        print(f"\n[WARN] {candidates_path} not found (gitignored — place it in data/)")

    print("\n=== Load test ===")
    try:
        embeddings, ids = validate_npy_files(embeddings_path, ids_path)
        print(f"Loaded embeddings shape={embeddings.shape}, dtype={embeddings.dtype}")
        print(f"Loaded ids shape={ids.shape}, dtype={ids.dtype}")
        print(f"First ID: {ids[0]}")
        print(f"Last ID:  {ids[-1]}")
        print("\nFiles look valid.")
        return 0
    except Exception as exc:
        print(f"\n[FAIL] {exc}")
        print("\nFix: delete data/candidate_embeddings.npy and data/candidate_ids.npy,")
        print("     then run:  python src/precompute_embeddings.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
