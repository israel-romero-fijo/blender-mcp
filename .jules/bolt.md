## 2025-05-15 - [JSON Parsing Optimization]
**Learning:** Checking for JSON terminators (`}` or `]`) at the end of a byte buffer before calling `json.loads` avoids $O(N^2)$ overhead when receiving large payloads in many small chunks.
**Action:** Always implement a trailing byte check for potential JSON completion in socket-based or stream-based JSON protocols.

## 2025-05-15 - [Connection Verification Latency]
**Learning:** Performing a network round-trip to verify connection health on every tool call significantly increases latency. A lightweight `socket.fileno()` check is sufficient for active connections, provided the sending logic handles dead-socket errors by invalidating the cache.
**Action:** Use local socket state checks for performance-critical connection management and rely on exception handling in the send/receive loop to trigger re-connection.
