import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def format_with_hyphen(hash_str):
    return '-'.join([hash_str[i:i+2] for i in range(0, len(hash_str), 2)])

def calculate_hashes(file_path):
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)

    return format_with_hyphen(md5_hash.hexdigest()), format_with_hyphen(sha256_hash.hexdigest())

def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        file_path_label.config(text=f"Selected File: {file_path}")

        md5, sha256 = calculate_hashes(file_path)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, f"MD5:\n{md5.strip()}\n\nSHA-256:\n{sha256.strip()}")
        result_text.config(state=tk.DISABLED)  

root = tk.Tk()
root.title("File Hash Generator")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TLabel", font=("Helvetica", 10))

frame_select = ttk.Frame(root)
frame_select.pack(pady=20)

instruction_label = ttk.Label(frame_select, text="Select a file to generate MD5 and SHA-256 hashes:")
instruction_label.pack()

select_button = ttk.Button(frame_select, text="Select File", command=select_file)
select_button.pack(pady=10)

file_path_label = ttk.Label(root, text="Selected File: None", foreground="blue")
file_path_label.pack(pady=5)

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", padx=10, pady=10)

frame_results = ttk.Frame(root)
frame_results.pack(pady=10)

result_text = tk.Text(frame_results, height=10, width=70, wrap="word", font=("Courier", 10))
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)

scrollbar = ttk.Scrollbar(frame_results, orient="vertical", command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
