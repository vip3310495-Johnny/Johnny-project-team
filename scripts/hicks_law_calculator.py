import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import math
import json

def calculate_hicks_law(options_count, b=0.15):
    # Hick's Law formula: T = b * log2(n + 1)
    decision_time = b * math.log2(options_count + 1)
    return decision_time

def main():
    parser = argparse.ArgumentParser(description="Calculate decision time using Hick's Law")
    parser.add_argument('--options', type=int, required=True, help="Number of options/buttons on the screen")
    parser.add_argument('--b', type=float, default=0.15, help="Constant for processing speed (default: 0.15s)")
    
    args = parser.parse_args()
    
    time_taken = calculate_hicks_law(args.options, args.b)
    is_overloaded = args.options > 7
    
    print(json.dumps({
        "options_count": args.options,
        "decision_time_seconds": round(time_taken, 3),
        "is_overloaded": is_overloaded,
        "recommendation": "Use Progressive Disclosure (e.g. nested menus or wizards)" if is_overloaded else "Options count is acceptable"
    }, indent=2))

if __name__ == "__main__":
    main()
