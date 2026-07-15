import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Gestalt Principles Spacing Validator")
    parser.add_argument('--inner_gap', type=float, required=True, help="Gap between related elements (e.g., Title and Description)")
    parser.add_argument('--outer_gap', type=float, required=True, help="Gap between separate groups (e.g., Card and Card)")
    
    args = parser.parse_args()
    
    # Gestalt Proximity: Elements that are closer together are perceived as more related
    # Therefore, inner gap MUST be strictly less than outer gap.
    is_valid = args.inner_gap < args.outer_gap
    
    print(json.dumps({
        "inner_gap": args.inner_gap,
        "outer_gap": args.outer_gap,
        "is_valid_gestalt_proximity": is_valid,
        "recommendation": "OK" if is_valid else "Violation of Gestalt Proximity! Inner gap must be smaller than outer gap to group related elements."
    }, indent=2))

if __name__ == "__main__":
    main()
