import pdfplumber
import pandas as pd
from tkinter import messagebox, filedialog

def convert_pdf_to_excel(self):
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return
    
    try:
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

        if not all_tables:
            messagebox.showinfo("No Tables Found", "No tables were found in the PDF.")
            return
        
        # combine all tables into one excel file with multiple sheets
        excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not excel_path:
            return
        with pd.ExcelWriter(excel_path) as writer:
            for idx, df in enumerate(all_tables):
                df.to_excel(writer, sheet_name=f'Page_{idx+1}', index=False)

            messagebox.showinfo("Success", "PDF converted to Excel successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF to Excel:\n{str(e)}")
