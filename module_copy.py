import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk

def copy_images(src_folder, dest_folder, selected_file_types, app_instance):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    total_files = 0
    rename_counter = 0

    def update_copied_label(filename, renamed=False):
        nonlocal total_files, rename_counter
        if not renamed:
            app_instance.counter += 1
        else:
            rename_counter += 1
        app_instance.copied_label["text"] = f"Original Files Copied: {app_instance.counter}, Files Copied with Renaming: {rename_counter}, Current File: {filename}"

    for foldername, subfolders, filenames in os.walk(src_folder):
        for filename in filenames:
            if selected_file_types == "Select File Type" or "ALL IMAGES" in selected_file_types or any(filename.lower().endswith(ext) for ext in selected_file_types):
                total_files += 1
                src_path = os.path.join(foldername, filename)
                base_filename, file_extension = os.path.splitext(filename)
                dest_path = os.path.join(dest_folder, filename)

                # Check if file with the same name already exists in the destination folder
                counter = 1
                while os.path.exists(dest_path):
                    new_filename = f"{base_filename}-copy-{counter:03d}{file_extension}"
                    dest_path = os.path.join(dest_folder, new_filename)
                    counter += 1

                shutil.copy2(src_path, dest_path)
                update_copied_label(os.path.basename(dest_path), renamed=counter > 1)

    app_instance.copied_label["text"] = f"Original Files Copied: {app_instance.counter}, Files Copied with Renaming: {rename_counter}, Total Files Copied: {total_files}"

class ImageCopyApp:
    def __init__(self, master):
        self.master = master
        # master.title("Image Copy App")

        # Add labels at the top
        self.top_label1 = tk.Label(master, text="Image Extraction from Folder", font=("Helvetica", 16))
        self.top_label1.grid(row=0, column=0, columnspan=4, pady=10)

        # Existing widgets shift one row down
        self.source_label = tk.Label(master, text="Source Folder:")
        self.source_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.source_entry_field = tk.Entry(master, width=50)
        self.source_entry_field.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_source_folder)
        self.browse_button.grid(row=1, column=3, padx=10, pady=10, sticky=tk.W)

        self.destination_label = tk.Label(master, text="Destination Folder:")
        self.destination_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.destination_entry_field = tk.Entry(master, width=50)
        self.destination_entry_field.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)

        self.browse_dest_button = tk.Button(master, text="Browse", command=self.browse_dest_folder)
        self.browse_dest_button.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)

        # Dropdown for file types
        self.file_types_label = tk.Label(master, text="File Types:")
        self.file_types_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        file_types = ["Select File Type", '.jpg', '.arw', '.tiff', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf', '.txt', 'ALL IMAGES']
        self.selected_file_types = tk.StringVar(value=file_types[0])
        self.file_types_dropdown = ttk.Combobox(master, textvariable=self.selected_file_types, values=file_types, state='readonly', width=15)
        self.file_types_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.copy_button = tk.Button(master, text="Copy Images", command=self.copy_images)
        self.copy_button.grid(row=4, column=0, columnspan=4, pady=10)

        # Add the label at the bottom spanning all columns
        self.copied_label = tk.Label(master, text="Total Files Copied: Waiting...", font=("Helvetica", 10))
        self.copied_label.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.bottom_label = tk.Label(master, 
                             text="Description: Select source folder then select destination folder and extensions (usually .jpg and .arw).\n In destination folder will be created a new folder named ALL_IMAGES.\n It will contain all images from the source folder and its subfolders. ", 
                             font=("Helvetica", 8), 
                             anchor=tk.W)
        self.bottom_label.grid(row=6, column=0, columnspan=4, pady=10, sticky=tk.W)

    def browse_source_folder(self):
        folder_path = filedialog.askdirectory()
        self.source_entry_field.delete(0, tk.END)
        self.source_entry_field.insert(0, folder_path)

    def browse_dest_folder(self):
        folder_path = filedialog.askdirectory()
        self.destination_entry_field.delete(0, tk.END)
        self.destination_entry_field.insert(0, folder_path)

    def copy_images(self):
        source_folder = self.source_entry_field.get()
        destination_folder = os.path.join(self.destination_entry_field.get(), "ALL_IMAGES")
        selected_file_types = self.file_types_dropdown.get().split(', ')
        self.total_files = 0
        self.counter = 0
        copy_images(source_folder, destination_folder, selected_file_types, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCopyApp(root)
    root.mainloop()
