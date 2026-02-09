import PyPDF2
from typing import Dict, Optional
import os

class PDFParser:
    """Parse PDF files to extract text content"""
    
    @staticmethod
    def extract_text(file_path: str) -> Dict[str, str]:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = pdf_reader.metadata
                num_pages = len(pdf_reader.pages)
                
                # Extract text from all pages
                text_parts = []
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text_parts.append(page.extract_text())
                
                full_text = '\n'.join(text_parts)
                
                # Try to extract title and abstract
                title = PDFParser._extract_title(full_text, metadata)
                abstract = PDFParser._extract_abstract(full_text)
                
                return {
                    'title': title,
                    'abstract': abstract,
                    'content': full_text,
                    'num_pages': num_pages,
                    'metadata': {
                        'author': metadata.get('/Author', '') if metadata else '',
                        'subject': metadata.get('/Subject', '') if metadata else '',
                        'creator': metadata.get('/Creator', '') if metadata else ''
                    }
                }
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def _extract_title(text: str, metadata: Optional[Dict]) -> str:
        """Extract title from PDF text or metadata"""
        # Try metadata first
        if metadata and '/Title' in metadata:
            title = metadata['/Title']
            if title and len(title) > 0:
                return title
        
        # Try to find title in first few lines
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                # Likely a title
                return line
        
        return "Untitled Proposal"
    
    @staticmethod
    def _extract_abstract(text: str) -> str:
        """Extract abstract from PDF text"""
        text_lower = text.lower()
        
        # Look for abstract section
        abstract_start = -1
        for keyword in ['abstract', 'summary']:
            idx = text_lower.find(keyword)
            if idx != -1:
                abstract_start = idx
                break
        
        if abstract_start == -1:
            # No abstract found, return first paragraph
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if len(para) > 100:
                    return para[:500]
            return text[:500]
        
        # Extract text after "abstract" keyword
        abstract_text = text[abstract_start:]
        
        # Find the end of abstract (usually before "introduction" or after 1-2 paragraphs)
        end_keywords = ['introduction', '1.', 'keywords', 'background']
        abstract_end = len(abstract_text)
        
        for keyword in end_keywords:
            idx = abstract_text.lower().find(keyword, 50)  # Skip first 50 chars
            if idx != -1 and idx < abstract_end:
                abstract_end = idx
        
        abstract = abstract_text[:abstract_end].strip()
        
        # Remove the "abstract" label
        abstract = abstract.replace('Abstract', '').replace('ABSTRACT', '').strip()
        
        return abstract[:1000]  # Limit to 1000 characters
    
    @staticmethod
    def parse_text_file(file_path: str) -> Dict[str, str]:
        """
        Parse a plain text file
        
        Args:
            file_path: Path to text file
            
        Returns:
            Dictionary with extracted text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Try to extract title (first line)
            lines = content.split('\n')
            title = lines[0].strip() if lines else "Untitled Proposal"
            
            # Try to extract abstract
            abstract = PDFParser._extract_abstract(content)
            
            return {
                'title': title,
                'abstract': abstract,
                'content': content,
                'num_pages': 1,
                'metadata': {}
            }
        except Exception as e:
            raise Exception(f"Error parsing text file: {str(e)}")
