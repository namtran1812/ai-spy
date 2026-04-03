# AI Spy: GPU/TPU Injection & Observability Research

Comprehensive defensive research combining GPU/TPU injection analysis with software observability testbed for multimodal AI systems.

## Project Structure

```
ai-spy/
├── track1_injection/           GPU/TPU Injection Research (4 Python files)
│   ├── gpu_poc.py             GPU buffer overflow demo (11 lines)
│   ├── dpu_poc.py             TPU/DPU injection demo (31 lines)
│   ├── test_gpu_injection.py  GPU attack surface tests (48 lines)
│   └── test_tpu_injection.py  TPU attack methods tests (97 lines)
│
├── track2_observability/       Software Observability Testbed (4 Python files)
│   ├── gpu_wrapper.py         Process-level observability wrapper (45 lines)
│   ├── dpu_proxy.py           FastAPI HTTP proxy for observability (65 lines)
│   ├── run_dpu_case.py        Main test runner (36 lines)
│   ├── summarize_results.py   Results aggregator and report generator (26 lines)
│   ├── requirements.txt       Python dependencies
│   ├── prompts/
│   │   └── prompts.jsonl      Test workloads (3 JSONL lines)
│   └── results/               CSV metric outputs (generated)
│
├── docs/                       Documentation (2 reference guides)
│   ├── INDEX.md               GPU/TPU injection findings archive
│   └── OBSERVABILITY.md       Testbed methodology and setup
│
└── README.md                  This comprehensive guide
```

---

## Track 1: GPU/TPU Injection Research

**Question:** Can GPU/TPU accelerators be exploited for malware injection?

### Attack Vectors

| Vector | Method | Evidence |
|--------|--------|----------|
| GPU Buffer Overflow | Write beyond CUDA kernel buffer | 462-float overflow (10.2x magnitude) |
| XLA Compiler | Intercept compiler passes | 2 of 6 tensors exfiltrated (33% of model) |
| TPU Integer Overflow | Wrap 32-bit boundary | Detected on memory allocation |
| Training Spy | Capture batch data in-flight | 20 of 20 batches captured (100% interception) |
| CISC Injection | Insert malicious instructions | 8 instructions successfully compiled |
| DMA Exploit | Size mismatch exploitation | 4x size mismatch (2GB claimed vs 0.5GB actual) |

### Quick Start - Track 1

```bash
cd track1_injection/

# Run individual demonstrations
python3 gpu_poc.py              # GPU buffer overflow demo
python3 dpu_poc.py              # TPU injection demo

# Run full test suites
python3 test_gpu_injection.py   # GPU attack surface (includes supply chain: 8 vectors, 100%)
python3 test_tpu_injection.py   # TPU attack methods (XLA, overflow, CISC, DMA)
```

**Expected Output:** SUCCESS messages with quantified metrics for each attack vector.

### Track 1 Files

- **gpu_poc.py** - Demonstrates GPU buffer overflow mechanism
  - Simulates CUDA kernel writing beyond buffer boundaries
  - Output: GPU Injection success with float overflow calculations
  
- **dpu_poc.py** - Demonstrates TPU/DPU injection methods
  - XLACompilerPass: Intercepts model tensors
  - TPUMemoryAllocator: Triggers integer overflow
  - TrainingSpyCallback: Captures training data
  - Output: SUCCESS for each method
  
- **test_gpu_injection.py** - Full GPU attack surface simulation
  - CUDAMemorySimulator: Allocates weights, activations, output buffer
  - Simulates kernel writing 512 floats to 50-float buffer
  - Output: GPU Overflow + Supply Chain vectors
  
- **test_tpu_injection.py** - Full TPU attack methods simulation
  - MaliciousXLAPass: Compiler pass interception
  - TPUv1MemoryAllocator: Memory overflow
  - TPUCISCInstructionInjection: Instruction injection
  - DMATransferExploit: DMA size mismatch
  - Output: SUCCESS for each method with metrics

---

## Track 2: Observability Testbed

