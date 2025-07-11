import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox, filedialog

class ImageToPDFApp:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Reorder Images for PDF")
        self.root.geometry("500x400")
        self.root.transient(root)    # Keeps this window above the main one
        self.root.grab_set()         # Makes it modal (disables main window)
        self.images = []
        self.pdf_name_var = tk.StringVar(value="reordered_images.pdf")

        self.build_ui()

    def build_ui(self):
        # Listbox to show selected image paths
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=60)
        self.listbox.pack(pady=10)

        # Buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=15)

        tk.Button(frame, text="Add Images", command=self.add_images).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Move Up", command=self.move_up).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Move Down", command=self.move_down).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Remove", command=self.remove_selected).grid(row=0, column=3, padx=5) 

        convert_btn = tk.Button(
            bottom_frame,
            text="Convert to PDF",
            command=self.convert_to_pdf,
            bg="#4CAF50",
            fg="white",
            font=('Helvetica', 12, 'bold'),
            width=25,
            height=2
        )
        convert_btn.pack()

         # PDF filename input
        name_frame = tk.Frame(self.root)
        name_frame.pack(pady=(10, 5))

        tk.Label(name_frame, text="PDF Filename:").pack(side=tk.LEFT, padx=5)
        name_entry = tk.Entry(name_frame, textvariable=self.pdf_name_var, width=30)
        name_entry.pack(side=tk.LEFT)

    def add_images(self):
        paths = list(filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        ))
        for path in paths:
            if path not in self.images:
                self.images.append(path)
                self.listbox.insert(tk.END, os.path.basename(path))

    def move_up(self):
        idx = self.listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.images[i], self.images[i-1] = self.images[i-1], self.images[i]
            self.refresh_listbox()
            self.listbox.select_set(i-1)

    def move_down(self):
        idx = self.listbox.curselection()
        if idx and idx[0] < len(self.images) - 1:
            i = idx[0]
            self.images[i], self.images[i+1] = self.images[i+1], self.images[i]
            self.refresh_listbox()
            self.listbox.select_set(i+1)
    
    def remove_selected(self):
        idx = self.listbox.curselection()
        if idx:
            i = idx[0]
            del self.images[i]
            self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for path in self.images:
            self.listbox.insert(tk.END, os.path.basename(path))

    def convert_to_pdf(self):
        if not self.images:
            messagebox.showwarning("No Images", "Please add images to convert.")
            return
        
        output_dir = filedialog.askdirectory(title = "Select Output Directory")
        if not output_dir:
            return
        
        pdf_name = self.pdf_name_var.get().strip()
        if not pdf_name.lower().endswith(".pdf"):
            pdf_name += ".pdf"

        output_path = os.path.join(output_dir, pdf_name)

        converted_images = []
        for path in self.images:
            img = Image.open(path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            converted_images.append(img)

        first_image = converted_images[0]
        rest_images = converted_images[1:]

        first_image.save(output_path, save_all=True, append_images=rest_images)

        messagebox.showinfo("Success", f"{len(self.images)} image(s) merged into PDF:\n{output_path}")
        self.root.grab_release()
        self.root.destroy() # Close the window after conversion

