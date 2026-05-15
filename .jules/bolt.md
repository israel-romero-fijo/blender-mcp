## 2025-05-14 - Optimized Socket JSON Parsing
**Learning:** 1MB+ JSON payloads sent over sockets in small chunks suffer from $O(N^2)$ parsing overhead when every chunk triggers a full `json.loads()`.
**Action:** Use a terminator-aware check (`chunk.rstrip().endswith((b'}', b']'))`) to only attempt parsing when the payload appears complete, reducing overhead to near-linear.
