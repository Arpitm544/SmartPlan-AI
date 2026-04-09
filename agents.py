import os
import time
import json
import re
from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import TravelState

if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

# 🔥 Gemini LLM setup - max_retries set to 0 because we will handle retry logic manually
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, max_retries=0)
llm_json = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=0)

def robust_invoke(llm_instance, prompt_messages):
    """Executes the LLM call with a guaranteed dynamic backoff handling for 429 errors"""
    MAX_RETRIES = 5
    for attempt in range(MAX_RETRIES):
        try:
            return llm_instance.invoke(prompt_messages)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                match = re.search(r"retry in (\d+\.?\d*)s", error_str)
                delay = float(match.group(1)) + 1 if match else 15.0
                print(f"[Rate Limit] Hit 429 Free Tier quota. Sleeping for {delay:.1f} seconds (Attempt {attempt+1}/{MAX_RETRIES})...")
                time.sleep(delay)
            else:
                raise e
    raise Exception("Max retries exceeded waiting for API quota.")

# -----------------------------
# Structured Model (optional)
# -----------------------------
class TravelPreferences(BaseModel):
    destination: str
    num_days: int
    budget: str
    preferences: List[str]

# -----------------------------
# 1️⃣ Preference Analyzer
# -----------------------------
def preference_analyzer_node(state: TravelState) -> TravelState:
    prompt = f"""
Extract travel details in JSON format ONLY.

Format:
{{
  "destination": "",
  "num_days": number,
  "budget": "",
  "preferences": []
}}

User Request: {state['user_input']}

Rules:
- Return ONLY JSON
- No explanation
"""

    response = robust_invoke(llm_json, prompt)

    # Clean markdown JSON formatting if present
    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        data = json.loads(content)
    except Exception as e:
        print(f"Error parsing JSON: {e}, Content: {response.content}")
        data = {}

    return {
        "destination": data.get("destination"),
        "num_days": data.get("num_days"),
        "budget": data.get("budget"),
        "preferences": data.get("preferences", [])
    }

# -----------------------------
# 2️⃣ Research Agent
# -----------------------------
def research_agent_node(state: TravelState) -> TravelState:
    system_msg = """You are a travel research assistant.

RULES:
- Max 8 attractions
- Each line under 10 words
- No paragraphs
"""

    prompt = f"""
Destination: {state.get('destination')}
Preferences: {', '.join(state.get('preferences', []))}

List top attractions.
"""

    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = robust_invoke(llm, messages)

    return {"attractions": response.content}

# -----------------------------
# 3️⃣ Itinerary Planner
# -----------------------------
def itinerary_planner_node(state: TravelState) -> TravelState:
    system_msg = """Create day-wise itinerary.

RULES:
- 3–4 activities per day
- Short lines only
- No explanation
"""

    prompt = f"""
Destination: {state.get('destination')}
Days: {state.get('num_days')}

Attractions:
{state.get('attractions')}
"""

    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = robust_invoke(llm, messages)

    return {"itinerary": response.content}

# -----------------------------
# 4️⃣ Final Response
# -----------------------------
def final_response_node(state: TravelState) -> TravelState:
    system_msg = """Generate a BEAUTIFUL, engaging final travel plan tailored perfectly for a premium demo presentation.

RULES:
- Use rich, heavily structured Markdown formatting (Headers, bold text, italics).
- Be extremely enthusiastic and welcoming in tone.
- Segment clearly by Days (Day 1, Day 2, etc.) with evocative titles for each day.
- Incorporate appropriate and fun emojis for activities ✨🌍🍽️.
- Include a small simulated 'Budget Est.' note at the end to prove budget-awareness.
- DO NOT constrain by word counts—make it read like a premium travel brochure!
"""

    prompt = f"""
Destination: {state.get('destination')}
Budget: {state.get('budget')}

Attractions:
{state.get('attractions')}

Itinerary:
{state.get('itinerary')}
"""

    messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]
    response = robust_invoke(llm, messages)

    return {"final_plan": response.content}