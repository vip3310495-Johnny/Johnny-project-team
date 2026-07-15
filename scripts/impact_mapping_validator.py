import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Impact Mapping Structure Validator")
    parser.add_argument('--map', type=str, required=True, help='JSON Impact Map: {"goal": "Increase revenue", "actors": [{"name": "User", "impacts": [{"name": "Buy more", "deliverables": ["1-click checkout"]}]}]}')
    
    args = parser.parse_args()
    try:
        imap = json.loads(args.map)
        
        if "goal" not in imap or not imap["goal"]:
            print(json.dumps({"error": "Missing Goal (Why)"}))
            return
            
        if "actors" not in imap or not isinstance(imap["actors"], list) or len(imap["actors"]) == 0:
            print(json.dumps({"error": "Missing Actors (Who)"}))
            return
            
        for actor in imap["actors"]:
            if "impacts" not in actor or len(actor["impacts"]) == 0:
                print(json.dumps({"error": f"Actor '{actor.get('name')}' missing Impacts (How)"}))
                return
            for impact in actor["impacts"]:
                if "deliverables" not in impact or len(impact["deliverables"]) == 0:
                    print(json.dumps({"error": f"Impact '{impact.get('name')}' missing Deliverables (What)"}))
                    return
                    
        print(json.dumps({
            "status": "Valid Impact Map",
            "goal": imap["goal"],
            "actors_count": len(imap["actors"]),
            "recommendation": "Map is complete: Goal -> Actor -> Impact -> Deliverable."
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
