## 2025-04-12 - [Communication] Quadratic JSON Parsing Overhead
**Learning:** Repeatedly calling `json.loads()` on an accumulating buffer during socket receipt leads to O(N^2) complexity relative to the number of chunks. This significantly degrades performance for large payloads (e.g., 5MB+ scene data).
**Action:** Always use a heuristic check (like `endswith((b'}', b']'))`) before attempting to parse incomplete chunks, and accumulate chunks in a list to avoid quadratic string concatenation overhead.

## 2025-04-12 - [Connectivity] Redundant Connection Heartbeats
**Learning:** Performing a full round-trip "ping" (e.g., `send_command("status")`) in a `get_connection()` utility doubles the latency of every subsequent tool call. For high-frequency tool calls, this is a major bottleneck.
**Action:** Use lightweight local checks like `socket.fileno() != -1` to verify connection health, and only perform round-trip pings on initial connection or after a suspected failure.
