import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="MECE (Mutually Exclusive, Collectively Exhaustive) Evaluator")
    parser.add_argument('--categories', type=str, required=True, help='JSON array of categories with percentages: [{"name": "Mobile", "pct": 40}, {"name": "Desktop", "pct": 50}, {"name": "Tablet", "pct": 10}]')
    
    args = parser.parse_args()
    try:
        categories = json.loads(args.categories)
        total_pct = sum(c.get('pct', 0) for c in categories)
        
        is_exhaustive = abs(total_pct - 100) < 0.1
        
        names = [c['name'].lower() for c in categories]
        overlaps = []
        for i, name1 in enumerate(names):
            for j, name2 in enumerate(names):
                if i != j and (name1 in name2 or name2 in name1):
                    overlaps.append((categories[i]['name'], categories[j]['name']))
                    
        is_exclusive = len(overlaps) == 0
        
        print(json.dumps({
            "total_percentage": total_pct,
            "is_collectively_exhaustive": is_exhaustive,
            "is_mutually_exclusive_guess": is_exclusive,
            "potential_overlaps": list(set(["<->".join(sorted(pair)) for pair in overlaps])),
            "recommendation": "MECE validated." if (is_exhaustive and is_exclusive) else "Violation of MECE principles. Please ensure categories add up to 100% and do not overlap."
        }, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
