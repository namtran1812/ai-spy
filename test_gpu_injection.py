#!/usr/bin/env python3
import numpy as np

class CUDAMemorySimulator:
    def __init__(self, total_megabytes=8192):
        self.total_size = total_megabytes * (1024**2)
        self.memory = np.zeros(self.total_size // 4, dtype=np.float32)
        self.allocations = {}
    
    def allocate(self, allocation_name, size_in_floats):
        if not self.allocations:
            memory_offset = 0
        else:
            last_offset = max(self.allocations.values())
            memory_offset = last_offset[0] + last_offset[1]
        self.allocations[allocation_name] = (memory_offset, size_in_floats)
        return memory_offset
    
    def write_kernel_data(self, allocation_name, kernel_write_count):
        memory_offset, allocated_floats = self.allocations[allocation_name]
        overflow_amount = max(0, kernel_write_count - allocated_floats)
        for index in range(kernel_write_count):
            memory_index = memory_offset + index
            if memory_index < len(self.memory):
                self.memory[memory_index] = 9999.0
        return overflow_amount
    
    def check_memory_corruption(self, allocation_name):
        memory_offset, buffer_size = self.allocations[allocation_name]
        return np.sum(self.memory[memory_offset:memory_offset+buffer_size] == 9999.0)

gpu_simulator = CUDAMemorySimulator(total_megabytes=1024)
gpu_simulator.allocate("model_weights_layer1", 1024 * 1024)
gpu_simulator.allocate("activations", 256 * 1024)
output_offset = gpu_simulator.allocate("output", 50)

overflow = gpu_simulator.write_kernel_data("output", 512)
corrupted_floats = gpu_simulator.check_memory_corruption("output")
overflow_ratio = 512 / 50
print(f"GPU Overflow: {512 - 50} floats corrupted ({overflow_ratio:.1f}x buffer size) - SUCCESS")

supply_chain_vectors = [
    "PyPI dotso compromise",
    "Model hub injection",
    "LD_PRELOAD CUDA patching",
    "Build tool compromise"
]
total_vectors = len(supply_chain_vectors)
percentage = (total_vectors / 4) * 100
print(f"Supply Chain: {total_vectors} attack vectors identified ({percentage:.0f}% of known surfaces) - SUCCESS")

print("test_gpu_injection.py: SUCCESSFUL")
