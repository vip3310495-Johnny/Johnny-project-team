import sys
import os
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Verify Milestone PRD Authorization Status")
    parser.add_argument("file_path", help="Path to the Milestone_PRD.md file")
    parser.add_argument("--auto", action="store_true", help="Enable fully automated mode (skips CEO check)")
    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' not found.")
        sys.exit(1)

    with open(args.file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find authorization section
    auth_section_match = re.search(r'##\s*授權狀態\s*\(Authorization Status\)(.*?)(?:##|\Z)', content, re.DOTALL | re.IGNORECASE)
    
    if not auth_section_match:
        print("\n========================================")
        print(" [RED LIGHT] 授權攔截 (Authorization Blocked)")
        print("========================================")
        print(f"錯誤：在 {args.file_path} 中找不到 `## 授權狀態 (Authorization Status)` 區塊。")
        print("請 PM 確認文件格式。")
        sys.exit(1)

    auth_content = auth_section_match.group(1)

    # Check SDD DQA
    # Matches '- [x] SDD DQA' ignoring case and spaces
    dqa_approved = bool(re.search(r'-\s*\[[xX]\]\s*SDD DQA', auth_content, re.IGNORECASE))
    
    # Check CEO
    ceo_approved = bool(re.search(r'-\s*\[[xX]\]\s*CEO', auth_content, re.IGNORECASE))

    errors = []

    if not dqa_approved:
        errors.append("=> SDD DQA 尚未簽核 `[ ] SDD DQA 授權同意`。")
    
    if not args.auto:
        if not ceo_approved:
            errors.append("=> CEO 尚未簽核 `[ ] CEO 授權同意`。(若為全自動模式，請加上 --auto 參數)")
    else:
        print("[INFO] 已啟用全自動模式 (--auto)，略過 CEO 簽核檢查。")

    if errors:
        print("\n========================================")
        print(" [RED LIGHT] 授權攔截 (Authorization Blocked)")
        print("========================================")
        for error in errors:
            print(error)
        print("========================================")
        print("請取得必要簽核 (將 [ ] 改為 [x]) 後再試一次。")
        sys.exit(1)

    print("\n========================================")
    print(" [GREEN LIGHT] 雙重授權檢查通過！(Authorization Granted)")
    print("========================================")
    print(f"文件 '{args.file_path}' 已具備足夠的簽核，准許進入 Phase 3 開發階段。")
    sys.exit(0)

if __name__ == "__main__":
    main()
