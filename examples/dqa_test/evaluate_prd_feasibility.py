import os
import re

def evaluate_prd_feasibility(prd_content):
    """
    Evaluates a PRD based on the TEAM-U framework.
    T: Testability (Acceptance Criteria, Error Handling)
    E: Estimability (Clear specifics, no vague magic terms)
    A: Architecture (Dependencies, APIs, DB Schema)
    M: Measurability (SLA, performance limits)
    U: UI Feasibility (Mockups provided, physically/technically logical)
    """
    results = {
        "T_Testability": False,
        "E_Estimability": False,
        "A_Architecture": False,
        "M_Measurability": False,
        "U_UI_Feasibility": False,
        "UX_Experience": False,
        "Vague_Words_Found": []
    }
    feedback = []

    # Check T: Testability
    if re.search(r'(Acceptance Criteria|驗收標準|Error Handling|例外處理)', prd_content, re.IGNORECASE):
        results["T_Testability"] = True
    else:
        feedback.append("[T-FAIL] 缺乏『驗收標準』或『例外處理』定義，DQA 無法設計測試案例。")

    # Check E: Estimability
    vague_words = ['智慧', '自動', '很方便', '很酷', '大概', '看情況']
    found_vague = [word for word in vague_words if word in prd_content]
    if len(found_vague) > 2:
        results["Vague_Words_Found"] = found_vague
        feedback.append(f"[E-FAIL] 需求包含太多模糊字眼 ({', '.join(found_vague)})，工程師無法精確估算工時。")
    else:
        results["E_Estimability"] = True

    # Check A: Architecture
    if re.search(r'(API|Database|Schema|第三方|Third-party|架構)', prd_content, re.IGNORECASE):
        results["A_Architecture"] = True
    else:
        feedback.append("[A-FAIL] 未定義任何外部依賴、API 規格或系統架構，RD 無法開工。")

    # Check M: Measurability
    if re.search(r'(SLA|毫秒|ms|QPS|TPS|效能指標|秒)', prd_content, re.IGNORECASE):
        results["M_Measurability"] = True
    else:
        feedback.append("[M-FAIL] 未定義任何量化的效能指標 (SLA)，無法進行壓力測試。")

    # Check U: UI Feasibility
    has_ui_images = re.search(r'(!\[.*?\]\(.*?\)|附圖|Mockup|Figma)', prd_content, re.IGNORECASE)
    has_impossible_ui = re.search(r'(3D 懸浮投影|隔空滑動|心電感應|腦波)', prd_content, re.IGNORECASE)
    
    if not has_ui_images:
        feedback.append("[U-FAIL] 未提供任何 UI Mockup 圖面供審視，請 PM 補齊參考圖。")
    elif has_impossible_ui:
        feedback.append("[U-FAIL] UI 設計要求極難在當前標準前端框架下實作 (檢測到不切實際的渲染要求)，實務技術風險過高。")
    else:
        results["U_UI_Feasibility"] = True

    # Check UX: vibe-pm-agent Experience Gatekeeping
    # Using insights from hicks_law_calculator, poka_yoke_validator, progressive_disclosure_evaluator
    ux_issues = []
    
    # 1. Hick's Law & Progressive Disclosure Check (Too many options)
    options_match = re.search(r'(顯示|包含|提供|有).*?([1-9][0-9]+)\s*個.*?(選項|按鈕|功能)', prd_content)
    if options_match:
        count = int(options_match.group(2))
        if count > 7:
            ux_issues.append(f"違反希克定律 (Hick's Law)：單一畫面超過 7 個選項 ({count} 個)，會導致決策癱瘓。請改用漸進式揭示 (Progressive Disclosure) 設計。")

    # 2. Poka-Yoke (Mistake-proofing) Check
    destructive_no_confirm = re.search(r'(立刻刪除|直接刪除|不囉嗦|不需確認).*?(帳號|資料|檔案)|(刪除|覆蓋).*?(立刻|直接|不需確認)', prd_content, re.IGNORECASE)
    if destructive_no_confirm:
        ux_issues.append("違反防呆機制 (Poka-Yoke)：破壞性操作 (如刪除帳號) 缺乏二次確認與安全防護機制，極易引發災難性客訴。")
        
    if ux_issues:
        for issue in ux_issues:
            feedback.append(f"[UX-FAIL] {issue}")
    else:
        results["UX_Experience"] = True

    return results, feedback

if __name__ == "__main__":
    prd_path = "vague_prd_plan.md"
    
    if not os.path.exists(prd_path):
        print(f"Error: {prd_path} not found.")
        exit(1)

    print("==================================================")
    print("DQA Agent - TEAM-U PRD 可行性評估系統啟動")
    print("==================================================\n")
    
    with open(prd_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    results, feedback = evaluate_prd_feasibility(content)
    
    print(f"Target: {prd_path}\n")
    
    passed = all([results["T_Testability"], results["E_Estimability"], results["A_Architecture"], results["M_Measurability"], results["U_UI_Feasibility"], results["UX_Experience"]])
    
    if passed:
        print("[結果] PASS - 審查通過")
        print("PRD 符合 TEAM-UX 框架要求，可以放行給 Engineering Team。")
    else:
        print("[結果] REJECT - 退件")
        print("原因清單：")
        for fb in feedback:
            print(f"  - {fb}")
            
        print("\n[Action Item] @專案PM：請根據上述退件原因重新修訂 PRD，補充相關細節與 UI 圖面後再次提交審查。")
