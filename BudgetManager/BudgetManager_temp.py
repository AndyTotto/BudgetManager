import sqlite3
import tkinter as tk
import os

# DBに接続
def open_db():
    # pyファイルと同階層を指定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "budget.db")

    # dbファイルに接続
    conn = sqlite3.connect(db_path)

    # (無い場合)テーブルutilitiesを作成
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS utilities (
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            electricity_cost INTEGER,
            gas_cost INTEGER,
            water_cost INTEGER, 
            PRIMARY KEY (year, month)
        )
        '''
    )

    return conn

# データの全件取得
def select_db(conn):
    rows = conn.execute(('''
                    SELECT year, month, electricity_cost, gas_cost, water_cost
                    FROM utilities
                    ORDER BY year DESC, month DESC
                    '''))
    #for row in rows:
    #    print(row[0], row[1],row[2], row[3], row[4])
    
    return rows

def create_main_window(conn):
    utilities_data = select_db(conn)

    # ウィンドウ作成
    root = tk.Tk()
    root.title("utilities")

    headers = ['Year', 'Month', 'Electricity Cost', 'Gas Cost', 'Water Cost']
    # 「光熱費」
    label_popup = tk.Label(root, text="光熱費", font=("Arial", 10, "bold"))
    label_popup.grid(row=0, column=0, columnspan=len(headers), pady=5)
    # ヘッダー定義
    for col, header in enumerate(headers):
        label = tk.Label(root, text=header, font=("Arial", 10, "bold"))
        label.grid(row=1, column=col, padx=1, pady=1)
    # 表示内容
    for row, data in enumerate(utilities_data):
        for col, data_num in enumerate(data):
            label = tk.Label(root, text=data_num, font=("Arial", 10, "bold"))
            label.grid(row=row+2, column=col, padx=0, pady=0)

    # 入力ボタン
    submit_button = tk.Button(root, text="入力", command=lambda: create_input_form(conn))
    submit_button.grid(row=row+3, column=0, columnspan=len(headers), pady=10)
    
    return root

def create_input_form(conn):
    # ウィンドウ作成
    input_form = tk.Toplevel()
    input_form.title("utilities submit form")

    # ヘッダー定義
    headers = ['Year', 'Month', 'Electricity Cost', 'Gas Cost', 'Water Cost']
    for col, header in enumerate(headers):
        label = tk.Label(input_form, text=header, font=("Arial", 10, "bold"))
        label.grid(row=0, column=col, padx=5, pady=5)
    
    # エントリーウィジェットを格納するリスト
    entries = []
    # 12行の入力フォーム作成
    for row_i in range(1, 13):
        row_entries = []
        for column_j in range(len(headers)):
            entry = tk.Entry(input_form, width=12)
            entry.grid(row=row_i, column=column_j, padx=1, pady=1)
            row_entries.append(entry)
        entries.append(row_entries)
    
    # 登録ボタン
    submit_button = tk.Button(input_form, text="登録", command=lambda: submit_data(entries, input_form))
    submit_button.grid(row=13, column=0, columnspan=len(headers), pady=10)

    return root

def submit_data(entries, input_form):
    entry_data = []

    for row_entries in entries:
        skip_this_row = False
        for entry in row_entries:
            if entry.get() == "":
                skip_this_row = True
                break
        if skip_this_row:
            continue

        year = row_entries[0].get()
        month = row_entries[1].get()
        electricity = row_entries[2].get()
        gas = row_entries[3].get()
        water = row_entries[4].get()

        insert_db(year, month, electricity, gas, water)
        print(year, month, electricity, gas, water)
        entry_data.append([year, month, electricity, gas, water])

    create_popup_window(input_form, entry_data)

# データの挿入
def insert_db(year, month, electricity, gas, water):
    # データの挿入
    conn.execute("INSERT OR REPLACE INTO utilities (year, month, electricity_cost, gas_cost, water_cost) VALUES (?, ?, ?, ?, ?)",
                  (year, month, electricity, gas, water))

    # 変更内容をコミット
    conn.commit()

def create_popup_window(input_form, entry_data):
    # ウィンドウ作成
    popup = tk.Toplevel()
    popup.title("submit complete")

    # 出力内容
    headers = ['Year', 'Month', 'Electricity Cost', 'Gas Cost', 'Water Cost']
    # 「登録完了」
    label_popup = tk.Label(popup, text="登録完了", font=("Arial", 10, "bold"))
    label_popup.grid(row=0, column=0, columnspan=len(headers), pady=10)
    # ヘッダー
    for col, header in enumerate(headers):
        label = tk.Label(popup, text=header, font=("Arial", 10, "bold"))
        label.grid(row=1, column=col, padx=5, pady=5)
    # 登録内容
    for row, data in enumerate(entry_data):
        for col, num in enumerate(data):
            label = tk.Label(popup, text=num, font=("Arial", 10, "bold"))
            label.grid(row=row+2, column=col, padx=5, pady=5)

    popup_button = tk.Button(popup, text="OK", command=lambda: close_window(popup, input_form))
    popup_button.grid(row=len(entry_data)+2, column=0, columnspan=len(headers), pady=10)

    return popup

def close_window(popup, input_form):
    popup.destroy()
    input_form.destroy()

if __name__ == '__main__':
    # DBに接続
    with open_db() as conn:
        # GUI起動
        root = create_main_window(conn)
        root.mainloop()
