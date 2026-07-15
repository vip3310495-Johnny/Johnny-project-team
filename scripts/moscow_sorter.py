import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="MoSCoW Method Sorter")
    parser.add_argument('--features', type=str, required=True, help='JSON list of features with effort and value: [{"name": "Auth", "value": 10, "effort": 3}]')
    parser.add_argument('--capacity', type=int, required=True, help="Total effort capacity for this sprint")
    
    args = parser.parse_args()
    
    try:
        features = json.loads(args.features)
        for f in features:
            f['ratio'] = f.get('value', 0) / f.get('effort', 1)
            
        features.sort(key=lambda x: x['ratio'], reverse=True)
        
        moscow = {"Must_Have": [], "Should_Have": [], "Could_Have": [], "Wont_Have": []}
        current_effort = 0
        
        for f in features:
            if current_effort + f['effort'] <= args.capacity * 0.6:
                moscow["Must_Have"].append(f['name'])
                current_effort += f['effort']
            elif current_effort + f['effort'] <= args.capacity * 0.8:
                moscow["Should_Have"].append(f['name'])
                current_effort += f['effort']
            elif current_effort + f['effort'] <= args.capacity:
                moscow["Could_Have"].append(f['name'])
                current_effort += f['effort']
            else:
                moscow["Wont_Have"].append(f['name'])
                
        print(json.dumps(moscow, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
