import sys
import os

# Reconfigure stdout/stderr to use UTF-8 for clean console output of unicode/Urdu
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def extract_pdf_text(pdf_path, output_path=None):
    if not output_path:
        base, _ = os.path.splitext(pdf_path)
        output_path = base + "_text.txt"
        
    print(f"Extracting text from: {pdf_path} ...")
    try:
        import pypdf
    except ImportError:
        print("Error: 'pypdf' is not installed. Please run: pip install pypdf")
        sys.exit(1)
        
    try:
        reader = pypdf.PdfReader(pdf_path)
        extracted_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text += f"--- Page {i+1} ---\n{text}\n\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
            
        print(f"SUCCESS! Text saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error extracting from {pdf_path}: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        extract_pdf_text(pdf_path, output_path)
    else:
        # Default: extract all PDFs in current directory
        pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
        if not pdf_files:
            print("No PDF files found in the current directory.")
            print("Usage: python extract_pdf.py <path_to_pdf> [output_txt_path]")
            sys.exit(1)
        for pdf_file in pdf_files:
            extract_pdf_text(pdf_file)

if __name__ == "__main__":
    main()
