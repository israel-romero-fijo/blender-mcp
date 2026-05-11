## 2026-05-11 - Trailing Whitespace in Terminator-Aware JSON Parsing
**Learning:** Strict terminator checks (e.g., `chunk.endswith(b'}')`) can cause deadlocks if the JSON payload is followed by whitespace or a newline (e.g., `\n`), as the check will fail and the receiver will block on the next `recv()`.
**Action:** Always use `rstrip()` before checking for JSON terminators in chunked reception loops to robustly handle common network protocol artifacts like trailing newlines.
