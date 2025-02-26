import tkinter as tk

def create_window():
    # window・ウィジェット作成

    root = tk.Tk()
    root.title("Tkinter Sample")

    # ラベルの作成と配置
    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=10)

    # ボタンの作成と配置
    # ラムダを使ってon_button_clickにラベルを渡す
    button = tk.Button(root, text="Click Me", command=lambda: on_button_click(label))
    # button = tk.Button(root, text="Click Me", command=on_button_click(label))
    button.pack(pady=10)

    return root

def on_button_click(label):
    # クリック時の動作
    label.config(text="Button clicked!")

def start_main_loop(root):
    # メインループ開始(ユーザー入力待機状態)
    root.mainloop()

if __name__ == "__main__":
    root = create_window()
    start_main_loop(root)

