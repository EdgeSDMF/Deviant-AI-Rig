import onnxruntime as ort
import numpy as np

# 1. Enforce strict session settings to shield the Pentium CPU
session_options = ort.SessionOptions()
session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
# Prevent any unmapped node from falling back to CPU vector math
session_options.add_session_config_entry("session.disable_cpu_ep_fallback", "1")

# 2. Asymmetric Execution Setup
# Define providers for both your NVIDIA and AMD lanes safely
cuda_provider_options = {
    'device_id': 0, # Maps to your RTX 3060
    'cudnn_conv_algo_search': 'DEFAULT',
}

migraphx_provider_options = {
    'device_id': 0, # Maps to your first RX 6700 XT lane (adjust index as needed)
    'migraphx_fp16_enable': True
}

# Explicitly allocate sessions targeting individual GPUs
try:
    # RTX 3060 Execution Session
    nvidia_session = ort.InferenceSession(
        "model.onnx", 
        sess_options=session_options, 
        providers=[('CUDAExecutionProvider', cuda_provider_options)]
    )
    print("NVIDIA RTX 3060 Lane: Initialized via ONNX Runtime (Bypassed PyTorch AVX2).")

    # Background RX 6700 XT Batch Session
    amd_session = ort.InferenceSession(
        "model.onnx", 
        sess_options=session_options, 
        providers=[('MIGraphXExecutionProvider', migraphx_provider_options)]
    )
    print("AMD Radeon RX 6700 XT Lane: Initialized via OpenCL/MIGraphX.")

except Exception as e:
    print(f"Hardware-safety halt: Graph optimization rejected fallback: {e}")
