#!/usr/bin/env bash
# ==============================================================================
# RIG IDENTIFIER: "Deviant" Asymmetric Multi-Vendor Pipeline Orchestration
# ==============================================================================
set -e

echo "=================================================================="
echo "Starting Asymmetric Environment Initialization Sequence for Deviant"
echo "=================================================================="

# Section 1: AVX2 Protection for Intel Pentium Gold G5400
export ORT_DISABLE_AVX2=1
export OPENBLAS_CORETYPE=Pentium
export MKL_DEBUG_CPU_TYPE=5
export CUDA_DEVICE_ORDER="PCI_BUS_ID"

# Section 2: Shared Library Linker Mapping
export LD_LIBRARY_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH

# Section 3: Launch Local Resident Model directly on RTX 3060 CUDA Lane
if [ -f "run_local_model.py" ]; then
    echo "[!] Launching run_local_model.py directly onto RTX 3060..."
    python3 run_local_model.py
else
    echo "[WARNING] Initialized environment cleanly, but run_local_model.py was not found."
fi
