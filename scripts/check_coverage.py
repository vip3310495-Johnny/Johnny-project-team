import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Simple Coverage Analyzer Watchdog.")
    parser.add_argument("--report", required=True, help="Path to the coverage report text or json")
    parser.add_argument("--threshold", type=float, default=80.0, help="Minimum coverage threshold (%)")
    args = parser.parse_args()

    if not os.path.exists(args.report):
        print(f"❌ Error: Coverage report '{args.report}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Analyzing coverage report: {args.report}")
    print(f"🎯 Target threshold: {args.threshold}%")
    
    coverage = None
    try:
        if args.report.endswith('.json'):
            import json
            with open(args.report, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Try to parse istanbul coverage-summary.json format
            if "total" in data and "lines" in data["total"] and "pct" in data["total"]["lines"]:
                coverage = float(data["total"]["lines"]["pct"])
            # Fallback for other custom json formats
            elif "coverage" in data:
                coverage = float(data["coverage"])
        else:
            with open(args.report, "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.findall(r'(?:Coverage|Total).*?(\d+(?:\.\d+)?)\s*%', content, re.IGNORECASE)
            if not matches:
                matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', content)
            if matches:
                coverage = float(matches[-1])
    except Exception as e:
        print(f"🚨 Could not parse the coverage report: {e}", file=sys.stderr)
        sys.exit(1)

    if coverage is not None:
        if coverage < args.threshold:
            print(f"❌ Coverage Check FAILED: {coverage}% is below threshold {args.threshold}%.", file=sys.stderr)
            print("❌ Please add more tests to meet the required test coverage.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"✅ Coverage Check PASSED: {coverage}% >= {args.threshold}%")
            sys.exit(0)
    else:
        print("🚨 Could not parse any percentage from the coverage report.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
