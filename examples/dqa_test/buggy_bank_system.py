import threading
import time

class BankAccount:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        # BUG: 沒有使用 threading.Lock() 來保護 balance (Race Condition)

    def withdraw(self, amount):
        # BUG: 缺乏邊界值檢查 (沒有檢查 amount 是否大於 balance 或是否為負數)
        print(f"嘗試提款: {amount}")
        
        # 模擬讀取餘額的時間延遲
        current_balance = self.balance
        time.sleep(0.1) 
        
        # 寫回餘額
        self.balance = current_balance - amount
        print(f"提款完成，剩餘餘額: {self.balance}")

def run_test():
    print("--- 啟動銀行系統測試 ---")
    account = BankAccount(100)
    
    def worker():
        account.withdraw(80)

    # 模擬兩個人同時從同一個帳戶提款 80 元
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"--- 最終餘額: {account.balance} ---")
    
if __name__ == "__main__":
    run_test()
