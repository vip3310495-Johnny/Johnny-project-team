# Phase 3: 開發與驗收循環 (The Chat Chain)

> **【中斷存檔提醒】** CEO 隨時可能下達「收工」或「暫停」等中斷指令。當收到該指令時，PM 必須立刻停止目前的開發迴圈，並觸發 `SKILL.md` 中定義的**中斷與存檔機制 (Interruption & Save State)**。

本階段為高頻率的實作與驗證循環，所有工作必須在獨立的 Feature 分支上進行。

## 1. 分支與開發前置
- Engineer 在獨立分支 (`feature/milestone-X`) 進行開發。
- 開發必須遵循 TDD 規範 (詳見 `references/tdd-integration.md`) 與終極戒律 (詳見 `references/engineering-agent.md`)。

## 2. Token Optimization (省 Token 留痕協議)
- **【強制規定】**所有 Agent 在聊天頻道中**禁止貼出大量程式碼**。
- 資訊傳遞一律採用「1-2句話解釋 + 檔案絕對路徑 (File Paths)」來回報進度與問題。

## 3. Smoke Test Barrier (工程師自檢防線)
- Engineer 準備交接給 DQA 之前，必須親自在終端機執行基礎建置或啟動指令 (如 `npm run build` 或 `npm start`)。
- **安全護欄 (AgentShield Self-Audit) [NEW]**：Engineer 必須在提交前強制執行 `python .agents/skills/Johnny-project-team/scripts/agent_shield_hook.py`。若掃描失敗 (紅燈)，工程師必須提供 Autofix 並重新掃描，絕對禁止將帶有安全漏洞或危險指令的程式碼交給 DQA。
- **防偷工減料 (Execution Verification)**：Engineer 必須透過 `ls` 證明檔案確實成功產生。若連基本編譯都會 Crash，嚴禁交接。
- **編譯自救方案**：若工程師遇到編譯失敗，PM 必須強制配發對應語言的 Build Resolver (位於 `references/ecc_agents/`，例如 `react-build-resolver.md`、`python-build-resolver.md`) 給工程師，要求其依照 RCA 流程排錯，嚴禁盲目試錯。

## 4. 單線程審查佇列 (Queue Manager)
- 當 Engineer 完工後，PM 必須透過 `scripts/dqa_queue_manager.py` 進行排隊。
- 系統保證一次只送審一位工程師的程式碼，徹底防堵 Git Merge Hell。
- **佇列死鎖防護 (Queue Lock Prevention)**：若 DQA 退回程式碼，必須同時呼叫 `finish` 指令釋放該次審查佇列，讓其他排隊中的工程師進入。該被退回的工程師修復完畢後，必須重新排隊。

## 5. 測試與串聯審查 (Sequential Review)
當輪到某程式碼審查時，流程如下：
1. **DQA 靜態審查 (Static Review)**：PM 指示 DQA 讀取對應語言的 Reviewer (位於 `references/ecc_agents/`，例如 `react-reviewer.md`、`python-reviewer.md`、`go-reviewer.md`)，對交接的程式碼進行靜態抓漏。若有架構問題直接退回。
2. **TE 執行工具**：指派 TE 執行 DQA 撰寫好的動態測試工具。**(注意：TE 必須嚴格遵守 `references/te-persona.md` 的禁令，禁止自己改 Code，只能輸出 JSON 報告)**。
3. **DQA Test Stalemate**：DQA 必須保證自己的腳本無語法錯誤。若修復腳本失敗超過 3 次，視為 Test Stalemate，交由 PM 處理。
4. **TDD DQA 第一關 (理科把關)**：
   - 確保測試 100% 通過且覆蓋率達 80%。
   - 使用 `references/dqa-analysis.md` 核對靜默錯誤、記憶體洩漏等易錯點。
   - **【動態運行強制令與 Docker 沙盒隔離 (Docker Sandbox Mandate)】**：絕對禁止只做靜態看 Code 分析，也**絕對禁止**直接在本地終端機 (Host OS) 下達任何執行指令 (如 `python test.py` 或 `npm test`)。
   - TDD DQA 必須且只能透過 Docker 容器來掛載執行測試指令，將所有潛在破壞行為 (爆炸半徑) 封死在虛擬貨櫃內。
     - *指令範例*：`docker run --rm -v ${PWD}:/app -w /app node:18 npm test` 或 `docker run --rm -v ${PWD}:/app -w /app python:3.9 pytest`
   - 若失敗，亮紅燈 (RED LIGHT) 直接退回。
