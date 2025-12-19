from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please add it to your .env file."
    )

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are an expert in drug discovery and toxicology.

Classify whether the following scientific abstract is relevant to:
- 3D in-vitro models
- organ-on-chip systems
- preclinical safety assessment or toxicology

Respond with ONLY one word:
HIGH
MEDIUM
LOW
"""

def classify_relevance(abstract: str) -> float:
    if not abstract or len(abstract.strip()) < 50:
        return 0.0

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": abstract}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().upper()

    if result == "HIGH":
        return 1.0
    elif result == "MEDIUM":
        return 0.5
    else:
        return 0.0
