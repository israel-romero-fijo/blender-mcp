
## 2025-05-14 - Optimized Socket JSON Receiving with Terminator Checks
**Learning:** Checking for a JSON terminator (`} ` or `] `) before attempting `json.loads()` on an accumulating buffer provides massive performance gains (up to 200x for 1MB payloads) by avoiding O(N²) parsing attempts on incomplete chunks. List-based chunk accumulation further avoids expensive string concatenations.
**Action:** Always implement terminator-aware parsing and list-based accumulation for socket-based JSON protocols handling variable-sized or large payloads.
