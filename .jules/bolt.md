## 2026-04-06 - [Socket Communication Optimization]
**Learning:** Quadratic overhead in socket data reception due to repeated `json.loads` on incomplete buffers and `+=` string concatenation on large payloads (like mesh data) was a significant bottleneck. Additionally, mandatory heartbeats ("pings") in connection health checks added unnecessary latency to every tool call.
**Action:** Implemented a JSON terminator heuristic (`}` or `]`) to skip redundant parsing attempts, switched to list-based chunk accumulation for $O(n)$ performance, and replaced active pings with lightweight `socket.fileno()` checks combined with lazy invalidation on failure.
>>>>>>> REPLACE
