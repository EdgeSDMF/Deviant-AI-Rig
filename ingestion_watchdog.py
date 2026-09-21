import os
import time
import re
import chromadb
from chromadb.utils import embedding_functions

# --- ENVIRONMENTAL CONFIGURATION PATHS ---
WATCH_DIR = "/root/ai_vault/sandbox/dropzone"
DB_DIR = "/root/ai_vault/sandbox/chroma_db"

print("[+] Initializing Advanced Data Ingestion Watchdog Service...")
print(f"[+] Active Monitoring Perimeter Locked Onto: '{WATCH_DIR}'")

# Establish a secure connection straight to your persistent vector database rails
client = chromadb.PersistentClient(path=DB_DIR)
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="vault_data", embedding_function=embed_fn)

def process_and_inject(file_path):
    print(f"\n[!] INGESTION EVENT DETECTED: Processing incoming asset file '{os.path.basename(file_path)}'...")
    
    try:
        # Read the raw unstructured text strings line by line
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if not lines:
            print("[-] File parsing warning: Target file is empty. Skipping injection.")
            return

        # Cluster the raw text lines into tight, overlapping 6-line high-density data windows
        chunks = []
        for i in range(0, len(lines), 3):
            window = " ".join(lines[i:i+6])
            chunks.append(window)

        print(f"[+] Text shredded cleanly into {len(chunks)} synchronized data windows.")
        print("[+] Calculating vector embeddings and injecting directly to persistent disk tracks...")
        
        documents, metadatas, ids = [], [], []
        timestamp_id = int(time.time())
        
        for idx, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": os.path.basename(file_path), "ingest_type": "automated_watchdog"})
            ids.append(f"watchdog_chunk_{timestamp_id}_{idx}")

        # Batch transaction loops processing chunks in safe allocations of 1000 nodes
        batch_size = 1000
        for i in range(0, len(documents), batch_size):
            collection.upsert(
                documents=documents[i:i+batch_size], 
                metadatas=metadatas[i:i+batch_size], 
                ids=ids[i:i+batch_size]
            )
            
        print(f"[+] INTEGRATION SUCCESSFUL: {len(documents)} new nodes active inside vector vault.")
        
        # Archive the source file immediately to clear the tracking runway
        os.remove(file_path)
        print("[+] Watchdog runway cleared. Standing by for next file event...")
        
    except Exception as e:
        print(f"[-] Critical file processing failure: {e}")

# --- CORE EVENT-DRIVEN POLLING LOOP ---
print("[+] Watchdog is officially live and scanning... (Press Ctrl+C to terminate runtime)")
try:
    while True:
        # Crawl the dropzone directory for any raw text assets
        for filename in os.listdir(WATCH_DIR):
            if filename.endswith(".txt"):
                target_file_path = os.path.join(WATCH_DIR, filename)
                # Give file I/O operations a half-second window to stabilize file transfer locks
                time.sleep(0.5)
                process_and_inject(target_file_path)
        
        # Low-overhead rest interval to ensure 0% CPU consumption during resting periods
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Watchdog automation pipeline safely powered down.")
