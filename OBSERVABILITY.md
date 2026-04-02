# Observability Testbed for AI Systems

Study software observability as an attack surface: what can wrappers, proxies, and loggers infer about AI workloads without touching model weights?

## Research Question

What sensitive workload information can be reconstructed from software observability layers during AI execution, and what protections reduce that leakage?

## Threat Model

- **Attacker:** Compromised software component (wrapper, proxy, logger, callback)
- **Goal:** Characterize information leakage from observability, not implant logic
- **Outcome:** Identify critical signals and propose defenses

## Tech Stack (MacBook Air Friendly)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Inference | llama.cpp | CPU-first, no GPU deps |
| GPU Observability | psutil + subprocess | Process-level metrics |
| DPU Observability | FastAPI + uvicorn | HTTP proxy metrics |
| Analysis | pandas + numpy | Results aggregation |

## Setup (5 minutes)

```bash
# 1. Build llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git && cd llama.cpp && make && cd ..

# 2. Python environment
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 3. Download model
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/Mistral-7B-Instruct-v0.1.Q4_K_M.gguf -O model.gguf

# 4. Run tests
python3 run_dpu_case.py && python3 summarize_results.py
```

## Two Observability Cases

### GPU-side: Process Wrapper
Measures: latency, memory, throughput per request
Key Finding: Latency rises with prompt length → timing leakage detected
Metrics: elapsed_seconds, memory_used_mb, throughput_tokens_per_sec

### DPU-side: HTTP Proxy
Measures: request metadata, response size, timing
Key Finding: Proxy reveals workload patterns without touching weights
Metrics: prompt_length, response_length, latency_seconds, inferred_complexity

## Files

- gpu_wrapper.py (46 lines) - Process instrumentation
- dpu_proxy.py (46 lines) - FastAPI proxy
- run_dpu_case.py (36 lines) - Test runner
- summarize_results.py (28 lines) - Results aggregator
- prompts/prompts.jsonl - Short/medium/long test workloads
- results/ - CSV outputs

## Defenses

| Leakage Vector | Defense |
|---|---|
| Timing | Constant-time ops, random delays |
| Memory | Pre-allocated pooling |
| Metadata | Telemetry minimization, encryption |
| Proxy | Request padding, multiplexing |
| Plugins | Signed verification |

## Multimodal AI Inspection Alignment

This framework applies to X-ray CT, acoustic microscopy, optical imaging pipelines where AI wraps acquisition/analysis software. Same wrapper patterns, telemetry hooks, reliability concerns.

Presentation Pitch: "I study observability as an attack surface in AI systems. A wrapper measures process signals; a proxy measures request patterns. Without touching weights, both reveal workload structure. This directly applies to multimodal inspection systems where AI is wrapped by orchestration software."

## References

- llama.cpp: https://github.com/ggerganov/llama.cpp
- FastAPI: https://fastapi.tiangolo.com/
- psutil: https://psutil.readthedocs.io/

Disclaimer: Educational and defensive purposes only.
