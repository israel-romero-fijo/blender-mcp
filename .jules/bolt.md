## 2026-04-16 - [Communication Layer Optimization]
**Learning:** Naive chunked reception that calls `json.loads()` on every chunk causes quadratic parsing overhead, especially painful for large scene data (e.g., 2MB+). Additionally, a network "ping" to verify connection health adds ~1ms of unnecessary latency to every tool call.
**Action:** Always use terminator-aware chunk accumulation (check for `}` or `]` before parsing) and prefer lightweight `fileno()` checks or lazy error handling over proactive network pings for connection health.
