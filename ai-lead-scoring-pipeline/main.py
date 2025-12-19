from dotenv import load_dotenv
load_dotenv()

from src.load_data import load_leads
from src.normalize import normalize_titles
from src.score_pipeline import apply_scoring
from src.export import export_to_google_sheets
import os

def main():
    df = load_leads("data/input/sample_leads.csv")
    df = normalize_titles(df)
    df = apply_scoring(df)

    df = df.sort_values("propensity_score", ascending=False)
    df.to_csv("data/output/scored_leads.csv", index=False)

    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "AI_Lead_Scoring_Output")
    sheet_url = export_to_google_sheets(df, sheet_name)

    print("Google Sheet created:")
    print(sheet_url)

if __name__ == "__main__":
    main()
