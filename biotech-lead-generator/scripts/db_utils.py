"""
Database Utilities
"""

def backup_database(db_path: str = "data/leads.db"):
    """Create backup of SQLite database"""
    import shutil
    from datetime import datetime
    
    backup_name = f"data/leads_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(db_path, backup_name)
    print(f"✅ Database backed up to: {backup_name}")
    return backup_name


def export_database_to_csv(db_path: str = "data/leads.db", output_path: str = "data/leads_export.csv"):
    """Export entire database to CSV"""
    import sqlite3
    import pandas as pd
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    
    df.to_csv(output_path, index=False)
    print(f"✅ Database exported to: {output_path}")
    print(f"   Total records: {len(df)}")


def clean_old_data(db_path: str = "data/leads.db", days_old: int = 90):
    """Remove leads older than X days"""
    import sqlite3
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM leads WHERE created_at < ?",
        (cutoff_date,)
    )
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ Deleted {deleted} leads older than {days_old} days")