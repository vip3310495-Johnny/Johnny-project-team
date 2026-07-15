import os
import sys
import argparse
import re
import json

DEFAULT_POLICY = {
    "banned_commands": [r"rm\s+(?:-\w*\s+)*-[rR]*[fF]+(?:\s+-\w+)*\s+/[*\s]*", r"rm\s+(?:-\w*\s+)*-[rR]*[fF]+(?:\s+-\w+)*\s+~[*\s]*", r"mkfs", r"dd\s+if=/dev/zero"],
    "banned_paths": ["~/.ssh", "/etc/shadow", "/etc/passwd", ".env", "secrets.json"],
    "banned_patterns": [
        r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['\"\`]?[A-Za-z0-9_-]{16,}['\"\`]?", # Hardcoded secrets (quotes optional)
        r"aws_access_key_id\s*=\s*['\"\`]?[A-Z0-9]{20}['\"\`]?",
        r"ghp_[a-zA-Z0-9]{36}"
    ]
}

def load_policy(target_dir):
    policy_path = os.path.join(target_dir, 'org_security_policy.json')
    if os.path.exists(policy_path):
        try:
            with open(policy_path, 'r', encoding='utf-8') as f:
                user_policy = json.load(f)
                
            # Merge policies
            merged = DEFAULT_POLICY.copy()
            if "banned_commands" in user_policy:
                merged["banned_commands"].extend(user_policy["banned_commands"])
            if "banned_paths" in user_policy:
                merged["banned_paths"].extend(user_policy["banned_paths"])
            if "banned_patterns" in user_policy:
                merged["banned_patterns"].extend(user_policy["banned_patterns"])
            return merged
        except Exception as e:
            print(f">> [AgentShield] 無法載入 {policy_path}: {e}")
    return DEFAULT_POLICY

def scan_file(filepath, policy):
    findings = []
    
    # Extension filter and exact directory name filter (skip binary and node_modules)
    parts = filepath.replace('\\', '/').split('/')
    if "node_modules" in parts or filepath.endswith((".png", ".jpg", ".zip", ".exe", ".dll", ".pdf", ".tar", ".gz")):
        return findings

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return findings

    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # 1. Check banned patterns (Secrets)
        for pattern in policy.get("banned_patterns", []):
            if re.search(pattern, line):
                snippet = line.strip()[:80]
                findings.append(f"{filepath}:{line_num} [CRITICAL] 偵測到疑似硬編碼機密 (Hardcoded Secret)。\n    -> Snippet: {snippet}")
                
        # 2. Check banned paths
        for path in policy.get("banned_paths", []):
            escaped_path = re.escape(path)
            # Match path enclosed in quotes/backticks, ensuring it aligns with a path boundary
            if re.search(r"['\"\`](?:[^'\"\`]*[/\\])?" + escaped_path + r"['\"\`]", line) or re.search(r"cat\s*[<\s]\s*" + escaped_path, line):
                snippet = line.strip()[:80]
                findings.append(f"{filepath}:{line_num} [HIGH] 試圖存取高敏感受保護路徑: {path}\n    -> Snippet: {snippet}")
                
        # 3. Check banned commands
        for cmd in policy.get("banned_commands", []):
            try:
                if re.search(cmd, line):
                    snippet = line.strip()[:80]
                    findings.append(f"{filepath}:{line_num} [FATAL] 偵測到毀滅性系統指令: {cmd}\n    -> Snippet: {snippet}")
            except re.error:
                if cmd in line: # Fallback to string match if not a valid regex
                    snippet = line.strip()[:80]
                    findings.append(f"{filepath}:{line_num} [FATAL] 偵測到毀滅性系統指令: {cmd}\n    -> Snippet: {snippet}")
                
    return findings

def scan_directory(target_dir, policy):
    all_findings = []
    for root, dirs, files in os.walk(target_dir):
        # Skip git and agents directory for scanning speed
        parts = root.replace('\\', '/').split('/')
        if '.git' in parts or '.agents' in parts or '.gemini' in parts:
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            all_findings.extend(scan_file(filepath, policy))
            
    return all_findings

def main():
    parser = argparse.ArgumentParser(description="AgentShield Static Security Hook")
    parser.add_argument("--target", default=".", help="Target directory to scan (default: current directory)")
    args = parser.parse_args()
    
    print(">> [AgentShield] 正在啟動靜態安檢 (Static Security Audit)...")
    
    policy = load_policy(args.target)
    
    findings = scan_directory(args.target, policy)
    
    if not findings:
        print(">> [AgentShield] ✅ 安檢通過，未發現安全風險。")
        sys.exit(0)
    else:
        print(">> [AgentShield] 🚨 發現安全漏洞 (SARIF/Audit Failed):")
        for finding in findings:
            print(f"  - {finding}")
        print("\n>> [ACTION_REQUIRED] 工程師，請立即提供 Autofix 修正這些漏洞，並重新執行此腳本。否則禁止提交給 DQA。")
        sys.exit(1)

if __name__ == "__main__":
    main()
