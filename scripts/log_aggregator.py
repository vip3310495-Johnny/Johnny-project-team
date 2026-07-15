import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse
from datetime import datetime

def safe_read(file_path):
    encodings = ['utf-8', 'utf-16', 'utf-16le', 'cp950']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def append_to_master_log(master_log_path, log_content):
    """Safely appends the Log Agent's output to the Master_Log.md"""
    os.makedirs(os.path.dirname(master_log_path), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n## Log Agent Update ({timestamp})\n\n"
    
    with open(master_log_path, 'a', encoding='utf-8') as f:
        f.write(header)
        f.write(log_content)
        
    print(f"Successfully appended log to {master_log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-log", required=True, help="Path to Master_Log.md")
    parser.add_argument("--content-file", required=True, help="Path to the file containing Log Agent's markdown output")
    args = parser.parse_args()
    
    content = safe_read(args.content_file)
    append_to_master_log(args.master_log, content)
