import sys
import os
import argparse

try:
    import cv2
    import numpy as np
    from skimage.metrics import structural_similarity as ssim
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

def evaluate_ui_similarity(mockup_path, screenshot_path, threshold=0.90):
    if not HAS_DEPS:
        print("[警告] 系統未安裝 opencv-python 或 scikit-image，啟動模擬模式。")
        print("請執行: pip install opencv-python scikit-image numpy 來啟用真實影像比對。")
        print("--------------------------------------------------")
        print("[模擬運算中...] 正在模擬比對像素結構...")
        # 模擬模式：回傳固定的失敗結果供展示
        sim_score = 0.82 
        return sim_score, sim_score >= threshold

    # 讀取圖片並轉為灰階
    mockup = cv2.imread(mockup_path, cv2.IMREAD_GRAYSCALE)
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)

    if mockup is None or screenshot is None:
        print(f"[錯誤] 無法讀取圖片檔案，請確認 {mockup_path} 與 {screenshot_path} 存在。")
        print("將啟動降級模擬模式展示...")
        sim_score = 0.82
        return sim_score, sim_score >= threshold

    # 強制將截圖縮放至 mockup 的解析度以便比對 (實務上可能需要 Feature Matching 或 AI 對齊)
    screenshot_resized = cv2.resize(screenshot, (mockup.shape[1], mockup.shape[0]))

    # 計算 SSIM
    score, diff = ssim(mockup, screenshot_resized, full=True)
    
    # 產出差異圖 (Diff Map)
    diff = (diff * 255).astype("uint8")
    diff_inv = cv2.bitwise_not(diff)
    diff_map_path = "diff_map_output.png"
    cv2.imwrite(diff_map_path, diff_inv)
    print(f"[VRT 引擎] 差異熱區圖 (Diff Map) 已產出: {diff_map_path}")

    return score, score >= threshold

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Visual Regression Tester using SSIM")
    parser.add_argument("--mockup", default="mockup_reference.png", help="PM 提供的設計原圖")
    parser.add_argument("--screenshot", default="frontend_screenshot.png", help="前端實作的截圖")
    parser.add_argument("--threshold", type=float, default=0.90, help="及格閾值 (0.0~1.0)")
    args = parser.parse_args()

    print("==================================================")
    print("DQA Agent - 前端 UI/UX 視覺回歸審查 (VRT) 引擎")
    print("==================================================\n")
    print(f"比對目標: {args.screenshot} (實作) vs {args.mockup} (設計圖)")
    print(f"嚴格標準: SSIM >= {args.threshold * 100}%\n")

    score, passed = evaluate_ui_similarity(args.mockup, args.screenshot, args.threshold)

    print(f"[檢測結果] 結構相似度 (SSIM) 分數: {score * 100:.2f}%")
    
    if passed:
        print("判定: PASS - UI 還原度達標，放行！")
    else:
        print("判定: REJECT - UI 還原度不足，退件！")
        print("\n[Action Item] @前端工程師：實作畫面與設計圖存在明顯落差！請比對 Diff Map，修正元件排版與間距後重新提交審查。")
