import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, StoppingCriteria, StoppingCriteriaList
import os
import sys
import re

# 🔇 ABSOLUTE SYSTEM LOG BLOCK
# This completely hijacks the terminal output stream to permanently kill the white tokenizer warning logs
sys.modules['transformers.utils.logging'].set_verbosity_error()
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

model_id = "NousResearch/Hermes-2-Theta-Llama-3-8B"

print("\n=== Initializing High-Speed Pristine-Output NVIDIA AI Pipeline ===")
print(f"Hardware Layer Locked: {torch.cuda.get_device_name(0)}")

print("\n[1/2] Mapping local tokenizer configurations...")
tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True)

class StopOnUserCriteria(StoppingCriteria):
    def __init__(self, target_sequence, tokenizer):
        self.target_ids = tokenizer.encode(target_sequence, add_special_tokens=False)
        self.target_len = len(self.target_ids)

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_tokens = input_ids[0, -self.target_len:].tolist()
        return last_tokens == self.target_ids

stop_criteria = StopOnUserCriteria("\nUser:", tokenizer)
stopping_criteria_list = StoppingCriteriaList([stop_criteria])

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

print("[2/2] Packing high-efficiency 4-bit quantization layers into VRAM...")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    device_map="auto",
    dtype=torch.float16,
    low_cpu_mem_usage=True,
    local_files_only=True
)
print("\n[✓] Pipeline Established. Hard-Coded Output Text Scrubber Armed.\n")

rolling_history = []

while True:
    user_input = input("Tiger-Prompt >>> ").strip()
    
    if user_input.lower() in ['exit', 'quit']:
        print("Closing memory loops. Logging off.")
        break
        
    if not user_input:
        continue

    rolling_history.append(f"User: {user_input}")
    full_context_prompt = "\n".join(rolling_history) + "\nAssistant:"

    inputs = tokenizer(full_context_prompt, return_tensors="pt").to("cuda:0")
    input_length = inputs.input_ids.shape

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria_list
        )

    generated_tokens = outputs[0, input_length[1]:]
    raw_response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    if raw_response.endswith("User:"):
        raw_response = raw_response[:-5].strip()

    # 🧼 THE HARD-CODED STRING SCRUBBER
    # This automatically strips out any bracketed links, parentheses blocks, URLs, and metadata tags before display
    clean_response = re.sub(r'\[.*?\]', '', raw_response)  # Strips out all [Source: ...] brackets
    clean_response = re.sub(r'\[\d+', '', clean_response)  # Strips an open bracket followed by any numbers
    clean_response = re.sub(r'\(.*?\)', '', clean_response) # Strips out all (End of Text) parentheses loops
    clean_response = re.sub(r'http\S+', '', clean_response)  # Strips out any loose web domains completely
    
    # Standardize spaces and clean up line breaks
    clean_response = "\n".join([line.strip() for line in clean_response.split("\n") if line.strip()])

    print(f"\nResponse: {clean_response}\n")

    rolling_history.append(f"Assistant: {clean_response}")
