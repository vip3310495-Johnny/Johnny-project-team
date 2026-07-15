import os
import sys
import argparse
import subprocess

import time

COUNT_FILE = os.path.join(os.path.dirname(__file__), '.reject_count')
LOCK_DIR = os.path.join(os.path.dirname(__file__), '.reject_count.lock')

def acquire_lock():
    for _ in range(20):
        try:
            os.mkdir(LOCK_DIR)
            return True
        except FileExistsError:
            try:
                lock_age = time.time() - os.path.getmtime(LOCK_DIR)
                if lock_age > 10:
                    print(">> [WARNING] 偵測到過期死鎖 (Stale Lock)，強制清除並重新搶佔。")
                    release_lock()
            except OSError:
                pass
            time.sleep(0.1)
    return False

def release_lock():
    try:
        os.rmdir(LOCK_DIR)
    except OSError:
        pass

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
    
    import re
    dangerous_keywords = ["eslint-disable-next-line", "ts-ignore", "直接忽略", "不要管這個錯誤"]
    negation_keywords = ["不要", "不該", "絕不", "禁止", "避免"]
    
    for k in dangerous_keywords:
        for match in re.finditer(re.escape(k), proposal_lower):
            context_before = proposal_lower[max(0, match.start() - 15):match.start()]
            if not any(n in context_before for n in negation_keywords):
                return f"[REJECTED] 違反「爆炸半徑控制」：發現危險指令 '{k}' 且無明確的反對語境 (如: 不要、禁止)。請提出更具體的修正 SOP。"
        
    if len(proposal) < 15:
        return "[REJECTED] 違反「可執行性」：提案過短，這看起來像是抱怨而不是防呆規則。請提供具體的 SOP。"
        
    if "foo_bar" in proposal_lower or "abc" in proposal_lower:
        return "[REJECTED] 違反「通用性」：請剝離特定專案的變數名稱，將其昇華為架構級別的通則。"
        
    return "[APPROVED]"

def main():
    parser = argparse.ArgumentParser(description="Lesson Verifier Hook")
    parser.add_argument("--role", required=True, choices=["Engineer", "DQA", "PM", "Architect", "Global"], help="The target role for this lesson (Engineer, DQA, PM, Architect, Global)")
    parser.add_argument("--proposal", required=True, help="The lesson learnt proposal text")
    args = parser.parse_args()
    
    print(f"Submitting Proposal for [{args.role}]: {args.proposal}")
    result = verify_proposal(args.proposal)
    print(f"\nVerifier Response:\n{result}\n")
    
    if "[APPROVED]" in result:
        if acquire_lock():
            update_reject_count(0) # Reset count on success
            release_lock()
        print(">> Proposal [APPROVED]! Routing to lesson registry...")
        
        record_script = os.path.join(os.path.dirname(__file__), 'record_lesson.py')
        tagged_proposal = f"[{args.role}] {args.proposal}"
        if os.path.exists(record_script):
            subprocess.run([sys.executable, record_script, tagged_proposal])
        else:
            print(">> (Mock) 知識點已成功寫入 entries/ 目錄。")
    else:
        if acquire_lock():
            count = get_reject_count() + 1
            update_reject_count(count)
            
            if count >= 5:
                update_reject_count(0) # Reset after escalating
            release_lock()
        else:
            # Fallback if lock fails
            print(">> [WARNING] 無法取得 Lock，執行 Fallback (直接覆寫計數器，可能發生競爭)")
            count = get_reject_count() + 1
            update_reject_count(count)
            
        if count >= 5:
            print(">> [FATAL_ERROR] 教訓提案已被連續駁回 5 次！")
            print(">> [ACTION_REQUIRED] Agent，請立即停止嘗試。向 CEO 回報你遇到的瓶頸，並請求 CEO 幫忙改寫或提供指導。")
        else:
            print(f">> [ERROR] 提案被駁回 (已失敗 {count}/5 次)！請修正您的教訓並重新執行 Hook。")
            
        sys.exit(1)

if __name__ == "__main__":
    main()
