from textwrap import fill
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog, Toplevel
from PIL import Image, ImageTk
import os
import sqlite3
from turtle import fillcolor
from tkinter import PhotoImage
from pathlib import Path
from module_copy import copy_images
from module_copy import ImageCopyApp
from module_rename import ImageRenameApp
from module_sort_by_month import ImageSorterMonthApp
from module_sort_by_year import ImageSorterYearApp


def create_main_menu():
    menu_frame = ttk.Frame(window, style="Frame1.TFrame")
    menu_frame.grid(row=0, column=0, sticky='nsew')

    menu_bar = tk.Menu(menu_frame)
    main_menu = tk.Menu(menu_bar, tearoff=0)

    main_menu.add_command(label="Extract files", command=copy_files_app)
    main_menu.add_command(label="Rename files", command=rename_files_app)
    main_menu.add_command(label="Sort by Year", command=sort_by_year_app)
    main_menu.add_command(label="Sort by Month", command=sort_by_month_app)
    main_menu.add_separator()
    main_menu.add_command(label="Exit", command=window.destroy)

    menu_bar.add_cascade(label="Operations", menu=main_menu)
    menu_bar.add_command(label="About Program", command=create_about_frame)

    window.config(menu=menu_bar)

    # s1 = ttk.Style()
    # s1.configure("Frame1.TFrame", background='Orange')  # Set the background color for menu_frame


def create_about_frame():
    # Destroy any existing frames
    for widget in window.winfo_children():
        widget.destroy()

    # Create main menu
    create_main_menu()

    s = ttk.Style()
    s.configure("Frame1.TFrame", background='white')

    # Create and configure the main frame
    main_frame_about = ttk.Frame(window, borderwidth=2, relief="groove", style="Frame1.TFrame")
    main_frame_about.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    main_frame_about.columnconfigure(0, weight=1)

    # Create a new style for the about frame
    about_frame_style = ttk.Style()
    about_frame_style.configure("AboutFrame.TFrame", background='#FAEBD7')  # Set the background color

    # Create the about frame using the new style
    about_frame = ttk.Frame(main_frame_about, borderwidth=2, relief="groove", style="AboutFrame.TFrame")
    about_frame.pack(expand=True)

    # Load the original logo image (replace 'path_to_logo.png' with the actual path to your logo)
    original_image = Image.open('data\\logo.png')

    # Resize the image to 200x200
    resized_image = original_image.resize((90, 90))

    # Convert the PIL Image to Tkinter PhotoImage
    logo_image = ImageTk.PhotoImage(resized_image)

    # Create and display the logo
    logo_label = ttk.Label(about_frame, image=logo_image, style="AboutFrame.TLabel")
    logo_label.image = logo_image  # to prevent garbage collection
    logo_label.pack(pady=10)

    # Create and display the text with transparent background
    about_text = "<APK_soft>\nCopyright © 2024 NPS\nBusiness Edition\n1.0"
    text_label = ttk.Label(about_frame, text=about_text, wraplength=300, justify='center', compound='top', style="AboutFrame.TLabel")
    text_label.pack(pady=10)


################################################################################################################

