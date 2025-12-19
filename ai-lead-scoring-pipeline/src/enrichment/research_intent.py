from src.ingestion.pubmed import fetch_recent_publications, fetch_abstract
from src.ai.llm_classifier import classify_relevance

def compute_scientific_intent_score(author_name: str) -> float:
    pubmed_ids = fetch_recent_publications(author_name)

    if not pubmed_ids:
        return 0.0

    scores = []
    for pid in pubmed_ids:
        abstract = fetch_abstract(pid)
        score = classify_relevance(abstract)
        scores.append(score)

    return max(scores)
