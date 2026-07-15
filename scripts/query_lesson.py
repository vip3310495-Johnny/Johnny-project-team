import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Query the global lesson learn repository by keywords.")
    parser.add_argument("keywords", nargs="+", help="Keywords to search for (e.g., 'redis', 'auth', 'database')")
    parser.add_argument("--agent-role", required=False, default="engineering", help="The role of the agent (e.g., engineering, dqa)")
    args = parser.parse_args()

    entries_dir = os.path.join(".agents", "lessons_learned", "entries")
    
    print(f"🔍 Searching for historical lessons containing: {', '.join(args.keywords)}\n")
    
    found_any = False
    
    if os.path.exists(entries_dir):
        for filename in os.listdir(entries_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(entries_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                lower_content = content.lower()
                if any(keyword.lower() in lower_content for keyword in args.keywords):
                    print(f"[{filename}]")
                    print(content.strip() + "\n" + "-"*40 + "\n")
                    found_any = True
                    # Update last_hit_date here in real implementation

    if not found_any:
        print("✅ No relevant historical errors found for these keywords. Proceed with confidence!")

if __name__ == "__main__":
    main()
