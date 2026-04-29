## 2025-05-22 - [JSON Parsing Optimization]
**Learning:** Calling `json.loads()` on every chunk received over a socket leads to $O(N^2)$ complexity, which significantly degrades performance for large payloads (e.g., >1MB). A simple check for JSON terminators (`}` or `]`) before parsing can provide a 50x+ speedup.
**Action:** Always check for terminators or use a delimiter-based protocol when receiving JSON over sockets.
