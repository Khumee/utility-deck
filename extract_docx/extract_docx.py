import zipfile
import xml.etree.ElementTree as ET
import os
import sys

def extract_docx_text(path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            paragraphs = []
            for elem in root.iter():
                # Check for paragraph element
                if elem.tag.endswith('}p'):
                    parts = []
                    for child in elem.iter():
                        if child.tag.endswith('}t'):
                            if child.text:
                                parts.append(child.text)
                        elif child.tag.endswith('}tab'):
                            parts.append('\t')
                        elif child.tag.endswith('}br') or child.tag.endswith('}cr'):
                            parts.append('\n')
                    paragraph_text = "".join(parts)
                    paragraphs.append(paragraph_text)
            return "\n".join(paragraphs)
    except Exception as e:
        return f"Error reading docx: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: extract-docx <path_to_docx> [path_to_output_txt]")
        sys.exit(1)
        
    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"Error: file not found at {docx_path}")
        sys.exit(1)
        
    text = extract_docx_text(docx_path)
    
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted content to {output_path}")
    else:
        print(text)

if __name__ == '__main__':
    main()
