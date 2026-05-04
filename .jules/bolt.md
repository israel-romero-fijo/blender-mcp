## 2025-05-15 - Terminator-aware JSON parsing
**Learning:** 1MB/2MB JSON payloads over socket in this architecture exhibit $O(N^2)$ parsing overhead if every chunk triggers a full `json.loads` call; terminator-aware parsing (checking for `}` or `]`) reduces this to near-linear growth.
**Action:** Always check for JSON terminators before attempting to parse byte streams from sockets in performance-critical communication layers.

## 2025-05-15 - Efficient Byte Accumulation
**Learning:** Accumulating socket data via `buffer += data` is $O(N^2)$ due to repeated buffer copying. Using a list and `b''.join(chunks)` is $O(N)$.
**Action:** Use list-based chunk accumulation for large network payloads.
