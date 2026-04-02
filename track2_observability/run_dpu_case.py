#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def run_gpu_case():
    from gpu_wrapper import GPUWrapper
    
    print("\n=== GPU-side Software Observability Case ===\n")
    wrapper = GPUWrapper()
    
    prompts_file = Path("prompts/prompts.jsonl")
    if not prompts_file.exists():
        print("Error: prompts/prompts.jsonl not found")
        return
    
    with open(prompts_file) as f:
        for line in f:
            prompt_data = json.loads(line)
            prompt = prompt_data["prompt"]
            length_category = prompt_data["length"]
            
            print(f"Testing {length_category} prompt ({len(prompt.split())} words)...")
            metric = wrapper.measure_inference(prompt, max_tokens=64)
            
            if "error" not in metric:
                print(f"  Latency: {metric['elapsed_seconds']:.2f}s")
                print(f"  Memory: {metric['memory_used_mb']:.2f}MB")
                print(f"  Throughput: {metric['throughput_tokens_per_sec']:.2f} tok/s\n")
    
    wrapper.save_metrics()
    print("GPU metrics saved to results/gpu_metrics.csv\n")

def run_dpu_case():
    print("\n=== DPU-side Software Observability Case ===\n")
    print("Start the DPU proxy with: python3 dpu_proxy.py")
    print("Then in another terminal, run:")
    print("  curl -X POST http://127.0.0.1:8001/inference -H 'Content-Type: application/json' -d '{\"prompt\": \"test\"}'")
    print("Get metrics with:")
    print("  curl http://127.0.0.1:8001/metrics\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dpu":
        run_dpu_case()
    else:
        run_gpu_case()
