from typing import List, Dict, Any, Optional
from services.openai_service import ai_service
import json

class ReActAgent:
    """
    ReAct (Reasoning + Acting) Agent Framework
    
    This agent follows the ReAct pattern:
    1. Thought: Reason about the current state
    2. Action: Take an action based on reasoning
    3. Observation: Observe the result of the action
    4. Repeat until task is complete
    """
    
    def __init__(self, role: str, context: Dict[str, Any]):
        self.role = role
        self.context = context
        self.trace = []  # Store reasoning trace for debugging/training
    
    def think(self, situation: str) -> str:
        """Generate reasoning about the current situation"""
        messages = [
            {
                "role": "system",
                "content": f"You are {self.role}. Think step by step about the situation."
            },
            {
                "role": "user",
                "content": f"Context: {json.dumps(self.context)}\n\nSituation: {situation}\n\nWhat are your thoughts?"
            }
        ]
        
        thought = ai_service.generate_completion(messages, temperature=0.7)
        self.trace.append({
            "type": "thought",
            "content": thought
        })
        return thought
    
    def act(self, action_prompt: str) -> str:
        """Take an action based on reasoning"""
        messages = [
            {
                "role": "system",
                "content": f"You are {self.role}. Based on your reasoning, take the requested action."
            },
            {
                "role": "user",
                "content": action_prompt
            }
        ]
        
        action_result = ai_service.generate_completion(messages, temperature=0.7)
        self.trace.append({
            "type": "action",
            "content": action_result
        })
        return action_result
    
    def observe(self, observation: str) -> Dict[str, Any]:
        """Observe and reflect on the result"""
        messages = [
            {
                "role": "system",
                "content": f"You are {self.role}. Reflect on the observation and determine next steps."
            },
            {
                "role": "user",
                "content": f"Observation: {observation}\n\nWhat do you conclude? Should we continue or are we done?"
            }
        ]
        
        reflection = ai_service.generate_completion(messages, temperature=0.5)
        self.trace.append({
            "type": "observation",
            "content": reflection
        })
        
        # Determine if task is complete
        is_complete = any(word in reflection.lower() for word in ['complete', 'done', 'finished', 'sufficient'])
        
        return {
            "reflection": reflection,
            "is_complete": is_complete
        }
    
    def execute_task(self, task: str, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Execute a task using the ReAct framework
        
        Args:
            task: The task to execute
            max_iterations: Maximum number of think-act-observe cycles
            
        Returns:
            Dictionary with final result and reasoning trace
        """
        self.trace = []
        result = None
        
        for i in range(max_iterations):
            # Think
            thought = self.think(f"Iteration {i+1}: {task}")
            
            # Act
            action_result = self.act(f"Based on this thought: {thought}\n\nExecute: {task}")
            
            # Observe
            observation = self.observe(action_result)
            
            if observation['is_complete']:
                result = action_result
                break
        
        return {
            "result": result or action_result,
            "trace": self.trace,
            "iterations": i + 1
        }
    
    def get_trace(self) -> List[Dict[str, Any]]:
        """Get the reasoning trace"""
        return self.trace
