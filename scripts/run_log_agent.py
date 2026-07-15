import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse
import subprocess

def run_pipeline(project_dir, transcript_path):
    print("?? Starting Log Agent Observability Pipeline...")
    
    # 1. Extract Trace
    logs_dir = os.path.join(project_dir, 'Logs')
    raw_traces_dir = os.path.join(logs_dir, 'raw_traces')
    trace_output = os.path.join(raw_traces_dir, 'latest_trace.json')
    
    extractor_script = os.path.join(os.path.dirname(__file__), 'trace_extractor.py')
    print(f"Step 1: Extracting trace to {trace_output}")
    
    try:
        subprocess.run(["python", extractor_script, "--transcript", transcript_path, "--output", trace_output], check=True)
    except Exception as e:
        print(f"Failed to extract trace: {e}")
        return
        
    # 2. Instructions for next steps
    print("\n? Trace extracted! The Log Agent (LLM) should now:")
    print("   1. Read the trace file (latest_trace.json)")
    print("   2. Generate a markdown report (e.g. Logs/temp_report.md)")
    print("   3. Generate a lesson learn (e.g. Logs/temp_lesson.md) if applicable.")
    print("\nAfter generation, the system should use:")
    print("   - log_aggregator.py to save the report to Master_Log.md")
    print("   - lesson_learn_manager.py to save the lesson to Lesson_Learn.md")

def find_latest_transcript():
    brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
    if not os.path.exists(brain_dir):
        return None
        
    latest_time = 0
    latest_transcript = None
    
    for conv_id in os.listdir(brain_dir):
        transcript_path = os.path.join(brain_dir, conv_id, ".system_generated", "logs", "transcript.jsonl")
        if os.path.exists(transcript_path):
            mtime = os.path.getmtime(transcript_path)
            if mtime > latest_time:
                latest_time = mtime
                latest_transcript = transcript_path
                
    return latest_transcript

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", help="Root directory of the project (defaults to current dir)")
    parser.add_argument("--transcript", help="Path to transcript.jsonl (defaults to auto-detect latest)")
    args = parser.parse_args()
    
    project_dir = args.project_dir if args.project_dir else os.getcwd()
    transcript = args.transcript
    
    if not transcript:
        transcript = find_latest_transcript()
        if not transcript:
            print("Error: Could not automatically locate the latest Gemini transcript.")
            exit(1)
        print(f"Auto-detected transcript at: {transcript}")
        
    run_pipeline(project_dir, transcript)
