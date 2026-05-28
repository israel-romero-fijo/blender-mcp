## 2025-05-15 - Quadratic JSON Parsing in Socket Receiver

**Learning:** Socket receiver loops that attempt to `json.loads()` every received chunk exhibit O(N²) complexity relative to the number of chunks. For large payloads or small MTUs, this becomes a significant bottleneck, causing high CPU usage and latency.

**Action:** Implement terminator-aware JSON parsing. Use `chunk.rstrip().endswith((b'}', b']'))` as a heuristic to only attempt parsing when a complete JSON object or array is likely received. Always include a fallback `try...except json.JSONDecodeError` to handle false positives (e.g., terminators inside strings).

## 2025-05-24 - Redundant RTT and O(N²) Buffer Reallocation

**Learning:** Macro-optimizations like removing redundant round-trips (RTT) in connection management can have as much impact as micro-optimizations. Pinging the backend on every tool call via `get_blender_connection` added ~0.3ms of unnecessary latency per command. Additionally, using `buffer += data` for bytes accumulation in socket loops leads to O(N²) memory reallocation overhead, which is devastating for large payloads.

**Action:** Audit connection/lifecycle getters for hidden "ping" or state-sync logic that can be deferred or cached. Always use list-based chunk accumulation (`chunks.append(data)` followed by `b"".join(chunks)`) for socket receiving loops to ensure linear performance.
