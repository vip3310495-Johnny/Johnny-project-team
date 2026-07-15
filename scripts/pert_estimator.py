import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def calculate_pert(optimistic, most_likely, pessimistic):
    expected_time = (optimistic + 4 * most_likely + pessimistic) / 6
    return expected_time

def main():
    parser = argparse.ArgumentParser(description="Calculate PERT expected time")
    parser.add_argument('-o', '--optimistic', type=float, required=True, help="Optimistic time estimate")
    parser.add_argument('-m', '--most_likely', type=float, required=True, help="Most likely time estimate")
    parser.add_argument('-p', '--pessimistic', type=float, required=True, help="Pessimistic time estimate")
    
    args = parser.parse_args()
    expected_time = calculate_pert(args.optimistic, args.most_likely, args.pessimistic)
    
    print(json.dumps({
        "optimistic": args.optimistic,
        "most_likely": args.most_likely,
        "pessimistic": args.pessimistic,
        "expected_time": round(expected_time, 2)
    }, indent=2))

if __name__ == "__main__":
    main()
