import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import os
import json
import argparse

def find_agents_dir():
    current_dir = os.getcwd()
    while True:
        target = os.path.join(current_dir, ".agents")
        if os.path.exists(target) and os.path.isdir(target):
            return target
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            # Fallback to current dir if not found
            fallback = os.path.join(os.getcwd(), ".agents")
            os.makedirs(fallback, exist_ok=True)
            return fallback
        current_dir = parent

def load_queue(file_path):
    if not os.path.exists(file_path):
        return {"in_progress": None, "queue": []}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"in_progress": None, "queue": []}

def save_queue(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="DQA Single-Threaded Review Queue Manager")
    subparsers = parser.add_subparsers(dest='command', required=True)

    push_parser = subparsers.add_parser('push', help='Add an engineer/task to the DQA queue')
    push_parser.add_argument('name', help='Name of the engineer or branch (e.g., Backend_MS1)')

    subparsers.add_parser('pop', help='Pop the next task for DQA review')
    subparsers.add_parser('finish', help='Mark the current DQA review as completed (unlocks the queue)')
    subparsers.add_parser('status', help='View the current queue status')

    args = parser.parse_args()

    agents_dir = find_agents_dir()
    queue_file = os.path.join(agents_dir, "dqa_queue.json")
    
    data = load_queue(queue_file)

    if args.command == 'push':
        data["queue"].append(args.name)
        save_queue(queue_file, data)
        print(f"✅ Added '{args.name}' to DQA Review Queue. Current queue size: {len(data['queue'])}")

    elif args.command == 'pop':
        if data["in_progress"] is not None:
            print(f"❌ ERROR: DQA is currently reviewing '{data['in_progress']}'.")
            print("You MUST wait for this review to pass and execute 'finish' before popping the next task.")
            sys.exit(1)
        
        if len(data["queue"]) == 0:
            print("ℹ️ DQA Review Queue is empty.")
            sys.exit(0)
            
        next_task = data["queue"].pop(0)
        data["in_progress"] = next_task
        save_queue(queue_file, data)
        print(f"✅ Popped '{next_task}' for DQA Review. The queue is now LOCKED.")

    elif args.command == 'finish':
        if data["in_progress"] is None:
            print("ℹ️ No task is currently in progress.")
        else:
            print(f"✅ Marked '{data['in_progress']}' as finished. DQA Queue is now UNLOCKED.")
            data["in_progress"] = None
            save_queue(queue_file, data)

    elif args.command == 'status':
        print("\n--- 🚦 DQA Queue Status ---")
        in_prog = data["in_progress"] if data["in_progress"] else "None (Unlocked)"
        print(f"Currently in Review: {in_prog}")
        print("Waiting in Queue:")
        if not data["queue"]:
            print("  (Empty)")
        else:
            for i, item in enumerate(data["queue"], 1):
                print(f"  {i}. {item}")
        print("---------------------------\n")

if __name__ == "__main__":
    main()
