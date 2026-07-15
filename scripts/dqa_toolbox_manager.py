import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import os
import json
import argparse

def find_toolbox_dir():
    current_dir = os.getcwd()
    while True:
        agents_dir = os.path.join(current_dir, ".agents")
        if os.path.exists(agents_dir) and os.path.isdir(agents_dir):
            toolbox_dir = os.path.join(agents_dir, "dqa_toolbox")
            os.makedirs(toolbox_dir, exist_ok=True)
            return toolbox_dir
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            fallback = os.path.join(os.getcwd(), ".agents", "dqa_toolbox")
            os.makedirs(fallback, exist_ok=True)
            return fallback
        current_dir = parent

def load_inventory(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_inventory(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="DQA Test Asset Toolbox Manager")
    subparsers = parser.add_subparsers(dest='command', required=True)

    reg_parser = subparsers.add_parser('register', help='Register a new test script')
    reg_parser.add_argument('path', help='Relative path to the test script')
    reg_parser.add_argument('description', help='Brief description of what the script does')
    reg_parser.add_argument('tags', help='Comma-separated tags (e.g., performance,api,stress)')

    search_parser = subparsers.add_parser('search', help='Search for an existing test script')
    search_parser.add_argument('keyword', help='Keyword to search in description or tags')

    args = parser.parse_args()

    toolbox_dir = find_toolbox_dir()
    inventory_file = os.path.join(toolbox_dir, "inventory.json")
    
    inventory = load_inventory(inventory_file)

    if args.command == 'register':
        # Check if already exists
        for item in inventory:
            if item['path'] == args.path:
                print(f"⚠️ Script '{args.path}' is already registered. Updating info...")
                item['description'] = args.description
                item['tags'] = [t.strip() for t in args.tags.split(',')]
                save_inventory(inventory_file, inventory)
                print("✅ Update successful.")
                sys.exit(0)
        
        inventory.append({
            "path": args.path,
            "description": args.description,
            "tags": [t.strip() for t in args.tags.split(',')]
        })
        save_inventory(inventory_file, inventory)
        print(f"✅ Successfully registered '{args.path}' to DQA Toolbox.")

    elif args.command == 'search':
        kw = args.keyword.lower()
        results = []
        for item in inventory:
            if kw in item['description'].lower() or any(kw in t.lower() for t in item['tags']):
                results.append(item)
        
        if not results:
            print(f"❌ No test scripts found matching '{args.keyword}'.")
        else:
            print(f"\n🔍 Found {len(results)} matching test script(s):")
            for i, r in enumerate(results, 1):
                print(f"  {i}. Path: {r['path']}")
                print(f"     Desc: {r['description']}")
                print(f"     Tags: {', '.join(r['tags'])}\n")

if __name__ == "__main__":
    main()
