# Python File Organizer

A simple Python GUI application that automatically organizes files into separate folders based on their file types.

## Project Overview

**File Organizer** is a Python desktop application developed as an **Industrial Training Project**. It provides a graphical interface where the user selects a folder and clicks **Organize Files**. The program sorts files into category folders.

Supported categories:
- Images
- Documents
- Videos
- Music
- Archives
- Installers
- Code
- Others

## Features

- Simple graphical user interface
- Folder selection using Browse
- Automatic file categorization
- Automatic creation of category folders
- Activity log
- Unknown extensions go to `Others`
- Prevents overwriting files with the same name
- Does not process files inside existing sub-folders

## Technologies Used

- Python 3
- Tkinter
- `os`
- `shutil`

## How to Run

Install Python 3.x.

### Windows
```bash
python file_organizer.py
```

### macOS / Linux
```bash
python3 file_organizer.py
```

## How to Use

1. Click **Browse...**
2. Select the folder to organize.
3. Click **Organize Files**.
4. Confirm the operation.
5. Check the activity log.

## Example

Before:
```text
MyFolder/
├── photo.jpg
├── assignment.pdf
├── movie.mp4
├── song.mp3
└── program.py
```

After:
```text
MyFolder/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── assignment.pdf
├── Videos/
│   └── movie.mp4
├── Music/
│   └── song.mp3
└── Code/
    └── program.py
```

## Safety Notes

- The program moves files; it does not delete them.
- Only files directly inside the selected folder are processed.
- Files inside sub-folders are not processed.
- If a destination file already exists, a new name such as `photo_1.jpg` is used.
- Test the program on a sample folder before using it on important data.

## Requirements

No external pip packages are required. The project uses Python standard-library modules.

## Project Structure

```text
Python-File-Organizer/
├── file_organizer.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Industrial Training

**Project:** Python Programming – File Organizer  
**Project Type:** Industrial Training Project  
**Student:** Kavya Kishor Jain  
**Roll No:** 24EJCCS186

## Purpose

The project automates file organization and demonstrates Python programming, file handling, directory management, functions, conditional statements, GUI development, exception handling, and automation.
