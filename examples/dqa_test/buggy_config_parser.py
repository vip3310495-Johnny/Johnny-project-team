import json

class ConfigParser:
    def __init__(self):
        # 假設這是新版系統的預期結構
        self.default_config = {
            "version": 2,
            "theme": "dark",
            "advanced_features": {"enabled": True, "cache_size": 1024}
        }

    def load_config(self, config_str):
        # BUG: 相容性與升級回滾 (Compatibility)
        # 未考量向後相容性，讀到 V1 版的設定檔時沒有做欄位補齊
        # 直接存取 advanced_features 會導致 KeyError Crash
        config = json.loads(config_str)
        
        print(f"載入設定檔版本: {config.get('version', 'Unknown')}")
        
        # 這裡會直接 Crash
        if config["advanced_features"]["enabled"]:
            print("啟用進階功能。")
        else:
            print("停用進階功能。")

def run_test():
    parser = ConfigParser()
    print("--- 測試設定檔相容性 ---")
    
    # 模擬軟體升級後，硬碟裡還殘留著舊版 (V1) 的設定檔
    old_v1_config = '{"version": 1, "theme": "light"}'
    
    try:
        parser.load_config(old_v1_config)
    except Exception as e:
        print(f"系統崩潰 (向後相容性測試失敗): {type(e).__name__} - {e}")
        print("問題：讀取舊版設定檔時未給予預設值，直接造成系統崩潰。")

if __name__ == "__main__":
    run_test()
