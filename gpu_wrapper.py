#!/usr/bin/env python3
import subprocess
import psutil
import time
import json
import os
from pathlib import Path

class GPUWrapper:
    def __init__(self, llama_cpp_path="/opt/llama.cpp", model_path="model.gguf"):
        self.llama_cpp_path = llama_cpp_path
        self.model_path = model_path
        self.metrics = []
    
    def measure_inference(self, prompt, max_tokens=128):
        process_memory_before = psutil.Process(os.getpid()).memory_info().rss / (1024**2)
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [f"{self.llama_cpp_path}/main", "-m", self.model_path, "-n", str(max_tokens), "-p", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.time() - start_time
            process_memory_after = psutil.Process(os.getpid()).memory_info().rss / (1024**2)
            
            memory_delta = process_memory_after - process_memory_before
            prompt_tokens = len(prompt.split())
            output_length = len(result.stdout.split())
            
            metric = {
                "prompt_length_words": prompt_tokens,
                "output_length_words": output_length,
                "elapsed_seconds": elapsed,
                "memory_used_mb": memory_delta,
                "throughput_tokens_per_sec": output_length / elapsed if elapsed > 0 else 0
            }
            self.metrics.append(metric)
            return metric
        except subprocess.TimeoutExpired:
            return {"error": "timeout", "prompt_length": len(prompt.split())}
    
    def save_metrics(self, output_path="results/gpu_metrics.csv"):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            if self.metrics:
                f.write(",".join(self.metrics[0].keys()) + "\n")
                for metric in self.metrics:
                    f.write(",".join(str(v) for v in metric.values()) + "\n")

if __name__ == "__main__":
    wrapper = GPUWrapper()
    
    prompts = [
        "What is machine learning?",
        "Explain deep neural networks and how they learn from data through backpropagation.",
        "Describe a complete multimodal AI inspection system processing X-ray, acoustic, and optical data."
    ]
    
    for prompt in prompts:
        print(f"Testing prompt ({len(prompt.split())} words)...")
        metric = wrapper.measure_inference(prompt, max_tokens=64)
        if "error" not in metric:
            print(f"  Latency: {metric['elapsed_seconds']:.2f}s, Memory: {metric['memory_used_mb']:.2f}MB, Throughput: {metric['throughput_tokens_per_sec']:.2f} tok/s")
    
    wrapper.save_metrics()
    print(f"\nMetrics saved to results/gpu_metrics.csv")
