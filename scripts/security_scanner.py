import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="Scan files for hardcoded secrets.")
    parser.add_argument("--path", default=".", help="Directory or file to scan")
    args = parser.parse_args()

    patterns = {
        "AWS Access Key": r"(?i)AKIA[0-9A-Z]{16}",
        "Google API Key": r"(?i)AIza[0-9A-Za-z-_]{35}",
        "GitHub Token": r"(?i)gh[p|u|s|o|r]_[a-zA-Z0-9]{36}",
        "Slack Token": r"(?i)xox[baprs]-[0-9a-zA-Z]{10,48}",
        "Stripe Key": r"(?i)sk_(live|test)_[0-9a-zA-Z]{24}",
        "Generic Secret/Token": r"(?i)(password|secret|token|api_key|apikey)[\s]*[:=][\s]*[\'\"][A-Za-z0-9\-_]{8,}[\'\"]"
    }
    
    multi_line_patterns = {
        "Private Key": r"(?s)-----BEGIN.*?PRIVATE KEY-----.*?-----END.*?PRIVATE KEY-----"
    }

    found_issues = False
    
    for root, dirs, files in os.walk(args.path):
        if ".git" in root or "node_modules" in root or "venv" in root or ".agents" in root:
            continue
        for file in files:
            is_env = file == ".env" or file.startswith(".env.")
            valid_ext = file.endswith(('.js', '.ts', '.py', '.go', '.java', '.json', '.yml', '.yaml', '.txt', '.pem', '.key', '.cfg', '.ini', '.sh', '.properties'))
            if not (is_env or valid_ext):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # 1. Single-line check
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        for key, pattern in patterns.items():
                            if re.search(pattern, line):
                                print(f"🚨 [Security Alert] Hardcoded {key} found in {filepath} (Line {i+1})")
                                print(f"   => {line.strip()}")
                                found_issues = True
                                
                    # 2. Multi-line check
                    for key, pattern in multi_line_patterns.items():
                        if re.search(pattern, content):
                            print(f"🚨 [Security Alert] Multi-line {key} found in {filepath}")
                            found_issues = True
            except Exception:
                pass
                
    if found_issues:
        print("\n❌ Security Check FAILED: Hardcoded secrets detected. Please remove them and use Environment Variables.", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ Security Check PASSED: No hardcoded secrets found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
