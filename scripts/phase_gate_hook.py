import sys
import os
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Universal Phase Gate Hook")
    parser.add_argument("--from_phase", required=True, help="The current phase exiting")
    parser.add_argument("--to_phase", required=True, help="The target phase entering")
    parser.add_argument("--auto", action="store_true", help="Enable fully automated mode (skips CEO check)")
    parser.add_argument("--ceo_signature", help="The exact command typed by the CEO")
    parser.add_argument("--prd_path", help="Path to the PRD file (required if jumping from Phase 2 to 3)")
    args = parser.parse_args()

    print(f"\n========================================")
    print(f" [PHASE GATE] Requesting jump from Phase {args.from_phase} to Phase {args.to_phase}")
    print(f"========================================")

    errors = []

    # 1. CEO Signature Check
    if not args.auto:
        if args.ceo_signature != "/approve":
            errors.append(f"=> CEO 簽核失敗: 預期收到 '/approve'，但收到 '{args.ceo_signature}'。")
            errors.append("=> PM 必須主動向 CEO 說明：「請輸入 /approve 進行授權」。")
    else:
        print("[INFO] 已啟用全自動模式 (--auto)，自動核准 CEO 簽核。")

    # 2. SDD DQA Check (Only needed when moving from Phase 2 to Phase 3)
    if args.from_phase == "2" and args.to_phase == "3":
        if not args.prd_path or not os.path.exists(args.prd_path):
            errors.append(f"=> SDD DQA 簽核失敗: 找不到 Milestone PRD 檔案 ({args.prd_path})。")
        else:
            with open(args.prd_path, 'r', encoding='utf-8') as f:
                content = f.read()
            auth_section_match = re.search(r'##\s*授權狀態\s*\(Authorization Status\)(.*?)(?:##|\Z)', content, re.DOTALL | re.IGNORECASE)
            
            if not auth_section_match:
                errors.append(f"=> SDD DQA 簽核失敗: 找不到 `## 授權狀態` 區塊。")
            else:
                auth_content = auth_section_match.group(1)
                dqa_approved = bool(re.search(r'-\s*\[[xX]\]\s*SDD DQA', auth_content, re.IGNORECASE))
                if not dqa_approved:
                    errors.append("=> SDD DQA 尚未簽核 `[ ] SDD DQA 授權同意`。")

    if errors:
        print("\n========================================")
        print(" [RED LIGHT] 階段跳轉攔截 (Transition Blocked)")
        print("========================================")
        for error in errors:
            print(error)
        print("========================================")
        print("請補齊條件後再重新執行本跳轉指令。")
        sys.exit(1)

    print("\n========================================")
    print(" [GREEN LIGHT] 階段跳轉核准 (Transition Granted)")
    print("========================================")
    print(f"准許進入 Phase {args.to_phase}。")
    sys.exit(0)

if __name__ == "__main__":
    main()
