## 2026-05-09 - Socket JSON Parsing Bottleneck
**Learning:** Large JSON payloads received over sockets in small chunks exhibit $O(N^2)$ performance degradation if `json.loads()` is called on every chunk. In this architecture, a 1MB payload split into 1024 chunks caused significant latency (~1s).
**Action:** Implement terminator-aware parsing (checking for `}` or `]`) and use list-based chunk accumulation to achieve near-linear performance (~4ms for 1MB).
