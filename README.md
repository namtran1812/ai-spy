# AI Spy: GPU/TPU Injection & Observability Research

Two-track defensive research: GPU/TPU injection analysis + software observability testbed for multimodal AI systems.

## Research Questions

| Q | Answer | Evidence |
|---|--------|----------|
| GPU injection? | YES | 462-float buffer overflow (10.2x) |
| TPU injection? | YES | 4 methods (XLA, overflow, CISC, DMA) |
| Supply chain? | YES | 8 attack vectors identified |

## Quick Start

```bash
# Track 1: GPU/TPU Injection Research
python3 gpu_poc.py && python3 test_gpu_injection.py
python3 dpu_poc.py && python3 test_tpu_injection.py

# Track 2: Observability Testbed
python3 run_dpu_case.py        # GPU-side wrapper
python3 dpu_proxy.py            # DPU-side proxy
python3 summarize_results.py    # Analyze metrics
```

## Track 1: GPU/TPU Injection

**Files:** gpu_poc.py, dpu_poc.py, test_gpu_injection.py, test_tpu_injection.py

GPU: Buffer overflow in CUDA kernel | TPU: XLA interception + integer overflow + CISC injection + DMA exploit

See INDEX.md for full research details, threat assessment, and defenses.

## Track 2: Observability Testbed

**Files:** gpu_wrapper.py, dpu_proxy.py, run_dpu_case.py, summarize_results.py

Study what software observability layers (wrappers, proxies) can infer about workloads without touching model weights.

See OBSERVABILITY.md for setup, tech stack, metrics, and alignment with multimodal AI inspection.

## Files

| File | Lines | Purpose |
|------|-------|---------|
| gpu_poc.py | 11 | GPU buffer overflow demo |
| dpu_poc.py | 31 | TPU/DPU injection demo |
| test_gpu_injection.py | 49 | GPU attack surface |
| test_tpu_injection.py | 82 | TPU attack surface |
| gpu_wrapper.py | 46 | Process observability |
| dpu_proxy.py | 46 | HTTP proxy observability |
| run_dpu_case.py | 36 | Test runner |
| summarize_results.py | 28 | Results aggregator |

## Documentation

- **INDEX.md** - GPU/TPU injection research findings, threat model, defenses
- **OBSERVABILITY.md** - Testbed setup, tech stack, metrics, job alignment

## Requirements

Python 3.8+, NumPy (injection tests), psutil/FastAPI/pandas (observability testbed)

## Disclaimer

Educational and defensive purposes only. Unauthorized system access is illegal.
