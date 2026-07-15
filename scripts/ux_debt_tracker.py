import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="UX & Tech Debt Tracker (CEO Override Logger)")
    parser.add_argument('--action', choices=['log_override', 'report'], required=True)
    parser.add_argument('--rule_broken', type=str, help="E.g., Hick's Law, Fitts's Law")
    parser.add_argument('--ceo_reason', type=str, help="Why the CEO bypassed the rule")
    
    args = parser.parse_args()
    debt_file = ".ux_debt_log.json"
    
    if os.path.exists(debt_file):
        with open(debt_file, 'r') as f:
            debt = json.load(f)
    else:
        debt = {"total_score": 0, "overrides": []}
        
    if args.action == 'log_override':
        if not args.rule_broken:
            print(json.dumps({"error": "Must provide --rule_broken"}))
            return
            
        debt["total_score"] += 1
        debt["overrides"].append({
            "rule_broken": args.rule_broken,
            "ceo_reason": args.ceo_reason or "Forced override"
        })
        
        with open(debt_file, 'w') as f:
            json.dump(debt, f, indent=2)
            
        warning = ""
        if debt["total_score"] > 3:
            warning = "CRITICAL WARNING: UX Debt is too high! The product is becoming unusable and bloated. Recommend scheduling a refactoring sprint."
            
        print(json.dumps({
            "status": "Logged",
            "current_debt_score": debt["total_score"],
            "warning": warning
        }, indent=2))
        
    else:
        print(json.dumps(debt, indent=2))

if __name__ == "__main__":
    main()
