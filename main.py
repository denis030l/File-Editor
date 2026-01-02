import os
import random
from tkinter import Tk, filedialog, Button, Label, StringVar, ttk, Frame
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.font import Font


class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        self.root.geometry("1920x1080")  # Fullscreen
        self.root.resizable(True, True)

        # Background color (dark blue)
        self.root.configure(bg="#003366")

        # Load custom font
        try:
            self.custom_font = Font(family="FingerPaint", size=14, weight="bold")
        except:
            self.custom_font = Font(family="Helvetica", size=14, weight="bold")  # Fallback font

        # Create main frame
        self.frame = Frame(self.root, bg="#003366")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create the upper table (with one column for file upload)
        self.upper_frame = Frame(self.frame, bg="#003366")
        self.upper_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.label = Label(self.upper_frame, text="Select a file to edit:", bg="#003366", fg="white", font=self.custom_font)
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.select_button = ttk.Button(self.upper_frame, text="Upload", command=self.select_file)
        self.select_button.grid(row=1, column=0, columnspan=2, pady=20)

        # File info label (with color change based on file status)
        self.file_info_label = Label(self.upper_frame, text="No file selected", bg="#003366", fg="red", font=self.custom_font)
        self.file_info_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Line separator
        self.separator_1 = Frame(self.frame, height=2, bg="white")
        self.separator_1.grid(row=1, column=0, sticky="ew", pady=10)

        # Create the lower table with two columns (extension and size)
        self.lower_frame = Frame(self.frame, bg="#003366")
        self.lower_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Left column: Extension selection
        self.extension_label = Label(self.lower_frame, text="Choose a new extension:", bg="#003366", fg="white", font=self.custom_font)
        self.extension_label.grid(row=0, column=0, pady=10)

        # Dropdown for selecting extension
        self.extension_var = StringVar()
        self.extension_combobox = ttk.Combobox(self.lower_frame, textvariable=self.extension_var)
        self.extension_combobox['values'] = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        self.extension_combobox.set('.jpg')  # Default selection
        self.extension_combobox.grid(row=1, column=0, pady=10)

        # Right column: Size selection
        self.size_label = Label(self.lower_frame, text="File Size:", bg="#003366", fg="white", font=self.custom_font)
        self.size_label.grid(row=0, column=1, pady=10)

        # Size choice (KB, MB, GB)
        self.size_unit_var = StringVar(value="KB")
        self.size_unit_combobox = ttk.Combobox(self.lower_frame, textvariable=self.size_unit_var, values=["KB", "MB", "GB"])
        self.size_unit_combobox.grid(row=1, column=1, pady=10)

        self.size_value_label = Label(self.lower_frame, text="Enter size limit:", bg="#003366", fg="white", font=self.custom_font)
        self.size_value_label.grid(row=2, column=0, pady=10)

        # Entry for size input
        self.size_value_entry = ttk.Entry(self.lower_frame, font=self.custom_font)
        self.size_value_entry.grid(row=2, column=1, pady=10)

        # Line separator
        self.separator_2 = Frame(self.frame, height=2, bg="white")
        self.separator_2.grid(row=3, column=0, sticky="ew", pady=10)

        # Download file button (lower)
        self.download_button = ttk.Button(self.frame, text="Download File", command=self.download_file)
        self.download_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Initialize filename
        self.filename = None

    def select_file(self):
        """Opens file dialog to choose a file"""
        file = filedialog.askopenfilename()
        if file:
            self.filename = file
            self.display_file_info()

    def display_file_info(self):
        """Displays file name, extension, and size"""
        file_name = os.path.basename(self.filename)
        file_size = os.path.getsize(self.filename) // 1024  # Size in KB
        file_extension = os.path.splitext(file_name)[1].lower()

        # Update the file info label with lime color when file is selected
        self.file_info_label.config(text=f"File: {file_name} ({file_extension})", fg="#00FF00")
        self.size_value_entry.delete(0, 'end')  # Clear size entry field

    def convert_file(self):
        """Converts the selected file to the new extension"""
        if not self.filename:
            messagebox.showwarning("Error", "Please select a file first.")
            return

        new_extension = self.extension_var.get()

        # Get the base file name and prepare new filename
        file_name, _ = os.path.splitext(self.filename)
        new_filename = file_name + new_extension

        try:
            # For image files, use Pillow to convert
            if new_extension.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                img = Image.open(self.filename)
                img.save(new_filename)
            else:
                # Just rename the file
                os.rename(self.filename, new_filename)

            messagebox.showinfo("Success", f"File successfully converted to {new_filename}")
            self.filename = new_filename  # Update the file to the new one
            self.display_file_info()  # Update file info on the UI
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert the file: {str(e)}")

    def download_file(self):
        """Downloads the file after modifications"""
        if not self.filename:
            messagebox.showwarning("Error", "Please select a file first.")
            return

        download_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(self.filename)[1])
        if download_path:
            try:
                with open(self.filename, 'rb') as file:
                    content = file.read()
                with open(download_path, 'wb') as file:
                    file.write(content)

                messagebox.showinfo("Success", f"File downloaded to {download_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the file: {str(e)}")


# Run the application
root = Tk()
app = FileEditorApp(root)
root.mainloop()
