from pypdf import PdfReader
import sys

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        print(f"--- Content of {file_path} ---")
        print(f"Total Pages: {len(reader.pages)}\n")
        
        for i, page in enumerate(reader.pages):
            print(f"--- Page {i+1} ---")
            print(page.extract_text())
            print("\n")
            
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    read_pdf("Project_Test_Script.pdf")
