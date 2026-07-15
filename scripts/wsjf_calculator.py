import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import sys

def calculate_wsjf(business_value, time_criticality, risk_reduction, job_size):
    cost_of_delay = business_value + time_criticality + risk_reduction
    return cost_of_delay / job_size if job_size > 0 else float('inf')

def main():
    parser = argparse.ArgumentParser(description="Calculate WSJF for multiple jobs")
    parser.add_argument('--jobs', type=str, help='JSON string containing list of jobs: [{"name": "A", "bv": 5, "tc": 3, "rr": 2, "size": 3}]')
    
    args = parser.parse_args()
    if not args.jobs:
        print("Please provide jobs data in JSON format.")
        sys.exit(1)
        
    try:
        jobs = json.loads(args.jobs)
        results = []
        for job in jobs:
            wsjf = calculate_wsjf(job.get('bv', 0), job.get('tc', 0), job.get('rr', 0), job.get('size', 1))
            results.append({"name": job['name'], "wsjf": wsjf})
        
        results.sort(key=lambda x: x['wsjf'], reverse=True)
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
