## 2025-04-14 - Quadratic JSON Parsing in Chunked Reception
**Learning:** Calling `json.loads()` on every chunk received from a socket results in quadratic time complexity relative to the number of chunks, as each call re-parses all previous data. This is particularly impactful for large payloads (e.g., 2MB+) where it can take several seconds to receive and parse.
**Action:** Only attempt `json.loads()` if the last byte of the received chunk (after stripping whitespace) is a potential JSON terminator like `}` or `]`.

## 2025-04-14 - Redundant Connection Health Checks
**Learning:** Sending a full tool command (like `get_polyhaven_status`) just to check if a persistent socket connection is still alive adds unnecessary latency (~0.4ms per call) and depends on the application state.
**Action:** Use a lightweight `sock.fileno()` check or similar socket-level verification for basic persistence, and only perform state-heavy checks during initial connection or when explicitly requested.
