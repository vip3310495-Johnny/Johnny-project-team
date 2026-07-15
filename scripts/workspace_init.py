#!/usr/bin/env python3
"""
workspace_init.py - Johnny-project-team 專案資料夾初始化腳本

用途：在 Phase 0 中被 PM 呼叫，自動建立專案所需的標準資料夾架構。
若資料夾已存在則跳過，確保在「專案恢復 (Resume)」場景下不會覆蓋舊檔案。

使用方式：
    python .agents/scripts/workspace_init.py [project_root]
    若不指定 project_root，則預設為目前工作目錄。
"""

import os
import sys
from datetime import datetime


# 標準專案資料夾架構
REQUIRED_DIRS = [
    "PM",
    "PM/Milestones",
    "Architect",
    "SDD_DQA",
    "SDD_DQA/tool",
    "TDD_DQA",
    "TDD_DQA/tool",
    "Logs",
    "src",
]

# 初始化時需要建立的空白檔案 (僅在不存在時建立)
INITIAL_FILES = {
    "Logs/Master_Log.md": (
        "# Master Log\n\n"
        f"- **專案初始化時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    ),
}


def init_workspace(project_root: str) -> None:
    """建立標準專案資料夾架構。"""
    print(f"🏗️  正在初始化專案工作區：{os.path.abspath(project_root)}")
    print("=" * 60)

    created_dirs = []
    skipped_dirs = []

    for dir_path in REQUIRED_DIRS:
        full_path = os.path.join(project_root, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            created_dirs.append(dir_path)
            print(f"  ✅ 建立資料夾：{dir_path}/")
        else:
            skipped_dirs.append(dir_path)
            print(f"  ⏭️  已存在，跳過：{dir_path}/")

    print()

    created_files = []
    for file_path, content in INITIAL_FILES.items():
        full_path = os.path.join(project_root, file_path)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            created_files.append(file_path)
            print(f"  📄 建立檔案：{file_path}")
        else:
            print(f"  ⏭️  已存在，跳過：{file_path}")

    print()
    print("=" * 60)
    print(f"📊 結果：建立 {len(created_dirs)} 個資料夾, {len(created_files)} 個檔案")
    print(f"         跳過 {len(skipped_dirs)} 個已存在的資料夾")
    print("✨ 工作區初始化完成！")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    init_workspace(root)
