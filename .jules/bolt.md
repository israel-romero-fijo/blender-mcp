## 2026-04-07 - Optimized JSON parsing and connection polling
**Learning:** Checking for JSON terminators (`}` or `]`) at the end of a byte buffer before attempting `json.loads()` avoids quadratic overhead in multi-chunk socket communication. Additionally, caching status values like `_polyhaven_enabled` and using `socket.fileno()` for health checks significantly reduces redundant network round-trips.
**Action:** Always implement lightweight terminator checks for streaming JSON data and cache expensive status queries in persistent connections.
