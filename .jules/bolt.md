## 2025-05-15 - Quadratic JSON Parsing in Socket Receiver

**Learning:** Socket receiver loops that attempt to `json.loads()` every received chunk exhibit O(N²) complexity relative to the number of chunks. For large payloads or small MTUs, this becomes a significant bottleneck, causing high CPU usage and latency.

**Action:** Implement terminator-aware JSON parsing. Use `chunk.rstrip().endswith((b'}', b']'))` as a heuristic to only attempt parsing when a complete JSON object or array is likely received. Always include a fallback `try...except json.JSONDecodeError` to handle false positives (e.g., terminators inside strings).

## 2025-05-16 - Quadratic Byte Concatenation in Large Payload Handling

**Learning:** Using `buffer += data` for byte accumulation in socket handlers leads to O(N²) memory allocation and copying overhead. While negligible for small commands, it becomes catastrophic (e.g., 15s+ delay) for multi-megabyte payloads like those containing base64 images or complex mesh data.

**Action:** Always use list-based accumulation (`chunks.append(data)`) followed by `b"".join(chunks)` when receiving data from a socket. Additionally, leverage `json.loads(bytes)` in Python 3.10+ to avoid redundant UTF-8 decoding in the main communication loop.
