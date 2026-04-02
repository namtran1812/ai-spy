#!/usr/bin/env python3
import fastapi
import uvicorn
import requests
import time
from pathlib import Path
from datetime import datetime

app = fastapi.FastAPI()

class DPUObservabilityProxy:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.requests_log = []
    
    def log_request(self, prompt, prompt_length, response_length, latency):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt_length_words": prompt_length,
            "response_length_words": response_length,
            "latency_seconds": latency,
            "inferred_batch_size": 1,
            "inferred_complexity": "high" if prompt_length > 100 else "medium" if prompt_length > 30 else "low"
        }
        self.requests_log.append(log_entry)
        return log_entry
    
    def save_requests_log(self, output_path="results/dpu_metrics.csv"):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            if self.requests_log:
                f.write(",".join(self.requests_log[0].keys()) + "\n")
                for entry in self.requests_log:
                    f.write(",".join(str(v) for v in entry.values()) + "\n")

proxy = DPUObservabilityProxy()

@app.post("/inference")
async def inference(payload: dict):
    prompt = payload.get("prompt", "")
    prompt_length = len(prompt.split())
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{proxy.backend_url}/inference",
            json=payload,
            timeout=60
        )
        elapsed = time.time() - start_time
        response_text = response.json().get("content", "")
        response_length = len(response_text.split())
        
        log_entry = proxy.log_request(prompt, prompt_length, response_length, elapsed)
        
        return {
            "content": response_text,
            "observability_metadata": log_entry
        }
    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start_time
        return {"error": str(e), "latency": elapsed}

@app.get("/metrics")
async def get_metrics():
    return {"requests_total": len(proxy.requests_log), "log": proxy.requests_log}

@app.on_event("shutdown")
async def shutdown():
    proxy.save_requests_log()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
