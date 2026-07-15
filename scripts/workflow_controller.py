import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
import os
import subprocess
import sys

def get_state_path(project_dir):
    pm_dir = os.path.join(project_dir, "PM")
    os.makedirs(pm_dir, exist_ok=True)
    return os.path.join(pm_dir, "workflow_state.json")

def load_state(project_dir):
    path = get_state_path(project_dir)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "total_failures": 0,
        "task_failures": {},
        "status": "GREEN_LIGHT",
        "max_task_failures": 3,
        "max_total_failures": 5
    }

def save_state(project_dir, state):
    path = get_state_path(project_dir)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def check_limits(state, task_id=None):
    if state["total_failures"] >= state["max_total_failures"]:
        state["status"] = "RED_LIGHT"
        return "RED_LIGHT (Max Total Failures Reached: {}/{})".format(state["total_failures"], state["max_total_failures"])
    
    if task_id and state["task_failures"].get(task_id, 0) >= state["max_task_failures"]:
        state["status"] = "RED_LIGHT"
        return "RED_LIGHT (Max Task Failures Reached for task '{}': {}/{})".format(task_id, state["task_failures"][task_id], state["max_task_failures"])
        
    state["status"] = "GREEN_LIGHT"
    return "GREEN_LIGHT"

def handle_record_failure(args):
    state = load_state(args.project_dir)
    state["total_failures"] += 1
    
    if args.task_id not in state["task_failures"]:
        state["task_failures"][args.task_id] = 0
    state["task_failures"][args.task_id] += 1
    
    status_msg = check_limits(state, args.task_id)
    save_state(args.project_dir, state)
    
    print(f"STATUS: {status_msg}")

def handle_commit(args):
    # Execute git commit with gate check
    try:
        # Pre-commit Gate Check: Security Scanner
        scanner_path = os.path.join(os.path.dirname(__file__), "security_scanner.py")
        if os.path.exists(scanner_path):
            try:
                subprocess.run(["python", scanner_path, "--path", args.project_dir], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"STATUS: COMMIT_BLOCKED (Security Check Failed:\n{e.stderr})")
                return

        # check if git repo exists
        if not os.path.exists(os.path.join(args.project_dir, ".git")):
            subprocess.run(["git", "init"], cwd=args.project_dir, check=True, capture_output=True)
        
        # Add files safely (excluding .env and keys)
        subprocess.run(["git", "add", "."], cwd=args.project_dir, check=True, capture_output=True)
        # Unstage sensitive files if accidentally added
        subprocess.run(["git", "reset", "HEAD", "--", ".env", "*.pem", "*.key"], cwd=args.project_dir, capture_output=True)
        
        subprocess.run(["git", "commit", "-m", args.message], cwd=args.project_dir, check=True, capture_output=True)
        print("STATUS: COMMIT_SUCCESS")
    except subprocess.CalledProcessError as e:
        print(f"STATUS: COMMIT_FAILED (No changes to commit or git error)")

def handle_status(args):
    state = load_state(args.project_dir)
    print(f"STATUS: {state['status']}")
    print(json.dumps(state, indent=2))

def main():
    parser = argparse.ArgumentParser(description="DQA Driven Dev Team - Workflow Controller")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    parser_fail = subparsers.add_parser("record_failure")
    parser_fail.add_argument("project_dir")
    parser_fail.add_argument("task_id")
    
    parser_commit = subparsers.add_parser("commit")
    parser_commit.add_argument("project_dir")
    parser_commit.add_argument("message")
    
    parser_status = subparsers.add_parser("status")
    parser_status.add_argument("project_dir")
    
    args = parser.parse_args()
    
    if args.command == "record_failure":
        handle_record_failure(args)
    elif args.command == "commit":
        handle_commit(args)
    elif args.command == "status":
        handle_status(args)

if __name__ == "__main__":
    main()
