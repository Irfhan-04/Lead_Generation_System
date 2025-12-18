"""
Configuration Management
Handles environment variables and app settings
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class Config:
    """Application configuration"""
    
    # App settings
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    APP_NAME = "Biotech Lead Generator"
    VERSION = "1.0.0"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/leads.db")
    
    # API Keys
    PUBMED_EMAIL = os.getenv("PUBMED_EMAIL", "user@example.com")
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
    
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Scoring weights (defaults)
    DEFAULT_WEIGHTS = {
        "role_fit": 30,
        "publication": 40,
        "funding": 20,
        "location": 10
    }
    
    # Rate limiting
    PUBMED_RATE_LIMIT = 3  # requests per second
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    # Search settings
    DEFAULT_YEARS_BACK = 3
    DEFAULT_MAX_RESULTS = 50
    
    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value"""
        return getattr(cls, key, default)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return cls.APP_ENV == "production"


# ============================================================================
# DATABASE MANAGER
# ============================================================================

"""
Simple SQLite database manager for lead persistence
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """
    Manages SQLite database for lead storage
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or str(DATA_DIR / "leads.db")
        self._initialize_database()
    
    def _initialize_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Leads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT,
                company TEXT,
                location TEXT,
                company_hq TEXT,
                email TEXT,
                linkedin TEXT,
                recent_publication BOOLEAN,
                publication_year INTEGER,
                publication_title TEXT,
                company_funding TEXT,
                uses_3d_models BOOLEAN,
                tenure_months INTEGER,
                propensity_score INTEGER,
                rank INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, company)
            )
        """)
        
        # Search history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                data_source TEXT,
                results_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Export history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS export_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_format TEXT,
                records_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_lead(self, lead: Dict) -> int:
        """
        Insert a single lead into database
        
        Args:
            lead: Dictionary with lead information
            
        Returns:
            ID of inserted lead
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO leads (
                    name, title, company, location, company_hq,
                    email, linkedin, recent_publication, publication_year,
                    publication_title, company_funding, uses_3d_models,
                    tenure_months, propensity_score, rank, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead.get('name'),
                lead.get('title'),
                lead.get('company'),
                lead.get('location'),
                lead.get('company_hq'),
                lead.get('email'),
                lead.get('linkedin'),
                lead.get('recent_publication'),
                lead.get('publication_year'),
                lead.get('publication_title'),
                lead.get('company_funding'),
                lead.get('uses_3d_models'),
                lead.get('tenure_months'),
                lead.get('propensity_score'),
                lead.get('rank'),
                datetime.now()
            ))
            
            lead_id = cursor.lastrowid
            conn.commit()
            return lead_id
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            conn.close()
    
    def insert_leads_bulk(self, leads: List[Dict]) -> int:
        """
        Insert multiple leads
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Number of leads inserted
        """
        count = 0
        for lead in leads:
            try:
                self.insert_lead(lead)
                count += 1
            except Exception as e:
                print(f"Error inserting lead {lead.get('name')}: {e}")
        
        return count
    
    def get_all_leads(self) -> pd.DataFrame:
        """
        Get all leads as DataFrame
        
        Returns:
            DataFrame with all leads
        """
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT 
                id, name, title, company, location, company_hq,
                email, linkedin, recent_publication, publication_year,
                publication_title, company_funding, uses_3d_models,
                tenure_months, propensity_score, rank,
                created_at, updated_at
            FROM leads
            ORDER BY rank ASC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def search_leads(
        self,
        search_term: Optional[str] = None,
        min_score: int = 0,
        locations: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Search leads with filters
        
        Args:
            search_term: Text to search in name, title, company
            min_score: Minimum propensity score
            locations: List of locations to filter
            
        Returns:
            Filtered DataFrame
        """
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT 
                id, name, title, company, location, company_hq,
                email, linkedin, recent_publication, publication_year,
                publication_title, company_funding, uses_3d_models,
                tenure_months, propensity_score, rank
            FROM leads
            WHERE propensity_score >= ?
        """
        
        params = [min_score]
        
        if search_term:
            query += " AND (name LIKE ? OR title LIKE ? OR company LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        if locations:
            placeholders = ",".join(["?" for _ in locations])
            query += f" AND location IN ({placeholders})"
            params.extend(locations)
        
        query += " ORDER BY rank ASC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_lead_by_id(self, lead_id: int) -> Optional[Dict]:
        """
        Get a single lead by ID
        
        Args:
            lead_id: Lead ID
            
        Returns:
            Lead dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, name, title, company, location, company_hq,
                email, linkedin, recent_publication, publication_year,
                publication_title, company_funding, uses_3d_models,
                tenure_months, propensity_score, rank
            FROM leads
            WHERE id = ?
        """, (lead_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [
                'id', 'name', 'title', 'company', 'location', 'company_hq',
                'email', 'linkedin', 'recent_publication', 'publication_year',
                'publication_title', 'company_funding', 'uses_3d_models',
                'tenure_months', 'propensity_score', 'rank'
            ]
            return dict(zip(columns, row))
        
        return None
    
    def delete_lead(self, lead_id: int) -> bool:
        """
        Delete a lead
        
        Args:
            lead_id: Lead ID
            
        Returns:
            True if deleted, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with stats
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total leads
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("SELECT AVG(propensity_score) FROM leads")
        avg_score = cursor.fetchone()[0] or 0
        
        # High priority leads
        cursor.execute("SELECT COUNT(*) FROM leads WHERE propensity_score >= 70")
        high_priority = cursor.fetchone()[0]
        
        # Recent publications
        cursor.execute("SELECT COUNT(*) FROM leads WHERE recent_publication = 1")
        recent_pubs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_leads': total_leads,
            'average_score': round(avg_score, 1),
            'high_priority_count': high_priority,
            'recent_publications_count': recent_pubs
        }
    
    def log_search(self, query: str, data_source: str, results_count: int):
        """Log a search operation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO search_history (query, data_source, results_count)
            VALUES (?, ?, ?)
        """, (query, data_source, results_count))
        
        conn.commit()
        conn.close()
    
    def log_export(self, file_format: str, records_count: int):
        """Log an export operation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO export_history (file_format, records_count)
            VALUES (?, ?)
        """, (file_format, records_count))
        
        conn.commit()
        conn.close()


# Example usage
if __name__ == "__main__":
    # Test configuration
    print(f"App Environment: {Config.APP_ENV}")
    print(f"Database URL: {Config.DATABASE_URL}")
    print(f"PubMed Email: {Config.PUBMED_EMAIL}")
    
    # Test database
    db = DatabaseManager()
    
    # Insert sample lead
    sample_lead = {
        'name': 'Dr. Test User',
        'title': 'Director of Toxicology',
        'company': 'Test Biotech',
        'location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'test@testbiotech.com',
        'linkedin': 'linkedin.com/in/testuser',
        'recent_publication': True,
        'publication_year': 2024,
        'publication_title': 'Test Publication',
        'company_funding': 'Series B',
        'uses_3d_models': True,
        'tenure_months': 12,
        'propensity_score': 85,
        'rank': 1
    }
    
    lead_id = db.insert_lead(sample_lead)
    print(f"\nInserted lead with ID: {lead_id}")
    
    # Get stats
    stats = db.get_stats()
    print(f"\nDatabase Stats: {stats}")