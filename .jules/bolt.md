## 2025-05-15 - Quadratic JSON Parsing in Socket Receiver

**Learning:** Socket receiver loops that attempt to `json.loads()` every received chunk exhibit O(N²) complexity relative to the number of chunks. For large payloads or small MTUs, this becomes a significant bottleneck, causing high CPU usage and latency.

**Action:** Implement terminator-aware JSON parsing. Use `chunk.rstrip().endswith((b'}', b']'))` as a heuristic to only attempt parsing when a complete JSON object or array is likely received. Always include a fallback `try...except json.JSONDecodeError` to handle false positives (e.g., terminators inside strings).

## 2026-05-30 - Quadratic Memory Allocation in Socket Receiver
**Learning:** Using `buffer += data` for accumulating bytes in a socket receiver loop has O(N²) time complexity because each concatenation creates a new copy of the entire buffer. For large payloads (e.g. 16MB), this can take seconds, whereas list-based accumulation (`chunks.append(data)` followed by `b"".join(chunks)`) takes milliseconds.
**Action:** Always use list-based accumulation for data received over sockets or when building large strings/bytes objects in loops.
