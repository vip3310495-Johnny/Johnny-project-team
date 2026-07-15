import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import math
import json

def calculate_fitts_law(distance, width, a=0.2, b=0.1):
    # Fitts's Law formula: T = a + b * log2(1 + D/W)
    time_taken = a + b * math.log2(1 + distance / width)
    return time_taken

def main():
    parser = argparse.ArgumentParser(description="Calculate interaction time using Fitts's Law")
    parser.add_argument('--distance', type=float, required=True, help="Distance from starting point to the target button (D)")
    parser.add_argument('--width', type=float, required=True, help="Width/size of the target button (W)")
    
    args = parser.parse_args()
    
    if args.width <= 0:
        print(json.dumps({"error": "Width must be greater than 0"}))
        return
        
    index_of_difficulty = math.log2(1 + args.distance / args.width)
    time_taken = calculate_fitts_law(args.distance, args.width)
    
    print(json.dumps({
        "distance": args.distance,
        "width": args.width,
        "index_of_difficulty": round(index_of_difficulty, 2),
        "movement_time_seconds": round(time_taken, 3),
        "recommendation": "Increase button size (W) or reduce distance (D) if time > 1.5s"
    }, indent=2))

if __name__ == "__main__":
    main()
