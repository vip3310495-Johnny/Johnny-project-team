import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Record a lesson learned for all Agents.")
    parser.add_argument("--cid", required=False, default="Unknown", help="Conversation ID or Agent ID")
    parser.add_argument("--issue", required=True, help="The issue or bug encountered")
    parser.add_argument("--cause", required=True, help="Root cause of the issue")
    parser.add_argument("--solution", required=True, help="How it was solved and how to prevent it")
    parser.add_argument("--agent-role", required=False, default="engineering", help="The role of the agent (e.g., engineering, dqa, global)")
    args = parser.parse_args()

    # Align path with new entries structure
    target_dir = os.path.join(".agents", "lessons_learned", "entries")
    os.makedirs(target_dir, exist_ok=True)
    
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(target_dir, f"{args.agent_role}_{timestamp_str}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f"role: {args.agent_role}\n")
        f.write(f"status: active\n")
        f.write(f"occurrence_count: 1\n")
        f.write(f"last_hit_date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"---\n\n")
        f.write(f"### Lesson Added: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Agent: {args.cid})\n")
        f.write(f"- **Issue:** {args.issue}\n")
        f.write(f"- **Root Cause:** {args.cause}\n")
        f.write(f"- **Solution & Prevention:** {args.solution}\n\n")

    print(f"✅ Lesson successfully recorded in repository: {filename}")

if __name__ == "__main__":
    main()
