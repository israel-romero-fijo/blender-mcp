## 2026-05-20 - Terminator-aware JSON parsing in socket receiver loops
**Learning:** 1MB/2MB JSON payloads over socket in this architecture exhibit O(N²) parsing overhead if every chunk triggers a full `json.loads` call. This is because `json.loads` must parse the entire accumulated buffer every time.
**Action:** Use a heuristic guard like `chunk.rstrip().endswith((b'}', b']'))` before attempting to parse. This reduces complexity to near-linear growth and provides a measured ~30x-200x speedup for large payloads.
