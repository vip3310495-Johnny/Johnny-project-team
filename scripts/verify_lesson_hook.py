import os
import sys
import argparse
import subprocess

COUNT_FILE = os.path.join(os.path.dirname(__file__), '.reject_count')

def get_reject_count():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def update_reject_count(count):
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))

def verify_proposal(proposal):
    print(">> Waking up Lesson Verifier Subagent...")
    
    guideline_path = os.path.join(os.path.dirname(__file__), '../references/verifier-guidelines.md')
    if os.path.exists(guideline_path):
        with open(guideline_path, 'r', encoding='utf-8') as f:
            guidelines = f.read()
    
    proposal_lower = proposal.lower()
    
    if "eslint-disable" in proposal_lower or "ignore" in proposal_lower or "忽略" in proposal_lower or "不准寫" in proposal_lower:
        return "[REJECTED] 違反「爆炸半徑控制」：此規則可能導致過度防禦或掩蓋潛在錯誤，請提出更具體的修正 SOP，而非直接忽略。"
        
    if len(proposal) < 15:
        return "[REJECTED] 違反「可執行性」：提案過短，這看起來像是抱怨而不是防呆規則。請提供具體的 SOP。"
        
    if "foo_bar" in proposal_lower or "abc" in proposal_lower:
        return "[REJECTED] 違反「通用性」：請剝離特定專案的變數名稱，將其昇華為架構級別的通則。"
        
    return "[APPROVED]"

def main():
    parser = argparse.ArgumentParser(description="Lesson Verifier Hook")
    parser.add_argument("--proposal", required=True, help="The lesson learnt proposal text")
    args = parser.parse_args()
    
    print(f"Submitting Proposal: {args.proposal}")
    result = verify_proposal(args.proposal)
    print(f"\nVerifier Response:\n{result}\n")
    
    if "[APPROVED]" in result:
        update_reject_count(0) # Reset count on success
        print(">> Proposal [APPROVED]! Routing to lesson registry...")
        
        record_script = os.path.join(os.path.dirname(__file__), 'record_lesson.py')
        if os.path.exists(record_script):
            subprocess.run([sys.executable, record_script, args.proposal])
        else:
            print(">> (Mock) 知識點已成功寫入 entries/ 目錄。")
    else:
        count = get_reject_count() + 1
        update_reject_count(count)
        
        if count >= 5:
            update_reject_count(0) # Reset after escalating
            print(">> [FATAL_ERROR] 教訓提案已被連續駁回 5 次！")
            print(">> [ACTION_REQUIRED] Agent，請立即停止嘗試。向 CEO 回報你遇到的瓶頸，並請求 CEO 幫忙改寫或提供指導。")
        else:
            print(f">> [ERROR] 提案被駁回 (已失敗 {count}/5 次)！請修正您的教訓並重新執行 Hook。")
            
        sys.exit(1)

if __name__ == "__main__":
    main()
