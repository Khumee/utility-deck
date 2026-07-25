import zipfile
import xml.etree.ElementTree as ET
import os
import sys
import re

def extract_pptx_text(path):
    namespaces = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    
    try:
        with zipfile.ZipFile(path) as z:
            # Find all slides inside the pptx package
            slide_files = [f for f in z.namelist() if re.match(r'^ppt/slides/slide\d+\.xml$', f)]
            # Sort slide files numerically
            slide_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
            
            output = []
            for slide_file in slide_files:
                slide_num = re.search(r'\d+', slide_file).group()
                slide_text = []
                
                xml_content = z.read(slide_file)
                root = ET.fromstring(xml_content)
                
                # Traverse slide XML elements to find text runs (<a:t>)
                for elem in root.iter():
                    if elem.tag.endswith('}t'):
                        if elem.text:
                            text_val = elem.text.strip()
                            if text_val:
                                slide_text.append(text_val)
                                
                if slide_text:
                    output.append(f"--- Slide {slide_num} ---")
                    output.append("\n".join(slide_text))
            
            return "\n\n".join(output)
    except Exception as e:
        return f"Error reading pptx: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: extract-pptx <path_to_pptx> [path_to_output_txt]")
        sys.exit(1)
        
    pptx_path = sys.argv[1]
    if not os.path.exists(pptx_path):
        print(f"Error: file not found at {pptx_path}")
        sys.exit(1)
        
    text = extract_pptx_text(pptx_path)
    
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted content to {output_path}")
    else:
        print(text)

if __name__ == '__main__':
    main()
