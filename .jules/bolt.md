# Bolt's Performance Journal ⚡

## Mission
- Speed is a feature
- Every millisecond counts
- Measure first, optimize second
- Don't sacrifice readability for micro-optimizations

## 2025-05-15 - Terminator-aware JSON parsing
**Learning:** In socket-based communication receiving JSON in chunks, attempting to `json.loads()` on every chunk results in $O(N^2)$ parsing overhead. For a 1MB payload split into 1KB chunks, this can be the difference between milliseconds and seconds of processing time.
**Action:** Use a list to accumulate chunks and only attempt `json.loads()` when the chunk ends with a likely JSON terminator (`}` or `]`).
