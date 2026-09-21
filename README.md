Deviant-AI-Rig: Asymmetric Multi-Vendor AI Cluster on Bare-Metal

A production-grade deployment layout for an isolated, self-contained multimodal private AI rig running mismatched silicon architectures concurrently on consumer-grade budget host hardware.

This repository documents the structural engineering strategies used to establish concurrent execution pipelines across different GPU driver stacks while managing strict host physical layer constraints.

🛠️ System Architecture ManifestHost Compute NodeHost Machine Identity: DeviantCentral Processor: Intel Pentium Gold G5400 (2 Cores, 4 Threads, 3.70 GHz)Physical Constraints: Native architecture lacks AVX2/AVX-512 vector instruction extensions.Memory Fallback Subsystem: 8GB System RAM augmented with a hard-allocated 8GB Swap File block configured persistently via /etc/fstab to prevent Out-Of-Memory (OOM) kernel process kills during tensor layer mapping.Heterogeneous Silicon TopologyPrimary VRAM Compute Lane: 1x NVIDIA GeForce RTX 3060 (12GB GDDR6)Secondary Parallel Compute Lanes: 2x AMD Radeon RX 6700 XT (12GB GDDR6 each)

🚀 Execution Pipelines

🟢 1. Native CUDA Text Generation PipelineThe primary compute lane leverages the NVIDIA driver stack inside an isolated virtual sandbox environment running PyTorch 2.4.1 compiled for CUDA 12.1. This environment hosts an uncensored, high-throughput 8B parameter model running fully resident in VRAM.Configuration Strategy: Incremental structural weight mapping enabled through low CPU memory usage tracking variables to protect the budget host RAM layer from exhaustion panics during tokenizer deployment.

🔴 2. Parallel AMD ONNX Execution Provider SubsystemThe dual Radeon RX 6700 XT cards run concurrently using cross-platform execution blocks. Weights are processed straight on the GPU architecture, avoiding the host processor's vector instruction caps.Circuit-Breaker Security: Node fallbacks are hard-blocked at the execution graph layer. If a mathematical operator fails to map natively to the GPU cores, the runtime triggers a safe software exception rather than letting a silent fallback to the CPU cause a fatal host kernel instruction dump.

📂 Core Deployment ModulesModule 

A: launch_pipeline.shAutomated environment wrapper that applies custom CPU instruction masks and explicitly binds internal shared runtime library links before booting Python.Module 

B: run_local_model.pyMain production interface targeting local file caches only. Maps configurations and loads model files directly into device storage without checking external network layers.Module 

C: test_onnx_pipeline.pyMulti-vendor cross-platform diagnostic script mapping GPU device identification variables and setting strict hardware fallback blocks.

# Deviant-AI-Rig

Self Contained Intel/AMD/Nvidia Multi Modal AI on a Budget
