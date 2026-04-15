## 2025-05-15 - [Optimization of Communication and Processing]
**Learning:** Quadratic parsing overhead in chunked network communication (repeatedly calling `json.loads` on an accumulating buffer) can significantly slow down large payloads. Checking for JSON terminators (`}` or `]`) before parsing yields massive speedups (~32x for 1MB).
**Action:** Always implement terminator-aware parsing in communication layers that handle variable-length JSON chunks.

## 2025-05-15 - [Lightweight Socket Health Checks]
**Learning:** Sending a "ping" command to verify connection health on every tool call adds unnecessary latency and network round-trips. `socket.fileno()` or similar OS-level checks are sufficient for passive health monitoring.
**Action:** Use lightweight socket state checks for persistent connections and only sync stateful information (like feature flags) during initial connection or explicit refresh calls.
