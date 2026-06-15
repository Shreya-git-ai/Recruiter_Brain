JD_FOCUS_TEXT = """
Senior AI Engineer at a Series A AI-native talent intelligence platform.
The ideal candidate has 6-8 years of total experience, with 4-5 years in applied
machine learning and AI roles at product companies, not pure services or consulting
firms. They have production experience with embeddings-based retrieval systems
such as sentence-transformers, OpenAI embeddings, BGE, or E5, deployed to real
users, including handling embedding drift, index refresh, and retrieval quality
regression. They have production experience with vector databases or hybrid
search infrastructure such as Pinecone, Weaviate, Qdrant, Milvus, OpenSearch,
Elasticsearch, or FAISS. They have strong Python skills and care about code
quality. They have hands-on experience designing evaluation frameworks for
ranking systems, including NDCG, MRR, MAP, and offline-to-online correlation
for A/B testing. They have shipped at least one end-to-end ranking, search, or
recommendation system to real users at meaningful scale. Their work involves
natural language processing and information retrieval, not purely computer
vision, speech, or robotics.
"""


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_semantic_scores(jd_embedding, candidate_embeddings):
    """
    jd_embedding: shape (embedding_dim,) - single vector for JD
    candidate_embeddings: shape (n_candidates, embedding_dim) - matrix

    Returns: array of similarity scores (0-1), one per candidate.
    """
    sims = cosine_similarity(jd_embedding.reshape(1, -1), candidate_embeddings)[0]
    sims = np.clip(sims, 0, 1)
    return sims