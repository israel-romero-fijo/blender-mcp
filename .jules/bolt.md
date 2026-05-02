## 2026-05-02 - [Terminator-aware JSON Parsing]
**Learning:** In socket-based communication where JSON payloads are received in chunks, calling `json.loads()` on every chunk results in $O(N^2)$ overhead. By checking for JSON terminators (`}` or `]`) before attempting to parse, we can avoid redundant parsing and achieve near-linear performance.
**Action:** Always implement terminator-aware parsing for chunked JSON reception.
