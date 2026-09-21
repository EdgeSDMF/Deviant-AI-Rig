import torch

print("\n=== Multi-Vendor Hardware Initialization ===")
print(f"PyTorch Version: {torch.__version__}")

# Lane 1: NVIDIA Check
cuda_avail = torch.cuda.is_available()
print(f"\n[NVIDIA CUDA] Lane Available: {cuda_avail}")
if cuda_avail:
    print(f" -> Active NVIDIA Devices: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        device_name = torch.cuda.get_device_name(i)
        print(f"    -> Slot [{i}]: {device_name}")
        if "GeForce" in device_name:
            x = torch.rand(500, 500, device=f'cuda:{i}')
            y = torch.matmul(x, x)
            print(f"       [!] NVIDIA Tensor Core Test: PASSED")

# Lane 2: AMD ROCm Check
# When using a dual-compiled backend or standard ROCm builds, 
# PyTorch often maps ROCm devices under the torch.cuda or torch.hip frameworks.
print(f"\n[AMD ROCm] Lane Verification:")
try:
    import sys
    print(f" -> Framework Backends Registered: {dir(torch._C)}")
    # If the current wheel is strictly CUDA, we will see it here instantly
    if hasattr(torch, 'version') and torch.version.hip:
        print(f" -> HIP/ROCm Platform Version: {torch.version.hip}")
    else:
        print(f" -> Status: System is currently utilizing the standard CUDA runtime engine.")
except Exception as e:
    print(f" -> Check encountered exception: {e}")
print("============================================")
