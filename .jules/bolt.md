## 2025-05-14 - [JSON Parsing Optimization]
**Learning:** Communication between the MCP server and Blender addon over sockets can involve large JSON payloads. By attempting to parse every chunk, the original code exhibited quadratic overhead. Implementing a terminator-aware check (`rstrip().endswith((b'}', b']'))`) reduces parsing attempts to typically one per payload.
**Action:** Always use terminator-aware parsing when receiving JSON over streaming sockets to maintain linear performance as payload size grows.

## 2025-05-14 - [Rejected: Local Socket Health Check]
**Learning:** Attempted to replace a network ping with `sock.fileno() != -1` to verify connection health. This was rejected because it failed to detect remote peer disconnection and broke synchronization of the global `_polyhaven_enabled` state.
**Action:** Keep the network ping for critical health checks where state synchronization or remote peer detection is required, despite the ~0.1ms latency.
