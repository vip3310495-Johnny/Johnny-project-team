# TDD 整合規範 (TDD Integration & Red-Green-Refactor)

本專案強烈要求工程師遵守 TDD (Test-Driven Development) 開發模式。
所有開發任務必須遵循以下循環：

## 1. RED (撰寫失敗的測試)
- Engineer 必須先根據 DQA 規劃的 `Mock_Data.json` 與測試計畫，撰寫自動化測試腳本。
- 此階段的測試執行結果必須是**失敗 (RED)**，藉此驗證測試案例本身具備捕捉 Bug 的能力。

## 2. GREEN (實作最低限度功能)
- Engineer 實作最少量的產品代碼，唯一目標是讓剛剛寫的測試腳本順利通過。
- 禁止在此階段進行過度設計 (Over-engineering)。

## 3. REFACTOR (重構與收斂)
- 當測試通過後 (GREEN)，Engineer 必須回頭檢視代碼。
- 發動 Code Simplifier 消除死代碼 (Dead Code)、移除不必要的相依性。
- 確保時間與空間複雜度達到最佳狀態。

## 4. DQA 80% 覆蓋率大關
- Engineer 完成開發後，必須確保本地端測試覆蓋率達到 80% 以上。
- 若覆蓋率未達 80%，TDD DQA 將會在 Phase 3 的第一關直接亮紅燈退件。
- PM **不具備**覆蓋率特批權限，此為系統硬性規範。

## 5. Silent Failure 獵殺
- TDD 必須特別針對「靜默錯誤」進行防護。
- 凡是使用 `try...except` 或 `catch` 捕捉異常時，必須明確記錄日誌 (Logging) 或向外拋出對應的錯誤狀態碼。
- 空的 catch block 將直接被視為不合格代碼。
