from typing import TypedDict, List, Dict, Optional

class CopilotState(TypedDict, total=False):
    '''
    Central state object that flows through the LangGraph workflow.
    Each node receives and returns this state.
    '''
    user_id: str
    user_input: str
    
    session_memory: Dict
    long_term_memory: Dict
    
    retrieved_memory: Dict
    filtered_memory: Dict
    
    constructed_prompt: str
    llm_responce: str