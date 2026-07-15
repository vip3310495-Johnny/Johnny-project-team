import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Global Project Context Manager for Dynamic Thresholds")
    parser.add_argument('--action', choices=['set', 'get'], required=True)
    parser.add_argument('--project_type', choices=['B2B', 'B2C', 'INTERNAL_TOOL'], help="Required if action=set")
    
    args = parser.parse_args()
    context_file = ".vibe_project_context.json"
    
    if args.action == 'set':
        if not args.project_type:
            print(json.dumps({"error": "Must provide --project_type when setting."}))
            return
            
        thresholds = {
            "B2B": {"max_options": 15, "fitts_time_limit": 2.5, "saliency_threshold": 3.0},
            "B2C": {"max_options": 7, "fitts_time_limit": 1.2, "saliency_threshold": 4.5},
            "INTERNAL_TOOL": {"max_options": 25, "fitts_time_limit": 3.0, "saliency_threshold": 2.5}
        }
        
        data = {
            "project_type": args.project_type,
            "thresholds": thresholds[args.project_type]
        }
        with open(context_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(json.dumps({"status": "Context updated", "data": data}, indent=2))
        
    else:
        if os.path.exists(context_file):
            with open(context_file, 'r') as f:
                data = json.load(f)
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps({"error": "No context set. Defaulting to B2C thresholds."}))

if __name__ == "__main__":
    main()
