import time

class OTAUpdater:
    def __init__(self):
        self.firmware_version = "v1.0"
        self.is_bricked = False

    def start_update(self, new_firmware):
        print(f"目前版本: {self.firmware_version}")
        print(f"開始下載並安裝新版本: {new_firmware}")
        
        try:
            self._download_and_flash()
            self.firmware_version = new_firmware
            print("升級成功")
        except Exception as e:
            print(f"升級失敗: {e}")
            # BUG: 沒有 Rollback 機制 (Compatibility & Deployment)
            # 升級中斷後，系統處於未完成狀態，無法開機 (變磚)
            self.is_bricked = True
            print("系統已毀損 (變磚)")

    def _download_and_flash(self):
        print("正在抹除舊韌體...")
        time.sleep(0.5)
        print("正在寫入新韌體 (20%)...")
        time.sleep(0.5)
        # 模擬升級中途斷線或斷電
        raise ConnectionError("寫入中途失去連線/斷電")

def run_test():
    updater = OTAUpdater()
    print("--- 測試 OTA 升級 ---")
    updater.start_update("v2.0")
    
    if updater.is_bricked:
        print("致命錯誤: 設備無法使用")

if __name__ == "__main__":
    run_test()
