import json
from typing import List, cast
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import TravelState

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
llm_json = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Structured Output for Preference Analyzer
class TravelPreferences(BaseModel):
    destination: str = Field(description="The destination for the travel")
    num_days: int = Field(description="Number of days for the trip")
    budget: str = Field(description="The budget for the trip, e.g., '$1000', 'Moderate', etc.")
    preferences: List[str] = Field(description="List of user interests or preferences (e.g., 'beaches', 'food')")

def preference_analyzer_node(state: TravelState) -> TravelState:
    """
    Extract and structure key details from user input.
    """
    analyzer_llm = llm_json.with_structured_output(TravelPreferences)
    
    prompt = f"""
    Analyze the following user travel request and extract the key details.
    User Request: {state['user_input']}
    """
    
    response = analyzer_llm.invoke(prompt)
    
    return {
        "destination": response.destination,
        "num_days": response.num_days,
        "budget": response.budget,
        "preferences": response.preferences
    }

def research_agent_node(state: TravelState) -> TravelState:
    """
    Suggest top attractions and activities based on preferences.
    """
    system_msg = "You are a specialized travel research assistant. Your task is to suggest top attractions and activities."
    prompt = f"""
    Destination: {state.get('destination')}
    Duration: {state.get('num_days')} days
    Preferences: {', '.join(state.get('preferences', []))}
    
    Based on the above, suggest a comprehensive list of top attractions and activities.
    Ensure suggestions align with the user's preferences. Include both popular and relevant experiences.
    """
    
    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {"attractions": response.content}

def itinerary_planner_node(state: TravelState) -> TravelState:
    """
    Create a detailed day-wise plan based on the research.
    """
    system_msg = "You are a master itinerary planner. Create a detailed day-by-day travel plan."
    prompt = f"""
    Destination: {state.get('destination')}
    Duration: {state.get('num_days')} days
    Attractions to include:
    {state.get('attractions')}
    
    Create a detailed day-wise plan. Ensure logical grouping of locations. Maintain realistic timing and flow.
    Avoid overcrowding each day.
    """
    
    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {"itinerary": response.content}

def budget_optimizer_node(state: TravelState) -> TravelState:
    """
    Provide estimated cost breakdown and ensure plan fits budget.
    """
    system_msg = "You are a travel budget optimization expert."
    prompt = f"""
    Destination: {state.get('destination')}
    Duration: {state.get('num_days')} days
    Budget: {state.get('budget')}
    Itinerary:
    {state.get('itinerary')}
    
    Provide an estimated cost breakdown for:
    - Travel
    - Accommodation
    - Food
    - Activities
    
    Ensure the plan fits within the {state.get('budget')} budget. Suggest cheaper alternatives if necessary.
    """
    
    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {"budget_breakdown": response.content}

def final_response_node(state: TravelState) -> TravelState:
    """
    Combine all outputs into a structured final response.
    """
    system_msg = "You are the final response agent for a travel planner. Your job is to format the final itinerary."
    prompt = f"""
    Combine the following information into a beautifully structured, comprehensive travel plan.
    Use clear markdown headings, bullet points, and formatting to ensure readability and usefulness.
    Do not repeat yourself unnecessarily.
    
    Destination: {state.get('destination')} ({state.get('num_days')} days)
    Budget: {state.get('budget')}
    
    ## Proposed Itinerary
    {state.get('itinerary')}
    
    ## Budget Breakdown
    {state.get('budget_breakdown')}
    """
    
    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {"final_plan": response.content}
