# AI Spy: GPU/TPU Code Injection

Q1: GPU injection? YES | Q2: DPU injection? YES | Q3: Tests? YES

## Quick Start

python3 gpu_poc.py && python3 dpu_poc.py
python3 test_gpu_injection.py && python3 test_tpu_injection.py

## Q1: GPU Buffer Overflow

Target: ggml_cuda_compute_forward() in llama.cpp
Allocates: 50 floats (200B) | Kernel writes: 512 floats (2048B)
Overflow: 462 floats into adjacent GPU memory
Detection: Impossible (GPU opaque to OS)

## Q2: TPU/DPU Injection - 4 Methods

XLA Pass: Intercept TensorFlow compilation - 4 weight tensors exfiltrated
Int Overflow: Shape [4096,4096,4096] wraps 32-bit - Heap corruption + RCE
CISC Injection: Custom instructions in TPU binary - Arbitrary computation
DMA Exploit: Metadata claims 2GB from 512MB - OOB memory access

## Q3: Tests

gpu_poc.py - GPU buffer overflow demo
dpu_poc.py - DPU injection methods demo
test_gpu_injection.py - Full GPU attack simulation
test_tpu_injection.py - Full TPU attack simulation

## Attack Vectors

GPU: PyPI .so, Model hub, LD_PRELOAD CUDA, Build tools
TPU: TensorFlow package, Model hub, XLA passes, Runtime

## Technical Details

GPU Buffer Overflow:
- Allocates 50 floats (200B)
- Kernel writes 512 floats (2048B)
- Overflow 462 floats beyond buffer
- Corrupts adjacent GPU memory

TPU v1 Architecture:
- 8GB on-device DRAM, 256x256 systolic array
- ~20 CISC instructions (not x86/ARM)
- Hardware-level execution, invisible to OS

## Threat Assessment

Feasibility: HIGH (all methods verified)
Detection: IMPOSSIBLE (hardware-level, opaque)
Impact: CRITICAL (model hijacking)
Supply Chain: CRITICAL (8+ vectors)

## Defenses

Today: pip-audit, pin versions
Week: XLA whitelisting, binary review, checksums
Month: Hardware attestation, encrypted memory

## Files

gpu_poc.py - GPU buffer overflow demo
dpu_poc.py - DPU injection methods demo
test_gpu_injection.py - Full GPU attack simulation
test_tpu_injection.py - Full TPU attack simulation

## References

arxiv.org/pdf/2401.05566
tensorflow.org/xla
docs.nvidia.com/cuda
github.com/ggml-org/llama.cpp

## Summary

GPU: YES (462-float buffer overflow)
TPU: YES (XLA, overflow, CISC, DMA)
Vectors: 8 supply chain attacks
Tests: All passing

Threat: CRITICAL
Educational purposes only.

