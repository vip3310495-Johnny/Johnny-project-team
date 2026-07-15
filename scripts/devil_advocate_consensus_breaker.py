import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Consensus Breaker (Anti-Sycophancy)")
    parser.add_argument('--attempts', type=int, required=True, help="Number of times the DQA/Dev passed the review")
    parser.add_argument('--errors_found', type=int, required=True, help="Number of errors found during this cycle")
    
    args = parser.parse_args()
    
    is_suspicious = args.attempts == 1 and args.errors_found == 0
    
    if is_suspicious:
        recommendation = "SUSPICIOUS CONSENSUS DETECTED. Multi-agent sycophancy probable. PM Agent MUST artificially inject a chaotic edge case (e.g., 'What if the database drops connection mid-query?') and force the Dev/DQA to handle it before passing."
    else:
        recommendation = "Healthy friction detected. The consensus is valid."
        
    print(json.dumps({
        "attempts": args.attempts,
        "errors_found": args.errors_found,
        "is_suspicious_consensus": is_suspicious,
        "action_required": recommendation
    }, indent=2))

if __name__ == "__main__":
    main()
