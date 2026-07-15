# Phase 0: Initialization, Recovery & Deep Planning

This phase establishes the project environment, recovers context from previous sessions, and generates the formal development plan using deep thinking methodologies.

## Step 1: Context Recovery (Resume vs. New)
Before creating any plans or initializing Git, the PM MUST check for existing project data:
1. **Check for Save State [CRITICAL]**: Read `Logs/Save_State.md` (if it exists). 這是最精準的甦醒恢復點。
2. **Check for PRD**: Read `PM/PRD.md` (if it exists).
3. **Check for Logs**: Read `Logs/Master_Log.md` (if it exists).
- **If Save_State.md or PRD exists**: This is a **Resumed Project**. PM 必須向 CEO 宣告：「發現專案已存在，啟動狀態檢視...判定應跳轉至 Phase X」。讀取 `Save_State.md` 或 `Master_Log.md`，精準掌握專案中斷前的 Milestone 狀態。
  - **[CRITICAL JUMP]**: 一旦確認為 Resumed Project，**PM 必須立刻中斷 Phase 0 的後續所有步驟 (Step 2~8)**，根據存檔紀錄直接去讀取目標 Phase 的文件 (如 `phase1.md` 或 `phase3.md`) 並開始工作。絕對禁止重跑一次新專案的架構審查流程。
- **If they do not exist**: This is a **Brand New Project**. 宣告啟動新專案，並繼續往下執行 Step 2。

## Step 2: Environment Initialization
For a new project, the PM MUST initialize the environment:
1. **Git Initialization**: Execute `git init` to initialize version control.
2. **Workspace Scaffolding**: Execute `python .agents/scripts/workspace_init.py` to create the standard project folder structure (`PM/`, `Logs/`, `SDD_DQA/tool/`, `TDD_DQA/tool/`, `src/`, etc.). This script is idempotent — it will skip existing folders.
3. **Agent Toolkit Provisioning**: Copy the contents of this skill (`Johnny-project-team/scripts`, `references`, etc.) into the `.agents/` folder in the project root so all subagents can access the rules and hooks locally.

## Step 3: 制定全局防護網 (Establish Defense & Test Strategy)
PM 必須引導 DQA 與 Architect 共同制定全局的測試與觀測策略。
1. **Lesson Learn Bootstrap (知識繼承)**：讀取 `.agents/lessons_learned/DIGEST.md`（若不存在，執行 `python scripts/generate_digest.py` 產生）。**嚴禁**在 Phase 0 讀取 `entries/` 內任何單筆全文或整份 index，只吸收 DIGEST 的摘要層。若 DIGEST 中某條教訓與本次專案技術棧高度相關，可在 PRD 草案備註，留待後續 Phase 用 `query_lesson.py` 深查全文。
2. **Team & AI Model Composition [CRITICAL]**: PM 必須檢視目前系統可用的 LLM 模型，並**主動列表推薦** CEO 應該在哪些角色上使用哪種模型，絕對禁止只丟空白問題讓 CEO 盲選。
   - *推薦範例*：「建議 Architect 與 PM 使用推論最強的模型 (如 `Gemini 3.1 Pro`)」、「建議獨立審查官強制使用 Claude Code CLI (`claude-sonnet 5`)」。
   - PM 必須將這個「模型與角色適配推薦矩陣」呈現給 CEO 進行最終確認與微調。
3. **Clarification**: Ask the CEO for the core project goal and clarify ambiguities. Assume the CEO has NO engineering background; use simple logic.
4. **Global PRD Generation**: Based on the gathered context, the PM MUST draft a highly structured **Global PRD Draft** and save it to `PM/PRD.md`.
   - **注意：Phase 0 的 PRD 是一個針對系統面的「全局規格書」。在進入各個 Milestone 前，PM 才需要再提出該階段詳細的「開發細節計畫書」。**
   - The PRD Draft MUST include: Overview, Requirements & Assumptions, and **Milestone Breakdown** (If >=5 Milestones, mark as a "Complex Project").

