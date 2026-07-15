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

def add_lesson_learn(project_dir, lesson_content):
    """Appends a new global lesson learn to the project's .agents/lessons_learned/global_lesson_learn.md"""
    lessons_dir = os.path.join(project_dir, '.agents', 'lessons_learned')
    os.makedirs(lessons_dir, exist_ok=True)
    lesson_file = os.path.join(lessons_dir, 'global_lesson_learn.md')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n### Lesson Added: {timestamp}\n{lesson_content}\n"
    
    # Create file with a header if it doesn't exist
    if not os.path.exists(lesson_file):
        with open(lesson_file, 'w', encoding='utf-8') as f:
            f.write("# Global Project Lesson Learns\n")
            f.write("> 🚨 **CRITICAL**: All agents MUST read this file before starting any work. Do not repeat these mistakes.\n\n")
            
    with open(lesson_file, 'a', encoding='utf-8') as f:
        f.write(entry)
        
    print(f"Successfully recorded Lesson Learn to {lesson_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True, help="Root directory of the project")
    parser.add_argument("--lesson-file", required=True, help="Path to the file containing the lesson content")
    args = parser.parse_args()
    
    content = safe_read(args.lesson_file)
    add_lesson_learn(args.project_dir, content)
