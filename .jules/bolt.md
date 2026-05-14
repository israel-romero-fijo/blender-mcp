## 2025-05-14 - Optimized Socket JSON Parsing
**Learning:** 1MB/2MB JSON payloads over socket exhibit O(N^2) parsing overhead if every chunk triggers a full `json.loads` call; terminator-aware parsing (checking for `}` or `]`) reduces this to near-linear growth. Also, list-based accumulation is more efficient than byte concatenation in Python for building large buffers from chunks.
**Action:** Always implement terminator-aware checks (`rstrip().endswith((b'}', b']'))`) when receiving JSON over sockets in chunks.
