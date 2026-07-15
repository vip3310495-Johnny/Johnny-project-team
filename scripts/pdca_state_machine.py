import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="PDCA Cycle State Machine Enforcer")
    parser.add_argument('--action', type=str, required=True, choices=['PLAN', 'DO', 'CHECK', 'ACT'], help="The PDCA phase the agent wants to enter")
    parser.add_argument('--evidence', type=str, required=False, help="Evidence required to pass the gate (e.g. Test Report for CHECK)")
    
    args = parser.parse_args()
    state_file = ".pdca_state.json"
    
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {"current_phase": "IDLE"}
        
    transitions = {
        "IDLE": "PLAN",
        "PLAN": "DO",
        "DO": "CHECK",
        "CHECK": "ACT",
        "ACT": "PLAN"
    }
    
    expected_next = transitions.get(state["current_phase"], "PLAN")
    
    if args.action != expected_next and not (state["current_phase"] == "IDLE" and args.action == "PLAN"):
        print(json.dumps({
            "error": f"Invalid PDCA transition. Current phase is {state['current_phase']}. Expected next phase is {expected_next}, but requested {args.action}."
        }, indent=2))
        return
        
    if args.action == "CHECK" and not args.evidence:
        print(json.dumps({
            "error": "Cannot enter CHECK phase without evidence (e.g., DQA Test Report or coverage metrics)."
        }, indent=2))
        return
        
    state["current_phase"] = args.action
    with open(state_file, 'w') as f:
        json.dump(state, f)
        
    print(json.dumps({
        "status": "Success",
        "current_phase": args.action,
        "message": f"Successfully transitioned to {args.action} phase."
    }, indent=2))

if __name__ == "__main__":
    main()
