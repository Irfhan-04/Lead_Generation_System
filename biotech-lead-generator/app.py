"""
Biotech Lead Generation System - Main Application
3D In-Vitro Models Lead Scoring Platform
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import sys

# Page configuration
st.set_page_config(
    page_title="Biotech Lead Generator - 3D In-Vitro Models",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from src.scoring.propensity_scorer import PropensityScorer
from src.data_sources.pubmed_scraper import PubMedScraper
from src.utils.export_helper import ExportHelper

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
    }
    .high-score {
        color: #2E7D32;
        font-weight: bold;
    }
    .medium-score {
        color: #F57C00;
        font-weight: bold;
    }
    .low-score {
        color: #C62828;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'scoring_weights' not in st.session_state:
    st.session_state.scoring_weights = {
        'role_fit': 30,
        'publication': 40,
        'funding': 20,
        'location': 10
    }

def load_sample_data():
    """Load sample data for demonstration"""
    sample_data = {
        'name': [
            'Dr. Sarah Mitchell', 'Dr. James Chen', 'Dr. Emily Rodriguez',
            'Dr. Michael Kumar', 'Dr. Lisa Anderson', 'Dr. David Park',
            'Dr. Maria Garcia', 'Dr. Robert Wilson', 'Dr. Jennifer Lee',
            'Dr. Thomas Brown'
        ],
        'title': [
            'Director of Toxicology', 'Head of Preclinical Safety', 'Principal Scientist',
            'VP Safety Assessment', 'Senior Scientist - Hepatotoxicity', 'Lead Toxicologist',
            'Director of Safety Sciences', 'Research Scientist II', 'Associate Director',
            'Safety Pharmacology Lead'
        ],
        'company': [
            'Moderna Therapeutics', 'Vertex Pharmaceuticals', 'BioMarin Pharmaceutical',
            'Alnylam Pharmaceuticals', 'Ginkgo Bioworks', 'Bluebird Bio',
            'Beam Therapeutics', 'Editas Medicine', 'Intellia Therapeutics',
            'CRISPR Therapeutics'
        ],
        'location': [
            'Cambridge, MA', 'Boston, MA', 'San Rafael, CA',
            'Cambridge, MA', 'Boston, MA', 'Cambridge, MA',
            'Cambridge, MA', 'Cambridge, MA', 'Cambridge, MA',
            'Cambridge, MA'
        ],
        'company_hq': [
            'Cambridge, MA', 'Boston, MA', 'San Rafael, CA',
            'Cambridge, MA', 'Boston, MA', 'Cambridge, MA',
            'Cambridge, MA', 'Cambridge, MA', 'Cambridge, MA',
            'Cambridge, MA'
        ],
        'email': [
            'sarah.mitchell@modernatx.com', 'james.chen@vrtx.com', 'emily.rodriguez@biomarin.com',
            'michael.kumar@alnylam.com', 'lisa.anderson@ginkgobioworks.com', 'david.park@bluebirdbio.com',
            'maria.garcia@beamtx.com', 'robert.wilson@editasmedicine.com', 'jennifer.lee@intelliatx.com',
            'thomas.brown@crisprtx.com'
        ],
        'linkedin': [
            'linkedin.com/in/sarahmitchell', 'linkedin.com/in/jameschen', 'linkedin.com/in/emilyrodriguez',
            'linkedin.com/in/michaelkumar', 'linkedin.com/in/lisaanderson', 'linkedin.com/in/davidpark',
            'linkedin.com/in/mariagarcia', 'linkedin.com/in/robertwilson', 'linkedin.com/in/jenniferlee',
            'linkedin.com/in/thomasbrown'
        ],
        'recent_publication': [
            True, True, False, True, True, False, True, False, True, False
        ],
        'publication_year': [
            2024, 2024, 2021, 2023, 2024, 2020, 2023, 2022, 2024, 2021
        ],
        'publication_title': [
            'Novel 3D hepatic models for DILI assessment',
            'Drug-induced liver injury prediction using spheroids',
            'N/A',
            'Advanced in vitro toxicity testing methods',
            'Liver organoid applications in drug discovery',
            'N/A',
            'NAMs for hepatotoxicity screening',
            'N/A',
            '3D cell culture models in safety pharmacology',
            'N/A'
        ],
        'company_funding': [
            'Public', 'Public', 'Public', 'Public', 'Series C',
            'Public', 'Series B', 'Public', 'Series C', 'Public'
        ],
        'uses_3d_models': [
            True, True, False, True, True, False, True, False, True, False
        ],
        'tenure_months': [
            24, 18, 36, 12, 30, 48, 15, 24, 20, 28
        ]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Calculate scores
    scorer = PropensityScorer(st.session_state.scoring_weights)
    df['propensity_score'] = df.apply(scorer.calculate_score, axis=1)
    df['rank'] = df['propensity_score'].rank(ascending=False, method='min').astype(int)
    
    # Sort by rank
    df = df.sort_values('rank').reset_index(drop=True)
    
    return df

def main():
    # Header
    st.markdown('<div class="main-header">🧬 Biotech Lead Generation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">3D In-Vitro Models - Lead Scoring & Prioritization Platform</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data Source Selection
        st.subheader("Data Sources")
        data_source = st.radio(
            "Select Data Source:",
            ["Sample Data (Demo)", "Upload CSV", "PubMed Search", "Full Pipeline"]
        )
        
        st.divider()
        
        # Scoring Weights Configuration
        st.subheader("📊 Scoring Weights")
        st.caption("Adjust weights for propensity scoring (Total = 100)")
        
        role_weight = st.slider("Role Fit", 0, 50, st.session_state.scoring_weights['role_fit'])
        pub_weight = st.slider("Recent Publication", 0, 50, st.session_state.scoring_weights['publication'])
        fund_weight = st.slider("Company Funding", 0, 30, st.session_state.scoring_weights['funding'])
        loc_weight = st.slider("Strategic Location", 0, 20, st.session_state.scoring_weights['location'])
        
        total_weight = role_weight + pub_weight + fund_weight + loc_weight
        
        if total_weight != 100:
            st.warning(f"⚠️ Total weight: {total_weight}/100")
        else:
            st.success(f"✅ Total weight: {total_weight}/100")
        
        if st.button("Apply Weights", type="primary"):
            st.session_state.scoring_weights = {
                'role_fit': role_weight,
                'publication': pub_weight,
                'funding': fund_weight,
                'location': loc_weight
            }
            if st.session_state.leads_df is not None:
                # Recalculate scores
                scorer = PropensityScorer(st.session_state.scoring_weights)
                st.session_state.leads_df['propensity_score'] = st.session_state.leads_df.apply(
                    scorer.calculate_score, axis=1
                )
                st.session_state.leads_df['rank'] = st.session_state.leads_df['propensity_score'].rank(
                    ascending=False, method='min'
                ).astype(int)
                st.session_state.leads_df = st.session_state.leads_df.sort_values('rank').reset_index(drop=True)
                st.success("Scores recalculated!")
                st.rerun()
        
        st.divider()
        
        # Export Options
        st.subheader("📥 Export")
        if st.session_state.leads_df is not None:
            export_helper = ExportHelper()
            
            col1, col2 = st.columns(2)
            with col1:
                csv_data = export_helper.to_csv(st.session_state.filtered_df or st.session_state.leads_df)
                st.download_button(
                    label="📄 CSV",
                    data=csv_data,
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            with col2:
                excel_data = export_helper.to_excel(st.session_state.filtered_df or st.session_state.leads_df)
                st.download_button(
                    label="📊 Excel",
                    data=excel_data,
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    # Main Content
    tabs = st.tabs(["📊 Dashboard", "🔍 Search & Filter", "➕ Add New Leads", "⚙️ Settings"])
    
    # Tab 1: Dashboard
    with tabs[0]:
        # Load Data
        if data_source == "Sample Data (Demo)":
            if st.button("Load Sample Data", type="primary"):
                with st.spinner("Loading sample data..."):
                    st.session_state.leads_df = load_sample_data()
                    st.success("Sample data loaded successfully!")
                    st.rerun()
        
        elif data_source == "Upload CSV":
            uploaded_file = st.file_uploader("Upload your leads CSV", type=['csv'])
            if uploaded_file:
                st.session_state.leads_df = pd.read_csv(uploaded_file)
                scorer = PropensityScorer(st.session_state.scoring_weights)
                st.session_state.leads_df['propensity_score'] = st.session_state.leads_df.apply(
                    scorer.calculate_score, axis=1
                )
                st.session_state.leads_df['rank'] = st.session_state.leads_df['propensity_score'].rank(
                    ascending=False, method='min'
                ).astype(int)
                st.success("File uploaded and processed!")
        
        elif data_source == "PubMed Search":
            st.subheader("🔬 PubMed Lead Discovery")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                query = st.text_input(
                    "Search Query",
                    value="drug-induced liver injury 3D models",
                    help="Enter PubMed search terms"
                )
            with col2:
                max_results = st.number_input("Max Results", 5, 100, 20)
            
            if st.button("Search PubMed", type="primary"):
                with st.spinner("Searching PubMed..."):
                    scraper = PubMedScraper()
                    results = scraper.search_authors(query, max_results=max_results)
                    
                    if results:
                        st.success(f"Found {len(results)} potential leads from PubMed!")
                        st.session_state.leads_df = pd.DataFrame(results)
                        
                        # Calculate scores
                        scorer = PropensityScorer(st.session_state.scoring_weights)
                        st.session_state.leads_df['propensity_score'] = st.session_state.leads_df.apply(
                            scorer.calculate_score, axis=1
                        )
                        st.session_state.leads_df['rank'] = st.session_state.leads_df['propensity_score'].rank(
                            ascending=False, method='min'
                        ).astype(int)
                        st.rerun()
                    else:
                        st.error("No results found. Try a different query.")
        
        # Display Dashboard
        if st.session_state.leads_df is not None:
            df = st.session_state.leads_df
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Leads",
                    value=len(df),
                    delta=f"{len(df[df['propensity_score'] >= 70])} high-priority"
                )
            
            with col2:
                avg_score = df['propensity_score'].mean()
                st.metric(
                    label="Avg Score",
                    value=f"{avg_score:.1f}",
                    delta=f"{(avg_score - 50):.1f} vs baseline"
                )
            
            with col3:
                recent_pubs = df['recent_publication'].sum()
                st.metric(
                    label="Recent Publications",
                    value=recent_pubs,
                    delta=f"{(recent_pubs/len(df)*100):.0f}% of leads"
                )
            
            with col4:
                funded = len(df[df['company_funding'].isin(['Series A', 'Series B', 'Series C'])])
                st.metric(
                    label="Well-Funded Companies",
                    value=funded,
                    delta=f"{(funded/len(df)*100):.0f}% of leads"
                )
            
            st.divider()
            
            # Lead Table
            st.subheader("🎯 Top Leads")
            
            # Score color formatting
            def score_color(score):
                if score >= 70:
                    return 'high-score'
                elif score >= 50:
                    return 'medium-score'
                else:
                    return 'low-score'
            
            # Display table
            display_df = df[[
                'rank', 'propensity_score', 'name', 'title', 
                'company', 'location', 'email', 'recent_publication'
            ]].copy()
            
            display_df.columns = [
                'Rank', 'Score', 'Name', 'Title', 
                'Company', 'Location', 'Email', 'Recent Pub'
            ]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # Score Distribution
            st.subheader("📈 Score Distribution")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                import plotly.express as px
                fig = px.histogram(
                    df,
                    x='propensity_score',
                    nbins=20,
                    title="Lead Score Distribution",
                    labels={'propensity_score': 'Propensity Score', 'count': 'Number of Leads'}
                )
                fig.add_vline(x=70, line_dash="dash", line_color="green", annotation_text="High Priority")
                fig.add_vline(x=50, line_dash="dash", line_color="orange", annotation_text="Medium Priority")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Score Breakdown:**")
                high = len(df[df['propensity_score'] >= 70])
                medium = len(df[(df['propensity_score'] >= 50) & (df['propensity_score'] < 70)])
                low = len(df[df['propensity_score'] < 50])
                
                st.markdown(f"🟢 **High (70+):** {high} leads ({high/len(df)*100:.1f}%)")
                st.markdown(f"🟡 **Medium (50-69):** {medium} leads ({medium/len(df)*100:.1f}%)")
                st.markdown(f"🔴 **Low (<50):** {low} leads ({low/len(df)*100:.1f}%)")
        
        else:
            st.info("👆 Please load data using the sidebar options to get started!")
    
    # Tab 2: Search & Filter
    with tabs[1]:
        if st.session_state.leads_df is not None:
            st.subheader("🔍 Advanced Search & Filtering")
            
            df = st.session_state.leads_df.copy()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔎 Search (Name, Title, Company)", "")
            
            with col2:
                min_score = st.slider("Minimum Score", 0, 100, 0)
            
            with col3:
                location_filter = st.multiselect(
                    "Location",
                    options=df['location'].unique().tolist(),
                    default=[]
                )
            
            # Apply filters
            filtered_df = df.copy()
            
            if search_term:
                mask = (
                    filtered_df['name'].str.contains(search_term, case=False, na=False) |
                    filtered_df['title'].str.contains(search_term, case=False, na=False) |
                    filtered_df['company'].str.contains(search_term, case=False, na=False)
                )
                filtered_df = filtered_df[mask]
            
            if min_score > 0:
                filtered_df = filtered_df[filtered_df['propensity_score'] >= min_score]
            
            if location_filter:
                filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
            
            st.session_state.filtered_df = filtered_df
            
            # Display results
            st.write(f"**Found {len(filtered_df)} leads matching your criteria**")
            
            if len(filtered_df) > 0:
                st.dataframe(
                    filtered_df[[
                        'rank', 'propensity_score', 'name', 'title', 
                        'company', 'location', 'email'
                    ]],
                    use_container_width=True,
                    height=500,
                    hide_index=True
                )
            else:
                st.warning("No leads match your search criteria.")
        else:
            st.info("Load data first in the Dashboard tab.")
    
    # Tab 3: Add New Leads
    with tabs[2]:
        st.subheader("➕ Manually Add New Lead")
        
        with st.form("add_lead_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Full Name*")
                new_title = st.text_input("Job Title*")
                new_company = st.text_input("Company*")
                new_location = st.text_input("Location*")
            
            with col2:
                new_email = st.text_input("Email")
                new_linkedin = st.text_input("LinkedIn URL")
                new_publication = st.checkbox("Recent Publication (2023+)")
                new_funding = st.selectbox("Funding Stage", 
                    ["Unknown", "Seed", "Series A", "Series B", "Series C", "Public"])
            
            submitted = st.form_submit_button("Add Lead", type="primary")
            
            if submitted:
                if new_name and new_title and new_company and new_location:
                    new_lead = {
                        'name': new_name,
                        'title': new_title,
                        'company': new_company,
                        'location': new_location,
                        'company_hq': new_location,
                        'email': new_email or 'N/A',
                        'linkedin': new_linkedin or 'N/A',
                        'recent_publication': new_publication,
                        'publication_year': 2024 if new_publication else None,
                        'publication_title': 'Manual Entry',
                        'company_funding': new_funding,
                        'uses_3d_models': False,
                        'tenure_months': 12
                    }
                    
                    if st.session_state.leads_df is not None:
                        new_df = pd.DataFrame([new_lead])
                        st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_df], ignore_index=True)
                        
                        # Recalculate scores
                        scorer = PropensityScorer(st.session_state.scoring_weights)
                        st.session_state.leads_df['propensity_score'] = st.session_state.leads_df.apply(
                            scorer.calculate_score, axis=1
                        )
                        st.session_state.leads_df['rank'] = st.session_state.leads_df['propensity_score'].rank(
                            ascending=False, method='min'
                        ).astype(int)
                        
                        st.success(f"✅ Added {new_name} to leads database!")
                        st.rerun()
                    else:
                        st.warning("Please load data first in Dashboard tab.")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Tab 4: Settings
    with tabs[3]:
        st.subheader("⚙️ System Settings")
        
        st.write("**Scoring Algorithm Configuration**")
        
        with st.expander("View Current Weights"):
            st.json(st.session_state.scoring_weights)
        
        with st.expander("Data Source Configuration"):
            st.write("Configure API keys and data sources")
            pubmed_email = st.text_input("PubMed Email (Optional)", type="password")
            hunter_key = st.text_input("Hunter.io API Key (Optional)", type="password")
            
            if st.button("Save API Keys"):
                st.success("API keys saved to session!")
        
        with st.expander("Export Settings"):
            st.checkbox("Include LinkedIn URLs in exports", value=True)
            st.checkbox("Include publication details", value=True)
            st.checkbox("Include scoring breakdown", value=False)
        
        st.divider()
        
        st.write("**Database Management**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Data", type="secondary"):
                st.session_state.leads_df = None
                st.session_state.filtered_df = None
                st.success("Data cleared!")
                st.rerun()
        
        with col2:
            if st.button("Reset Weights to Default"):
                st.session_state.scoring_weights = {
                    'role_fit': 30,
                    'publication': 40,
                    'funding': 20,
                    'location': 10
                }
                st.success("Weights reset!")
                st.rerun()

if __name__ == "__main__":
    main()