import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Import the ttk module for the combobox
from PIL import Image
from PIL.ExifTags import TAGS

# Function to rename images
def rename_images(src_folder, new_name, selected_extension, use_original_name):
    count = 1
    total_renamed = 0

    for filename in os.listdir(src_folder):
        if filename.lower().endswith(tuple(selected_extension)):
            try:
                old_path = os.path.join(src_folder, filename)
                
                with Image.open(old_path) as image:
                    exif_data = image._getexif()

                    if exif_data:
                        date_created = exif_data.get(36867)  # 36867 corresponds to DateTimeOriginal tag
                        if date_created:
                            date_created = date_created.split()[0].replace(":", "-")
                        else:
                            date_created = "unknown_date"
                    else:
                        date_created = "unknown_date"

                # Preserve the original file extension
                original_extension = os.path.splitext(filename)[1].lower()

                if use_original_name:
                    new_filename = f"{new_name} - {date_created} - ({filename})"
                else:
                    new_filename = f"{new_name} - {date_created} - ({count:05d}){original_extension}"
                    count += 1

                new_path = os.path.join(src_folder, new_filename)

                # Append the original file extension to the new filename
                new_path_with_extension = f"{new_path[:-1 * len(original_extension)]}{original_extension}"

                os.rename(old_path, new_path_with_extension)
                print(f"Renamed: {filename} to {new_filename}")
                total_renamed += 1
            except Exception as e:
                print(f"Error renaming {filename}: {str(e)}")

    return total_renamed

class ImageRenameApp:
    def __init__(self, master):
        self.master = master
        # master.title("File Renaming Module")

        self.top_label = tk.Label(master, text="File Renaming Module", font=("Helvetica", 16))
        self.top_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.folder_label = tk.Label(master, text="Image Folder:")
        self.folder_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.folder_entry = tk.Entry(master, width=50)
        self.folder_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=1, column=3, padx=5, pady=5, sticky='we')

        self.name_label = tk.Label(master, text="Enter New Name:")
        self.name_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.name_entry = tk.Entry(master, width=50)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky=tk.W)

        # Add the combobox for selecting extensions
        self.extension_label = tk.Label(master, text="Select Extension:")
        self.extension_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        # Include extensions from the ImageCopyApp module
        image_copy_extensions = ['.jpg', '.arw', '.tiff', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf', '.txt']
        self.extensions = image_copy_extensions + ['ALL IMAGES']  # Default extensions
        self.extension_combobox = ttk.Combobox(master, values=self.extensions, state="readonly")
        self.extension_combobox.set(self.extensions[0])  # Set the default extension
        self.extension_combobox.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        # Add the check button for using original name or a 5-digit count
        self.use_original_name_var = tk.BooleanVar()
        self.use_original_name_var.set(True)  # Default is to use original name
        self.use_original_name_checkbox = tk.Checkbutton(master, text="Use Original Name", variable=self.use_original_name_var)
        self.use_original_name_checkbox.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        self.rename_button = tk.Button(master, text="Rename Images", command=self.rename_images)
        self.rename_button.grid(row=4, column=2, padx=1, pady=1, sticky=tk.W)

        # Labels for displaying information
        self.renamed_label = tk.Label(master, text="Files Renamed: 0", font=("Helvetica", 10))
        self.renamed_label.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.description_label = tk.Label(master,
                             text="Description: Enter source folder, new name, select file extension, and choose whether to use the original name or a count. Click 'Rename Images' to proceed.",
                             font=("Helvetica", 8),
                             anchor=tk.W)
        self.description_label.grid(row=6, column=0, columnspan=4, pady=10, sticky=tk.W)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, folder_path)

    def rename_images(self):
        source_folder = self.folder_entry.get()
        new_name = self.name_entry.get()
        selected_extension = [self.extension_combobox.get()]
        use_original_name = self.use_original_name_var.get()
        total_renamed = rename_images(source_folder, new_name, selected_extension, use_original_name)
        
        # Update the renamed label
        self.renamed_label["text"] = f"Files Renamed: {total_renamed}"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenameApp(root)
    root.mainloop()