## Step 4: UI/UX Exploration (If Applicable)
If the project involves a user interface:
1. Generate **3 distinct UI style mockups** using the `generate_image` tool (e.g., `PM/UI_Option_1.png`).
2. Present them to the CEO to choose the preferred visual direction.
3. Once the CEO selects a style, **DELETE the 2 unused UI mockups** from the folder.

## Step 5: Architect Review & System Flow Diagram
The PM MUST invoke the **Architect Agent** to review the PRD draft and chosen UI.
1. **Architect Review & Report**: The Architect evaluates technical trade-offs, creates formal **ADRs (Architecture Decision Records)**, and MUST output an audit report to `/Architect/` (e.g., `M1_Review_v1.md`).
2. **System Flow Diagram**: The Architect MUST draw a **程式系統流程圖 (System Flow Diagram)** using Mermaid syntax.
   - *Engineer Challenge Right*: This diagram guides Engineers. If they find it flawed during implementation, they have the right to request an Architect revision.

## Step 6: SDD & TDD DQA Pre-Audit
Before presenting to the CEO, the PM MUST involve the specialized DQA roles:
1. **SDD DQA (Spec-Driven Development DQA)**: 
   - Audits the PM's PRD, the Architect's System Flow Diagram, and the chosen UI mockups to ensure perfect alignment with the CEO's intent.
   - **視覺審查與技術可行性 (Visual & Feasibility Check)**: SDD DQA must view the generated UI mockups (e.g., using vision capabilities or screenshots). SDD DQA MUST evaluate if the UI is technically easy to achieve using standard frameworks. If the UI is overly complex or impractical, SDD DQA MUST raise a red flag and provide alternative, simpler suggestions.
   - **審查報告 (Audit Report)**: 審查結束後，SDD DQA 必須撰寫報告並存入 `/SDD_DQA/` (例如：`M1_Review_v1.md`)。
2. **TDD DQA (Test-Driven Development DQA)**: 
   - Based on the Architect's design and the visual mockups, formulates the **Global Testing Strategy** (Unit/Integration/E2E boundaries) and defines the **Product Telemetry & Log Design** (startup logs, error catching) to prevent runtime blind spots.
   - **極端邊界測試規劃 (Extreme Boundary Testing)**: 針對系統的極端或惡意輸入進行前置規劃防禦。
   - **審查報告 (Audit Report)**: 審查結束後，TDD DQA 必須撰寫報告並存入 `/TDD_DQA/` (例如：`M1_Review_v1.md`)。

## Step 7: Grill-Me Confirmation (Stop and Ask)
Before finalizing the Phase, the PM MUST:
1. Present the finalized PRD, the **System Flow Diagram**, ADRs, DQA strategies, and chosen UI to the CEO.
2. **Explicitly instruct the CEO**: "CEO，為了確保我們對產品規格、架構流程與設計決策有絕對的共識，請您使用 `/grill-me` slash command 或是呼叫 `grill-me` skill 來對這份計畫進行嚴格的盤問與規格確認。"
3. **[防呆逃生門]**: 若 CEO 陷入「無決斷力癱瘓」(例如反覆詢問還有沒有問題，陷入無限規劃迴圈)，PM 必須主動呼叫 `scripts/analysis_paralysis_breaker.py` 來強行打破僵局。
4. **[STOP AND WAIT]**: Pause execution immediately. Do not proceed until the CEO has explicitly approved the entire system plan via Grill-Me.

## Step 8: Milestone Review Preference (Stop and Ask)
ONLY AFTER the plan is fully approved via Grill-Me, the PM MUST ask the CEO how they want to review the upcoming milestones, precisely using the following format:
"How would you like to review the milestones? (A) Review after *every* milestone, (B) Review after *specific* milestones, or (C) Run fully automatically until Phase 4?"
- **CRITICAL RULE**: If you propose option (C), you MUST explicitly remind the CEO to reply using the `/goal` command (e.g., "`/goal 我選 C`"). Explain that without the `/goal` command, the agent might pause unexpectedly due to safety limits, so `/goal` is required for true overnight unattended execution. Record the preference.
