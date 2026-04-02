# AI Spy: GPU/TPU Injection & Observability Research

Two-track defensive research: GPU/TPU injection analysis + software observability testbed for multimodal AI systems.

## Project Structure

```
ai-spy/
├── track1_injection/           GPU/TPU injection research
│   ├── README.md              Track 1 overview and quick start
│   ├── gpu_poc.py             GPU buffer overflow demo
│   ├── dpu_poc.py             TPU/DPU injection demo
│   ├── test_gpu_injection.py  GPU attack surface tests
│   └── test_tpu_injection.py  TPU attack methods tests
│
├── track2_observability/       Software observability testbed
│   ├── README.md              Track 2 overview and quick start
│   ├── gpu_wrapper.py         Process-level observability wrapper
│   ├── dpu_proxy.py           FastAPI HTTP proxy for observability
│   ├── run_dpu_case.py        Main test runner
│   ├── summarize_results.py   Results aggregator
│   ├── requirements.txt       Python dependencies
│   ├── prompts/               Test workloads
│   └── results/               CSV metric outputs
│
├── docs/                       Documentation
│   ├── INDEX.md               GPU/TPU injection findings
│   └── OBSERVABILITY.md       Testbed setup and methodology
│
└── README.md                  This file
```

## Quick Start

### Track 1: GPU/TPU Injection Research

```bash
cd track1_injection/
python3 gpu_poc.py
python3 dpu_poc.py
python3 test_gpu_injection.py
python3 test_tpu_injection.py
```

### Track 2: Observability Testbed

```bash
cd track2_observability/
pip install -r requirements.txt
python3 run_dpu_case.py        # GPU-side wrapper test
python3 summarize_results.py   # Generate report
```

## Research Questions & Findings

| Q | Answer | Evidence |
|---|--------|----------|
| GPU injection? | YES | 462-float buffer overflow (10.2x magnitude) |
| TPU injection? | YES | 4 methods verified (XLA, overflow, CISC, DMA) |
| Supply chain? | YES | 8 attack vectors identified |
| Observability leakage? | YES | Timing & memory patterns reveal workload structure |

## Track 1: GPU/TPU Injection

**Research:** Can GPU/TPU accelerators be exploited for malware injection?

**Methods:**
- GPU: Buffer overflow in CUDA kernel
- TPU: XLA compiler pass interception + integer overflow + CISC injection + DMA exploit

**Files:** See `track1_injection/README.md`

## Track 2: Observability Testbed

**Research:** What can software observability layers infer about AI workloads without touching weights?

**Methods:**
- GPU-side: Process wrapper measuring latency, memory, throughput
- DPU-side: HTTP proxy measuring request metadata and response patterns

**Files:** See `track2_observability/README.md`

## Documentation

- **docs/INDEX.md** - Complete GPU/TPU injection research findings
- **docs/OBSERVABILITY.md** - Testbed methodology, setup, and defenses

## Requirements

Python 3.8+

**Track 1:** NumPy (for simulations)
**Track 2:** psutil, FastAPI, uvicorn, pandas, NumPy

## Disclaimer

Educational and defensive purposes only. Unauthorized system access is illegal.
