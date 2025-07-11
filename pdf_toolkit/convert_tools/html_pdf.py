import os
from weasyprint import HTML
from tkinter import filedialog, messagebox


def convert_html_to_pdf():
    try:
        input_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm")]
        )

        if not input_path or not os.path.exists(input_path):
            return

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return

        file_name = os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        output_path = os.path.join(output_dir, file_name)

        HTML(input_path).write_pdf(output_path)

        messagebox.showinfo("Success", f"HTML file converted to PDF:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert HTML to PDF:\n\n{str(e)}")
