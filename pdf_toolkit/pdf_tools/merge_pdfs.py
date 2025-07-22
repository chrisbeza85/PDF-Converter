import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("PDF Merger")
        self.root.geometry("500x400")
        self.root.transient(root)    # Keeps this window above the main one
        self.root.grab_set()         # Makes it modal (disables main window)
        self.pdf_list =[]
        self.pdf_name_var = tk.StringVar(value="merged.pdf")

        self.build_ui()

    def build_ui(self):
        # Listbox to show selected PDF paths
        self.listbox = tk.Listbox(self.root, width=60, height=10)
        self.listbox.pack(pady=10)


        # buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=15)

        tk.Button(btn_frame, text="Add PDF", command=self.add_pdfs).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Move Up", command=self.move_up).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Move Down", command=self.move_down).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected).grid(row=0, column=3, padx=5)

        convert_btn = tk.Button(
            bottom_frame,
            text="Merge PDFs",
            command=self.merge_pdfs,
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

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.pdf_list:
                self.pdf_list.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def move_up(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == 0:
            return
        idx = selected[0]
        self.pdf_list[idx - 1], self.pdf_list[idx] = self.pdf_list[idx], self.pdf_list[idx - 1]
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx - 1, text)
        self.listbox.select_set(idx - 1)

    def move_down(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == len(self.pdf_list) - 1:
            return
        idx = selected[0]
        self.pdf_list[idx + 1], self.pdf_list[idx] = self.pdf_list[idx], self.pdf_list[idx + 1]
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx + 1, text)
        self.listbox.select_set(idx + 1)

    def remove_selected(self):
        selected = self.listbox.curselection()
        for i in reversed(selected):
            del self.pdf_list[i]
            self.listbox.delete(i)

    def merge_pdfs(self):
        if len(self.pdf_list) < 2:
            messagebox.showwarning("Warning", "Please select at least two PDF files.")
            return
        
        output_filename = self.pdf_name_var.get().strip()
        if not output_filename:
            messagebox.showwarning("Warning", "Please enter a filename for the merged PDF.")
            return
        
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=output_filename
        )
        if not output_path:
            return
        
        merger = PdfMerger()
        try:
            for pdf in self.pdf_list:
                merger.append(pdf)
            merger.write(output_path)
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")
        finally:
            merger.close()

        self.root.grab_release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    PDFMergerApp(root)
    root.mainloop()