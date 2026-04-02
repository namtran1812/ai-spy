# GPU/TPU Malware Injection Research

Research package demonstrating GPU/TPU injection attack vectors and proof-of-concepts targeting AI inference systems.

## Overview

This repository contains:
- **GPU PoC** (gpu_poc.py): CUDA buffer overflow mechanism demonstration
- **DPU/TPU PoC** (dpu_poc.py): TPU/DPU injection methods including XLA compiler pass interception and training spy
- **GPU Test Suite** (test_gpu_injection.py): Full GPU attack surface simulation with supply chain analysis
- **TPU Test Suite** (test_tpu_injection.py): All 4 TPU attack methods with quantitative metrics
- **Research Documentation** (INDEX.md): Complete Q&A reference with findings and defenses

## Quick Start

```bash
python3 gpu_poc.py      # GPU buffer overflow demo
python3 dpu_poc.py      # TPU/DPU injection demo
python3 test_gpu_injection.py   # GPU attack surface tests
python3 test_tpu_injection.py   # TPU attack method tests
```

## Research Questions Answered

**Q1: Can GPU kernels be exploited for malware injection?**
- YES: 462-float buffer overflow demonstrated (10.2x buffer size)

**Q2: Can TPU/DPU accelerators be exploited?**
- YES: 4 attack methods verified (XLA pass, integer overflow, CISC injection, DMA exploit)

**Q3: What supply chain vectors enable injection?**
- 8 vectors identified: PyPI, model hubs, LD_PRELOAD, build tools, etc.

## Attack Vectors

**GPU (4 vectors):**
- Buffer overflow in kernel computation
- Weight poisoning during training
- Activation hijacking
- Model substitution

**TPU/DPU (4 vectors):**
- XLA compiler pass interception
- Integer overflow in shape calculations
- CISC instruction injection
- DMA transfer size mismatch exploitation

## Requirements

- Python 3.8+
- NumPy (for simulations)

## Test Results

All simulations passing with quantitative metrics:
- GPU Overflow: 462 floats corrupted (10.2x buffer size)
- XLA Pass: 4 of 6 tensors exfiltrated (67% of model, 4.0 MB)
- TPU Memory: 1 of 3 allocations overflowed (33% compromised)
- Training Spy: 20 of 20 batches captured (100% interception)
- CISC Injection: 8 malicious instructions compiled
- DMA Exploit: 2GB claimed vs 0.5GB actual (4x size mismatch)

## Documentation

See `INDEX.md` for:
- Detailed technical specifications
- Threat assessment and impact analysis
- Defense mechanisms and mitigations
- References and related work

## Disclaimer

This research is for educational and defensive purposes only. Unauthorized access to computer systems is illegal.
