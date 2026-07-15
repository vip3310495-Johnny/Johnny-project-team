import subprocess
import sys
import os

SCRIPTS = [
    "buggy_bank_system.py",
    "buggy_network_device.py",
    "buggy_web_api.py",
    "buggy_ota_updater.py",
    "buggy_ui_app.py",
    "buggy_data_pipeline.py",
    "buggy_auth_service.py",
    "buggy_hardware_controller.py",
    "buggy_config_parser.py"
]

def run_tests():
    print("=" * 50)
    print("DQA 測試環境啟動 - 準備收集崩潰日誌")
    print("=" * 50)
    
    log_content = ""
    
    for script in SCRIPTS:
        print(f"\n執行腳本: {script}")
        log_content += f"\n{'='*20} 執行腳本: {script} {'='*20}\n"
        
        script_path = os.path.join(os.path.dirname(__file__), script)
        if not os.path.exists(script_path):
            print(f"錯誤: 找不到腳本 {script}")
            continue
            
        try:
            # 這裡我們設定 timeout 為 5 秒，防止 buggy_hardware_controller 或死鎖腳本卡死
            result = subprocess.run([sys.executable, script_path], 
                                    capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            print(output)
            log_content += output
            
            if result.returncode != 0:
                print(f"[!] 腳本 {script} 以非零狀態結束 (Crash)")
                log_content += f"\n[!] 腳本 {script} 以非零狀態結束 (Crash)\n"
                
        except subprocess.TimeoutExpired as e:
            msg = f"[!] 腳本執行超時 (可能發生死鎖或無窮迴圈): {e}"
            print(msg)
            log_content += msg + "\n"
        except Exception as e:
            msg = f"[!] 執行腳本發生預期外錯誤: {e}"
            print(msg)
            log_content += msg + "\n"

    # 將結果輸出到 log 檔案
    log_file_path = os.path.join(os.path.dirname(__file__), "dqa_execution.log")
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(log_content)
        
    print("=" * 50)
    print(f"測試執行完畢，所有日誌已儲存至: {log_file_path}")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()
