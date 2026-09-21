import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Tell the transformers framework to strictly look at local files and block all internet calls
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Specify the direct model identity tag to pull out of your local cache folder
model_id = "NousResearch/Hermes-2-Theta-Llama-3-8B"

print("\n=== Initializing Resident Offline NVIDIA AI Pipeline ===")
print(f"Hardware Layer Locked: {torch.cuda.get_device_name(0)}")

print("\n[1/2] Mapping local tokenizer configurations...")
tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True)

print("[2/2] Loading weights straight into RTX 3060 VRAM...")
# Force placement directly to your active CUDA lane 0
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    local_files_only=True
).to("cuda:0")

print("\n[!] Pipeline Established. Uncensored model is 100% resident in VRAM.")
print("====================================================================\n")

while True:
    user_input = input("Tiger-Prompt >>> ")
    if user_input.lower() in ['exit', 'quit']:
        break
    if not user_input.strip():
        continue
        
    inputs = tokenizer(user_input, return_tensors="pt").to("cuda:0")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
    response = tokenizer.decode(outputs, skip_special_tokens=True)
    print(f"\nResponse:\n{response}\n")

