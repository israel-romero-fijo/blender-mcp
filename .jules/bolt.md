## 2025-02-14 - Optimized Socket Communication with Terminator-Aware JSON Parsing

**Learning:** Large JSON payloads over TCP sockets exhibit O(N²) parsing overhead when every chunk triggers a full `json.loads` call. Additionally, repeated byte string concatenation (`buffer += chunk`) in Python is inefficient due to frequent memory re-allocations.

**Action:** Use list-based accumulation (`chunks.append(chunk)`) and implement a terminator-aware check (`chunk.rstrip().endswith((b'}', b']'))`) before attempting to parse the accumulated buffer. This reduces overhead to near-linear O(N).
