import sqlite3

def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE users (username text, password text)''')
    c.execute("INSERT INTO users VALUES ('admin', 'supersecret')")
    conn.commit()
    return conn

def login(conn, username, password):
    c = conn.cursor()
    # BUG 1: SQL Injection vulnerability (Security)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"Executing query: {query}")
    
    try:
        c.execute(query)
        result = c.fetchone()
        if result:
            print("登入成功")
        else:
            print("登入失敗")
    except Exception as e:
        # BUG 2: Bad Logging (Serviceability)
        # 只印出 Exception，沒有 Error Code、沒有 Timestamp、沒有 Request Context
        print(f"Error occurred")

def run_test():
    print("--- 測試 Web API ---")
    conn = init_db()
    
    print("\n正常登入測試:")
    login(conn, 'admin', 'supersecret')
    
    print("\nSQL Injection 攻擊測試:")
    login(conn, 'admin', "' OR '1'='1")

if __name__ == "__main__":
    run_test()
