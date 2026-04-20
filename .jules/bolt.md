## 2025-05-14 - terminator-aware JSON parsing
**Learning:** Attempting `json.loads()` on every received network chunk causes $O(N^2)$ parsing overhead, which becomes a major bottleneck for large payloads (e.g., 1MB+). By checking for potential JSON terminators (`}` or `]`) before parsing, this overhead is virtually eliminated.
**Action:** Always implement terminator-aware checks when receiving JSON payloads in chunks over a stream.

## 2025-05-14 - redundant network pings in connection check
**Learning:** Performing a full command round-trip to verify connection health on every tool call adds significant constant overhead (latency) to every operation.
**Action:** Use lightweight socket state checks (like `fileno()`) for health checks and cache status that doesn't change frequently.
