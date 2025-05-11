import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def start_download():
    date = date_entry.get()
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    status_label.config(text=f"Downloading files for {date}...")
    # Here you would call your actual download/validation code
    messagebox.showinfo("Completed", f"Files for {date} downloaded and processed.")
    status_label.config(text="Ready.")

root = tk.Tk()
root.title("Pharmaceutical Trial Data Downloader")

tk.Label(root, text="Enter Date (YYYY-MM-DD):").pack(pady=5)
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

download_button = tk.Button(root, text="Download Files", command=start_download)
download_button.pack(pady=10)

status_label = tk.Label(root, text="Ready.")
status_label.pack(pady=5)

root.geometry("400x200")
root.mainloop()
