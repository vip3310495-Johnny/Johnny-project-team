import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import math
import collections
import json

def calculate_entropy(text):
    words = text.lower().split()
    if not words:
        return 0
    
    word_counts = collections.Counter(words)
    total_words = len(words)
    
    entropy = 0
    for count in word_counts.values():
        p = count / total_words
        entropy -= p * math.log2(p)
        
    return entropy

def main():
    parser = argparse.ArgumentParser(description="Calculate Shannon Entropy for a Prompt")
    parser.add_argument('--prompt', type=str, required=True, help='The text prompt to evaluate')
    parser.add_argument('--threshold', type=float, default=4.5, help='Entropy threshold')
    
    args = parser.parse_args()
    entropy = calculate_entropy(args.prompt)
    is_confusing = entropy > args.threshold
    
    print(json.dumps({
        "entropy": round(entropy, 2),
        "threshold": args.threshold,
        "requires_clarification": is_confusing
    }, indent=2))

if __name__ == "__main__":
    main()
