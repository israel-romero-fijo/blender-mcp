## 2026-05-19 - Optimized Socket Communication and JSON Parsing
**Learning:** (N^2)$ JSON parsing and buffer concatenation can severely bottleneck socket-based communication for large payloads. Terminator-aware receiving and list-based accumulation provide near-linear scaling.
**Action:** Always use terminator-aware heuristics (`rstrip().endswith()`) before attempting to parse JSON from a socket buffer, and prefer `list.append()` + `join()` for buffer management.
