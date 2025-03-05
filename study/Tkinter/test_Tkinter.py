import tkinter as tk

# window・ウィジェット作成
def create_window():

    root = tk.Tk()
    root.title("Tkinter Sample")

    # ラベルの作成と配置
    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=10)

    # ボタンの作成と配置
    # ラムダを使ってon_button_clickにラベルを渡す
    button = tk.Button(root, text="Click Me", command=lambda: on_button_click(label))
    button.pack(pady=10)

    return root

# ボタンクリック時の動作
def on_button_click(label):
    label.config(text="Button clicked!")

# メインループ開始(ユーザー入力待機状態)
def start_main_loop(root):
    root.mainloop()

if __name__ == "__main__":
    # window・ウィジェット作成
    root = create_window()
    # メインループ開始(ユーザー入力待機状態)
    start_main_loop(root)

