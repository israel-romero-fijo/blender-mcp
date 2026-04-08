## 2025-05-15 - Redundant Network Pings in Tool Connections
**Learning:** Performing a live "ping" command to verify a persistent socket connection before every tool invocation adds significant latency (doubling the round-trips). A local `fileno()` check is much faster and sufficient for most cases, as the subsequent send/receive will handle the actual connection failure if the peer has died.
**Action:** Use lightweight local state checks for persistent connections; only perform full network-based verification during initial connection or explicit reconnection logic.

## 2025-05-15 - Quadratic Overhead in Multi-chunk JSON Parsing
**Learning:** Attempting to `json.loads()` on every data chunk received from a socket is inefficient because it triggers expensive exception handling for every incomplete chunk.
**Action:** Use a heuristic check (e.g., checking for JSON terminators like `}` or `]`) before attempting to parse. Also, parse bytes directly to avoid extra string decoding/allocation.
