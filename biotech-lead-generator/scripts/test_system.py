"""
Quick Test Runner
"""

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