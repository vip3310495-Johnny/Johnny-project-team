# Phase 1: Milestone 執行拆解與微觀規劃 (Milestone Detailed Planning)

本階段發生在 Phase 0 確立全局架構，或是前一個 Milestone 剛執行完畢之時。
PM 必須將抽象的「全局目標」具體轉化為工程師與 DQA 能立刻動手的「微觀規格」。

## 1. 鎖定當前 Milestone
- PM 必須讀取 `PM/PRD.md` (全局 PRD)。
- 找出目前尚未完成的下一個 Milestone (例如：`Milestone 2: User Authentication`)。
- **邊界確認**：明確定義這個 Milestone 的範圍 (In-Scope) 與不做的部分 (Out-of-Scope)。

## 2. 撰寫 Milestone 專屬 PRD
- PM 針對這個選定的 Milestone，撰寫一份詳細的 `Milestone_PRD.md` (建議存放在 `PM/Milestones/M<N>_PRD.md`)。
- 內容必須包含：
  - 核心 User Stories。
  - 需要實作的 UI 畫面與互動邏輯 (精確描述)。
  - 需要串接的後端 API 或資料存取邏輯。

## 3. Architect 微觀架構設計 (Component Design)
- PM 必須呼叫 **Architect Agent**，針對 `Milestone_PRD.md` 進行微觀架構設計。
- Architect 必須輸出以下內容：
  - **資料結構 (Data Schema)**：定義關聯式資料庫的 Table 或是 NoSQL 的 Document 結構。
  - **API 規格約定 (API Contracts)**：定義前端與後端的 Request/Response JSON 格式。
  - **元件樹 (Component Tree)**：若是前端專案，定義要切解多少個 React/Vue Components。

## 4. 準備進入測試驅動規劃 (Transition to Phase 2)
- 當 PM 與 Architect 產出完整的微觀規劃後：
  - **若該 Milestone 包含前端 UI 畫面或重大業務邏輯變更**：PM **必須**將 `Milestone_PRD.md` 呈報 CEO 確認，確保微觀規格與 CEO 的想像一致。若 CEO 提出修改意見，PM 須修改後重新確認。只有 CEO 明確同意後，才可進入 Phase 2。
  - **若該 Milestone 為純後端/基礎設施/無 UI 變更**：PM 無須額外詢問 CEO，可直接帶領團隊進入 **Phase 2 (DQA Planning & Boundary Handshake)**，讓 DQA 開始依據這份 `Milestone_PRD.md` 制定測試計畫。
