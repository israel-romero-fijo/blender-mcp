## 2025-05-15 - Terminator-aware JSON parsing optimization
**Learning:** For large JSON payloads received over sockets in chunks, calling `json.loads` on every chunk results in $O(N^2)$ overhead.
**Action:** Always check if a chunk ends with a JSON terminator (`}` or `]`) before attempting to parse. This reduces processing time for 1MB payloads from ~1.03s to ~0.005s (a ~200x speedup).

## 2025-05-15 - Connection ping overhead
**Learning:** Performing a "ping" command roundtrip to verify connection health on every tool call significantly adds to latency (especially if the ping involves an external API check).
**Action:** Use local socket health checks and only perform state-refreshing pings when necessary.

## 2025-05-15 - Closure capture in timer callbacks
**Learning:** Capturing loop variables in nested functions (like `execute_wrapper`) in `addon.py` can lead to race conditions where the variable changes before the callback executes.
**Action:** Use default arguments (e.g., `def func(val=val):`) to capture the value at definition time.
