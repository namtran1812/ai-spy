# Organization & File Structure Guide

## Directory Hierarchy

```
ai-spy/
├── track1_injection/               GPU/TPU Injection Research
│   ├── README.md                   Track 1 documentation
│   ├── gpu_poc.py                  Proof-of-concept: GPU buffer overflow
│   ├── dpu_poc.py                  Proof-of-concept: TPU/DPU injection
│   ├── test_gpu_injection.py       Test suite: Full GPU attack surface
│   └── test_tpu_injection.py       Test suite: Full TPU attack methods
│
├── track2_observability/           Software Observability Testbed
│   ├── README.md                   Track 2 documentation
│   ├── gpu_wrapper.py              Process wrapper for GPU observability
│   ├── dpu_proxy.py                FastAPI proxy for DPU observability
│   ├── run_dpu_case.py             Main test runner (GPU + DPU cases)
│   ├── summarize_results.py        Results aggregator and reporter
│   ├── requirements.txt            Python dependencies
│   ├── prompts/                    Test workloads directory
│   │   └── prompts.jsonl           Short/medium/long test prompts
│   └── results/                    CSV metric outputs
│       ├── gpu_metrics.csv         GPU wrapper measurements (generated)
│       └── dpu_metrics.csv         DPU proxy measurements (generated)
│
├── docs/                           Documentation
│   ├── INDEX.md                    GPU/TPU injection findings & threat model
│   └── OBSERVABILITY.md            Testbed methodology & defenses
│
├── README.md                       Project overview & quick start
├── .gitignore                      Git ignore rules (.venv, *.csv, etc)
└── .git/                           Git repository
```

## File Organization Principles

### Track 1: Injection Research
- **Purpose:** Demonstrate GPU/TPU injection attack vectors
- **Focus:** Technical proof-of-concept and comprehensive testing
- **Outputs:** SUCCESS messages with quantified metrics
- **Files:** 4 Python files (PoC + tests)

### Track 2: Observability Testbed
- **Purpose:** Study information leakage from software layers
- **Focus:** MacBook Air-friendly, reproducible setup
- **Outputs:** CSV metrics + aggregated reports
- **Files:** 4 Python files + config + data

### Documentation
- **Index.md:** GPU/TPU research (static, archived)
- **OBSERVABILITY.md:** Testbed methodology (how-to guide)
- **README.md:** Project entry point
- **Track READMEs:** Quick start for each track

## Consistency Conventions

### File Naming
- `*_poc.py` - Proof of concept demonstrations
- `test_*.py` - Full test suites
- `*_wrapper.py` - Process instrumentation
- `*_proxy.py` - HTTP intermediaries
- `run_*.py` - Main execution runners
- `summarize_*.py` - Report generators

### Output Consistency
All Python files print metrics in format:
```
[COMPONENT]: [METRIC VALUES] ([CALCULATION]) - SUCCESS
```

Example:
```
GPU Injection: 50 to 512 equals 462 float overflow (10.2x buffer size) - SUCCESS
```

### Data Format
All observability data saved to CSV with headers:
```
GPU: prompt_length_words, output_length_words, elapsed_seconds, memory_used_mb, throughput_tokens_per_sec
DPU: timestamp, prompt_length_words, response_length_words, latency_seconds, inferred_batch_size, inferred_complexity
```

## Code Quality Standards

✅ **All files follow:**
- No unused imports (every import used)
- No unused variables (every computed value reported)
- No dead code (every function contributes to output)
- Consistent metric names across all files
- All output contributes to final reports
- Clean separation of concerns
- Humanized variable names (not cryptic)
- Simple numbers metrics (quantified leakage)

## Navigation Guide

**To run GPU/TPU injection research:**
```bash
cd track1_injection/
python3 gpu_poc.py && python3 dpu_poc.py
python3 test_gpu_injection.py && python3 test_tpu_injection.py
```

**To run observability testbed:**
```bash
cd track2_observability/
pip install -r requirements.txt
python3 run_dpu_case.py
python3 summarize_results.py
```

**To read documentation:**
- Overview: `README.md`
- Track 1 details: `docs/INDEX.md`
- Track 2 details: `docs/OBSERVABILITY.md`
- Track-specific: `track1_injection/README.md` or `track2_observability/README.md`

## Maintenance Guidelines

1. **Adding new code:**
   - Injection research → `track1_injection/`
   - Observability testbed → `track2_observability/`
   - General utils → Root level or new `utils/` dir

2. **Updating documentation:**
   - Research findings → `docs/INDEX.md`
   - Testbed methods → `docs/OBSERVABILITY.md`
   - Quick start → Track-specific README

3. **Code standards:**
   - Every variable must be used
   - Every print must report a metric
   - Every metric must have units
   - All outputs format consistently

4. **File cleanup:**
   - `.gitignore` automatically excludes *.csv and .venv/
   - Generated results/ files are not committed
   - Only source code and documentation tracked
