import sys
import os
import argparse
import re

def count_words_and_chars(text):
    # Remove markdown formatting characters for a fairer count, though simple length is safer
    clean_text = re.sub(r'[#*`\->]', '', text)
    # Remove whitespaces
    clean_text = re.sub(r'\s+', '', clean_text)
    return len(clean_text)

def main():
    parser = argparse.ArgumentParser(description="PM Context Compressor (ECC Enforcer)")
    parser.add_argument("file_path", help="Path to the Milestone Digest markdown file")
    args = parser.parse_args()

    abs_path = os.path.abspath(args.file_path)

    if not os.path.exists(abs_path):
        print(f"Error: File '{abs_path}' not found.")
        sys.exit(1)

    # 1. Check if it's in PM/Memory/
    if not (os.path.sep + "PM" + os.path.sep + "Memory" in abs_path or 
            "/PM/Memory" in abs_path.replace("\\", "/")):
        print("\n========================================")
        print(" [RED LIGHT] 路徑違規 (Path Violation)")
        print("========================================")
        print("錯誤：Digest 檔案必須統一存放在 `/PM/Memory/` 目錄下！")
        print(f"當前路徑：{abs_path}")
        print("請建立目錄並移動檔案後重試。")
        sys.exit(1)

    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Check word/character count
    total_length = count_words_and_chars(content)
    MAX_LIMIT = 800

    if total_length > MAX_LIMIT:
        print("\n========================================")
        print(" [RED LIGHT] 上下文爆炸警告 (Context Explosion Detected)")
        print("========================================")
        print(f"錯誤：您的摘要太長了！當前有效字數為 {total_length} 字，超過上限 {MAX_LIMIT} 字。")
        print("PM 的記憶體非常寶貴。請刪除流水帳與瑣碎的 Bug 修復過程，")
        print("只保留最重要的「架構變更」、「技術債」與「依賴關係」。")
        print("請將內容壓縮後再次執行此檢查。")
        sys.exit(1)

    print("\n========================================")
    print(" [GREEN LIGHT] 記憶壓縮成功！(Memory Compressed)")
    print("========================================")
    print(f"文件 '{os.path.basename(abs_path)}' (共 {total_length} 字) 已封存。")
    print("【系統提示】您可以安全跳轉至下一個 Milestone。")
    print("【認知防火牆啟動】從現在開始，請依賴此文件作為唯一的真實記憶，停止回想先前的對話歷史。")
    sys.exit(0)

if __name__ == "__main__":
    main()
