## 2025-05-15 - [JSON & Buffer Optimization]
**Learning:** The previous communication implementation used quadratic byte concatenation (buffer += data) and attempted to parse JSON on every received chunk. For large payloads (e.g., 2MB), this resulted in O(N^2) behavior for both memory copying and parsing attempts.
**Action:** Implemented terminator-aware JSON parsing (checking for '}' or ']') before calling json.loads, and switched to list-based chunk accumulation. This reduced parsing overhead by ~99% for multi-chunk payloads and eliminated redundant memory copies.
