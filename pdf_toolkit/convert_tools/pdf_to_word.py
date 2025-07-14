import os
from pdf2docx import Converter
from tkinter import messagebox, filedialog

def convert_pdf_to_word():
    try:
        input_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not input_path:
            return
        
        # output folder
        output_dir = filedialog.askdirectory(title = "Select Output folder")
        if not output_dir:
            return
        
        # generate output path
        file_name = os.path.splitext(os.path.basename(input_path))[0] + ".docx"
        output_path = os.path.join(output_dir, file_name)

        # convert PDF to Word
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()

        messagebox.showinfo("Success", f"PDF converted to Word document successfully!\nSaved at: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF to Word document: \n\n{str(e)}")