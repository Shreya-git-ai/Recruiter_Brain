import time
import numpy as np
from sentence_transformers import SentenceTransformer

from src.data_loader import load_candidates, build_candidate_text


def precompute_embeddings(candidates_path, output_npy_path, output_ids_path, limit=None):
    t0 = time.time()
    print("Loading candidates...")
    candidates = load_candidates(candidates_path, limit=limit)
    print(f"Loaded {len(candidates)} candidates in {time.time()-t0:.1f}s")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Building candidate texts...")
    candidate_texts = [build_candidate_text(c) for c in candidates]
    candidate_ids = [c["candidate_id"] for c in candidates]

    print(f"Embedding {len(candidate_texts)} candidates...")
    t1 = time.time()
    embeddings = model.encode(candidate_texts, batch_size=128, show_progress_bar=True)
    print(f"Embedding done in {time.time()-t1:.1f}s")

    print(f"Saving embeddings to {output_npy_path}...")
    np.save(output_npy_path, embeddings)

    print(f"Saving candidate_ids to {output_ids_path}...")
    np.save(output_ids_path, np.array(candidate_ids))

    print(f"TOTAL TIME: {time.time()-t0:.1f}s")
    print("Done.")


if __name__ == "__main__":
    precompute_embeddings(
        candidates_path="data/candidates.jsonl",
        output_npy_path="data/candidate_embeddings.npy",
        output_ids_path="data/candidate_ids.npy",
    )