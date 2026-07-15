import time
import queue
import threading

class HardwareController:
    def __init__(self):
        # BUG: 極值應力 (Stress Testing)
        # Queue 沒有設定 maxsize，當硬體中斷頻率大於處理速度時，會造成記憶體耗盡 (OOM)
        # 或處理緒因為 Queue 過大而拖慢整個系統，無法 Fail-Safe。
        self.interrupt_queue = queue.Queue()
        self.is_running = True

    def hardware_interrupt_handler(self, event_data):
        # 模擬底層硬體高速發送中斷
        self.interrupt_queue.put(event_data)

    def process_loop(self):
        while self.is_running:
            try:
                # 模擬處理硬體事件較慢
                event = self.interrupt_queue.get(timeout=0.1)
                time.sleep(0.01) # 每個事件處理需 10ms
            except queue.Empty:
                pass

def run_test():
    ctrl = HardwareController()
    t = threading.Thread(target=ctrl.process_loop)
    t.start()
    
    print("--- 測試硬體控制器 (極值應力) ---")
    print("模擬硬體發生異常，以極高頻率 (1ms) 狂發中斷...")
    
    start_time = time.time()
    for i in range(5000):
        # 產生速度遠大於消耗速度 (1ms 產生 vs 10ms 消耗)
        ctrl.hardware_interrupt_handler(f"Event_{i}")
        time.sleep(0.001) 
        
    print(f"產生完畢。目前 Queue 積壓未處理事件數量: {ctrl.interrupt_queue.qsize()}")
    print("問題：若長時間運行，記憶體將會耗盡 (OOM) 導致整個系統死機。")
    
    ctrl.is_running = False
    t.join()

if __name__ == "__main__":
    run_test()
