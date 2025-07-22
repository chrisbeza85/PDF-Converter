from pdf2image import convert_from_path
from tkinter import messagebox, filedialog
import os

def pdf_to_images():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return
    
    try:
        images = convert_from_path(pdf_path)
        output_dir = filedialog.askdirectory(title= "Select Folder to Save Images")

        if not output_dir:
            return
        
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.png")
            image.save(image_path, "PNG")

        messagebox.showinfo("Success", f"{len(images)} images saved to:\n{output_dir}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF", f"Error: {e}")