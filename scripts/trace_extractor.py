import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import json
import argparse
from collections import deque

def extract_trace(transcript_path, output_path, limit=100):
    """
    Reads the system transcript.jsonl, extracts the last `limit` steps efficiently,
    filters out huge data payloads, and saves a compact JSON.
    """
    if not os.path.exists(transcript_path):
        print(f"Transcript not found at {transcript_path}")
        return

    compact_trace = []
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        recent_lines = deque(f, maxlen=limit)
    
    for line in recent_lines:
        try:
            step = json.loads(line)
            # Filter logic: Keep type, source, tool names, but truncate big outputs
            trace_entry = {
                "step_index": step.get("step_index"),
                "source": step.get("source"),
                "type": step.get("type"),
                "status": step.get("status")
            }
            
            # Extract tool calls without full arguments if they are too big
            if "tool_calls" in step and step["tool_calls"]:
                calls = []
                for tc in step["tool_calls"]:
                    call_info = {"tool_name": tc.get("name")}
                    calls.append(call_info)
                trace_entry["tool_calls"] = calls
                
            # If user input, keep a snippet
            if step.get("type") == "USER_INPUT":
                content = step.get("content", "")
                trace_entry["user_input_snippet"] = content[:200] + ("..." if len(content) > 200 else "")
                
            compact_trace.append(trace_entry)
        except Exception as e:
            continue
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(compact_trace, out_f, indent=2, ensure_ascii=False)
        
    print(f"Extracted compact trace to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True, help="Path to transcript.jsonl")
    parser.add_argument("--output", required=True, help="Path to save compact trace")
    parser.add_argument("--limit", type=int, default=100, help="Number of recent steps to parse")
    args = parser.parse_args()
    extract_trace(args.transcript, args.output, args.limit)
