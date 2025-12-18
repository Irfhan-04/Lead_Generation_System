"""
Additional Helper Scripts and Utilities
Collection of useful scripts for data generation, testing, and maintenance
"""

# ============================================================================
# SCRIPT 1: Generate Sample Data
# File: scripts/generate_sample_data.py
# ============================================================================

import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sample_leads(num_leads: int = 100) -> pd.DataFrame:
    """
    Generate realistic sample lead data for testing
    
    Args:
        num_leads: Number of leads to generate
        
    Returns:
        DataFrame with sample leads
    """
    
    # Sample data pools
    first_names = ['Sarah', 'James', 'Emily', 'Michael', 'Lisa', 'David', 'Maria', 
                   'Robert', 'Jennifer', 'Thomas', 'Jessica', 'Daniel', 'Amanda',
                   'Christopher', 'Michelle', 'Matthew', 'Susan', 'Andrew', 'Karen']
    
    last_names = ['Mitchell', 'Chen', 'Rodriguez', 'Kumar', 'Anderson', 'Park',
                  'Garcia', 'Wilson', 'Lee', 'Brown', 'Taylor', 'Martinez',
                  'Johnson', 'Smith', 'Williams', 'Davis', 'Miller', 'Jones']
    
    titles = [
        'Director of Toxicology',
        'Head of Preclinical Safety',
        'Principal Scientist',
        'VP Safety Assessment',
        'Senior Scientist - Hepatotoxicity',
        'Lead Toxicologist',
        'Director of Safety Sciences',
        'Research Scientist II',
        'Associate Director',
        'Safety Pharmacology Lead',
        'Senior Research Associate',
        'Staff Scientist',
        'Group Leader - DMPK',
        'Principal Investigator'
    ]
    
    companies = [
        'Moderna Therapeutics', 'Vertex Pharmaceuticals', 'BioMarin Pharmaceutical',
        'Alnylam Pharmaceuticals', 'Ginkgo Bioworks', 'Bluebird Bio',
        'Beam Therapeutics', 'Editas Medicine', 'Intellia Therapeutics',
        'CRISPR Therapeutics', 'Biogen', 'Alexion Pharmaceuticals',
        'Takeda', 'Novartis', 'Pfizer', 'Merck', 'GSK', 'AstraZeneca',
        'Regeneron', 'Amgen', 'Gilead Sciences', 'BMS', 'Eli Lilly',
        'Sanofi', 'Roche', 'J&J', 'AbbVie'
    ]
    
    locations = [
        'Cambridge, MA', 'Boston, MA', 'San Francisco, CA', 'South San Francisco, CA',
        'San Diego, CA', 'New York, NY', 'New Jersey', 'Seattle, WA',
        'Basel, Switzerland', 'Oxford, UK', 'Cambridge, UK', 'London, UK',
        'Remote - Colorado', 'Remote - Texas', 'Chicago, IL', 'Philadelphia, PA'
    ]
    
    funding_stages = ['Seed', 'Series A', 'Series B', 'Series C', 'Public', 'IPO', 'Private']
    
    publication_titles = [
        'Novel 3D hepatic models for DILI assessment',
        'Drug-induced liver injury prediction using spheroids',
        'Advanced in vitro toxicity testing methods',
        'Liver organoid applications in drug discovery',
        'NAMs for hepatotoxicity screening',
        '3D cell culture models in safety pharmacology',
        'Microphysiological systems for toxicity prediction',
        'Organ-on-chip technology in drug development',
        'High-throughput screening using 3D models',
        'Predictive toxicology with advanced in vitro systems'
    ]
    
    leads = []
    
    for i in range(num_leads):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"Dr. {first_name} {last_name}"
        
        title = random.choice(titles)
        company = random.choice(companies)
        location = random.choice(locations)
        
        # Generate email
        email_domain = company.lower().replace(' ', '').replace('pharmaceuticals', 'pharma')[:15]
        email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}.com"
        
        # Generate LinkedIn
        linkedin = f"linkedin.com/in/{first_name.lower()}{last_name.lower()}"
        
        # Random publication status (60% have recent publications)
        has_publication = random.random() < 0.6
        pub_year = random.randint(2022, 2024) if has_publication else None
        pub_title = random.choice(publication_titles) if has_publication else None
        
        # Funding stage (70% are Series B+ or Public)
        funding = random.choice(funding_stages)
        if random.random() < 0.7:
            funding = random.choice(['Series B', 'Series C', 'Public'])
        
        # Uses 3D models (50% probability)
        uses_3d = random.random() < 0.5
        
        # Tenure (6-60 months)
        tenure = random.randint(6, 60)
        
        lead = {
            'name': name,
            'title': title,
            'company': company,
            'location': location,
            'company_hq': location,
            'email': email,
            'linkedin': linkedin,
            'recent_publication': has_publication,
            'publication_year': pub_year,
            'publication_title': pub_title,
            'company_funding': funding,
            'uses_3d_models': uses_3d,
            'tenure_months': tenure
        }
        
        leads.append(lead)
    
    df = pd.DataFrame(leads)
    
    # Calculate scores
    from src.scoring.propensity_scorer import PropensityScorer
    scorer = PropensityScorer()
    df['propensity_score'] = df.apply(scorer.calculate_score, axis=1)
    df['rank'] = df['propensity_score'].rank(ascending=False, method='min').astype(int)
    
    # Sort by rank
    df = df.sort_values('rank').reset_index(drop=True)
    
    return df


