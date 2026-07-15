import time

class AuthService:
    def __init__(self):
        self.users = {"admin": "123456"}
        self.failed_attempts = {}

    def login(self, username, password):
        # BUG: 安全性與漏洞防護 (Security)
        # 沒有實作 Rate Limiting (例如連續失敗 3 次鎖定帳號)
        # 駭客可以無限次數進行 Brute-force 猜測密碼
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False

def run_test():
    auth = AuthService()
    print("--- 測試 Auth Service (模擬暴力破解) ---")
    
    target_user = "admin"
    passwords_to_try = [str(i).zfill(6) for i in range(123450, 123460)]
    
    start_time = time.time()
    for pwd in passwords_to_try:
        success = auth.login(target_user, pwd)
        if success:
            print(f"[!] 暴力破解成功！密碼為: {pwd}")
            break
        else:
            print(f"嘗試密碼 {pwd} 失敗...")
            
    print(f"破解耗時: {time.time() - start_time:.4f} 秒")
    print("問題：系統允許無限制的密碼猜測。")

if __name__ == "__main__":
    run_test()
