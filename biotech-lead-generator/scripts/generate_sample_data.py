"""
Generate Sample Data
"""

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