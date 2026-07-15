import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Evaluate Make-or-Buy Decision based on ROI")
    parser.add_argument('--dev_cost', type=float, required=True, help="Estimated cost to build in-house")
    parser.add_argument('--dev_time_days', type=float, required=True, help="Estimated days to build in-house")
    parser.add_argument('--api_cost_per_month', type=float, required=True, help="Monthly cost of external API/Service")
    parser.add_argument('--integration_days', type=float, required=True, help="Days to integrate the API")
    parser.add_argument('--lifespan_months', type=float, default=12, help="Expected lifespan of the feature in months")
    parser.add_argument('--data_compliance_risk', type=str, default='LOW', choices=['LOW', 'HIGH'], help="If HIGH, external APIs are banned due to privacy")
    
    args = parser.parse_args()
    
    if args.data_compliance_risk == 'HIGH':
        print(json.dumps({
            "decision": "MAKE (In-House)",
            "reason": "VETOED by Data Compliance Risk. Cannot use external API for sensitive data."
        }, indent=2))
        return

    # Calculate Total Costs
    total_make_cost = args.dev_cost
    dev_cost_per_day = args.dev_cost / args.dev_time_days if args.dev_time_days > 0 else 0
    total_buy_cost = (args.api_cost_per_month * args.lifespan_months) + (args.integration_days * dev_cost_per_day)
    
    # Time savings
    time_saved_days = args.dev_time_days - args.integration_days
    
    decision = "BUY (External API)" if total_buy_cost < total_make_cost else "MAKE (In-House)"
    
    if time_saved_days > 14 and total_buy_cost < total_make_cost * 1.5:
        decision = "BUY (Strongly Recommended for Time-to-Market)"
        
    print(json.dumps({
        "make_cost": round(total_make_cost, 2),
        "buy_cost": round(total_buy_cost, 2),
        "time_saved_days": round(time_saved_days, 1),
        "lifespan_months": args.lifespan_months,
        "data_compliance_risk": args.data_compliance_risk,
        "decision": decision
    }, indent=2))

if __name__ == "__main__":
    main()
