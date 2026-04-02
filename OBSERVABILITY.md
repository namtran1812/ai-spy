# Observability and Reliability in Multimodal AI Inspection Systems

A software-only GPU/DPU observability testbed on a MacBook Air using llama.cpp, Python wrappers, and FastAPI proxies to study what sensitive information surrounding software layers can reconstruct during AI execution.

## Executive Summary

This project combines defensive research framing, a Mac-friendly tech stack, and full starter code for studying observability as an attack surface in AI systems. Rather than modifying weights or embedding hidden logic, we study what legitimate surrounding software components—wrappers, callbacks, loggers, benchmarks, and proxies—can observe during inference.

**Research Question:** What sensitive workload information can be reconstructed from software observability layers during AI execution, and what protections reduce that leakage?

## Threat Model

- **Attacker:** Compromised or over-privileged software component in the AI pipeline
- **Components:** Wrapper, callback, logger, benchmark harness, or request proxy
- **Goal:** Not to implant malicious logic, but to characterize leakage from observability
- **Outcome:** Identify critical signals and propose mitigations (telemetry minimization, signed plugins, runtime anomaly detection)

## Tech Stack (MacBook Air Friendly)

| Component | Technology | Why |
|-----------|-----------|-----|
| Inference Engine | llama.cpp | CPU-first, no GPU deps, small GGUF models run fast |
| Python Wrapper | psutil + subprocess | Process-level observability without system changes |
| Proxy Layer | FastAPI + uvicorn | Lightweight HTTP observation layer |
| Analysis | pandas + numpy | Structured metric collection and reporting |
| Environment | Python 3.8+ venv | Reproducible, isolated setup |

## Project Layout

```
ai-spy/
├── gpu_wrapper.py          # GPU-side observability via process wrapper
├── dpu_proxy.py            # DPU-side observability via HTTP proxy
├── run_dpu_case.py         # Main runner for both cases
├── summarize_results.py    # Results aggregator and reporter
├── requirements.txt        # Python dependencies
├── prompts/
│   └── prompts.jsonl       # Test prompts (short/medium/long)
├── results/
│   ├── gpu_metrics.csv     # GPU wrapper measurements
│   └── dpu_metrics.csv     # DPU proxy measurements
└── README.md               # This file
```

## Quick Start

### 1. Clone and Build llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
cd ..
export LLAMA_CPP_PATH=$(pwd)/llama.cpp
```

### 2. Create Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Get a Small GGUF Model

Download a small quantized model from Hugging Face:

```bash
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/Mistral-7B-Instruct-v0.1.Q4_K_M.gguf -O model.gguf
```

### 4. Run GPU-side Observability Case

```bash
python3 run_dpu_case.py
```

This measures process-level latency, throughput, memory, and prompt-size correlation.

### 5. Run DPU-side Proxy Case (Optional)

Terminal 1:
```bash
# Start llama.cpp server
./llama.cpp/server -m model.gguf --port 8000
```

Terminal 2:
```bash
python3 dpu_proxy.py
```

Terminal 3:
```bash
curl -X POST http://127.0.0.1:8001/inference \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain machine learning"}'

# View metrics
curl http://127.0.0.1:8001/metrics
```

### 6. Summarize Results

```bash
python3 summarize_results.py
```

## What Each Case Measures

### GPU-side Software Observability Case

**What:** Process-level metrics from a wrapper around the inference binary.

**Metrics:**
- Prompt length (words)
- Output length (words)
- Elapsed time (seconds)
- Memory delta (MB)
- Throughput (tokens/sec)

**Why:** A surrounding software layer can infer workload characteristics without touching model weights. Timing and memory patterns leak information about request complexity.

**Defense:** Constant-time operations, memory pooling, noise injection, rate limiting.

### DPU-side Software Observability Case

**What:** Request metadata, timing, and response-size correlation from a sidecar/proxy in front of the inference server.

**Metrics:**
- Timestamp
- Prompt length (words)
- Response length (words)
- Latency (seconds)
- Inferred batch size
- Inferred complexity (low/medium/high)

**Why:** An orchestration or transfer layer can infer workload structure from application metadata alone, even when it never touches model weights.

**Defense:** Telemetry minimization, padding responses to fixed sizes, request multiplexing, randomized timing.

## Example Findings

After running the experiments, your results should show patterns like:

| Prompt Length | Latency (s) | Memory (MB) | Throughput (tok/s) | Complexity |
|---------------|-------------|------------|-------------------|-----------|
| 5 words       | 0.8         | 15.2       | 80                | low       |
| 35 words      | 2.1         | 42.5       | 75                | medium    |
| 150+ words    | 8.5         | 128.3      | 70                | high      |

**Key Observations:**
- Latency rises with prompt length → timing leakage detected
- Memory footprint scales with request complexity → memory-based inference possible
- Proxy layer observes patterns without touching model weights
- Overhead remains practical despite instrumentation

## Alignment with Multimodal AI Inspection

This project directly supports the position in multimodal AI inspection systems:

1. **Python-focused:** All code is pure Python with clear observability hooks.
2. **Wrapper pattern:** Same architecture used in X-ray CT, acoustic microscopy, and optical imaging pipelines.
3. **Structured telemetry:** Extends easily to image-derived metadata from inspection tools.
4. **Reliability focus:** Studies how observability layers affect system robustness and information leakage.
5. **VLM/LLM ready:** Framework applies directly to vision-language models processing inspection data.

## Presentation-Ready Pitch

> I am studying observability as an attack surface in machine learning systems using a software-only testbed on a MacBook Air. In the GPU case, a wrapper around the inference runtime measures execution and memory signals; in the DPU case, a proxy in front of the inference server measures transfer and workload metadata. The goal is to understand what sensitive information these surrounding software layers can reconstruct, how much overhead they add, and what defenses reduce that leakage. This connects directly to reliability in multimodal AI inspection systems, where AI models are wrapped by acquisition, analysis, and orchestration software.

## Suggested Next Steps

1. **Run the baseline** with three prompt lengths (short/medium/long)
2. **Save results** in `results/gpu_metrics.csv` and `results/dpu_metrics.csv`
3. **Generate report** with `python3 summarize_results.py`
4. **Add visualization** with a scatter plot (prompt length vs latency)
5. **Extend workload** from text prompts to image-derived findings from inspection data

## Defenses and Mitigations

| Leakage Vector | Defense | Implementation |
|---------------|---------|-----------------|
| Timing side-channels | Constant-time ops | Add random delays, batch requests |
| Memory patterns | Memory pooling | Pre-allocate, reuse buffers |
| Request metadata | Telemetry minimization | Log only essentials, encrypt logs |
| Proxy visibility | Multiplexing | Pad requests, mix real/dummy traffic |
| Plugin compromise | Signed verification | Check plugin signatures at load |
| Cascading failures | Anomaly detection | Monitor for unexpected patterns |

## Disclaimer

This research is for educational and defensive purposes only. Unauthorized access to computer systems is illegal. This project demonstrates defensive analysis techniques to improve AI system reliability and security.

## References

- llama.cpp: https://github.com/ggerganov/llama.cpp
- GGUF Format: https://github.com/philpax/ggml/blob/main/docs/gguf.md
- FastAPI: https://fastapi.tiangolo.com/
- psutil: https://psutil.readthedocs.io/

## License

MIT
