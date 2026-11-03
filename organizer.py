import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

EXTENSION_MAPPING = {
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.xlsx': 'Documents',
    '.pptx': 'Documents',
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.avi': 'Videos',
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.tar': 'Archives',
    '.py': 'Code',
    '.html': 'Code',
    '.css': 'Code',
    '.js': 'Code'
}

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def start_organizing():
    target_dir = path_entry.get().strip()
    
    if not target_dir or not os.path.exists(target_dir):
        messagebox.showerror("Error", "Please select a valid directory first!")
        return

    moved_files_count = 0

    with os.scandir(target_dir) as entries:
        for entry in entries:
            if entry.is_file():
                file_name = entry.name
                file_path = entry.path
                
                _, ext = os.path.splitext(file_name)
                ext = ext.lower()

                if ext in EXTENSION_MAPPING:
                    folder_name = EXTENSION_MAPPING[ext]
                    dest_folder = os.path.join(target_dir, folder_name)
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_path = os.path.join(dest_folder, file_name)

                    try:
                        base_name, extension = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(dest_path):
                            new_file_name = f"{base_name}_{counter}{extension}"
                            dest_path = os.path.join(dest_folder, new_file_name)
                            counter += 1

                        shutil.move(file_path, dest_path)
                        moved_files_count += 1
                    except Exception:
                        pass

    messagebox.showinfo("Success", f"Organization Complete!\nTotal files relocated: {moved_files_count}")

root = tk.Tk()
root.title("File Organizer GUI")
root.geometry("350x220")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="Automated File Organizer", font=("Arial", 12, "bold"), bg="#f0f0f0")
title_label.pack(pady=15)

path_entry = tk.Entry(root, width=35, font=("Arial", 10))
path_entry.pack(pady=5)

browse_btn = tk.Button(root, text="Select Folder", command=browse_folder, width=20, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
browse_btn.pack(pady=5)

organize_btn = tk.Button(root, text="Organize Files", command=start_organizing, width=20, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
organize_btn.pack(pady=10)

root.mainloop()