def copy_files_app():
    for widget in window.winfo_children():
        widget.destroy()
    create_main_menu()
    s1 = ttk.Style()
    s1.configure("Horizontal.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s1.configure("Vertical.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s1.configure("copy_frame.TFrame") #,background='Orange')

    copy_frame = ttk.Frame(window, style="copy_frame.TFrame")
    copy_frame.grid(row=0, column=0, sticky='nsew')
    
    # window.grid_rowconfigure(0, weight=1)  # Row 0
    # window.grid_rowconfigure(1, weight=1)  # Row 1
    
    # window.grid_columnconfigure(0, weight=1)  # Column 0
    # window.grid_columnconfigure(1, weight=1)  # Column 1
        
    copy_frame.columnconfigure(0, weight=9)  # Configure column weight
    copy_frame.columnconfigure(1, weight=1)  # Configure column weight
    copy_frame.rowconfigure(0, weight=9)     # Configure row weight
    copy_frame.rowconfigure(1, weight=1)     # Configure row weight

    copy_canvas = tk.Canvas(copy_frame, borderwidth=0, highlightthickness=0)
    copy_canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(copy_frame, orient="horizontal", style="Horizontal.TScrollbar", command=copy_canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ews")
    scrollbar_y = ttk.Scrollbar(copy_frame, orient="vertical", style="Vertical.TScrollbar", command=copy_canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="nse")
    copy_canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    copy_content_frame = ttk.Frame(copy_canvas)
    copy_canvas.create_window((0, 0), window=copy_content_frame, anchor="nw")
    copy_content_frame.columnconfigure(0, weight=1)  # Configure column weight
    copy_content_frame.rowconfigure(0, weight=1) 
    image_copy_app = ImageCopyApp(copy_content_frame)

    # title_label = ttk.Label(copy_content_frame, text="Copy images from folders")
    # title_label.grid(row=0, column=0, pady=10)
    
    copy_content_frame.update_idletasks()
    copy_canvas.config(scrollregion=copy_canvas.bbox("all"))
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def rename_files_app():
    for widget in window.winfo_children():
        widget.destroy()
    create_main_menu()
    s2 = ttk.Style()
    s2.configure("Horizontal.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s2.configure("Vertical.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s2.configure("rename_frame.TFrame", background='Orange')

    rename_frame = ttk.Frame(window, style="rename_frame.TFrame")
    rename_frame.grid(row=0, column=0, sticky='nsew')
    rename_frame.columnconfigure(0, weight=1)  # Configure column weight
    rename_frame.rowconfigure(0, weight=1)     # Configure row weight

    rename_canvas = tk.Canvas(rename_frame, borderwidth=0, highlightthickness=0)
    rename_canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(rename_frame, orient="horizontal", style="Horizontal.TScrollbar", command=rename_canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    scrollbar_y = ttk.Scrollbar(rename_frame, orient="vertical", style="Vertical.TScrollbar", command=rename_canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    rename_canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    rename_content_frame = ttk.Frame(rename_canvas)
    rename_canvas.create_window((0, 0), window=rename_content_frame, anchor="nw")
    image_rename_app = ImageRenameApp(rename_content_frame)

    # title_label = ttk.Label(rename_content_frame, text="rename images from folders")
    # title_label.grid(row=0, column=0, pady=10)
    
    rename_content_frame.update_idletasks()
    rename_canvas.config(scrollregion=rename_canvas.bbox("all"))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def sort_by_year_app():
    for widget in window.winfo_children():
        widget.destroy()
    create_main_menu()
    s3 = ttk.Style()
    s3.configure("Horizontal.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s3.configure("Vertical.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s3.configure("sortyear_frame.TFrame", background='Orange')

    sortyear_frame = ttk.Frame(window, style="sortyear_frame.TFrame")
    sortyear_frame.grid(row=0, column=0, sticky='nsew')
    sortyear_frame.columnconfigure(0, weight=1)  # Configure column weight
    sortyear_frame.rowconfigure(0, weight=1)     # Configure row weight

    sortyear_canvas = tk.Canvas(sortyear_frame, borderwidth=0, highlightthickness=0)
    sortyear_canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(sortyear_frame, orient="horizontal", style="Horizontal.TScrollbar", command=sortyear_canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    scrollbar_y = ttk.Scrollbar(sortyear_frame, orient="vertical", style="Vertical.TScrollbar", command=sortyear_canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    sortyear_canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    sortyear_content_frame = ttk.Frame(sortyear_canvas)
    sortyear_canvas.create_window((0, 0), window=sortyear_content_frame, anchor="nw")
    sort_by_year_app = ImageSorterYearApp(sortyear_content_frame)

    # title_label = ttk.Label(sortyear_content_frame, text="sortyear images from folders")
    # title_label.grid(row=0, column=0, pady=10)
    
    sortyear_content_frame.update_idletasks()
    sortyear_canvas.config(scrollregion=sortyear_canvas.bbox("all"))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def sort_by_month_app():
    for widget in window.winfo_children():
        widget.destroy()
    create_main_menu()
    s3 = ttk.Style()
    s3.configure("Horizontal.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s3.configure("Vertical.TScrollbar", troughcolor="lightgray", sliderthickness=10)
    s3.configure("sortmonth_frame.TFrame", background='Orange')

    sortmonth_frame = ttk.Frame(window, style="sortmonth_frame.TFrame")
    sortmonth_frame.grid(row=0, column=0, sticky='nsew')
    sortmonth_frame.columnconfigure(0, weight=1)  # Configure column weight
    sortmonth_frame.rowconfigure(0, weight=1)     # Configure row weight

    sortmonth_canvas = tk.Canvas(sortmonth_frame, borderwidth=0, highlightthickness=0)
    sortmonth_canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_x = ttk.Scrollbar(sortmonth_frame, orient="horizontal", style="Horizontal.TScrollbar", command=sortmonth_canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    scrollbar_y = ttk.Scrollbar(sortmonth_frame, orient="vertical", style="Vertical.TScrollbar", command=sortmonth_canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    sortmonth_canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    sortmonth_content_frame = ttk.Frame(sortmonth_canvas)
    sortmonth_canvas.create_window((0, 0), window=sortmonth_content_frame, anchor="nw")
    sort_by_month_app = ImageSorterMonthApp(sortmonth_content_frame)

    # title_label = ttk.Label(sortmonth_content_frame, text="sortmonth images from folders")
    # title_label.grid(row=0, column=0, pady=10)
    
    sortmonth_content_frame.update_idletasks()
    sortmonth_canvas.config(scrollregion=sortmonth_canvas.bbox("all"))
###################################################################################################################
window = tk.Tk()
window.title('Window of widgets')
window.geometry('800x500+300+100')
window.attributes('-alpha', 0.95)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

create_main_menu()

window.mainloop()
