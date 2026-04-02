# Track 1: GPU/TPU Injection Research

Defensive research demonstrating GPU/TPU injection attack vectors and proof-of-concepts targeting AI inference systems.

## Files

- **gpu_poc.py** - GPU buffer overflow mechanism demo
- **dpu_poc.py** - TPU/DPU injection methods demo (XLA, integer overflow, CISC, DMA)
- **test_gpu_injection.py** - Full GPU attack surface simulation
- **test_tpu_injection.py** - Full TPU attack methods simulation

## Quick Start

```bash
python3 gpu_poc.py
python3 dpu_poc.py
python3 test_gpu_injection.py
python3 test_tpu_injection.py
```

## Research Findings

| Question | Answer | Evidence |
|----------|--------|----------|
| GPU injection? | YES | 462-float buffer overflow (10.2x) |
| TPU injection? | YES | 4 methods verified (XLA, overflow, CISC, DMA) |
| Supply chain? | YES | 8 attack vectors identified |

## Metrics

- GPU: 462-float buffer overflow with 10.2x magnitude
- XLA: 2 of 6 tensors exfiltrated (33% of model)
- TPU Memory: Integer overflow detected on 32-bit boundary
- Training Spy: 20 of 20 batches captured (100% interception)
- CISC: 8 malicious instructions compiled
- DMA: 4x size mismatch exploitation verified

See `../docs/INDEX.md` for full details.
