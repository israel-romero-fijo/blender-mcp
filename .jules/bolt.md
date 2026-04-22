## 2026-04-22 - Communication Layer Optimization
**Learning:** Frequent small pings and redundant JSON parsing of large payloads create significant overhead in MCP-to-Blender communication. Using a local `fileno()` check instead of a network roundtrip for heartbeat, and implementing terminator-aware JSON parsing (checking for `}` or `]`), drastically improves performance.
**Action:** Always check for redundant network calls in connection-heavy loops and implement terminator-aware parsing for chunked socket data.

## 2026-04-22 - JSON Parsing Efficiency
**Learning:** In Python, `json.loads()` can accept bytes directly, and doing so is faster than decoding to a string first. Additionally, $O(N^2)$ parsing attempts during chunk accumulation can be avoided by only attempting to parse when the chunk ends with a potential JSON terminator.
**Action:** Favor `json.loads(bytes)` and use terminator heuristics for chunked reception.
