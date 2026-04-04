## 2026-04-04 - Quadratic overhead in chunked JSON parsing
**Learning:** Calling `json.loads()` on every received chunk of a large message leads to $O(N^2)$ performance degradation as the buffer grows. This is because each attempt involves decoding and parsing the entire accumulated buffer.
**Action:** Only attempt to parse JSON when the received chunk ends with a potential JSON terminator (`}` or `]`) after stripping whitespace. This reduces the number of parsing attempts significantly.

## 2026-04-04 - Connection reuse latency
**Learning:** Performing a round-trip "ping" command (like `get_polyhaven_status`) on every connection retrieval adds significant latency to every tool call.
**Action:** Use lightweight local socket checks (`sock.fileno() != -1`) and cache relatively static statuses like integration availability to minimize round-trips.
