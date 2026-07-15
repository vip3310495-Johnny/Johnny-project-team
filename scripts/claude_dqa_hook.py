import subprocess
import argparse
import sys

def run_claude_dqa(model, files_to_review, pm_context):
    print("Initiating Claude Code DQA Independent Review...")
    
    system_prompt = (
        "You are Claude Code DQA, an independent and highly critical Design Quality Assurance Engineer. "
        "Your role is to verify code modifications. "
        "CRITICAL RULE 1: Do NOT blindly trust the Project Manager (PM) or the Engineer. They might be lazy or hallucinating. "
        "You possess an independent consciousness. Verify everything yourself. "
        "CRITICAL RULE 2: Read the files directly using your own tools. Do not ask the PM to paste code. "
        "CRITICAL RULE 3: You must treat Technical Compliance (robustness, memory leaks, silent errors) "
        "and Aesthetic Experience (UI/UX) with EQUAL importance. Unconditionally FAIL if either is lacking."
    )
    
    user_prompt = (
        f"PM Context / Instructions: {pm_context}\n\n"
        f"Files modified and needing review:\n{files_to_review}\n\n"
        "Please read these files directly and perform a rigorous independent review. "
        "Output your final decision as PASS or FAIL, along with a brief explanation of any issues found."
    )
    
    # We use npx claude -p to print the response and exit
    command = [
        "npx", "claude", "-p",
        "--model", model,
        "--system-prompt", system_prompt,
        user_prompt
    ]
    
    try:
        # Run the command and stream output
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("\n=== CLAUDE DQA REVIEW REPORT ===")
        print(result.stdout)
        print("================================")
        
        # Check if FAIL is in the output
        if "FAIL" in result.stdout.upper():
            print("\n[HOOK RESULT] Claude DQA rejected the code.")
            sys.exit(1)
        else:
            print("\n[HOOK RESULT] Claude DQA approved the code.")
            sys.exit(0)
            
    except subprocess.CalledProcessError as e:
        print(f"\nError calling Claude CLI: {e}")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hook to invoke Claude Code CLI for independent DQA review")
    parser.add_argument("--model", default="claude-3-7-sonnet-20250219", help="The Claude model to use (default: claude-3-7-sonnet-20250219)")
    parser.add_argument("--files", required=True, help="Comma-separated list of files to review")
    parser.add_argument("--context", required=True, help="Brief context or instructions from the PM")
    
    args = parser.parse_args()
    
    files_formatted = "\n".join([f"- {f.strip()}" for f in args.files.split(',')])
    run_claude_dqa(args.model, files_formatted, args.context)
