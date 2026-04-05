## 2025-05-14 - Redundant connection pings and quadratic JSON parsing
**Learning:** The MCP server was performing a full round-trip 'get_polyhaven_status' ping on every tool execution to verify connection health, adding unnecessary latency. Additionally, JSON response accumulation was re-parsing the entire buffer on every received chunk, leading to O(N^2) overhead for large responses.
**Action:** Implement lightweight socket health checks using `fileno()` and only attempt JSON parsing when the received chunk ends with a potential JSON terminator (`}` or `]`).
