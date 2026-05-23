## 2026-05-23 - Optimized Socket JSON Receiving
**Learning:** Socket-based JSON receiving loops that attempt `json.loads` on every chunk exhibit quadratic O(N²) time complexity relative to the number of chunks. A simple terminator-aware check (`rstrip().endswith((b'}', b']'))`) reduces this to near-linear O(N) performance.
**Action:** Always use terminator-aware checks and list-based chunk accumulation for large JSON payloads over sockets.
