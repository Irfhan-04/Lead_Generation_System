"""
Scoring Service
Integrates Phase 1 scoring algorithm with database models
"""

from typing import Dict, Optional
from datetime import datetime
from app.models.lead import Lead
from app.core.config import settings


class ScoringService:
    """
    Service for calculating lead propensity scores
    Wraps the Phase 1 PropensityScorer logic
    """
    
    def __init__(self, custom_weights: Optional[Dict[str, int]] = None):
        """
        Initialize scoring service
        
        Args:
            custom_weights: Optional custom scoring weights
                          (defaults to user preferences or system defaults)
        """
        self.weights = custom_weights or {
            'role_fit': settings.DEFAULT_ROLE_WEIGHT,
            'publication': settings.DEFAULT_PUBLICATION_WEIGHT,
            'funding': settings.DEFAULT_FUNDING_WEIGHT,
            'location': settings.DEFAULT_LOCATION_WEIGHT,
        }
        
        # Validate weights sum to 100
        total = sum(self.weights.values())
        if total != 100:
            raise ValueError(f"Weights must sum to 100, got {total}")
    
    def calculate_score(self, lead: Lead) -> int:
        """
        Calculate propensity score for a lead
        
        Args:
            lead: Lead model instance
            
        Returns:
            Score between 0-100
        """
        score = 0
        
        # 1. Role Fit Score
        score += self._score_role_fit(lead)
        
        # 2. Publication Score
        score += self._score_publication(lead)
        
        # 3. Funding Score
        score += self._score_funding(lead)
        
        # 4. Location Score
        score += self._score_location(lead)
        
        # Ensure score is between 0-100
        return max(0, min(100, int(score)))
    
    def _score_role_fit(self, lead: Lead) -> float:
        """
        Score based on job title relevance
        """
        title = (lead.title or "").lower()
        max_score = self.weights['role_fit']
        
        if not title:
            return max_score * 0.2  # Baseline for unknown
        
        # Primary keywords (full score)
        primary_keywords = ['toxicology', 'toxicologist', 'safety', 'hepatic', 'liver']
        if any(kw in title for kw in primary_keywords):
            score = max_score
        # Tech keywords (80%)
        elif any(kw in title for kw in ['3d', 'in vitro', 'in-vitro']):
            score = max_score * 0.8
        # Other relevant keywords (60%)
        elif any(kw in title for kw in ['scientist', 'researcher', 'director', 'vp', 'head']):
            score = max_score * 0.6
        else:
            score = max_score * 0.2
        
        # Seniority bonus (20%)
        seniority_keywords = ['director', 'head', 'vp', 'chief', 'lead', 'principal']
        if any(kw in title for kw in seniority_keywords):
            score *= 1.2
        
        return min(score, max_score)
    
    def _score_publication(self, lead: Lead) -> float:
        """
        Score based on recent publications
        """
        max_score = self.weights['publication']
        
        if not lead.recent_publication:
            return max_score * 0.1  # Baseline
        
        current_year = datetime.now().year
        pub_year = lead.publication_year or 0
        
        # Recent publication (last 2 years) - full score
        if pub_year >= current_year - 2:
            # Check if highly relevant
            pub_title = (lead.publication_title or "").lower()
            if any(kw in pub_title for kw in ['dili', 'liver injury', '3d', 'organoid', 'toxicity']):
                return max_score
            else:
                return max_score * 0.8
        
        # Older publication (3-5 years) - 50%
        elif pub_year >= current_year - 5:
            return max_score * 0.5
        
        # Very old or unknown - baseline
        else:
            return max_score * 0.1
    
    def _score_funding(self, lead: Lead) -> float:
        """
        Score based on company funding
        """
        max_score = self.weights['funding']
        funding = (lead.company_funding or "").lower()
        
        if not funding or funding == "unknown":
            return max_score * 0.2
        
        # Series A/B/C (prime buying stage)
        if any(stage in funding for stage in ['series a', 'series b', 'series c']):
            return max_score
        
        # Public/IPO (established)
        elif any(stage in funding for stage in ['public', 'ipo']):
            return max_score * 0.8
        
        # Seed/Early (limited budget)
        elif 'seed' in funding or 'early' in funding:
            return max_score * 0.4
        
        else:
            return max_score * 0.2
    
    def _score_location(self, lead: Lead) -> float:
        """
        Score based on strategic location
        """
        max_score = self.weights['location']
        location = (lead.location or "").lower()
        
        if not location:
            return max_score * 0.2
        
        # Primary hubs
        primary_hubs = ['cambridge, ma', 'boston', 'bay area', 'basel']
        if any(hub in location for hub in primary_hubs):
            return max_score
        
        # Secondary hubs
        secondary_hubs = [
            'san francisco', 'south san francisco', 'san diego',
            'oxford', 'cambridge uk', 'london', 'seattle', 'new jersey'
        ]
        if any(hub in location for hub in secondary_hubs):
            return max_score * 0.6
        
        # Other locations (remote work still valuable)
        else:
            return max_score * 0.2
    
    def get_score_breakdown(self, lead: Lead) -> Dict[str, float]:
        """
        Get detailed breakdown of score components
        
        Returns:
            Dictionary with individual component scores
        """
        return {
            'role_fit': self._score_role_fit(lead),
            'publication': self._score_publication(lead),
            'funding': self._score_funding(lead),
            'location': self._score_location(lead),
            'total': self.calculate_score(lead)
        }
    
    def explain_score(self, lead: Lead) -> str:
        """
        Generate human-readable explanation of score
        
        Returns:
            Text explanation of scoring factors
        """
        breakdown = self.get_score_breakdown(lead)
        total = breakdown['total']
        tier = self._get_tier(total)
        
        explanation = f"""
Lead Score: {total}/100 ({tier} Priority)

Score Breakdown:
• Role Fit: {breakdown['role_fit']:.1f}/{self.weights['role_fit']} points
  - Job title: {lead.title or 'N/A'}
  
• Publication: {breakdown['publication']:.1f}/{self.weights['publication']} points
  - Recent publication: {lead.recent_publication}
  - Year: {lead.publication_year or 'N/A'}
  
• Funding: {breakdown['funding']:.1f}/{self.weights['funding']} points
  - Company stage: {lead.company_funding or 'Unknown'}
  
• Location: {breakdown['location']:.1f}/{self.weights['location']} points
  - Based in: {lead.location or 'N/A'}

Recommendation: {"HIGH priority outreach - strong fit!" if tier == 'HIGH' 
                 else "Medium priority - good potential" if tier == 'MEDIUM' 
                 else "Lower priority - consider for nurture campaign"}
"""
        return explanation.strip()
    
    def _get_tier(self, score: int) -> str:
        """Get priority tier from score"""
        if score >= 70:
            return 'HIGH'
        elif score >= 50:
            return 'MEDIUM'
        else:
            return 'LOW'