5. **SDD DQA 第二關 (文科把關)**：
   - TDD 通過後，SDD 進行視覺對齊、A11y (無障礙) 審查與業務邏輯驗證。
   - **【規格合規性確認】**：SDD DQA 必須嚴格比對產品實作是否 100% 吻合當前 Milestone 的 PRD 與 Spec。若有任何遺漏或實作與 Spec 描述不符之處，立即退回。
   - **【動態體驗驗證 (Computer Use 整合)】**：絕對禁止只看截圖。SDD DQA 必須優先嘗試使用以下工具輔助測試：
     - 若為 Web 專案：使用 `gstack` (極速無頭瀏覽器) 實際開啟網頁、點擊按鈕、填寫表單。
     - 跨平台 UI 解析：強制呼叫 `omniparser` 來解析產品的螢幕截圖，取得所有按鈕、圖示的精確 Bounding Box (邊界框) 座標，判斷是否破版或對齊。
     - **若為非瀏覽器 (如 Native App / Desktop 軟體)**：`omniparser` 依然能精準解析任何截圖的 UI 元素。針對操作，SDD DQA 應利用 Python 的 `pyautogui`、`appium` 等自動化工具，配合 `omniparser` 回傳的座標進行實體游標點擊與輸入。
     - **【優雅降級 (Graceful Degradation)】**：若上述外部工具未安裝，SDD DQA 必須自動切換至替代方案，不得因此卡住流程：
       - `gstack` 未安裝 → 改用 `generate_image` 截取畫面 + 視覺分析能力進行 UI 審查。
       - `omniparser` 未安裝 → 改用目視比對方式審查 UI 對齊與破版，並在報告中註明「未使用自動化 UI 解析」。
   - **【邊緣狀態與微交互 (Vibe Review)】**：針對前端/UI 專案，SDD DQA 必須無情獵殺缺乏「Loading 狀態」、「無資料 (Empty) 狀態」與「Error 狀態」的裸奔畫面；並確保所有按鈕與連結都具備符合高質感 (Vibe) 的 Hover/Active 微動畫回饋。

6. **Claude Code DQA 第三關 (外部獨立核查) [選配]**：
   - **【優雅降級】**：若未安裝 Claude Code CLI (`npx claude`)，PM 可跳過此關，以內部的 TDD + SDD 雙關審查作為最終防線。但須在 `Logs/Master_Log.md` 中記錄「已跳過外部獨立核查」。
   - 當本地的 TDD 與 SDD DQA 都給予綠燈後，PM 必須呼叫 `scripts/claude_dqa_hook.py`，將修改的檔案路徑交給外部的 Claude Code CLI 進行最終獨立審查。
   - **獨立意識**：Claude DQA 被嚴格設定為「不可輕信 PM 說的話」。它會親自去讀取專案檔案，用它強大的模型心智 (預設為最新的 `claude-3-7-sonnet`) 進行二次抓漏。
   - 只有當 Claude DQA 也回傳 PASS 時，這段程式碼才算真正通過測試。

## 6. 僵局裁決 (Stalemate Escalate)
- 若 Engineer 提交的代碼被 DQA 退回超過 **5 次**，觸發僵局。
- PM 強制暫停開發，撰寫 `Conflict_Report.md`，交由 CEO 進行最終裁決。
- **【PM 反推卸責任 (Anti-Buck-Passing)】**：PM 必須提出結構化的 Option A / Option B 給 CEO 選擇，絕對禁止直接把錯誤丟給 CEO 去敲指令。

## 7. 合併與大腦清洗
- **GREEN LIGHT**：若全數通過，PM 將分支合併回 `main` (若有衝突，Engineer 必須手動解衝突，詳見 `git-strategy.md`)。
- **知識匯流 (Knowledge Merge) [CRITICAL]**：在 `kill` Agent 之前，PM **必須先**讀取 `.agents/lessons_learned/` 目錄中各 Agent 的個人筆記 (如 `engineering_lesson_learn.md`、`dqa_lessons_learned.md`)，將有價值的踩坑經驗提煉合併至團隊統一知識庫 `Logs/lesson_learnt_registry.md`。這是防止 Agent 被回收後，個人記憶永久消失的最後防線。
- **Context Window Reset**：大型 Milestone 結束後，PM 必須強制 `kill` 掉舊的 Engineer 與 DQA，並 `invoke` 新的 Agent 以避免大腦幻覺。
- **知識繼承**：PM 確認知識已匯流完畢後，宣告該 Milestone 完成。新 `invoke` 的 Agent 只需讀取 `Logs/lesson_learnt_registry.md` 即可獲得完整的團隊記憶。

## 8. 狀態跳轉 (State Transition)
Milestone 結束後，PM 必須檢視 `PM/PRD.md` 中的 Milestone 清單：
- 若**還有未完成的 Milestone** ➔ PM 必須跳回 **Phase 1 (Milestone Detailed Planning)**，開始拆解下一個任務。
- 若**所有 Milestone 皆已完成** ➔ PM 必須推進至 **Phase 4 (Final Acceptance & Release)**，準備系統驗收。
