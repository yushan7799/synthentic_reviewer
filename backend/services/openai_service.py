import openai
import google.generativeai as genai
from config import Config
from typing import List, Dict, Optional

class AIService:
    """Unified AI service supporting both OpenAI and Google Gemini"""
    
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        
        if self.provider == 'openai':
            openai.api_key = Config.OPENAI_API_KEY
            self.model = Config.OPENAI_MODEL
        elif self.provider == 'gemini':
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def generate_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate completion using configured AI provider"""
        
        if self.provider == 'openai':
            return self._openai_completion(messages, temperature, max_tokens)
        elif self.provider == 'gemini':
            return self._gemini_completion(messages, temperature, max_tokens)
    
    def _openai_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using OpenAI"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _gemini_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using Google Gemini"""
        try:
            # Convert messages to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt for Gemini"""
        prompt_parts = []
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                prompt_parts.append(f"System Instructions: {content}\n")
            elif role == 'user':
                prompt_parts.append(f"User: {content}\n")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}\n")
        return "\n".join(prompt_parts)
    
    def extract_structured_data(
        self, 
        prompt: str, 
        schema: Dict
    ) -> Dict:
        """Extract structured data from text using AI"""
        messages = [
            {
                "role": "system",
                "content": "You are a data extraction assistant. Extract information according to the provided schema and return valid JSON."
            },
            {
                "role": "user",
                "content": f"Schema: {schema}\n\nText: {prompt}\n\nExtract the data and return as JSON."
            }
        ]
        
        response = self.generate_completion(messages, temperature=0.3)
        
        # Try to parse JSON from response
        import json
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {}
        except:
            return {}

# Global AI service instance
ai_service = AIService()
