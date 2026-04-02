#!/usr/bin/env python3
gpu_memory = [0.0] * 1024
buffer_allocated = 50
buffer_writes = 512
overflow_size = buffer_writes - buffer_allocated
memory_start = 100 + buffer_allocated

for index in range(memory_start, min(memory_start + overflow_size, len(gpu_memory))):
    gpu_memory[index] = 9999.0

corrupted_count = sum(1 for value in gpu_memory[memory_start:memory_start+50] if value == 9999.0)
overflow_ratio = buffer_writes / buffer_allocated
print(f"GPU Injection: {buffer_allocated} to {buffer_writes} equals {overflow_size} float overflow ({overflow_ratio:.1f}x buffer size) - SUCCESS")