# ============================================================================
# SCRIPT 2: Data Validation
# File: src/utils/data_validator.py
# ============================================================================

def validate_lead_data(lead: dict) -> tuple[bool, list]:
    """
    Validate lead data completeness and format
    
    Args:
        lead: Dictionary with lead information
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    required_fields = ['name', 'title', 'company', 'location']
    for field in required_fields:
        if field not in lead or not lead[field]:
            errors.append(f"Missing required field: {field}")
    
    # Email format validation
    if 'email' in lead and lead['email'] and lead['email'] != 'N/A':
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, lead['email']):
            errors.append(f"Invalid email format: {lead['email']}")
    
    # LinkedIn URL validation
    if 'linkedin' in lead and lead['linkedin'] and lead['linkedin'] != 'N/A':
        if not lead['linkedin'].startswith(('linkedin.com', 'www.linkedin.com', 'https://linkedin.com')):
            errors.append(f"Invalid LinkedIn URL: {lead['linkedin']}")
    
    # Year validation
    if 'publication_year' in lead and lead['publication_year']:
        current_year = datetime.now().year
        if lead['publication_year'] > current_year or lead['publication_year'] < 1950:
            errors.append(f"Invalid publication year: {lead['publication_year']}")
    
    return len(errors) == 0, errors


def validate_dataframe(df: pd.DataFrame) -> dict:
    """
    Validate entire DataFrame
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'total_rows': len(df),
        'valid_rows': 0,
        'invalid_rows': 0,
        'errors': []
    }
    
    for idx, row in df.iterrows():
        is_valid, errors = validate_lead_data(row.to_dict())
        
        if is_valid:
            results['valid_rows'] += 1
        else:
            results['invalid_rows'] += 1
            results['errors'].append({
                'row': idx,
                'name': row.get('name', 'Unknown'),
                'errors': errors
            })
    
    return results


# ============================================================================
# SCRIPT 3: Quick Test Runner
# File: scripts/test_system.py
# ============================================================================

