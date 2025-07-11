import os
import win32com.client
from tkinter import messagebox, filedialog

def convert_excel_to_pdf():
    try:
        input_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx;*.xls")]
        )

        if not input_path:
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"File does not exist:\n{input_path}")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return
        file_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        output_path = os.path.normpath(os.path.join(output_dir, file_name))

        print(f"Input Excel: {input_path}")
        print(f"Output PDF: {output_path}")

        # Launch Excel COM object
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        abs_input_path = os.path.abspath(input_path)
        workbook = excel.Workbooks.Open(abs_input_path)

        # Export to PDF
        workbook.ExportAsFixedFormat(0, output_path) # 0 = PDF
        workbook.Close(False)
        excel.Quit()

        messagebox.showinfo("Success", f"Excel file converted to PDF sucessfully\nSaved at: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")