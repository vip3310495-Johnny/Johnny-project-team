import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Weighted Scoring Matrix for Alternatives (AHP Alternative)")
    parser.add_argument('--criteria', type=str, required=True, help='JSON of criteria weights: {"Speed": 0.4, "Cost": 0.2}')
    parser.add_argument('--alternatives', type=str, required=True, help='JSON of alternative scores (0-10): {"PostgreSQL": {"Speed": 8, "Cost": 7}}')
    
    args = parser.parse_args()
    criteria = json.loads(args.criteria)
    alternatives = json.loads(args.alternatives)
    
    results = []
    for alt_name, scores in alternatives.items():
        total_score = 0
        for crit, weight in criteria.items():
            total_score += scores.get(crit, 0) * weight
        results.append({"name": alt_name, "score": round(total_score, 2)})
        
    results.sort(key=lambda x: x['score'], reverse=True)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
