import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic File Organizer")
        self.root.geometry("600x500")

        # Frame for buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # Button to select folder
        self.btn_select_folder = tk.Button(self.frame, text="Select Folder", command=self.select_folder)
        self.btn_select_folder.pack(side=tk.LEFT, padx=10)

        # Button to process files
        self.btn_process = tk.Button(self.frame, text="Organize Files", command=self.organize_files, state=tk.DISABLED)
        self.btn_process.pack(side=tk.LEFT, padx=10)

        # ScrolledText widget to display file contents
        self.txt_display = scrolledtext.ScrolledText(self.root, width=70, height=20)
        self.txt_display.pack(pady=20)

        self.folder_path = None

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            return
        
        self.display_folder_contents()

        # Enable the "Organize Files" button
        self.btn_process.config(state=tk.NORMAL)

    def display_folder_contents(self):
        self.txt_display.delete(1.0, tk.END)
        self.txt_display.insert(tk.END, f"Contents of the selected folder:\n\n")
        
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.txt_display.insert(tk.END, f"{file}\n")

    def organize_files(self):
        if not self.folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        try:
            self._organize_files_by_extension()
            messagebox.showinfo("Success", "Files have been organized successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.display_organized_folder_contents()

    def _organize_files_by_extension(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = file.split('.')[-1]
                if not file_extension:
                    file_extension = "no_extension"

                extension_folder = os.path.join(self.folder_path, file_extension)
                if not os.path.exists(extension_folder):
                    os.makedirs(extension_folder)

                shutil.move(file_path, os.path.join(extension_folder, file))

    def display_organized_folder_contents(self):
        self.txt_display.delete(1.0, tk.END)
        self.txt_display.insert(tk.END, f"Organized contents of the folder:\n\n")
        
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.txt_display.insert(tk.END, f"{file} in {os.path.basename(root)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
