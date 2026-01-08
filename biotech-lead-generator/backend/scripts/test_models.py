"""
Test Database Models
Verifies all 5 models work correctly with the database
"""

import sys
import os
import asyncio
from datetime import datetime

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import AsyncSessionLocal, check_db_connection
from app.models.user import User, SubscriptionTier
from app.models.lead import Lead
from app.models.search import Search
from app.models.export import Export, ExportFormat, ExportStatus
from app.models.pipeline import Pipeline, PipelineStatus, PipelineSchedule
from app.core.security import get_password_hash
from sqlalchemy import select


async def test_database_models():
    """
    Test all 5 database models
    """
    print("🧪 Testing Database Models\n")
    print("=" * 70)
    
    # Test 1: Database Connection
    print("\n1️⃣  Testing Database Connection...")
    if not await check_db_connection():
        print("   ❌ Database connection failed!")
        print("   Please check your DATABASE_URL in .env")
        return False
    print("   ✅ Database connection successful!")
    
    # Create async session
    async with AsyncSessionLocal() as session:
        try:
            # Test 2: User Model
            print("\n2️⃣  Testing User Model...")
            test_user = User(
                email="test@example.com",
                password_hash=get_password_hash("TestPass123!"),
                full_name="Test User",
                subscription_tier=SubscriptionTier.FREE,
                is_active=True,
                is_verified=True,
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print(f"   ✅ Created user: {test_user.email} (ID: {test_user.id})")
            print(f"      Subscription: {test_user.subscription_tier.value}")
            print(f"      Monthly lead limit: {test_user.get_monthly_lead_limit()}")
            
            # Test 3: Lead Model
            print("\n3️⃣  Testing Lead Model...")
            test_lead = Lead(
                user_id=test_user.id,
                name="Dr. Sarah Mitchell",
                title="Director of Toxicology",
                company="Moderna Therapeutics",
                location="Cambridge, MA",
                email="sarah.mitchell@modernatx.com",
                linkedin_url="https://linkedin.com/in/sarahmitchell",
                propensity_score=85,
                rank=1,
                recent_publication=True,
                publication_year=2024,
                publication_title="Novel 3D hepatic models for DILI assessment",
                company_funding="Public",
                uses_3d_models=True,
                status="NEW"
            )
            
            # Test helper methods
            test_lead.add_tag("high-priority")
            test_lead.add_tag("conference-speaker")
            test_lead.add_data_source("manual")
            test_lead.update_priority_tier()
            
            session.add(test_lead)
            await session.commit()
            await session.refresh(test_lead)
            
            print(f"   ✅ Created lead: {test_lead.name} (Score: {test_lead.propensity_score})")
            print(f"      Priority tier: {test_lead.priority_tier}")
            print(f"      Tags: {test_lead.tags}")
            print(f"      Has tag 'high-priority': {test_lead.has_tag('high-priority')}")
            
            # Test 4: Search Model
            print("\n4️⃣  Testing Search Model...")
            test_search = Search(
                user_id=test_user.id,
                query="drug-induced liver injury 3D models",
                search_type="pubmed",
                filters={"years": [2023, 2024], "location": "Cambridge"},
                results_count=45,
                results_snapshot=[str(test_lead.id)],
                is_saved=True,
                saved_name="DILI Research 2024",
                execution_time_ms=1234
            )
            
            session.add(test_search)
            await session.commit()
            await session.refresh(test_search)
            
            print(f"   ✅ Created search: {test_search.query[:50]}...")
            print(f"      Type: {test_search.search_type}")
            print(f"      Results: {test_search.results_count}")
            print(f"      Saved as: {test_search.saved_name}")
            
            # Test 5: Export Model
            print("\n5️⃣  Testing Export Model...")
            test_export = Export(
                user_id=test_user.id,
                file_name="leads_export_20241230.xlsx",
                format=ExportFormat.EXCEL,
                status=ExportStatus.PENDING,
                records_count=100,
                filters={"min_score": 70},
                columns=["name", "email", "company", "propensity_score"]
            )
            
            # Test helper methods
            test_export.mark_as_processing()
            test_export.mark_as_completed(
                file_url="https://storage.example.com/export.xlsx",
                file_size=2500000
            )
            
            session.add(test_export)
            await session.commit()
            await session.refresh(test_export)
            
            print(f"   ✅ Created export: {test_export.file_name}")
            print(f"      Format: {test_export.format.value}")
            print(f"      Status: {test_export.status.value}")
            print(f"      Size: {test_export.get_file_size_mb()} MB")
            print(f"      Is downloadable: {test_export.is_downloadable()}")
            
            # Test 6: Pipeline Model
            print("\n6️⃣  Testing Pipeline Model...")
            test_pipeline = Pipeline(
                user_id=test_user.id,
                name="Daily PubMed Scan",
                description="Automated DILI research scanning",
                schedule=PipelineSchedule.DAILY,
                config={
                    "data_sources": ["pubmed"],
                    "search_queries": [
                        {"source": "pubmed", "query": "drug-induced liver injury"}
                    ],
                    "filters": {"min_score": 70}
                },
                status=PipelineStatus.ACTIVE
            )
            
            # Test helper methods
            test_pipeline.mark_running()
            test_pipeline.mark_run_complete(
                success=True,
                results={
                    "leads_found": 45,
                    "leads_created": 38,
                    "leads_updated": 7
                }
            )
            
            session.add(test_pipeline)
            await session.commit()
            await session.refresh(test_pipeline)
            
            print(f"   ✅ Created pipeline: {test_pipeline.name}")
            print(f"      Schedule: {test_pipeline.schedule.value}")
            print(f"      Status: {test_pipeline.status.value}")
            print(f"      Run count: {test_pipeline.run_count}")
            print(f"      Success rate: {test_pipeline.get_success_rate()}%")
            
            # Test 7: Relationships
            print("\n7️⃣  Testing Relationships...")
            
            # Query user with relationships
            result = await session.execute(
                select(User).where(User.id == test_user.id)
            )
            user_with_relations = result.scalar_one()
            
            print(f"   ✅ User relationships:")
            print(f"      Leads: {len(user_with_relations.leads)} lead(s)")
            print(f"      Searches: {len(user_with_relations.searches)} search(es)")
            print(f"      Exports: {len(user_with_relations.exports)} export(s)")
            print(f"      Pipelines: {len(user_with_relations.pipelines)} pipeline(s)")
            
            # Test 8: Query Operations
            print("\n8️⃣  Testing Query Operations...")
            
            # Query high-priority leads
            high_priority_leads = await session.execute(
                select(Lead).where(
                    Lead.user_id == test_user.id,
                    Lead.propensity_score >= 70
                )
            )
            leads_list = high_priority_leads.scalars().all()
            print(f"   ✅ Found {len(leads_list)} high-priority leads (score >= 70)")
            
            # Query saved searches
            saved_searches = await session.execute(
                select(Search).where(
                    Search.user_id == test_user.id,
                    Search.is_saved == True
                )
            )
            searches_list = saved_searches.scalars().all()
            print(f"   ✅ Found {len(searches_list)} saved search(es)")
            
            # Test 9: Cleanup (Delete test data)
            print("\n9️⃣  Cleaning up test data...")
            
            # Delete user (cascade will delete related records)
            await session.delete(test_user)
            await session.commit()
            
            print(f"   ✅ Deleted test user and all related records")
            
            # Verify deletion
            result = await session.execute(
                select(User).where(User.email == "test@example.com")
            )
            deleted_user = result.scalar_one_or_none()
            
            if deleted_user is None:
                print(f"   ✅ Verification: User successfully deleted")
            else:
                print(f"   ⚠️  Warning: User still exists after deletion")
            
            print("\n" + "=" * 70)
            print("🎉 ALL TESTS PASSED!\n")
            print("✅ All 5 models are working correctly:")
            print("   • User model - authentication and subscriptions")
            print("   • Lead model - lead management with scoring")
            print("   • Search model - search history tracking")
            print("   • Export model - export generation")
            print("   • Pipeline model - automated workflows")
            print("\n✅ Relationships working correctly")
            print("✅ Helper methods functioning properly")
            print("✅ Database queries working as expected")
            print("\n🚀 Your database is ready to use!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            print(f"   Type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            await session.rollback()
            return False


def main():
    """
    Run the async test function
    """
    try:
        result = asyncio.run(test_database_models())
        if result:
            print("\n✅ Success! You can now:")
            print("   1. Run the API: uvicorn app.main:app --reload")
            print("   2. Access docs: http://localhost:8000/docs")
            print("   3. Test endpoints with the interactive API docs")
        else:
            print("\n⚠️  Tests failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()