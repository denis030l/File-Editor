# VERSION B.E.T.A - OPEN TEST
# v0.2
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image


BLUE = "#0b3c8a"


class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg=BLUE)

        self.file_path = None
        self.image = None

        self.main = tk.Frame(root, bg=BLUE)
        self.main.pack(expand=True)

        # ===== FILE INFO =====
        self.file_label = tk.Label(
            self.main, text="No file selected",
            fg="red", bg=BLUE,
            font=("Arial", 14, "bold")
        )
        self.file_label.pack(pady=10)

        self.size_label = tk.Label(
            self.main, text="Size: -",
            fg="white", bg=BLUE
        )
        self.size_label.pack()

        tk.Button(
            self.main, text="Upload image",
            command=self.upload_file,
            width=20
        ).pack(pady=15)

        self.line()

        # ===== EXTENSION =====
        tk.Label(
            self.main, text="Change extension",
            fg="white", bg=BLUE,
            font=("Arial", 14, "bold")
        ).pack()

        self.ext_var = tk.StringVar(value=".jpg")
        ttk.Combobox(
            self.main,
            textvariable=self.ext_var,
            values=[".jpg", ".png", ".bmp"],
            state="readonly",
            width=10
        ).pack(pady=10)

        self.line()

        # ===== COMPRESSION =====
        tk.Label(
            self.main, text="Compression level",
            fg="white", bg=BLUE,
            font=("Arial", 14, "bold")
        ).pack()

        self.quality = tk.IntVar(value=80)
        tk.Scale(
            self.main,
            from_=10, to=100,
            orient="horizontal",
            variable=self.quality,
            length=300,
            bg=BLUE, fg="white",
            highlightthickness=0
        ).pack(pady=10)

        self.line()

        tk.Button(
            self.main, text="Convert & Save",
            command=self.convert_file,
            width=20
        ).pack(pady=20)

    # =======================

    def line(self):
        tk.Frame(self.main, height=2, width=400, bg="white").pack(pady=15)

    def upload_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not path:
            return

        self.file_path = path
        self.image = Image.open(path)

        self.file_label.config(
            text=os.path.basename(path),
            fg="lime"
        )
        self.size_label.config(
            text=f"Size: {self.format_size(os.path.getsize(path))}"
        )

    def convert_file(self):
        if not self.file_path or not self.image:
            messagebox.showerror("Error", "No image loaded")
            return

        ext = self.ext_var.get()
        quality = self.quality.get()

        base = os.path.splitext(self.file_path)[0]
        new_path = base + "_converted" + ext

        try:
            if ext == ".jpg":
                self.image.convert("RGB").save(
                    new_path,
                    "JPEG",
                    quality=quality,
                    optimize=True
                )
            elif ext == ".png":
                self.image.save(
                    new_path,
                    "PNG",
                    optimize=True
                )
            else:
                self.image.save(new_path)

            messagebox.showinfo(
                "Success",
                f"Saved as:\n{new_path}\n"
                f"New size: {self.format_size(os.path.getsize(new_path))}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024


if __name__ == "__main__":
    root = tk.Tk()
    app = FileEditorApp(root)
    root.mainloop()
