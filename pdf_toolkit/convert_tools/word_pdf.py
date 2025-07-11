from docx2pdf import convert
import os
from os import path as os_path
from tkinter import messagebox, filedialog

def convert_word_to_pdf():
    try:
        input_path = filedialog.askopenfilename(
            title="Select Word file",
            filetypes=[("Word Documents", "*.docx;*.doc")]
        )

        if not input_path:
            return # User cancelled
        
        output_path = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if not output_path:
            return # User cancelled
        
        convert(input_path, os_path.join(output_path, os.path.basename(input_path).replace(".docx", ".pdf")))

        messagebox.showinfo("Success", "Word document converted to PDF successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert Word document to PDF:\n\n{str(e)}")
        