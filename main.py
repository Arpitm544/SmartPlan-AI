import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from graph import graph

def main():
    print("Welcome to SmartPlan-AI: The Multi-Agent Travel Planner!")
    print("-" * 50)
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is missing.")
        print("Please set it in your .env file.")
        return

    user_input = input("Please describe your perfect trip (e.g., 'I want to go to Tokyo for 5 days with a budget of $2000, focusing on gaming and food'):\n> ")
    
    if not user_input.strip():
        print("No input provided. Exiting.")
        return
        
    print("\n[System] Let me plan that for you! Starting the agents...\n")
    
    initial_state = {
        "user_input": user_input
    }
    
    # Run the graph and stream the state updates
    try:
        final_state = None
        for step in graph.stream(initial_state):
            # Print which agent just ran
            for node_name, node_state in step.items():
                print(f"✅ Agent Completed: {node_name}")
                final_state = node_state
        
        print("\n\n" + "=" * 50)
        print("🎉 YOUR PERSONALIZED TRAVEL PLAN 🎉")
        print("=" * 50 + "\n")
        
        if final_state and "final_plan" in final_state:
            print(final_state["final_plan"])
        else:
            print("Failed to generate the final plan.")
            
    except Exception as e:
        print(f"\n[Error] An error occurred while planning your trip: {e}")

if __name__ == "__main__":
    main()
