## 2026-04-03 - [Optimizing Socket Communication Latency and JSON Parsing]
**Learning:** Redundant network roundtrips for status checks (e.g., pinging Blender on every tool call) can double the latency of simple commands. Additionally, repeated JSON parsing attempts on accumulating byte chunks leads to quadratic $O(n^2)$ overhead for large payloads.
**Action:** Use lightweight local socket state checks (like `fileno()`) for connection heartbeat and implement heuristics (e.g., checking for JSON terminators `}` or `]`) to skip redundant parsing attempts during stream reception.
