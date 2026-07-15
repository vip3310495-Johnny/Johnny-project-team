import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="5 Whys RCA Validator")
    parser.add_argument('--whys', type=str, required=True, help='JSON array of 5 causes: ["Server crashed", "Out of memory", "Memory leak in cache", "Cache not evicted", "No TTL set on Redis"]')
    
    args = parser.parse_args()
    try:
        whys = json.loads(args.whys)
        if len(whys) < 3:
            print(json.dumps({"error": "Insufficient depth. 5 Whys requires at least 3-5 levels of depth."}))
            return
            
        last_cause = whys[-1].lower()
        human_error_keywords = ['forgot', 'mistake', 'tired', 'human error', 'did not know', 'careless', '敹?', '?蕭', '鈭箇', '銝?敹?]
        
        is_human_blame = any(keyword in last_cause for keyword in human_error_keywords)
        
        if is_human_blame:
            recommendation = "Invalid Root Cause! 5 Whys must find a SYSTEMIC flaw, not a human error. Ask: 'Why did the system allow the human to make this mistake?'"
            is_valid = False
        else:
            recommendation = "Valid Systemic Root Cause. Please create an Action Item to fix this."
            is_valid = True
            
        print(json.dumps({
            "depth_reached": len(whys),
            "root_cause": whys[-1],
            "is_valid_systemic_cause": is_valid,
            "recommendation": recommendation
        }, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
