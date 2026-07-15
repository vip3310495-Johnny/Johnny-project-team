import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def classify_kano(functional_score, dysfunctional_score):
    if functional_score >= 4 and dysfunctional_score <= 2:
        return "Attractive (擳???)"
    elif functional_score >= 4 and dysfunctional_score >= 4:
        return "One-Dimensional (????)"
    elif functional_score <= 3 and dysfunctional_score >= 4:
        return "Must-Be (敹???)"
    elif functional_score <= 3 and dysfunctional_score <= 3:
        return "Indifferent (?∪榆?啣?蝝?"
    else:
        return "Questionable / Reverse"

def main():
    parser = argparse.ArgumentParser(description="Kano Model Classifier")
    parser.add_argument('--features', type=str, required=True, help='JSON list of features with functional/dysfunctional scores (1-5): [{"name": "Animation", "func": 5, "dys": 2}]')
    
    args = parser.parse_args()
    try:
        features = json.loads(args.features)
        results = []
        for f in features:
            category = classify_kano(f.get('func', 3), f.get('dys', 3))
            results.append({
                "name": f['name'],
                "category": category,
                "action": "Prioritize implementation" if category in ["Must-Be (敹???)", "One-Dimensional (????)"] else "Hold for Vibe Polish" if category == "Attractive (擳???)" else "Drop"
            })
            
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
