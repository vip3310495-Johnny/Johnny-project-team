import json

class DataPipeline:
    def process_data(self, raw_data_list):
        processed_data = []
        for data in raw_data_list:
            try:
                # 模擬 JSON 解析與轉換
                parsed = json.loads(data)
                processed = {"id": parsed["id"], "value": int(parsed["val"]) * 2}
                processed_data.append(processed)
            except Exception as e:
                # BUG: 功能性驗證 (Functionality)
                # 遇到異常格式資料時，沒有報錯，也沒有放入 Dead Letter Queue，直接默默丟棄 (Silent Drop)
                pass 
                
        return processed_data

def run_test():
    pipeline = DataPipeline()
    print("--- 測試 Data Pipeline ---")
    
    raw_inputs = [
        '{"id": 1, "val": "10"}',
        '{"id": 2, "val": "20"}',
        '{"id": 3, "val": "ABC"}', # 惡意/錯誤格式資料
        '{"id": 4, "val": "40"}'
    ]
    
    print(f"輸入資料筆數: {len(raw_inputs)}")
    result = pipeline.process_data(raw_inputs)
    print(f"成功處理筆數: {len(result)}")
    print(f"處理結果: {result}")
    print("問題：有 1 筆資料憑空消失了，沒有留下任何追蹤紀錄。")

if __name__ == "__main__":
    run_test()
