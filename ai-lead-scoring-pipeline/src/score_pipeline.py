from src.score import calculate_propensity_score
from src.enrichment.research_intent import compute_scientific_intent_score

def apply_scoring(df):
    scores = []
    breakdowns = []

    for _, row in df.iterrows():
        ai_intent = compute_scientific_intent_score(row["name"])

        score, breakdown = calculate_propensity_score(row)
        breakdown["scientific_intent_ai"] = int(ai_intent * 20)

        final_score = min(score + breakdown["scientific_intent_ai"], 100)

        scores.append(final_score)
        breakdowns.append(breakdown)

    df["propensity_score"] = scores
    df["score_breakdown"] = breakdowns
    return df
