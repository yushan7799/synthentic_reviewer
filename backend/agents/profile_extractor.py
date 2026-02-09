import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from config import Config
import re
import time

class ProfileExtractor:
    """
    Extract professional profile information from URLs
    Supports LinkedIn, Google Scholar, personal websites, etc.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }
        self.timeout = Config.SCRAPING_TIMEOUT
    
    def extract_profile(self, url: str) -> Dict[str, any]:
        """
        Extract profile information from a URL
        
        Args:
            url: URL to extract profile from
            
        Returns:
            Dictionary containing extracted profile information
        """
        try:
            # Determine URL type
            if 'linkedin.com' in url:
                return self._extract_linkedin(url)
            elif 'scholar.google' in url:
                return self._extract_google_scholar(url)
            else:
                return self._extract_generic_website(url)
        except Exception as e:
            return {
                'error': str(e),
                'name': '',
                'bio': '',
                'expertise_areas': [],
                'publications': [],
                'affiliations': []
            }
    
    def _extract_linkedin(self, url: str) -> Dict[str, any]:
        """Extract profile from LinkedIn (limited due to authentication)"""
        # Note: LinkedIn requires authentication for full access
        # This is a simplified version that extracts basic public info
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract basic information
            name = self._extract_text(soup, ['h1', '.name', '.top-card-layout__title'])
            headline = self._extract_text(soup, ['.top-card-layout__headline', '.headline'])
            
            # Extract skills/expertise from visible text
            text_content = soup.get_text()
            expertise = self._extract_keywords(text_content)
            
            return {
                'name': name or 'Unknown',
                'bio': headline or '',
                'expertise_areas': expertise[:10],
                'publications': [],
                'affiliations': [headline] if headline else [],
                'source': 'linkedin'
            }
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_google_scholar(self, url: str) -> Dict[str, any]:
        """Extract profile from Google Scholar"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract name
            name = self._extract_text(soup, ['#gsc_prf_in', '.gsc_prf_in'])
            
            # Extract affiliation
            affiliation = self._extract_text(soup, ['.gsc_prf_il'])
            
            # Extract research interests
            interests_div = soup.find('div', {'id': 'gsc_prf_int'})
            interests = []
            if interests_div:
                interest_links = interests_div.find_all('a')
                interests = [link.get_text(strip=True) for link in interest_links]
            
            # Extract publications
            publications = []
            pub_rows = soup.find_all('tr', {'class': 'gsc_a_tr'})
            for row in pub_rows[:10]:  # Top 10 publications
                title_elem = row.find('a', {'class': 'gsc_a_at'})
                if title_elem:
                    publications.append({
                        'title': title_elem.get_text(strip=True),
                        'link': 'https://scholar.google.com' + title_elem.get('href', '')
                    })
            
            return {
                'name': name or 'Unknown',
                'bio': affiliation or '',
                'expertise_areas': interests,
                'publications': publications,
                'affiliations': [affiliation] if affiliation else [],
                'source': 'google_scholar'
            }
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_generic_website(self, url: str) -> Dict[str, any]:
        """Extract profile from a generic website"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title/name
            name = self._extract_text(soup, ['h1', 'title', '.name', '.author'])
            
            # Extract bio/about
            bio = self._extract_text(soup, ['.bio', '.about', '#about', 'p'])
            
            # Extract all text for keyword analysis
            text_content = soup.get_text()
            
            # Extract expertise keywords
            expertise = self._extract_keywords(text_content)
            
            # Try to find publication links
            publications = []
            links = soup.find_all('a')
            for link in links[:20]:
                text = link.get_text(strip=True).lower()
                if any(word in text for word in ['paper', 'publication', 'article', 'research']):
                    publications.append({
                        'title': link.get_text(strip=True),
                        'link': link.get('href', '')
                    })
            
            return {
                'name': name or 'Unknown',
                'bio': bio[:500] if bio else '',
                'expertise_areas': expertise[:10],
                'publications': publications[:10],
                'affiliations': [],
                'source': 'website'
            }
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_text(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text from soup using multiple selectors"""
        for selector in selectors:
            if selector.startswith('#') or selector.startswith('.'):
                elem = soup.select_one(selector)
            else:
                elem = soup.find(selector)
            
            if elem:
                return elem.get_text(strip=True)
        return ''
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential expertise keywords from text"""
        # Common academic/research keywords
        keywords = []
        
        # Look for capitalized phrases (potential research areas)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Common research terms
        research_terms = [
            'machine learning', 'artificial intelligence', 'deep learning',
            'computer vision', 'natural language processing', 'data science',
            'robotics', 'neuroscience', 'biology', 'chemistry', 'physics',
            'mathematics', 'statistics', 'engineering', 'medicine',
            'climate', 'energy', 'materials', 'quantum', 'genomics'
        ]
        
        text_lower = text.lower()
        for term in research_terms:
            if term in text_lower:
                keywords.append(term.title())
        
        # Add unique capitalized phrases
        keywords.extend(list(set(capitalized))[:5])
        
        return list(set(keywords))[:10]
    
    def _create_error_profile(self, error: str) -> Dict[str, any]:
        """Create an error profile"""
        return {
            'error': error,
            'name': 'Unknown',
            'bio': '',
            'expertise_areas': [],
            'publications': [],
            'affiliations': []
        }
    
    def enhance_with_ai(self, profile_data: Dict[str, any]) -> Dict[str, any]:
        """Enhance extracted profile with AI-generated insights"""
        from services.openai_service import ai_service
        
        # Create prompt for AI enhancement
        prompt = f"""
Based on this profile information, provide additional insights:

Name: {profile_data.get('name')}
Bio: {profile_data.get('bio')}
Expertise: {', '.join(profile_data.get('expertise_areas', []))}
Publications: {len(profile_data.get('publications', []))} found

Please:
1. Infer additional expertise areas based on the bio and publications
2. Suggest a more comprehensive bio if the current one is limited
3. Identify the primary research domain

Return as JSON:
{{
    "additional_expertise": [<list>],
    "enhanced_bio": "<string>",
    "primary_domain": "<string>"
}}
"""
        
        try:
            schema = {
                "additional_expertise": "list",
                "enhanced_bio": "string",
                "primary_domain": "string"
            }
            
            enhanced = ai_service.extract_structured_data(prompt, schema)
            
            # Merge with original profile
            if enhanced:
                profile_data['expertise_areas'].extend(
                    enhanced.get('additional_expertise', [])
                )
                profile_data['expertise_areas'] = list(set(profile_data['expertise_areas']))[:15]
                
                if enhanced.get('enhanced_bio'):
                    profile_data['bio'] = enhanced['enhanced_bio']
                
                profile_data['primary_domain'] = enhanced.get('primary_domain', '')
            
            return profile_data
        except:
            return profile_data
