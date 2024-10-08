import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load CSV file
def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path, encoding='utf-8')
            messagebox.showinfo("파일 불러오기", "CSV 파일이 성공적으로 불러와졌습니다!")
            populate_user_listbox()  # 파일을 불러온 후 사용자 리스트를 업데이트
        except Exception as e:
            messagebox.showerror("오류", f"파일을 불러오는 중 오류가 발생했습니다: {e}")
    else:
        messagebox.showwarning("파일 선택", "파일을 선택하지 않았습니다.")

# Function to populate Listbox with unique users from the CSV
def populate_user_listbox():
    user_listbox.delete(0, tk.END)  # 기존 사용자 목록 초기화
    if 'df' in globals():
        unique_users = df['User'].unique()  # 사용자 리스트 생성
        for user in unique_users:
            user_listbox.insert(tk.END, user)  # Listbox에 사용자 추가

# Function to search messages by selected user from Listbox
def search_by_selected_user():
    selected_user = user_listbox.get(tk.ACTIVE)  # 선택한 사용자의 이름
    if 'df' in globals():
        result = df[df['User'].str.contains(selected_user, case=False, na=False)].sort_values(by='Date')
        if not result.empty:
            formatted_result = format_results(result)
            display_result(formatted_result)
        else:
            display_result("해당 사용자의 메시지를 찾을 수 없습니다.")
    else:
        messagebox.showwarning("파일 없음", "먼저 CSV 파일을 불러오세요.")

# Function to search messages by keyword
def search_by_keyword():
    keyword = keyword_entry.get()
    if 'df' in globals():
        result = df[df['Message'].str.contains(keyword, case=False, na=False)].sort_values(by='Date')
        if not result.empty:
            formatted_result = format_results(result)
            display_result(formatted_result)
        else:
            display_result("해당 키워드가 포함된 메시지를 찾을 수 없습니다.")
    else:
        messagebox.showwarning("파일 없음", "먼저 CSV 파일을 불러오세요.")

# Function to format the result for better readability
def format_results(result_df):
    formatted = ""
    for index, row in result_df.iterrows():
        formatted += f"Date: {row['Date']}\nUser: {row['User']}\nMessage: {row['Message']}\n{'-'*40}\n"
    return formatted

# Function to display result in the textbox
def display_result(result):
    result_textbox.delete(1.0, tk.END)  # Clear the textbox
    result_textbox.insert(tk.END, result)  # Display new result

# Create the main window
root = tk.Tk()
root.title("CSV 메시지 검색 프로그램")
root.geometry("800x600")

# Frame for file loading
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

# Load CSV button
load_button = tk.Button(file_frame, text="CSV 파일 불러오기", command=load_csv)
load_button.pack()

# Frame for user search and listbox
user_frame = tk.Frame(root)
user_frame.pack(pady=10)

# User listbox label
tk.Label(user_frame, text="사용자 선택").pack()

# Listbox for user selection
user_listbox = tk.Listbox(user_frame, height=6, width=50)
user_listbox.pack()

# Button to search selected user
user_search_button = tk.Button(user_frame, text="선택한 사용자로 검색", command=search_by_selected_user)
user_search_button.pack(pady=5)

# Frame for keyword search
keyword_frame = tk.Frame(root)
keyword_frame.pack(pady=10)

# Keyword search section
tk.Label(keyword_frame, text="키워드 검색").grid(row=0, column=0, padx=5)
keyword_entry = tk.Entry(keyword_frame)
keyword_entry.grid(row=0, column=1, padx=5)
keyword_search_button = tk.Button(keyword_frame, text="검색", command=search_by_keyword)
keyword_search_button.grid(row=0, column=2, padx=5)

# Textbox to display search results
result_textbox = tk.Text(root, height=20, width=80)
result_textbox.pack(pady=20)

# Start the GUI loop
root.mainloop()
