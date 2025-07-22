import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import os


class RemovePDFApp:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Remove Pages from PDF")
        self.file_path = None
        self.total_pages = 0
        self.pages_to_remove = set()

        # Make modal
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

        tk.Label(self.left_frame, text="Remove Range (e.g. 2-4)").pack()
        self.range_entry = tk.Entry(self.left_frame)
        self.range_entry.pack(fill='x')

        tk.Button(self.left_frame, text="Add Range", command=self.add_range).pack(pady=5, fill='x')

        tk.Label(self.left_frame, text="Remove Specific Pages (e.g. 1,3,5)").pack()
        self.pages_entry = tk.Entry(self.left_frame)
        self.pages_entry.pack(fill='x')

        tk.Button(self.left_frame, text="Add Pages", command=self.add_pages).pack(pady=5, fill='x')

        # Right Frame
        tk.Label(self.right_frame, text="Pages to Remove").pack()
        self.pages_listbox = tk.Listbox(self.right_frame, width=30, height=10)
        self.pages_listbox.pack()

        tk.Button(self.right_frame, text="Remove Selected", command=self.remove_selected).pack(pady=5, fill='x')

        tk.Label(self.right_frame, text="Output File Name").pack()
        self.output_name_entry = tk.Entry(self.right_frame)
        self.output_name_entry.pack(fill='x')

        tk.Button(self.right_frame, text="Remove Pages", command=self.remove_pages, bg="#f44336", fg="white", font=('Helvetica')).pack(pady=10, fill='x')

        self.progress = ttk.Progressbar(self.right_frame, length=200, mode='determinate')
        self.progress.pack(pady=5)

        tk.Button(self.right_frame, text="Reset", command=self.reset_all).pack(fill='x')

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            reader = PdfReader(self.file_path)
            self.total_pages = len(reader.pages)
            self.page_info.config(text=f"Total Pages: {self.total_pages}")
            self.pages_to_remove.clear()
            self.pages_listbox.delete(0, tk.END)

    def add_range(self):
        text = self.range_entry.get().strip()
        try:
            start, end = map(int, text.split('-'))
            if 1 <= start <= end <= self.total_pages:
                for p in range(start, end + 1):
                    if p not in self.pages_to_remove:
                        self.pages_to_remove.add(p)
                        self.pages_listbox.insert(tk.END, f"Page {p}")
            else:
                raise ValueError
        except:
            messagebox.showerror("Invalid Range", "Please enter a valid page range.")

    def add_pages(self):
        text = self.pages_entry.get().strip()
        try:
            pages = [int(p) for p in text.split(',') if 1 <= int(p) <= self.total_pages]
            for p in pages:
                if p not in self.pages_to_remove:
                    self.pages_to_remove.add(p)
                    self.pages_listbox.insert(tk.END, f"Page {p}")
        except:
            messagebox.showerror("Invalid Input", "Please enter valid page numbers separated by commas.")

    def remove_selected(self):
        selection = self.pages_listbox.curselection()
        for i in reversed(selection):
            text = self.pages_listbox.get(i)
            page_num = int(text.replace("Page ", ""))
            self.pages_to_remove.discard(page_num)
            self.pages_listbox.delete(i)

    def remove_pages(self):
        if not self.file_path or not self.pages_to_remove:
            messagebox.showwarning("Missing Info", "Please select a PDF and specify pages to remove.")
            return

        output_name = self.output_name_entry.get().strip() or "removed_output"
        base_dir = os.path.dirname(self.file_path)
        output_path = os.path.join(base_dir, f"{output_name}.pdf")

        reader = PdfReader(self.file_path)
        writer = PdfWriter()

        self.progress["maximum"] = self.total_pages
        self.progress["value"] = 0
        self.window.update_idletasks()

        for i in range(1, self.total_pages + 1):
            if i not in self.pages_to_remove:
                writer.add_page(reader.pages[i - 1])
            self.progress["value"] += 1
            self.window.update_idletasks()

        with open(output_path, 'wb') as f:
            writer.write(f)

        messagebox.showinfo("Success", f"Pages removed successfully.\nOutput saved as:\n{output_path}")

    def reset_all(self):
        self.pages_to_remove.clear()
        self.pages_listbox.delete(0, tk.END)
        self.range_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        self.output_name_entry.delete(0, tk.END)
        self.page_info.config(text="Total Pages: 0")
        self.progress["value"] = 0
        self.file_path = None
        self.total_pages = 0


# Standalone usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    RemovePDFApp(root)
    root.mainloop()
