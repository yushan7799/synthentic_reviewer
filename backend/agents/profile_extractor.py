"""
Profile Extractor - Improved Version

Key Improvements:
1. Structured data extraction first (JSON-LD, OpenGraph)
2. Clean text before keyword/AI extraction
3. Centralized session with retries
4. Hybrid rendering only when needed
5. Reduced site-specific logic
6. AI-driven structured extraction
7. Optional caching support
8. Better error handling

Extraction Pipeline:
1. JSON-LD (Person, ProfilePage)
2. OpenGraph / meta description
3. Cleaned main text (readability-style)
4. AI normalization
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from config import Config
import re
import json
import time


class ProfileExtractor:
    """
    Extract professional profile information from URLs
    Optimized for speed, accuracy, and maintainability
    """
    
    def __init__(self):
        # Centralized session with retries and connection pooling
        self.session = self._create_session()
        self.timeout = Config.SCRAPING_TIMEOUT
        
        # Cache for repeated URLs (optional)
        self._cache = {}
    
    def _create_session(self) -> requests.Session:
        """Create a session with retry logic and connection pooling"""
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({'User-Agent': Config.USER_AGENT})
        
        return session
    
    def extract_profile(self, url: str, use_cache: bool = True) -> Dict[str, any]:
        """
        Extract profile information from a URL
        
        Args:
            url: URL to extract profile from
            use_cache: Whether to use cached results
            
        Returns:
            Dictionary containing extracted profile information
        """
        # Check cache
        if use_cache and url in self._cache:
            return self._cache[url]
        
        try:
            # Fetch HTML
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Determine extraction strategy
            if 'scholar.google' in url:
                profile = self._extract_google_scholar(soup, url)
            elif 'linkedin.com' in url:
                profile = self._extract_linkedin(soup, url)
            else:
                profile = self._extract_generic(soup, url)
            
            # Cache result
            if use_cache:
                self._cache[url] = profile
            
            return profile
            
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_generic(self, soup: BeautifulSoup, url: str) -> Dict[str, any]:
        """
        Extract from generic website using structured data first
        
        Pipeline:
        1. JSON-LD structured data
        2. OpenGraph metadata
        3. Cleaned HTML text
        4. Keyword extraction
        """
        profile = {
            'name': '',
            'bio': '',
            'expertise_areas': [],
            'publications': [],
            'affiliations': [],
            'source': 'website',
            'url': url
        }
        
        # Step 1: Try JSON-LD structured data (FASTEST & MOST RELIABLE)
        structured_data = self._extract_json_ld(soup)
        if structured_data:
            profile.update(structured_data)
            if profile['name']:  # If we got good data, we're mostly done
                return profile
        
        # Step 2: Try OpenGraph metadata
        og_data = self._extract_opengraph(soup)
        if og_data:
            if not profile['name']:
                profile['name'] = og_data.get('name', '')
            if not profile['bio']:
                profile['bio'] = og_data.get('bio', '')
        
        # Step 3: Clean text extraction
        clean_text = self._clean_visible_text(soup)
        
        # Step 4: Extract from cleaned text if still missing data
        if not profile['name']:
            profile['name'] = self._extract_name_from_text(soup, clean_text)
        
        if not profile['bio']:
            profile['bio'] = self._extract_bio_from_text(soup, clean_text)
        
        # Step 5: Extract expertise from clean text (not raw HTML)
        profile['expertise_areas'] = self._extract_expertise_from_clean_text(clean_text)
        
        # Step 6: Extract publications
        profile['publications'] = self._extract_publications(soup)
        
        return profile
    
    def _extract_json_ld(self, soup: BeautifulSoup) -> Optional[Dict[str, any]]:
        """Extract structured data from JSON-LD"""
        try:
            # Find all JSON-LD scripts
            scripts = soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle array of objects
                    if isinstance(data, list):
                        data = data[0] if data else {}
                    
                    # Look for Person or ProfilePage schema
                    if data.get('@type') in ['Person', 'ProfilePage']:
                        return {
                            'name': data.get('name', ''),
                            'bio': data.get('description', ''),
                            'affiliations': [data.get('affiliation', '')] if data.get('affiliation') else [],
                            'expertise_areas': data.get('knowsAbout', []) if isinstance(data.get('knowsAbout'), list) else []
                        }
                except json.JSONDecodeError:
                    continue
            
            return None
        except Exception:
            return None
    
    def _extract_opengraph(self, soup: BeautifulSoup) -> Optional[Dict[str, any]]:
        """Extract OpenGraph metadata"""
        try:
            og_data = {}
            
            # Get title
            title_tag = soup.find('meta', property='og:title')
            if title_tag:
                og_data['name'] = title_tag.get('content', '')
            
            # Get description
            desc_tag = soup.find('meta', property='og:description') or \
                       soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                og_data['bio'] = desc_tag.get('content', '')
            
            return og_data if og_data else None
        except Exception:
            return None
    
    def _clean_visible_text(self, soup: BeautifulSoup) -> str:
        """
        Extract clean, visible text by removing noise
        
        Removes:
        - Scripts, styles
        - Navigation, headers, footers
        - Cookie banners, ads
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                            'aside', 'iframe', 'noscript']):
            element.decompose()
        
        # Remove common noise classes
        noise_classes = ['cookie', 'banner', 'ad', 'advertisement', 'popup', 
                        'modal', 'sidebar', 'menu', 'navigation']
        for noise_class in noise_classes:
            for element in soup.find_all(class_=re.compile(noise_class, re.I)):
                element.decompose()
        
        # Get clean text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _extract_name_from_text(self, soup: BeautifulSoup, clean_text: str) -> str:
        """Extract name from HTML structure"""
        # Try h1 first
        h1 = soup.find('h1')
        if h1:
            name = h1.get_text(strip=True)
            if len(name) < 50:  # Reasonable name length
                return name
        
        # Try title tag
        title = soup.find('title')
        if title:
            title_text = title.get_text(strip=True)
            # Remove common suffixes
            name = re.sub(r'\s*[-|]\s*.*$', '', title_text)
            if len(name) < 50:
                return name
        
        return 'Unknown'
    
    def _extract_bio_from_text(self, soup: BeautifulSoup, clean_text: str) -> str:
        """Extract bio/about section"""
        # Try common bio selectors
        bio_selectors = [
            '.bio', '.about', '#about', '.description', 
            '.profile-description', '.summary'
        ]
        
        for selector in bio_selectors:
            elem = soup.select_one(selector)
            if elem:
                bio = elem.get_text(strip=True)
                if 50 < len(bio) < 1000:  # Reasonable bio length
                    return bio
        
        # Try first substantial paragraph
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if 100 < len(text) < 1000:
                return text
        
        # Fallback: first 500 chars of clean text
        return clean_text[:500] if len(clean_text) > 100 else ''
    
    def _extract_expertise_from_clean_text(self, clean_text: str) -> List[str]:
        """
        Extract expertise keywords from CLEAN text (not raw HTML)
        
        This is much more accurate than parsing raw HTML
        """
        expertise = []
        text_lower = clean_text.lower()
        
        # Expanded research terms
        research_terms = [
            # CS/AI
            'machine learning', 'artificial intelligence', 'deep learning',
            'computer vision', 'natural language processing', 'nlp',
            'data science', 'robotics', 'computer science',
            # Sciences
            'neuroscience', 'biology', 'chemistry', 'physics',
            'mathematics', 'statistics', 'genomics', 'bioinformatics',
            # Engineering
            'engineering', 'electrical engineering', 'mechanical engineering',
            'civil engineering', 'materials science',
            # Medicine/Health
            'medicine', 'public health', 'epidemiology', 'clinical research',
            # Other
            'climate science', 'environmental science', 'energy',
            'quantum computing', 'cryptography', 'cybersecurity',
            'economics', 'finance', 'social science', 'psychology'
        ]
        
        for term in research_terms:
            if term in text_lower:
                expertise.append(term.title())
        
        return list(set(expertise))[:15]
    
    def _extract_publications(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract publication links"""
        publications = []
        
        # Find links that look like publications
        links = soup.find_all('a', href=True)
        pub_keywords = ['paper', 'publication', 'article', 'research', 'pdf', 'doi']
        
        for link in links[:30]:
            text = link.get_text(strip=True).lower()
            href = link.get('href', '')
            
            if any(keyword in text or keyword in href.lower() for keyword in pub_keywords):
                if len(text) > 10 and len(text) < 200:  # Reasonable title length
                    publications.append({
                        'title': link.get_text(strip=True),
                        'link': href
                    })
            
            if len(publications) >= 10:
                break
        
        return publications
    
    def _extract_google_scholar(self, soup: BeautifulSoup, url: str) -> Dict[str, any]:
        """Extract from Google Scholar (specialized)"""
        try:
            # Name
            name = self._extract_text(soup, ['#gsc_prf_in'])
            
            # Affiliation
            affiliation = self._extract_text(soup, ['.gsc_prf_il'])
            
            # Research interests (structured data!)
            interests = []
            interests_div = soup.find('div', {'id': 'gsc_prf_int'})
            if interests_div:
                interest_links = interests_div.find_all('a')
                interests = [link.get_text(strip=True) for link in interest_links]
            
            # Publications
            publications = []
            pub_rows = soup.find_all('tr', {'class': 'gsc_a_tr'})
            for row in pub_rows[:10]:
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
                'source': 'google_scholar',
                'url': url
            }
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_linkedin(self, soup: BeautifulSoup, url: str) -> Dict[str, any]:
        """
        Extract from LinkedIn (LIMITED - requires auth for full access)
        
        Note: This only works for public profiles and is very limited.
        For production, use LinkedIn API or user-provided export.
        """
        try:
            # Clean text first
            clean_text = self._clean_visible_text(soup)
            
            # Try structured data
            structured = self._extract_json_ld(soup)
            if structured:
                structured['source'] = 'linkedin'
                structured['url'] = url
                return structured
            
            # Fallback to basic extraction
            name = self._extract_text(soup, ['h1', '.top-card-layout__title'])
            headline = self._extract_text(soup, ['.top-card-layout__headline'])
            
            # Extract expertise from clean text
            expertise = self._extract_expertise_from_clean_text(clean_text)
            
            return {
                'name': name or 'Unknown',
                'bio': headline or '',
                'expertise_areas': expertise,
                'publications': [],
                'affiliations': [headline] if headline else [],
                'source': 'linkedin',
                'url': url,
                'note': 'Limited extraction - LinkedIn requires authentication for full access'
            }
        except Exception as e:
            return self._create_error_profile(str(e))
    
    def _extract_text(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text using CSS selectors"""
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return ''
    
    def _create_error_profile(self, error: str) -> Dict[str, any]:
        """Create error profile"""
        return {
            'error': error,
            'name': 'Unknown',
            'bio': '',
            'expertise_areas': [],
            'publications': [],
            'affiliations': [],
            'source': 'error'
        }
    
    def enhance_with_ai(self, profile_data: Dict[str, any]) -> Dict[str, any]:
        """
        Enhance profile with AI-driven structured extraction
        
        This is where the heavy lifting happens for expertise extraction
        and bio enhancement.
        """
        from services.openai_service import ai_service
        
        # Skip if error profile
        if profile_data.get('error'):
            return profile_data
        
        # Create focused prompt for AI
        prompt = f"""
Analyze this professional profile and extract structured information:

Name: {profile_data.get('name')}
Bio: {profile_data.get('bio', '')[:500]}
Current Expertise: {', '.join(profile_data.get('expertise_areas', [])[:5])}
Publications: {len(profile_data.get('publications', []))} found

Extract:
1. **All expertise areas** (be comprehensive - include methods, domains, applications)
2. **Enhanced bio** (2-3 sentences, professional tone)
3. **Primary research domain** (one phrase)
4. **Career level** (PhD Student, Postdoc, Assistant Professor, Associate Professor, Full Professor, Industry Researcher, etc.)

Return as JSON:
{{
    "expertise_areas": [<comprehensive list of 5-15 areas>],
    "enhanced_bio": "<2-3 sentence professional bio>",
    "primary_domain": "<one phrase>",
    "career_level": "<level>"
}}
"""
        
        try:
            schema = {
                "expertise_areas": "list",
                "enhanced_bio": "string",
                "primary_domain": "string",
                "career_level": "string"
            }
            
            enhanced = ai_service.extract_structured_data(prompt, schema)
            
            if enhanced:
                # Merge expertise (AI + extracted)
                all_expertise = list(set(
                    profile_data.get('expertise_areas', []) + 
                    enhanced.get('expertise_areas', [])
                ))
                profile_data['expertise_areas'] = all_expertise[:15]
                
                # Use enhanced bio if better
                if enhanced.get('enhanced_bio') and len(enhanced['enhanced_bio']) > 50:
                    profile_data['bio'] = enhanced['enhanced_bio']
                
                # Add metadata
                profile_data['primary_domain'] = enhanced.get('primary_domain', '')
                profile_data['career_level'] = enhanced.get('career_level', '')
                profile_data['ai_enhanced'] = True
            
            return profile_data
            
        except Exception as e:
            # Return original profile if AI enhancement fails
            profile_data['ai_enhancement_error'] = str(e)
            return profile_data