**Question:** What can software observability layers infer about AI workloads without touching weights?

### Observability Methods

| Layer | Measurement | Metrics |
|-------|-------------|---------|
| GPU-side (Wrapper) | Process-level instrumentation | Latency, memory, throughput, word counts |
| DPU-side (Proxy) | HTTP proxy interception | Request timing, response patterns, complexity |

### Key Findings

- **Timing Leakage:** Latency correlates with prompt length → workload structure inference possible
- **Memory Correlation:** Memory usage scales with request complexity → resource-based inference
- **Proxy Patterns:** HTTP-level proxy observes patterns without touching model weights
- **Practical Overhead:** Instrumentation overhead remains acceptable

### Quick Start - Track 2

```bash
cd track2_observability/

# Install dependencies
pip install -r requirements.txt

# Run observability tests
python3 run_dpu_case.py         # GPU wrapper + DPU proxy tests
python3 summarize_results.py    # Generate aggregated report
```

**Expected Output:** CSV metric exports + statistics table showing timing/memory/throughput patterns.

### Track 2 Files

- **gpu_wrapper.py** - Process-level observability wrapper
  - Class: GPUWrapper with measure_inference() and save_metrics()
  - Measures: prompt_length_words, output_length_words, elapsed_seconds, memory_used_mb, throughput_tokens_per_sec
  - Output: CSV export to results/gpu_metrics.csv
  
- **dpu_proxy.py** - FastAPI HTTP proxy for DPU-side observability
  - Class: DPUObservabilityProxy with FastAPI endpoints
  - Endpoints: POST /inference (proxies requests), GET /metrics (returns logs)
  - Measures: timestamp, prompt_length_words, response_length_words, latency_seconds, inferred_complexity
  - Output: JSON responses + CSV export to results/dpu_metrics.csv
  
- **run_dpu_case.py** - Main test runner
  - Functions: run_gpu_case(), run_dpu_case()
  - Input: prompts/prompts.jsonl (short/medium/long workloads)
  - Output: Calls gpu_wrapper and provides DPU proxy test instructions
  
- **summarize_results.py** - Results aggregator and reporter
  - Reads: results/gpu_metrics.csv, results/dpu_metrics.csv
  - Computes: Statistics, averages, complexity distribution
  - Output: Formatted tables + key findings interpretation
  
- **requirements.txt** - Python dependencies
  - numpy (simulations), psutil (process metrics), fastapi (web framework), uvicorn (ASGI server), requests (HTTP client), pandas (analysis)
  
- **prompts/prompts.jsonl** - Test workloads
  - 3 prompts: short (5 words), medium (35 words), long (150+ words)
  - Format: JSONL with prompt, length category, research category

---

## Documentation Reference

### docs/INDEX.md
Complete GPU/TPU injection research findings in Q&A format. Includes:
- Detailed attack vectors and technical explanations
- Threat assessment for AI systems
- Defense recommendations
- Academic references

### docs/OBSERVABILITY.md
Testbed methodology and defensive research framing. Includes:
- Threat model analysis
- Tech stack justification
- Setup instructions
- Defense mechanisms
- Job alignment and research context

## Requirements

**Python:** 3.8 or higher

**Track 1 Dependencies:**
- NumPy (for simulations)

**Track 2 Dependencies:**
- psutil (process metrics)
- FastAPI (HTTP framework)
- uvicorn (ASGI server)
- pandas (data analysis)
- NumPy (for simulations)

## Running the Full Research

### Complete Analysis Flow

```bash
# 1. Run injection demonstrations
cd track1_injection/
python3 gpu_poc.py
python3 dpu_poc.py
python3 test_gpu_injection.py
python3 test_tpu_injection.py

# 2. Run observability testbed
cd ../track2_observability/
pip install -r requirements.txt
python3 run_dpu_case.py
python3 summarize_results.py

# 3. Review findings
cat results/gpu_metrics.csv
cat ../docs/INDEX.md
cat ../docs/OBSERVABILITY.md
```
