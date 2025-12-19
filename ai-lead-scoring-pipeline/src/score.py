def score_role_fit(title: str) -> int:
    keywords = ["toxicology", "safety", "hepatic", "3d"]
    for kw in keywords:
        if kw in title:
            return 30
    return 0


def score_scientific_intent(research_area: str, year: int | None) -> int:
    if year is None:
        return 0

    score = 0
    if any(kw in research_area.lower() for kw in ["toxicity", "hepatic", "3d"]):
        score += 20

    if year >= 2023:
        score += 20

    return min(score, 40)


def score_funding(funding_stage: str | None) -> int:
    if funding_stage in ["Series A", "Series B"]:
        return 20
    if funding_stage == "Series C":
        return 15
    return 0


def score_location(location: str) -> int:
    hubs = ["boston", "cambridge", "basel", "bay area"]
    if location.lower() in hubs:
        return 10
    return 0
def calculate_propensity_score(row: dict) -> tuple[int, dict]:
    breakdown = {}

    breakdown["role_fit"] = score_role_fit(row["title"])
    breakdown["scientific_intent"] = score_scientific_intent(
        row["research_area"], row["last_publication_year"]
    )
    breakdown["funding"] = score_funding(row["funding_stage"])
    breakdown["location"] = score_location(row["person_location"])

    total_score = sum(breakdown.values())
    return min(total_score, 100), breakdown
