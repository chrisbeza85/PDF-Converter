import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class PDFToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit - by Chris Beza")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.pdf_tools_tab = ttk.Frame(tab_control)
        self.convert_to_tab = ttk.Frame(tab_control)
        self.convert_from_tab = ttk.Frame(tab_control)

        tab_control.add(self.pdf_tools_tab, text="PDF Tools")
        tab_control.add(self.convert_to_tab, text="Convert to PDF")
        tab_control.add(self.convert_from_tab, text="Convert from PDF")

        tab_control.pack(expand=1, fill="both")

        self.build_pdf_tools_tab()
        self.build_convert_to_tab()
        self.build_convert_from_tab()

    def build_pdf_tools_tab(self):
        ttk.Label(self.pdf_tools_tab, text="PDF Tools", font=('Helvetica', 14)).pack(pady=10)

        buttons =[
            ("Merge PDFs", self.merge_pdfs),
            ("Split PDF", self.split_pdf),
            ("Encrypt PDF", self.encrypt_pdf),
            ("Decrypt PDF", self.decrypt_pdf)
        ]

        for text, command in buttons:
            ttk.Button(self.pdf_tools_tab, text=text, command=command, width=30).pack(pady=5)

    def build_convert_to_tab(self):
        ttk.Label(self.convert_to_tab, text="Convert to PDF", font=('Helvetica', 14)).pack(pady=10)

        buttons = [
            ("Word to PDF", self.word_to_pdf),
            ("PowerPoint to PDF", self.ppt_to_pdf),
            ("Excel to PDF", self.excel_to_pdf),
            ("Images to PDF", self.image_to_pdf),
            ("HTML to PDF", self.html_to_pdf)
        ]

        for text, command in buttons:
            ttk.Button(self.convert_to_tab, text=text, command=command, width=30).pack(pady=5)

    def build_convert_from_tab(self):
        ttk.Label(self.convert_from_tab, text="Convert from PDF", font=('Helvetica', 14)).pack(pady=10)

        buttons = [
            ("PDF to Word", self.pdf_to_word),
            ("PDF to PowerPoint", self.pdf_to_ppt),
            ("PDF to Excel", self.pdf_to_excel),
            ("PDF to Images", self.pdf_to_images),
            ("PDF to HTML", self.pdf_to_html)
        ]

        for text, command in buttons:
            ttk.Button(self.convert_from_tab, text=text, command=command, width=30).pack(pady=5)

     # Placeholder functions for buttons
    def merge_pdfs(self):
        messagebox.showinfo("Merge", "Merge PDFs clicked!")

    def split_pdf(self):
        messagebox.showinfo("Split", "Split PDF clicked!")

    def encrypt_pdf(self):
        messagebox.showinfo("Encrypt", "Encrypt PDF clicked!")

    def decrypt_pdf(self):
        messagebox.showinfo("Decrypt", "Decrypt PDF clicked!")

    def word_to_pdf(self):
        from convert_tools import word_pdf
        word_pdf.convert_word_to_pdf()

    def ppt_to_pdf(self):
        from convert_tools import ppt_pdf
        ppt_pdf.convert_ppt_to_pdf()

    def excel_to_pdf(self):
        from convert_tools import excel_pdf
        excel_pdf.convert_excel_to_pdf()

    def image_to_pdf(self):
        from convert_tools.image_pdf import ImageToPDFApp
        ImageToPDFApp(self.root)

    def html_to_pdf(self):
        from convert_tools import html_pdf
        html_pdf.convert_html_to_pdf()

    def pdf_to_word(self):
        from convert_tools import pdf_to_word
        pdf_to_word.convert_pdf_to_word()

    def pdf_to_ppt(self):
        from convert_tools import pdf_to_ppt
        pdf_to_ppt.convert_pdf_to_ppt()

    def pdf_to_excel(self):
        messagebox.showinfo("Convert", "PDF to Excel clicked!")

    def pdf_to_images(self):
        messagebox.showinfo("Convert", "PDF to Images clicked!")

    def pdf_to_html(self):
        messagebox.showinfo("Convert", "PDF to HTML clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolkitApp(root)
    root.mainloop()