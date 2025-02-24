import sqlite3
import os

def open_db():
    # pyファイルと同階層を指定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "example.db")

    # dbファイルに接続
    conn = sqlite3.connect(db_path)
    return conn

def init_db(conn):
    # 既存の users テーブルがあれば削除する
    conn.execute("DROP TABLE IF EXISTS users")

    # テーブル users を作成
    conn.execute(
        '''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
        '''
    )

def insert_db(conn):
    # サンプルデータの挿入
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))

    conn.commit()

def select_db(conn):
    # データの全件取得
    rows = conn.execute(("SELECT id, name, age FROM users"))
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

if __name__ == '__main__':
    with open_db() as conn:
        init_db(conn)
        insert_db(conn)
        select_db(conn)
    