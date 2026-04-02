# Track 2: Observability Testbed

Software-only GPU/DPU observability testbed on MacBook Air to study what sensitive information surrounding software layers can infer during AI execution.

## Files

- **gpu_wrapper.py** - Process wrapper measuring latency, memory, throughput
- **dpu_proxy.py** - FastAPI HTTP proxy measuring request metadata and timing
- **run_dpu_case.py** - Main test runner for both GPU and DPU cases
- **summarize_results.py** - Results aggregator and report generator
- **requirements.txt** - Python dependencies (psutil, fastapi, pandas, numpy)
- **prompts/prompts.jsonl** - Test workloads (short/medium/long)
- **results/** - CSV outputs for metrics

## Quick Start

```bash
pip install -r requirements.txt
python3 run_dpu_case.py
python3 summarize_results.py
```

## Two Cases

### GPU-side: Process Wrapper
Measures: prompt_length, output_length, elapsed_seconds, memory_used_mb, throughput_tokens_per_sec

### DPU-side: HTTP Proxy  
Measures: timestamp, prompt_length_words, response_length_words, latency_seconds, inferred_complexity

## Key Findings

- Latency correlates with prompt length → timing leakage detected
- Memory usage scales with request complexity → memory-based inference possible
- Proxy observes patterns without touching model weights
- Overhead remains practical despite instrumentation

See `../docs/OBSERVABILITY.md` for full details.
