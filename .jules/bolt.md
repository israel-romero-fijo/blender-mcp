## 2025-05-14 - Quadratic JSON parsing in socket handlers
**Learning:** Accumulating bytes with `+=` and calling `json.loads()` on every received chunk leads to $O(N^2)$ overhead (both in string copying and redundant parsing). This is particularly severe for large payloads like scene info or asset data.
**Action:** Use list-based accumulation (`chunks.append(data)`) and a terminator-aware heuristic (checking if the chunk ends with `}` or `]`) before attempting to parse. This reduces processing time by ~35x for 250KB payloads and keeps overhead near-linear.
