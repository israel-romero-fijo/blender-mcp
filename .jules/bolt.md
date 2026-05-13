## 2025-05-15 - Terminator-aware JSON parsing
**Learning:** Socket receiver loops that accumulate chunks and attempt `json.loads` on every chunk exhibit quadratic O(N^2) complexity. This is because each chunk triggers a full parse of the current buffer.
**Action:** Use a heuristic like `chunk.rstrip().endswith((b'}', b']'))` to only attempt parsing when the buffer likely contains a complete JSON object or array. Combined with list-based chunk accumulation (`chunks.append` + `b''.join`), this reduces overhead to near-linear O(N).
