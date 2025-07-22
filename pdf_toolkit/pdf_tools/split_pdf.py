import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import os


class SplitPDFApp:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Split PDF Tool")
        self.file_path = None
        self.total_pages = 0
        self.ranges = []

        # modal window functions
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()


        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self.window)
        container.pack(padx=10, pady=10)

        self.left_frame = tk.Frame(container)
        self.right_frame = tk.Frame(container)

        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Left Frame
        tk.Button(self.left_frame, text="Select PDF", command=self.load_pdf).pack(fill='x')
        self.page_info = tk.Label(self.left_frame, text="Total Pages: 0")
        self.page_info.pack(pady=5)

        tk.Label(self.left_frame, text="Add Custom Range (e.g. 1-3)").pack()
        self.range_entry = tk.Entry(self.left_frame)
        self.range_entry.pack(fill='x')

        tk.Button(self.left_frame, text="Add Range", command=self.add_range).pack(pady=5, fill='x')

        tk.Label(self.left_frame, text="Add Specific Pages (e.g. 2,5,7)").pack()
        self.specific_pages_entry = tk.Entry(self.left_frame)
        self.specific_pages_entry.pack(fill='x')

        tk.Button(self.left_frame, text="Add Pages", command=self.add_specific_pages).pack(pady=5, fill='x')

        tk.Label(self.left_frame, text="Fixed Range (e.g. every 5 pages)").pack()
        self.fixed_range_entry = tk.Entry(self.left_frame)
        self.fixed_range_entry.pack(fill='x')

        tk.Button(self.left_frame, text="Add Fixed Ranges", command=self.add_fixed_ranges).pack(pady=5, fill='x')

        # Right Frame
        tk.Label(self.right_frame, text="Ranges to Extract").pack()
        self.range_listbox = tk.Listbox(self.right_frame, width=30, height=10)
        self.range_listbox.pack()

        tk.Button(self.right_frame, text="Remove Selected", command=self.remove_selected_range).pack(pady=5, fill='x')

        tk.Label(self.right_frame, text="Output File Name").pack()
        self.output_name_entry = tk.Entry(self.right_frame)
        self.output_name_entry.pack(fill='x')

        tk.Button(self.right_frame, text="Split PDF", command=self.split_pdf, bg="#4CAF50", fg="white", font=('Helvetica')).pack(pady=10, fill='x')
        self.progress = ttk.Progressbar(self.right_frame, length=200, mode='determinate')
        self.progress.pack(pady=5)
        tk.Button(self.right_frame, text="Reset", command=self.reset_all).pack(fill='x')

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            reader = PdfReader(self.file_path)
            self.total_pages = len(reader.pages)
            self.page_info.config(text=f"Total Pages: {self.total_pages}")
            self.ranges.clear()
            self.range_listbox.delete(0, tk.END)

    def add_range(self):
        text = self.range_entry.get().strip()
        if '-' in text:
            try:
                start, end = map(int, text.split('-'))
                if 1 <= start <= end <= self.total_pages:
                    self.ranges.append((start, end))
                    self.range_listbox.insert(tk.END, f"Pages {start}-{end}")
                else:
                    raise ValueError
            except:
                messagebox.showerror("Invalid Range", "Please enter a valid page range.")

    def add_specific_pages(self):
        text = self.specific_pages_entry.get().strip()
        try:
            pages = [int(p) for p in text.split(',') if 1 <= int(p) <= self.total_pages]
            for p in pages:
                self.ranges.append((p, p))
                self.range_listbox.insert(tk.END, f"Page {p}")
        except:
            messagebox.showerror("Invalid Pages", "Please enter valid page numbers separated by commas.")

    def add_fixed_ranges(self):
        try:
            step = int(self.fixed_range_entry.get())
            for start in range(1, self.total_pages + 1, step):
                end = min(start + step - 1, self.total_pages)
                self.ranges.append((start, end))
                self.range_listbox.insert(tk.END, f"Pages {start}-{end}")
        except:
            messagebox.showerror("Invalid Step", "Please enter a valid number.")

    def remove_selected_range(self):
        selection = self.range_listbox.curselection()
        for i in reversed(selection):
            self.range_listbox.delete(i)
            del self.ranges[i]

    def split_pdf(self):
        if not self.file_path or not self.ranges:
            messagebox.showwarning("Missing Info", "Please select a PDF and specify ranges.")
            return

        output_name = self.output_name_entry.get().strip() or "split_output"
        base_dir = os.path.dirname(self.file_path)

        reader = PdfReader(self.file_path)

        self.progress["maximum"] = len(self.ranges)
        self.progress["value"] = 0
        self.window.update_idletasks()

        for idx, (start, end) in enumerate(self.ranges):
            writer = PdfWriter()
            for p in range(start - 1, end):
                writer.add_page(reader.pages[p])

            output_path = os.path.join(base_dir, f"{output_name}_{idx + 1}.pdf")
            with open(output_path, 'wb') as f:
                writer.write(f)

            self.progress["value"] += 1
            self.window.update_idletasks()

        messagebox.showinfo("Success", f"PDF split into {len(self.ranges)} parts.")

    def reset_all(self):
        self.ranges.clear()
        self.range_listbox.delete(0, tk.END)
        self.output_name_entry.delete(0, tk.END)
        self.range_entry.delete(0, tk.END)
        self.specific_pages_entry.delete(0, tk.END)
        self.fixed_range_entry.delete(0, tk.END)
        self.page_info.config(text="Total Pages: 0")
        self.file_path = None
        self.total_pages = 0
        self.progress["value"] = 0


# Example standalone runs
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide root if using standalone
    SplitPDFApp(root)
    root.mainloop()
