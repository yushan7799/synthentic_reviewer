from agents.react_agent import ReActAgent
from services.openai_service import ai_service
from typing import Dict, Any, List
import json

class PanelistAgent(ReActAgent):
    """
    Specialized agent representing an AI panelist reviewer
    
    This agent uses the ReAct framework to generate reviews based on:
    - Panelist expertise and background
    - Personality traits (critical, openness, seriousness)
    - Proposal content
    """
    
    def __init__(self, panelist_data: Dict[str, Any]):
        """
        Initialize panelist agent
        
        Args:
            panelist_data: Dictionary containing panelist information
        """
        self.panelist = panelist_data
        
        # Create context for ReAct agent
        context = {
            "name": panelist_data.get('name'),
            "expertise": panelist_data.get('expertise_areas', []),
            "publications": panelist_data.get('publications', [])[:5],  # Top 5
            "bio": panelist_data.get('bio', ''),
            "personality": panelist_data.get('personality', {})
        }
        
        # Create role description
        role = self._create_role_description()
        
        super().__init__(role, context)
    
    def _create_role_description(self) -> str:
        """Create a detailed role description for the agent"""
        personality = self.panelist.get('personality', {})
        
        role_parts = [
            f"an expert reviewer named {self.panelist.get('name')}",
            f"with expertise in {', '.join(self.panelist.get('expertise_areas', [])[:3])}"
        ]
        
        # Add personality traits
        critical = personality.get('critical_score', 5)
        openness = personality.get('openness_score', 5)
        seriousness = personality.get('seriousness_score', 5)
        
        if critical >= 7:
            role_parts.append("You are highly critical and rigorous in your evaluations")
        elif critical <= 3:
            role_parts.append("You are supportive and encouraging in your reviews")
        
        if openness >= 7:
            role_parts.append("You are very open to novel and unconventional ideas")
        elif openness <= 3:
            role_parts.append("You prefer well-established methodologies and approaches")
        
        if seriousness >= 7:
            role_parts.append("You provide extremely thorough and formal analysis")
        elif seriousness <= 3:
            role_parts.append("You provide concise and practical feedback")
        
        return ". ".join(role_parts) + "."
    
    def review_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive review of a proposal
        
        Args:
            proposal: Dictionary containing proposal information
            
        Returns:
            Dictionary containing review scores and feedback
        """
        # Prepare proposal summary
        proposal_summary = {
            "title": proposal.get('title'),
            "abstract": proposal.get('abstract', '')[:500],
            "content_preview": proposal.get('content', '')[:1000],
            "research_area": proposal.get('research_area')
        }
        
        # Generate review using structured approach
        review = self._generate_structured_review(proposal_summary)
        
        return review
    
    def _generate_structured_review(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured review with scores and feedback"""
        
        personality = self.panelist.get('personality', {})
        
        # Create detailed prompt for review generation
        prompt = f"""
You are reviewing a research proposal. Provide a comprehensive review with the following structure:

PROPOSAL INFORMATION:
Title: {proposal.get('title')}
Research Area: {proposal.get('research_area')}
Abstract: {proposal.get('abstract')}

YOUR BACKGROUND:
Expertise: {', '.join(self.panelist.get('expertise_areas', []))}
Bio: {self.panelist.get('bio', '')}

YOUR PERSONALITY TRAITS:
- Critical Score: {personality.get('critical_score', 5)}/10 (higher = more critical)
- Openness Score: {personality.get('openness_score', 5)}/10 (higher = more open to novel ideas)
- Seriousness Score: {personality.get('seriousness_score', 5)}/10 (higher = more thorough and formal)

REVIEW REQUIREMENTS:
1. Provide scores (1-10) for:
   - Novelty: How original and innovative is the research?
   - Feasibility: How realistic is the proposed methodology?
   - Impact: What is the potential significance of the work?
   - Methodology: How sound is the research approach?
   - Clarity: How well-written and clear is the proposal?

2. Provide an overall score (1-10) and recommendation (accept/revise/reject)

3. List 3-5 specific strengths

4. List 3-5 specific weaknesses

5. Write a summary paragraph (3-5 sentences)

6. Provide detailed comments addressing methodology, novelty, and impact

7. Offer constructive suggestions for improvement

Adjust your tone and scoring based on your personality traits. Be consistent with your expertise and background.

Return your review in the following JSON format:
{{
    "overall_score": <float>,
    "recommendation": "<accept|revise|reject>",
    "novelty_score": <float>,
    "feasibility_score": <float>,
    "impact_score": <float>,
    "methodology_score": <float>,
    "clarity_score": <float>,
    "strengths": [<list of strings>],
    "weaknesses": [<list of strings>],
    "summary": "<string>",
    "detailed_comments": "<string>",
    "suggestions": "<string>"
}}
"""
        
        messages = [
            {
                "role": "system",
                "content": self.role
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Generate review
        response = ai_service.generate_completion(messages, temperature=0.7, max_tokens=2500)
        
        # Parse JSON response
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                review_data = json.loads(json_str)
                
                # Store reasoning trace
                review_data['reasoning_trace'] = self.get_trace()
                
                return review_data
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            # Fallback: return structured error
            return {
                "overall_score": 5.0,
                "recommendation": "revise",
                "novelty_score": 5.0,
                "feasibility_score": 5.0,
                "impact_score": 5.0,
                "methodology_score": 5.0,
                "clarity_score": 5.0,
                "strengths": ["Unable to generate review"],
                "weaknesses": [f"Error: {str(e)}"],
                "summary": "Review generation failed. Please try again.",
                "detailed_comments": response,
                "suggestions": "N/A",
                "reasoning_trace": []
            }
    
    def explain_reasoning(self) -> str:
        """Get explanation of the review reasoning process"""
        trace = self.get_trace()
        
        explanation_parts = []
        for step in trace:
            step_type = step.get('type', 'unknown')
            content = step.get('content', '')
            explanation_parts.append(f"**{step_type.upper()}**: {content}")
        
        return "\n\n".join(explanation_parts)
