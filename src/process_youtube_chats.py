import os
from pathlib import Path
from fpdf import FPDF

# Define folder paths relative to the script
BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / "source"
PDF_DIR = BASE_DIR / "pdfs"
MD_DIR = BASE_DIR / "markdown"

# Ensure output directories exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR.mkdir(parents=True, exist_ok=True)

# Clean up text for PDF compatibility
def clean_text(text):
    return (
        text.replace("—", "-")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("…", "...")
    )

# Process each .txt file in the source folder
for txt_file in SOURCE_DIR.glob("*.txt"):
    base_name = txt_file.stem
    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    safe_text = clean_text(content)

    # --- Generate PDF ---
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Dude Asks AI: {base_name.replace('_', ' ').title()}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for line in safe_text.splitlines():
        if line.strip() == "":
            pdf.ln(5)
        elif line.strip().endswith(":"):
            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, line.strip())
            pdf.set_font("Arial", size=12)
        else:
            pdf.multi_cell(0, 10, line.strip())

    pdf_path = PDF_DIR / f"{base_name}.pdf"
    pdf.output(str(pdf_path))

    # --- Generate Markdown ---
    md_path = MD_DIR / f"{base_name}.md"
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# Dude Asks AI: {base_name.replace('_', ' ').title()}

")
        md_file.write(safe_text.strip())

print("✅ Conversion complete. PDFs saved in /pdfs and Markdown in /markdown.")