# Repository Script Manifest & Architecture Maps

This repository maintains the isolated execution wrappers engineered for a localized, asymmetric multi-GPU artificial intelligence environment. The architecture decouples interactive conversational workflows from asynchronous background data pipelines to maximize silicon efficiency on non-homogenous hardware.

### 1. `run_local_prompt.py`
* **Execution Lane:** NVIDIA CUDA / TensorRT Core Array (RTX 3060 12GB VRAM).
* **Primary Role:** Hosts the localized, unaligned text generation pipeline (Llama-3 8B) running under 4-bit NF4 double-quantization parameters via `bitsandbytes`.
* **Hardware Shielding:** Fully handles memory management hooks to restrict operations exclusively to CUDA cores, keeping interactive latency to sub-second thresholds.

### 2. `run_parallel_batch.py`
* **Execution Lane:** AMD ROCm / MIGraphX Infrastructure Staging.
* **Primary Role:** Formulated as a high-density, multi-threaded background parsing engine utilizing ONNX Runtime. 
* **Hardware Shielding:** Features custom session configuration constraints (`session.disable_cpu_ep_fallback = "1"`) acting as an explicit hardware circuit breaker. If GPU execution paths fail, it cleanly halts processing to prevent silent fallback to the host CPU, which would trigger instruction panics.

### 3. `run_direct_opencl.py`
* **Execution Lane:** Dual AMD Radeon RX 6700 XT Compute Cores (OpenCL / Mesa Clover).
* **Primary Role:** A highly optimized, direct vector-mapped ingestion script designed to bypass external compiler header limitations (`Protobuf parsing constraints`).
* **Hardware Shielding:** Leverages NumPy numerical arrays mapped directly into Python OpenCL context queues (`pyopencl`). By streaming text transformations directly to the Radeon VRAM registers, it executes parallel byte matrices with 100% isolation from host CPU math instructions.