def test_scoring_algorithm():
    """Test the scoring algorithm with sample data"""
    print("=" * 60)
    print("Testing Scoring Algorithm")
    print("=" * 60)
    
    from src.scoring.propensity_scorer import PropensityScorer
    import pandas as pd
    
    # Test cases
    test_cases = [
        {
            'name': 'Perfect Lead',
            'title': 'Director of Toxicology',
            'company': 'Moderna',
            'location': 'Cambridge, MA',
            'recent_publication': True,
            'publication_year': 2024,
            'publication_title': 'DILI assessment with 3D models',
            'company_funding': 'Series B',
            'uses_3d_models': True,
            'expected_score': 95
        },
        {
            'name': 'Medium Lead',
            'title': 'Research Scientist',
            'company': 'Startup Inc',
            'location': 'Boston, MA',
            'recent_publication': False,
            'publication_year': None,
            'publication_title': None,
            'company_funding': 'Seed',
            'uses_3d_models': False,
            'expected_score': 40
        }
    ]
    
    scorer = PropensityScorer()
    
    for i, test_case in enumerate(test_cases, 1):
        expected = test_case.pop('expected_score')
        lead = pd.Series(test_case)
        
        score = scorer.calculate_score(lead)
        breakdown = scorer.get_score_breakdown(lead)
        
        print(f"\nTest Case {i}: {test_case['name']}")
        print(f"  Score: {score}/100 (expected ~{expected})")
        print(f"  Breakdown: {breakdown}")
        print(f"  Status: {'✅ PASS' if abs(score - expected) < 10 else '❌ FAIL'}")


def test_pubmed_integration():
    """Test PubMed API integration"""
    print("\n" + "=" * 60)
    print("Testing PubMed Integration")
    print("=" * 60)
    
    from src.data_sources.pubmed_scraper import PubMedScraper
    
    scraper = PubMedScraper(email="test@example.com")
    
    print("\nSearching PubMed for: 'liver toxicity'")
    leads = scraper.search_authors("liver toxicity", max_results=5)
    
    print(f"\nFound {len(leads)} leads")
    for lead in leads[:3]:
        print(f"\n  - {lead['name']}")
        print(f"    Company: {lead['company']}")
        print(f"    Publication: {lead['publication_title'][:60]}...")


def test_export_functionality():
    """Test data export"""
    print("\n" + "=" * 60)
    print("Testing Export Functionality")
    print("=" * 60)
    
    # Generate sample data
    df = generate_sample_leads(10)
    
    from src.utils.export_helper import ExportHelper
    exporter = ExportHelper()
    
    # Test CSV
    csv_data = exporter.to_csv(df)
    print(f"\n✅ CSV Export: {len(csv_data)} bytes")
    
    # Test Excel
    excel_data = exporter.to_excel(df)
    print(f"✅ Excel Export: {len(excel_data)} bytes")
    
    # Test summary report
    report = exporter.create_summary_report(df)
    print(f"✅ Summary Report: {len(report)} characters")
    print("\nSample Report Preview:")
    print(report[:300] + "...")


def run_all_tests():
    """Run all system tests"""
    print("\n🧪 Running System Tests\n")
    
    try:
        test_scoring_algorithm()
        test_pubmed_integration()
        test_export_functionality()
        
        print("\n" + "=" * 60)
        print("✅ All Tests Completed Successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# SCRIPT 4: Database Utilities
# File: scripts/db_utils.py
# ============================================================================

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


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate":
            # Generate sample data
            num = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            df = generate_sample_leads(num)
            df.to_csv("data/sample/sample_leads.csv", index=False)
            print(f"✅ Generated {len(df)} sample leads")
            print(f"   Saved to: data/sample/sample_leads.csv")
        
        elif command == "test":
            # Run tests
            run_all_tests()
        
        elif command == "backup":
            # Backup database
            backup_database()
        
        elif command == "export":
            # Export database
            export_database_to_csv()
        
        else:
            print("Unknown command. Available commands:")
            print("  python helper_scripts.py generate [num]  - Generate sample data")
            print("  python helper_scripts.py test           - Run system tests")
            print("  python helper_scripts.py backup         - Backup database")
            print("  python helper_scripts.py export         - Export database to CSV")
    
    else:
        print("Biotech Lead Generator - Helper Scripts")
        print("=" * 60)
        print("\nUsage:")
        print("  python helper_scripts.py generate [num]  - Generate sample data")
        print("  python helper_scripts.py test           - Run system tests")
        print("  python helper_scripts.py backup         - Backup database")
        print("  python helper_scripts.py export         - Export database to CSV")