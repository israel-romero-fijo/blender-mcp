## 2025-05-15 - Quadratic JSON Parsing in Socket Receiver

**Learning:** Socket receiver loops that attempt to `json.loads()` every received chunk exhibit O(N²) complexity relative to the number of chunks. For large payloads or small MTUs, this becomes a significant bottleneck, causing high CPU usage and latency.

**Action:** Implement terminator-aware JSON parsing. Use `chunk.rstrip().endswith((b'}', b']'))` as a heuristic to only attempt parsing when a complete JSON object or array is likely received. Always include a fallback `try...except json.JSONDecodeError` to handle false positives (e.g., terminators inside strings).
