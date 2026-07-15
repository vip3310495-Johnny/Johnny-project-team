import os
import subprocess
import argparse
import sys

def run_command(command_list):
    try:
        result = subprocess.run(command_list, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command_list)}")
        print(e.stderr)
        sys.exit(1)

def get_latest_tag():
    try:
        tags = run_command(["git", "tag", "--sort=-v:refname"])
        if not tags:
            return "v0.0.0"
        return tags.split('\n')[0]
    except:
        return "v0.0.0"

def increment_version(latest_tag, bump_type):
    tag = latest_tag.lstrip('v')
    parts = tag.split('.')
    if len(parts) != 3:
        parts = ['0', '0', '0']
    
    major, minor, patch = map(int, parts)
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    else: # patch
        patch += 1
        
    return f"v{major}.{minor}.{patch}"

def release(bump_type, message):
    print("Initiating release process...")
    
    # Check if branch is clean
    status = run_command(["git", "status", "--porcelain"])
    if status:
        print("Working directory is not clean. Please commit changes before releasing.")
        sys.exit(1)
        
    latest_tag = get_latest_tag()
    new_tag = increment_version(latest_tag, bump_type)
    
    print(f"Bumping version from {latest_tag} to {new_tag}")
    
    # Merge feature branch to main if we are on a feature branch
    current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if current_branch != "main" and current_branch != "master":
        print(f"Merging {current_branch} into main...")
        run_command(["git", "checkout", "main"])
        run_command(["git", "merge", current_branch, "--no-ff", "-m", f"Merge branch {current_branch}"])
    
    # Create Tag
    print(f"Creating tag {new_tag}...")
    run_command(["git", "tag", "-a", new_tag, "-m", message])
    
    # Push
    print("Pushing to remote...")
    run_command(["git", "push", "origin", "main"])
    run_command(["git", "push", "origin", "--tags"])
    
    print(f"Release {new_tag} successfully published!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure Release Manager for Antigravity PM Agent")
    parser.add_argument("--bump", choices=['major', 'minor', 'patch'], default='patch', help="Semantic version bump type")
    parser.add_argument("--message", required=True, help="Release message or changelog summary")
    
    args = parser.parse_args()
    release(args.bump, args.message)
