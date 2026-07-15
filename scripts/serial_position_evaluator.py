import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Serial Position Effect Evaluator")
    parser.add_argument('--menu_items', type=str, required=True, help='JSON array of objects with usage frequency (1-100): [{"name": "Home", "freq": 90}, {"name": "Settings", "freq": 20}]')
    
    args = parser.parse_args()
    try:
        items = json.loads(args.menu_items)
        if len(items) < 3:
            print(json.dumps({"status": "Too few items to evaluate serial position."}))
            return
            
        first_item = items[0]
        last_item = items[-1]
        middle_items = items[1:-1]
        
        middle_avg = sum(item.get('freq', 0) for item in middle_items) / len(middle_items) if middle_items else 0
        
        is_optimized = (first_item.get('freq', 0) > middle_avg) and (last_item.get('freq', 0) > middle_avg)
        
        sorted_items = sorted(items, key=lambda x: x.get('freq', 0), reverse=True)
        optimal_first = sorted_items[0]
        optimal_last = sorted_items[1] if len(sorted_items) > 1 else sorted_items[0]
        
        print(json.dumps({
            "current_first": first_item['name'],
            "current_last": last_item['name'],
            "is_optimized_for_memory": is_optimized,
            "recommendation": "Optimal." if is_optimized else f"Violation of Serial Position Effect! Place highest frequency items at the ends. Recommended First: {optimal_first['name']}, Recommended Last: {optimal_last['name']}."
        }, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
