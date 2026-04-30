## 2025-04-30 - Terminator-aware JSON parsing
**Learning:** Checking for JSON terminators ('}' or ']') before calling `json.loads` on accumulated socket chunks avoids quadratic parsing overhead. For a 1MB payload, this yielded a ~40x speedup (0.1207s to 0.0031s).
**Action:** Always implement terminator checks when receiving JSON over sockets in chunks.

**Learning:** Passing bytes directly to `json.loads` is faster and more memory-efficient than decoding to a UTF-8 string first.
**Action:** Use `json.loads(bytes_data)` instead of `json.loads(bytes_data.decode('utf-8'))`.
