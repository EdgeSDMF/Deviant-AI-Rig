import os
import re
import urllib.request
import json
import chromadb
from chromadb.utils import embedding_functions

# --- LAYER 1: DATA LOSS PREVENTION FRAMEWORK ---
class LocalDLPFilter:
    def __init__(self):
        self.rules = {
            "Social Security Number": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "VA Claim File Tracking Number": re.compile(r'\bC\d{7,8}\b'),
            "Restricted Alpha Case Key": re.compile(r'\b[A-Z]{3,4}\d{4,6}[A-Z]\b'),
            "Internal Verification String": re.compile(r'\bal-cert/[A-Z0-9]{12}\b')
        }

    def inspect_and_redact(self, output_text: str) -> tuple:
        redacted_text = output_text
        violations_logged = []
        for rule_name, pattern in self.rules.items():
            if pattern.search(redacted_text):
                violations_logged.append(rule_name)
                redacted_text = pattern.sub(f" [REDACTED BY SECURITY INTERCEPTOR: {rule_name}] ", redacted_text)
        return redacted_text, violations_logged

# --- LAYER 2: VECTOR RE-INDEXING TRACK ---
db_dir = "/root/ai_vault/sandbox/chroma_db"
knowledge_file = "/root/ai_vault/sandbox/parsed_knowledge.txt"

client = chromadb.PersistentClient(path=db_dir)
embed_fn = embedding_functions.DefaultEmbeddingFunction()


# Check if the index already exists to prevent re-indexing
try:
    collection = client.get_collection(name="vault_data", embedding_function=embed_fn)
    print("[+] Persistent vector cache detected! Bypassing ingestion layer...")
except Exception:
    print("[+] No cache found. Executing raw line indexing...")
    collection = client.create_collection(name="vault_data", embedding_function=embed_fn)

    print("[+] Reading raw text ledger files for precision line re-indexing...")
    with open(knowledge_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Cluster lines into small, tight, overlapping 6-line data windows
    chunks = []
    for i in range(0, len(lines), 3):
        window = " ".join(lines[i:i+6])
        chunks.append(window)

    print(f"[+] Loading {len(chunks)} synchronized data windows into safe database batch allocations...")
    documents, metadatas, ids = [], [], []
    for idx, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": "parsed_knowledge.txt"})
        ids.append(f"line_chunk_{idx}")

    batch_size = 1000
    for i in range(0, len(documents), batch_size):
        collection.upsert(documents=documents[i:i+batch_size], metadatas=metadatas[i:i+batch_size], ids=ids[i:i+batch_size])
    print("[+] Re-indexing complete! Database cache optimized for single-line logs.")

# --- LAYER 3: CORE RUNTIME RETRIEVAL CONTROLLER ---
dlp = LocalDLPFilter()
user_query = "Clean sprays of blood and that"

print(f"\n[!] Input Query Received: '{user_query}'")
db_results = collection.query(query_texts=[user_query], n_results=10)

if db_results and "documents" in db_results and db_results["documents"]:
    inner_docs = db_results["documents"][0]  # Grab the primary list match slice cleanly
    isolated_context = "\n\n---\n\n".join([str(doc) for doc in inner_docs])
    
    print("[+] Live local context isolated. Routing directly to uncensored Dolphin core...")
    prompt_payload = (
        f"You are a secure administrative assistant. Review the provided case notes to answer the question.\n\n"
        f"CONTEXT FROM VA FILES:\n{isolated_context}\n\n"
        f"REQUEST: Analyze the provided text context and locate any specific narrative entries or technical lines matching the target query phrase.\n\n"
        f"INSTRUCTION: Base your answer strictly on the provided text details. Respond below:"
    )
    
    url = "http://localhost:11434/api/generate"
    data = json.dumps({"model": "dolphin-llama3", "prompt": prompt_payload, "stream": False}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            raw_ai_response = res_body.get("response", "")
            
            print("\n" + "="*35 + " LIVE MODEL GENERATION (RAW) " + "="*35)
            print(raw_ai_response)
            
            clean_output, alerts = dlp.inspect_and_redact(raw_ai_response)
            print("\n" + "="*38 + " SECURE DLP STREAMED OUTPUT " + "="*38)
            print(clean_output)
    except Exception as e:
        print(f"[-] Execution error: {e}")
