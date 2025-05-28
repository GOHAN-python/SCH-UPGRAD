Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import os
import shutil

# Path to the folder you want to organize (you can modify this)
folder_path = input("Enter the full path of the folder to organize: ").strip()

# Define file type categories
file_types = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    "Videos": ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    "Archives": ['.zip', '.rar', '.tar', '.gz', '.7z'],
    "Scripts": ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css'],
    "Others": []
}

... def create_folder(destination_folder):
...     """Create folder if it doesn't exist"""
...     if not os.path.exists(destination_folder):
...         os.makedirs(destination_folder)
... 
... def get_category(file_extension):
...     """Get category name based on file extension"""
...     for category, extensions in file_types.items():
...         if file_extension.lower() in extensions:
...             return category
...     return "Others"
... 
... def organize_files(path):
...     if not os.path.isdir(path):
...         print("Invalid folder path. Please try again.")
...         return
... 
...     for filename in os.listdir(path):
...         file_path = os.path.join(path, filename)
... 
...         # Skip if it's a folder
...         if os.path.isdir(file_path):
...             continue
... 
...         # Get file extension
...         _, ext = os.path.splitext(filename)
...         category = get_category(ext)
... 
...         # Destination folder
...         dest_folder = os.path.join(path, category)
...         create_folder(dest_folder)
... 
...         # Move file
...         try:
...             shutil.move(file_path, os.path.join(dest_folder, filename))
...             print(f"Moved: {filename} → {category}/")
...         except Exception as e:
...             print(f"Error moving {filename}: {e}")
... 
