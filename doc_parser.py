import os
from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path

VAULT_DIR = "/mnt/core_ai_vault"
OUTPUT_FILE = "/root/ai_vault/sandbox/parsed_knowledge.txt"

def initialize_ocr_parser():
    print("=== STARTING HEAVY INTEGRATED OCR SWEEP ===")
    if not os.path.exists(VAULT_DIR):
        print("ERROR: DRIVE UNREACHABLE")
        return
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as master_log:
        for file_name in os.listdir(VAULT_DIR):
            if file_name.lower().endswith(".pdf"):
                file_path = os.path.join(VAULT_DIR, file_name)
                print(f"[SCANNING]: {file_name}")
                text_content = ""
                
                try:
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text_content += extracted
                    
                    if len(text_content.strip()) == 0:
                        print(" -> IMAGE PDF DETECTED. SWEEPING PIXELS...")
                        images = convert_from_path(file_path)
                        for image in images:
                            text_content += pytesseract.image_to_string(image)
                            
                    if text_content.strip():
                        master_log.write(f"\n--- SOURCE: {file_name} ---\n")
                        master_log.write(text_content)
                        print(" -> SUCCESS: EXTRACTED SECTORS")
                    else:
                        print(" -> EMPTY PAGE WARNING")
                        
                except Exception as e:
                    print(f"[ERROR] CANNOT PARSE: {str(e)}")
                    
    print("=== FINISHED COMPILING MASTER LEDGER ===")

if __name__ == "__main__":
    initialize_ocr_parser()
EOF
