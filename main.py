# Version **BETA - OPEN TEST**
# v0.1

import os
from tkinter import Tk, filedialog, Button, Label, StringVar, ttk, Frame
from tkinter import messagebox
from PIL import Image, ImageTk


class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        self.root.geometry("800x600")  # Уменьшенный размер для удобства
        self.root.resizable(True, True)

        # Set the background image
        self.bg_image = Image.open("images/bg.png")  # Обновлено на bg.png
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Create main frame
        self.frame = Frame(self.root, bg="#003366")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # File Upload Section
        self.upload_frame = Frame(self.frame, bg="#003366")
        self.upload_frame.pack(fill="x", pady=20)

        self.upload_label = Label(self.upload_frame, text="Select a file to edit:", bg="#003366", fg="white", font=("Helvetica", 14, "bold"))
        self.upload_label.pack(side="left", padx=10)

        self.select_button = Button(self.upload_frame, text="Upload", command=self.select_file, font=("Helvetica", 14, "bold"))
        self.select_button.pack(side="left", padx=10)

        self.file_info_label = Label(self.upload_frame, text="No file selected", bg="#003366", fg="red", font=("Helvetica", 14, "bold"))
        self.file_info_label.pack(side="left", padx=10)

        self.file_size_label = Label(self.upload_frame, text="Size: N/A", bg="#003366", fg="white", font=("Helvetica", 14, "bold"))
        self.file_size_label.pack(side="left", padx=10)

        # Horizontal Line after Upload Section
        self.line1 = Frame(self.frame, height=2, bg="white")
        self.line1.pack(fill="x", pady=10)

        # Extension Change Section
        self.extension_frame = Frame(self.frame, bg="#003366")
        self.extension_frame.pack(fill="x", pady=20)

        self.extension_label = Label(self.extension_frame, text="Choose a new extension:", bg="#003366", fg="white", font=("Helvetica", 14, "bold"))
        self.extension_label.pack(side="left", padx=10)

        self.extension_var = StringVar()
        self.extension_combobox = ttk.Combobox(self.extension_frame, textvariable=self.extension_var, values=['.jpg', '.jpeg', '.png', '.bmp', '.gif'], state="readonly", font=("Helvetica", 14, "bold"))
        self.extension_combobox.set('.jpg')  # Default value
        self.extension_combobox.pack(side="left", padx=10)

        # Horizontal Line after Extension Change Section
        self.line2 = Frame(self.frame, height=2, bg="white")
        self.line2.pack(fill="x", pady=10)

        # Size Change Section
        self.size_frame = Frame(self.frame, bg="#003366")
        self.size_frame.pack(fill="x", pady=20)

        self.size_label = Label(self.size_frame, text="File Size (KB/MB/GB):", bg="#003366", fg="white", font=("Helvetica", 14, "bold"))
        self.size_label.pack(side="left", padx=10)

        self.size_unit_var = StringVar(value="KB")
        self.size_unit_combobox = ttk.Combobox(self.size_frame, textvariable=self.size_unit_var, values=["KB", "MB", "GB"], font=("Helvetica", 14, "bold"))
        self.size_unit_combobox.pack(side="left", padx=10)

        self.size_value_label = Label(self.size_frame, text="Enter size limit:", bg="#003366", fg="white", font=("Helvetica", 14, "bold"))
        self.size_value_label.pack(side="left", padx=10)

        self.size_value_entry = ttk.Entry(self.size_frame, font=("Helvetica", 14, "bold"))
        self.size_value_entry.pack(side="left", padx=10)

        # Horizontal Line after Size Change Section
        self.line3 = Frame(self.frame, height=2, bg="white")
        self.line3.pack(fill="x", pady=10)

        # Convert Button
        self.convert_button = Button(self.frame, text="Convert File", command=self.convert_file, font=("Helvetica", 14, "bold"))
        self.convert_button.pack(pady=20)

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
        self.file_size_label.config(text=f"Size: {file_size} KB")
        self.size_value_entry.delete(0, 'end')  # Clear size entry field

    def convert_file(self):
        """Converts the selected file to the new extension and size"""
        if not self.filename:
            messagebox.showwarning("Error", "Please select a file first.")
            return

        # Get the new extension
        new_extension = self.extension_var.get()

        # Get the base file name and prepare new filename
        file_name, _ = os.path.splitext(self.filename)
        new_filename = file_name + new_extension

        # If file size needs to be reduced
        size_limit = self.size_value_entry.get()
        if size_limit:
            try:
                size_limit = float(size_limit)
                unit = self.size_unit_var.get()

                # Convert size to bytes
                if unit == "KB":
                    size_limit *= 1024  # KB to bytes
                elif unit == "MB":
                    size_limit *= 1024 * 1024  # MB to bytes
                elif unit == "GB":
                    size_limit *= 1024 * 1024 * 1024  # GB to bytes

                # Check if file is larger than the size limit
                file_size = os.path.getsize(self.filename)
                if file_size > size_limit:
                    messagebox.showwarning("Warning", f"The file is too large for the selected size limit ({size_limit} bytes).")
                    return
            except ValueError:
                messagebox.showwarning("Error", "Please enter a valid size limit.")
                return

        try:
            # For image files, use Pillow to convert
            if new_extension.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                img = Image.open(self.filename)
                img.save(new_filename)

            # Update the file to the new one
            self.filename = new_filename
            messagebox.showinfo("Success", f"File successfully converted to {new_filename}")
            self.display_file_info()  # Update file info on the UI
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert the file: {str(e)}")


# Run the application
root = Tk()
app = FileEditorApp(root)
root.mainloop()
