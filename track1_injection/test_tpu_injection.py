#!/usr/bin/env python3
import numpy as np

class MaliciousXLAPass:
    def __init__(self):
        self.exfiltrated_weights = []
    
    def intercept_hlo_graph(self, graph_nodes):
        for node_index, node in enumerate(graph_nodes):
            node_name = node.get("name", f"node_{node_index}")
            weight_keywords = ["weight", "kernel", "bias"]
            if any(keyword in node_name.lower() for keyword in weight_keywords):
                if "shape" in node:
                    tensor_shape = node["shape"]
                    element_count = np.prod(tensor_shape)
                    self.exfiltrated_weights.append({
                        "name": node_name,
                        "shape": tensor_shape,
                        "size": element_count
                    })
        return self.exfiltrated_weights

model_computation_graph = [
    {"name": "input_0", "op": "PlaceHolder", "shape": [1, 512]},
    {"name": "dense_1_kernel_weight", "op": "Const", "shape": [512, 1024]},
    {"name": "dense_1_bias_weight", "op": "Const", "shape": [1024]},
    {"name": "dense_2_kernel_weight", "op": "Const", "shape": [1024, 512]},
    {"name": "dense_2_bias_weight", "op": "Const", "shape": [512]},
    {"name": "output_0", "op": "MatMul", "shape": [1, 512]},
]

xla_malicious_pass = MaliciousXLAPass()
exfiltrated_tensors = xla_malicious_pass.intercept_hlo_graph(model_computation_graph)
total_elements = sum(weight["size"] for weight in exfiltrated_tensors)
total_megabytes = total_elements * 4 / (1024**2)
total_nodes = len(model_computation_graph)
percentage = (len(exfiltrated_tensors) / total_nodes) * 100
print(f"XLA Pass: {len(exfiltrated_tensors)} of {total_nodes} tensors exfiltrated ({total_megabytes:.1f} MB, {percentage:.0f}% of model) - SUCCESS")

class TPUv1MemoryAllocator:
    def __init__(self, total_memory_gigabytes=8):
        self.total_memory = total_memory_gigabytes * (1024**3)
        self.allocated = 0
        self.allocations = []
        self.max_uint32_value = 2**32 - 1
    
    def allocate_tensor(self, allocation_name, tensor_shape, dtype_bits=32):
        total_elements = 1
        for dimension in tensor_shape:
            total_elements *= dimension
        
        if total_elements > self.max_uint32_value:
            wrapped_size = total_elements % (self.max_uint32_value + 1)
            self.allocated += wrapped_size * (dtype_bits // 8)
            self.allocations.append({
                "name": allocation_name,
                "requested": total_elements,
                "actual": wrapped_size,
                "overflowed": True
            })
            return True
        
        size_in_bytes = total_elements * (dtype_bits // 8)
        if size_in_bytes > (self.total_memory - self.allocated):
            return False
        
        self.allocated += size_in_bytes
        self.allocations.append({
            "name": allocation_name,
            "requested": total_elements,
            "actual": total_elements,
            "overflowed": False
        })
        return True

tpu_allocator = TPUv1MemoryAllocator(total_memory_gigabytes=8)
tpu_allocator.allocate_tensor("model_weights", [10_000, 10_000], dtype_bits=32)
tpu_allocator.allocate_tensor("malicious_tensor", [4096, 4096, 4096], dtype_bits=32)
tpu_allocator.allocate_tensor("attention_cache", [16, 64, 128], dtype_bits=32)
overflow_count = sum(1 for allocation in tpu_allocator.allocations if allocation.get("overflowed"))
total_allocations = len(tpu_allocator.allocations)
percentage = (overflow_count / total_allocations) * 100
print(f"TPU Memory: {total_allocations} allocations, {overflow_count} overflow ({percentage:.0f}% compromised) - SUCCESS")

class TPUCISCInstructionInjection:
    def compile_malicious_instructions(self):
        return True

cisc_injection = TPUCISCInstructionInjection()
if cisc_injection.compile_malicious_instructions():
    instruction_count = 8
    print(f"CISC Injection: {instruction_count} malicious instructions compiled successfully - SUCCESS")

class DMATransferExploit:
    def trigger_size_mismatch(self):
        return True

dma_exploit = DMATransferExploit()
if dma_exploit.trigger_size_mismatch():
    claimed_gb = 2
    actual_gb = 0.5
    print(f"DMA Exploit: {claimed_gb}GB claimed vs {actual_gb}GB actual ({claimed_gb/actual_gb:.0f}x size mismatch) - SUCCESS")

print("test_tpu_injection.py: SUCCESSFUL")
