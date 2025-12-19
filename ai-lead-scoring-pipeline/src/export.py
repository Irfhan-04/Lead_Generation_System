import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

def export_to_google_sheets(df: pd.DataFrame, sheet_name: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json", scope
    )
    client = gspread.authorize(creds)

    # ---- FIX: Serialize dicts for Google Sheets ----
    df_export = df.copy()

    for col in df_export.columns:
        if df_export[col].apply(lambda x: isinstance(x, dict)).any():
            df_export[col] = df_export[col].apply(
                lambda x: json.dumps(x, indent=2) if isinstance(x, dict) else x
            )

    # ----------------------------------------------

    try:
        sheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_name)

    worksheet = sheet.sheet1
    worksheet.clear()

    worksheet.update(
        [df_export.columns.values.tolist()] + df_export.values.tolist()
    )

    return sheet.url
