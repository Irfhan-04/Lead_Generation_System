"""
Generate sample lead data
"""

import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scoring.propensity_scorer import PropensityScorer
import random

def generate_leads(num_leads=100):
    """Generate sample leads"""
    
    first_names = ['Sarah', 'James', 'Emily', 'Michael', 'Lisa', 'David', 'Maria', 
                   'Robert', 'Jennifer', 'Thomas', 'Jessica', 'Daniel', 'Amanda',
                   'Christopher', 'Michelle', 'Matthew', 'Susan', 'Andrew', 'Karen',
                   'Brian', 'Laura', 'Kevin', 'Nancy', 'Steven', 'Betty']
    
    last_names = ['Mitchell', 'Chen', 'Rodriguez', 'Kumar', 'Anderson', 'Park',
                  'Garcia', 'Wilson', 'Lee', 'Brown', 'Taylor', 'Martinez',
                  'Johnson', 'Smith', 'Williams', 'Davis', 'Miller', 'Jones',
                  'Moore', 'White', 'Harris', 'Martin', 'Thompson', 'Young']
    
    titles = [
        'Director of Toxicology', 'Head of Preclinical Safety',
        'Principal Scientist - Toxicology', 'VP Safety Assessment',
        'Senior Scientist - Hepatotoxicity', 'Lead Toxicologist',
        'Director of Safety Sciences', 'Research Scientist II',
        'Associate Director - Safety', 'Safety Pharmacology Lead',
        'Senior Research Scientist', 'Staff Scientist - DMPK',
        'Group Leader - Toxicology', 'Principal Investigator',
        'Senior Director - Nonclinical Safety', 'Toxicology Manager',
        'Research Fellow', 'Scientist II - Safety Assessment'
    ]
    
    companies = [
        'Moderna Therapeutics', 'Vertex Pharmaceuticals', 'BioMarin',
        'Alnylam Pharmaceuticals', 'Ginkgo Bioworks', 'Bluebird Bio',
        'Beam Therapeutics', 'Editas Medicine', 'Intellia Therapeutics',
        'CRISPR Therapeutics', 'Biogen', 'Alexion', 'Takeda', 'Novartis',
        'Pfizer', 'Merck', 'GSK', 'AstraZeneca', 'Regeneron', 'Amgen',
        'Gilead Sciences', 'Bristol Myers Squibb', 'Eli Lilly', 'Sanofi',
        'Roche', 'Johnson & Johnson', 'AbbVie', 'Bayer', 'Novo Nordisk'
    ]
    
    locations = [
        'Cambridge, MA', 'Boston, MA', 'San Francisco, CA',
        'South San Francisco, CA', 'San Diego, CA', 'New York, NY',
        'New Jersey', 'Seattle, WA', 'Basel, Switzerland',
        'Oxford, UK', 'Cambridge, UK', 'London, UK',
        'Remote - Colorado', 'Remote - Texas', 'Chicago, IL',
        'Philadelphia, PA', 'Research Triangle Park, NC',
        'Indianapolis, IN', 'Remote - California'
    ]
    
    funding_stages = ['Seed', 'Series A', 'Series B', 'Series C', 'Public', 'IPO']
    
    pub_titles = [
        'Novel 3D hepatic models for DILI assessment',
        'Drug-induced liver injury prediction using spheroids',
        'Advanced in vitro toxicity testing methods',
        'Liver organoid applications in drug discovery',
        'NAMs for hepatotoxicity screening',
        '3D cell culture models in safety pharmacology',
        'Microphysiological systems for toxicity prediction',
        'Organ-on-chip technology in drug development',
        'High-throughput screening using 3D models',
        'Predictive toxicology with in vitro systems'
    ]
    
    leads = []
    
    for i in range(num_leads):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"Dr. {first} {last}"
        
        title = random.choice(titles)
        company = random.choice(companies)
        location = random.choice(locations)
        
        email_domain = company.lower().replace(' ', '').replace('pharmaceuticals', '')[:12]
        email = f"{first.lower()}.{last.lower()}@{email_domain}.com"
        linkedin = f"linkedin.com/in/{first.lower()}{last.lower()}"
        
        has_pub = random.random() < 0.6
        pub_year = random.randint(2022, 2024) if has_pub else None
        pub_title = random.choice(pub_titles) if has_pub else None
        
        funding = random.choice(funding_stages)
        if random.random() < 0.6:
            funding = random.choice(['Series B', 'Series C', 'Public'])
        
        uses_3d = random.random() < 0.5
        tenure = random.randint(6, 60)
        
        leads.append({
            'name': name,
            'title': title,
            'company': company,
            'location': location,
            'company_hq': location,
            'email': email,
            'linkedin': linkedin,
            'recent_publication': has_pub,
            'publication_year': pub_year,
            'publication_title': pub_title,
            'company_funding': funding,
            'uses_3d_models': uses_3d,
            'tenure_months': tenure
        })
    
    df = pd.DataFrame(leads)
    
    # Calculate scores
    scorer = PropensityScorer()
    df['propensity_score'] = df.apply(scorer.calculate_score, axis=1)
    df['rank'] = df['propensity_score'].rank(ascending=False, method='min').astype(int)
    df = df.sort_values('rank').reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    
    print(f"Generating {num} sample leads...")
    df = generate_leads(num)
    
    # Save to CSV
    output_path = 'data/sample/sample_leads.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} leads")
    print(f"   Saved to: {output_path}")
    print(f"\n   Score distribution:")
    print(f"   - High (70+): {len(df[df['propensity_score'] >= 70])}")
    print(f"   - Medium (50-69): {len(df[(df['propensity_score'] >= 50) & (df['propensity_score'] < 70)])}")
    print(f"   - Low (<50): {len(df[df['propensity_score'] < 50])}")