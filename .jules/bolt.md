## 2025-05-15 - Quadratic JSON Parsing in Socket Receiver

**Learning:** Socket receiver loops that attempt to `json.loads()` every received chunk exhibit O(N²) complexity relative to the number of chunks. For large payloads or small MTUs, this becomes a significant bottleneck, causing high CPU usage and latency.

**Action:** Implement terminator-aware JSON parsing. Use `chunk.rstrip().endswith((b'}', b']'))` as a heuristic to only attempt parsing when a complete JSON object or array is likely received. Always include a fallback `try...except json.JSONDecodeError` to handle false positives (e.g., terminators inside strings).
## 2025-05-16 - Cached Connection Health and Byte-Native JSON Parsing
**Learning:** Per-request network health checks (even over local sockets) create significant cumulative latency (~0.12s per 1000 calls). Modern Python `json.loads` handles bytes natively, saving a string decoding step in hot communication loops.
**Action:** Implement time-based caching (e.g., 30s) for connection status checks to preserve performance without sacrificing auto-recovery. Always pass bytes directly to `json.loads` in projects requiring Python 3.6+.
