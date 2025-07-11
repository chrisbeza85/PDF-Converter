import os
import comtypes.client
from tkinter import messagebox, filedialog

def convert_ppt_to_pdf():
    try:
        input_path = filedialog.askopenfilename(
            title="Select PowerPoint file",
            filetypes=[("PowerPoint Files", "*.pptx;*.ppt")]
        )

        if not input_path:
            return
        
        # Debug: Print and check if file exists
        print(f"Selected file: {input_path}")
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"File does not exist:\n{input_path}")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:  
            return
        
        # Output PDF file path
        file_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        output_path = os.path.normpath(os.path.join(output_dir, file_name))
        # changed from os.path.join to os.path.normpath(os.path.join) to ensure correct path formatting

        print(f"Output PDF path: {output_path}")

        # Launch Powerpoint COM object
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        # Use absolute path and raw string
        abs_input_path = os.path.abspath(input_path)
        presentation = powerpoint.Presentations.Open(abs_input_path, WithWindow=False)
        presentation.SaveAs(output_path, FileFormat=32)
        presentation.Close()
        powerpoint.Quit()

        messagebox.showinfo("Success", f"PowerPoint file converted to PDF successfully!\nSaved at: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PowerPoint file to PDF:\n\n{str(e)}")