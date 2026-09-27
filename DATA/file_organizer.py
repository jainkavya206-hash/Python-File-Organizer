"""
FILE ORGANIZER
==============
A simple program with a window (GUI) that lets you pick a folder,
then automatically sorts the files inside it into sub-folders like
"Images", "Documents", "Videos", "Music", "Archives", and "Others" -
based on each file's type.

You do NOT need to know Python to use this. Just run the file
(instructions are in README.txt) and click the buttons.

HOW IT WORKS (for the curious):
1. tkinter (built into Python) draws the window/buttons.
2. We look at every file in the folder you chose.
3. We check each file's extension (the part after the dot, like .jpg or .pdf).
4. Based on the extension, we decide which category it belongs to.
5. We create a folder for that category (if it doesn't exist) and
   move the file into it.
6. Every action is written to a log box on screen, so you can see
   exactly what happened.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ---------------------------------------------------------------------
# STEP 1: Define which file extensions belong to which category.
# Feel free to add more extensions to any list below.
# ---------------------------------------------------------------------
CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
                  ".ppt", ".pptx", ".csv"],
    "Videos":    [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"],
    "Music":     [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Code":      [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
}
# Anything that doesn't match one of the lists above goes here:
OTHER_CATEGORY = "Others"


def get_category(file_extension: str) -> str:
    """Given a file extension like '.jpg', return which category folder
    it should go into. If it's not in our list, return 'Others'."""
    file_extension = file_extension.lower()
    for category_name, extensions in CATEGORIES.items():
        if file_extension in extensions:
            return category_name
    return OTHER_CATEGORY


def organize_folder(target_directory: str, log_callback):
    """
    Goes through every file directly inside `target_directory`
    (not inside sub-folders) and moves it into a category sub-folder.

    `log_callback` is a function we call with a text message every
    time something happens, so the GUI can show progress live.
    """
    if not os.path.isdir(target_directory):
        log_callback(f"ERROR: '{target_directory}' is not a valid folder.")
        return

    moved_count = 0
    skipped_count = 0

    # os.listdir gives us every item (files AND folders) in the directory
    items = os.listdir(target_directory)

    for item_name in items:
        full_path = os.path.join(target_directory, item_name)

        # Skip folders - we only want to move FILES
        if os.path.isdir(full_path):
            continue

        # Skip this script itself if it happens to be in that folder
        if item_name == os.path.basename(__file__):
            continue

        # Split "photo.jpg" into ("photo", ".jpg")
        _, extension = os.path.splitext(item_name)

        if extension == "":
            # Files with no extension go to "Others"
            category = OTHER_CATEGORY
        else:
            category = get_category(extension)

        # Build the path to the category folder, e.g. .../Images
        category_folder = os.path.join(target_directory, category)

        # Create the category folder if it doesn't already exist
        os.makedirs(category_folder, exist_ok=True)

        destination_path = os.path.join(category_folder, item_name)

        # If a file with the same name already exists there, rename to avoid overwriting
        if os.path.exists(destination_path):
            base, ext = os.path.splitext(item_name)
            counter = 1
            while os.path.exists(destination_path):
                new_name = f"{base}_{counter}{ext}"
                destination_path = os.path.join(category_folder, new_name)
                counter += 1

        try:
            shutil.move(full_path, destination_path)
            log_callback(f"Moved '{item_name}'  ->  {category}/")
            moved_count += 1
        except Exception as error:
            log_callback(f"Could not move '{item_name}': {error}")
            skipped_count += 1

    log_callback("")
    log_callback(f"Done! {moved_count} file(s) organized, {skipped_count} skipped.")


# ---------------------------------------------------------------------
# STEP 2: Build the window (GUI) itself.
# ---------------------------------------------------------------------
class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        root.title("File Organizer")
        root.geometry("560x420")
        root.resizable(False, False)

        # --- Folder selection row ---
        top_frame = tk.Frame(root, pady=15)
        top_frame.pack(fill="x", padx=15)

        tk.Label(top_frame, text="Folder to organize:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        path_row = tk.Frame(top_frame)
        path_row.pack(fill="x", pady=(5, 0))

        self.path_entry = tk.Entry(path_row, font=("Segoe UI", 10))
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=4)

        browse_button = tk.Button(path_row, text="Browse...", command=self.browse_folder)
        browse_button.pack(side="left", padx=(8, 0))

        # --- Organize button ---
        self.organize_button = tk.Button(
            root, text="Organize Files", font=("Segoe UI", 11, "bold"),
            bg="#2e7d32", fg="white", height=2, command=self.start_organizing
        )
        self.organize_button.pack(fill="x", padx=15, pady=15)

        # --- Log output box ---
        tk.Label(root, text="Activity log:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15)

        self.log_box = scrolledtext.ScrolledText(root, height=14, font=("Consolas", 9), state="disabled")
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    def browse_folder(self):
        """Opens the native 'choose a folder' dialog."""
        selected = filedialog.askdirectory()
        if selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected)

    def log(self, message: str):
        """Adds a line of text to the log box."""
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")
        self.root.update_idletasks()

    def start_organizing(self):
        target_directory = self.path_entry.get().strip()

        if not target_directory:
            messagebox.showwarning("No folder selected", "Please choose a folder first.")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            f"This will move files inside:\n\n{target_directory}\n\n"
            "into new category sub-folders (Images, Documents, etc). Continue?"
        )
        if not confirm:
            return

        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

        self.log(f"Organizing: {target_directory}")
        self.log("-" * 50)
        organize_folder(target_directory, self.log)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
