import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import os


class AddWatermarkApp:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Add Watermark to PDF")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()

        self.pdf_path = None
        self.watermark_path = None
        self.total_pages = 0

        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self.window)
        container.pack(padx=10, pady=10)

        tk.Button(container, text="Select PDF", command=self.select_pdf).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.pdf_label = tk.Label(container, text="No PDF selected")
        self.pdf_label.grid(row=0, column=1, sticky="w")

        tk.Button(container, text="Select Watermark (PDF)", command=self.select_watermark).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.watermark_label = tk.Label(container, text="No watermark selected")
        self.watermark_label.grid(row=1, column=1, sticky="w")

        tk.Label(container, text="Apply to Pages (e.g. 1-3 or leave blank for all)").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.range_entry = tk.Entry(container)
        self.range_entry.grid(row=3, column=0, columnspan=2, sticky="ew")

        tk.Label(container, text="Output File Name").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.output_entry = tk.Entry(container)
        self.output_entry.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.progress = ttk.Progressbar(container, length=250, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(container, text="Add Watermark", command=self.add_watermark, bg="#2196F3", fg="white").grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path = path
            reader = PdfReader(path)
            self.total_pages = len(reader.pages)
            self.pdf_label.config(text=os.path.basename(path))

    def select_watermark(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.watermark_path = path
            self.watermark_label.config(text=os.path.basename(path))

    def parse_range(self, range_text):
        """Returns a set of 1-based page numbers to apply watermark to."""
        if not range_text.strip():
            return set(range(1, self.total_pages + 1))  # All pages
        try:
            parts = range_text.strip().split('-')
            if len(parts) == 2:
                start = int(parts[0])
                end = int(parts[1])
                return set(range(start, end + 1))
            elif len(parts) == 1:
                return {int(parts[0])}
        except:
            return None
        return None

    def add_watermark(self):
        if not self.pdf_path or not self.watermark_path:
            messagebox.showwarning("Missing Input", "Please select both a PDF and a watermark.")
            return

        range_text = self.range_entry.get().strip()
        pages_to_watermark = self.parse_range(range_text)
        if pages_to_watermark is None:
            messagebox.showerror("Invalid Page Range", "Enter a valid page range like 1-3 or leave blank.")
            return

        output_name = self.output_entry.get().strip() or "watermarked_output"
        base_dir = os.path.dirname(self.pdf_path)
        output_path = os.path.join(base_dir, f"{output_name}.pdf")

        try:
            reader = PdfReader(self.pdf_path)
            watermark_reader = PdfReader(self.watermark_path)
            watermark_page = watermark_reader.pages[0]

            writer = PdfWriter()

            self.progress["maximum"] = self.total_pages
            self.progress["value"] = 0
            self.window.update_idletasks()

            for i in range(self.total_pages):
                page = reader.pages[i]
                if (i + 1) in pages_to_watermark:
                    page.merge_page(watermark_page)
                writer.add_page(page)
                self.progress["value"] += 1
                self.window.update_idletasks()

            with open(output_path, 'wb') as f:
                writer.write(f)

            messagebox.showinfo("Success", f"Watermark added successfully.\nSaved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

        self.root.grab_release()
        self.root.destroy()
