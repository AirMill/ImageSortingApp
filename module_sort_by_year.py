import os
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
from PIL import Image
import shutil

class ImageSorterYearApp:
    def __init__(self, master):
        self.master = master
        # self.master.title("Image Sorter")
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.selected_extension = tk.StringVar()
        self.extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.arw', '.pdf', '.txt']
        self.sorted_files_count = 0  # Counter for sorted files
        self.error_message = tk.StringVar()
        self.modifications_made = False  # Flag to track modifications

        self.create_widgets()

    def create_widgets(self):
        # Frame to contain widgets
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(expand=True)

        # Label and Entry for source folder
        source_label = tk.Label(main_frame, text="Source Folder:")
        source_label.grid(row=0, column=0, sticky="e")

        source_entry = tk.Entry(main_frame, textvariable=self.input_folder_path, width=40)
        source_entry.grid(row=0, column=1, padx=10)

        browse_source_button = tk.Button(main_frame, text="Browse", command=self.browse_source_folder)
        browse_source_button.grid(row=0, column=2)

        # Label and Entry for output folder
        output_label = tk.Label(main_frame, text="Output Folder:")
        output_label.grid(row=1, column=0, sticky="e")

        output_entry = tk.Entry(main_frame, textvariable=self.output_folder_path, width=40)
        output_entry.grid(row=1, column=1, padx=10)

        browse_output_button = tk.Button(main_frame, text="Browse", command=self.browse_output_folder)
        browse_output_button.grid(row=1, column=2)

        # Dropdown for selecting file extensions
        extension_label = tk.Label(main_frame, text="Select Extension:")
        extension_label.grid(row=2, column=0, sticky="e")

        extension_dropdown = ttk.Combobox(main_frame, textvariable=self.selected_extension, values=['All'] + self.extensions)
        extension_dropdown.grid(row=2, column=1, padx=10)
        extension_dropdown.current(0)  # Set the default selection to 'All'

        # Counter label
        counter_label = tk.Label(main_frame, text="Sorted Files:")
        counter_label.grid(row=3, column=0, sticky="e")

        self.counter_var = tk.StringVar()
        counter_value_label = tk.Label(main_frame, textvariable=self.counter_var)
        counter_value_label.grid(row=3, column=1, padx=10)

        # Error display label
        error_label = tk.Label(main_frame, text="Errors:")
        error_label.grid(row=4, column=0, sticky="e")

        error_display_label = tk.Label(main_frame, textvariable=self.error_message, fg="red")
        error_display_label.grid(row=4, column=1, padx=10, sticky="w")

        # Submit Button
        self.submit_button = tk.Button(main_frame, text="Submit", command=self.organize_images, state=tk.NORMAL)
        self.submit_button.grid(row=5, column=1, pady=10)

    def browse_source_folder(self):
        source_folder_path = filedialog.askdirectory()
        self.input_folder_path.set(source_folder_path)
        self.modifications_made = True
        self.update_submit_button_state()

    def browse_output_folder(self):
        output_folder_path = filedialog.askdirectory()
        self.output_folder_path.set(output_folder_path)
        self.modifications_made = True
        self.update_submit_button_state()

    def get_creation_year(self, file_path):
        try:
            # Try to get the creation year from EXIF data
            with open(file_path, 'rb') as f:
                exif_info = Image.open(f)._getexif()
                if exif_info and 36867 in exif_info:
                    date_str = exif_info[36867]
                    date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    return date_obj.year
        except Exception as exif_error:
            print(f"EXIF Error: {exif_error}")

        try:
            # If EXIF fails, try to get the creation time of the file
            ctime = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(ctime)
            return creation_date.year
        except Exception as ctime_error:
            print(f"Creation Time Error: {ctime_error}")

        return None

    def update_counter(self):
        self.sorted_files_count += 1
        self.counter_var.set(str(self.sorted_files_count))

    def update_submit_button_state(self):
        if self.modifications_made:
            self.error_message.set("")  # Clear error message
            self.sorted_files_count = 0  # Reset counter
            self.counter_var.set("0")
            self.submit_button["state"] = tk.NORMAL  # Enable submit button
        else:
            self.submit_button["state"] = tk.DISABLED  # Disable submit button

    def organize_images(self):
        input_folder = self.input_folder_path.get()
        output_folder = self.output_folder_path.get()
        selected_extension = self.selected_extension.get()

        if not os.path.exists(input_folder) or not os.path.exists(output_folder):
            self.error_message.set("Invalid folder paths. Please choose valid folders.")
            return

        if selected_extension == 'All':
            valid_extensions = self.extensions
        else:
            valid_extensions = [selected_extension]

        for filename in os.listdir(input_folder):
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                image_path = os.path.join(input_folder, filename)
                creation_year = self.get_creation_year(image_path)

                if creation_year is not None:
                    year_folder = os.path.join(output_folder, str(creation_year))

                    if not os.path.exists(year_folder):
                        os.makedirs(year_folder)

                    destination_path = os.path.join(year_folder, filename)
                    shutil.copy2(image_path, destination_path)
                    self.update_counter()
                    print(f"Moved {filename} to {year_folder}")

                else:
                    unsorted_folder = os.path.join(output_folder, "unsorted")
                    if not os.path.exists(unsorted_folder):
                        os.makedirs(unsorted_folder)

                    destination_path = os.path.join(unsorted_folder, "unsorted_" + filename)
                    shutil.copy2(image_path, destination_path)
                    self.update_counter()
                    print(f"Moved {filename} to {unsorted_folder}")

        self.error_message.set("")  # Clear error message
        self.modifications_made = False  # Reset modifications flag
        self.submit_button["state"] = tk.DISABLED  # Disable submit button
        tk.messagebox.showinfo("Success", "Image sorting completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterYearApp(root)
    root.mainloop()
