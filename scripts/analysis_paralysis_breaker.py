import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import os
import time

def main():
    parser = argparse.ArgumentParser(description="Analysis Paralysis Breaker (CEO Loop Detector)")
    parser.add_argument('--query', type=str, required=True, help="The current query or action from the CEO")
    
    args = parser.parse_args()
    state_file = ".pm_interaction_log.json"
    
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {"last_query": "", "repeat_count": 0, "last_action_timestamp": time.time()}
        
    current_query = args.query.strip().lower()
    
    if current_query == state.get("last_query", ""):
        state["repeat_count"] += 1
    else:
        state["last_query"] = current_query
        state["repeat_count"] = 1
        
    state["last_action_timestamp"] = time.time()
    
    with open(state_file, 'w') as f:
        json.dump(state, f)
        
    is_paralyzed = state["repeat_count"] >= 3
    
    if is_paralyzed:
        recommendation = "?? CEO ANALYSIS PARALYSIS DETECTED. The CEO has asked the same review/planning question repeatedly. PM Agent MUST invoke executive authority, stop the planning phase immediately, and force the Dev Agent to start writing code (Transition to DO phase)."
    else:
        recommendation = "Healthy interaction. Continue."
        
    print(json.dumps({
        "query": current_query,
        "repeat_count": state["repeat_count"],
        "is_analysis_paralysis": is_paralyzed,
        "action_required": recommendation
    }, indent=2))

if __name__ == "__main__":
    main()
