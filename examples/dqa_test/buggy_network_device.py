import time
import random

class IoTDeviceParser:
    def parse_packet(self, data):
        # BUG: 沒有 try-except 例外處理 (可靠性與動態自癒)
        # 如果收到不完整的封包，會直接報錯 Crash
        header, payload = data.split(':')
        if len(payload) != 5:
            raise ValueError("Payload length mismatch")
        return payload

class IoTDevice:
    def __init__(self):
        self.connected = False
        self.parser = IoTDeviceParser()

    def connect(self):
        print("設備嘗試連線中...")
        # 模擬網路不穩定 (網路應力與弱網模擬)
        if random.random() < 0.5:
            # BUG: 遇到 Timeout 沒有 Retry 機制，直接拋出 Exception 卡死
            raise TimeoutError("連線超時，無回應")
        self.connected = True
        print("設備連線成功")

    def receive_data(self, packet):
        print(f"收到封包: {packet}")
        try:
            parsed = self.parser.parse_packet(packet)
            print(f"解析成功: {parsed}")
        except Exception as e:
            # 這裡雖然有抓例外，但這是模擬外層，如果 Parser 直接 crash 且不回傳狀態，會影響後續業務
            print(f"處理封包時發生未預期錯誤: {e}")
            raise e

def run_test():
    device = IoTDevice()
    print("--- 測試網路連線 ---")
    try:
        device.connect()
    except Exception as e:
        print(f"系統崩潰: {e}")
        return # 直接結束

    print("--- 測試接收畸形封包 ---")
    bad_packet = "DATA" # 故意少掉冒號，這會讓 split(':') 失敗
    try:
        device.receive_data(bad_packet)
    except Exception as e:
        print(f"系統崩潰: {e}")

if __name__ == "__main__":
    run_test()
