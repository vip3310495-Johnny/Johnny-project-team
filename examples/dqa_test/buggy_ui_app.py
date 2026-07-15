class DummyUIApp:
    def __init__(self):
        self.data_store = ["Data1", "Data2", "Data3"]
        self.memory_leak_list = []

    def handle_user_input(self, action):
        if action == "delete_all":
            # BUG: 易用性與用戶體驗 (Usability)
            # 破壞性操作缺乏二次確認，直接刪除所有資料
            self.data_store.clear()
            print("資料已全數刪除！(未跳出防呆確認)")
            
        elif action == "load_images":
            # BUG: 效能與資源容量 (Performance)
            # 模擬連續點擊時的 Memory Leak
            for _ in range(10000):
                self.memory_leak_list.append("Image_Data_Buffer" * 100)
            print(f"載入圖片完成，目前記憶體佔用陣列長度: {len(self.memory_leak_list)}")

def run_test():
    app = DummyUIApp()
    print("--- 測試 UI 應用程式 ---")
    
    print("\n測試一：危險按鈕點擊")
    app.handle_user_input("delete_all")
    print(f"殘留資料: {app.data_store}")
    
    print("\n測試二：模擬使用者瘋狂點擊載入")
    for i in range(5):
        app.handle_user_input("load_images")
        
if __name__ == "__main__":
    run_test()
