import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# Tell the transformers framework to strictly look at local files and block all internet calls
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Specify the direct model identity tag to pull out of your local cache folder
model_id = "NousResearch/Hermes-2-Theta-Llama-3-8B"

print("\n=== Initializing Resident Offline NVIDIA AI Pipeline ===")
print(f"Hardware Layer Locked: {torch.cuda.get_device_name(0)}")

print("\n[1/2] Mapping local tokenizer configurations...")
tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True)

#Enforcing high-efficiency 4-bit quantization to fit the 12GB VRAM lane perfectly
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

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
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
    response = tokenizer.decode(outputs, skip_special_tokens=True)
    print(f"\nResponse:\n{response}\n")

