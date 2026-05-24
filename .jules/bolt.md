## 2025-05-14 - Quadratic JSON Parsing Overhead in Socket Receivers
**Learning:** In socket-based communication, attempting to `json.loads()` every received chunk leads to O(N^2) overhead, as each chunk causes the entire accumulated buffer to be re-parsed. For large payloads (e.g., 1MB+), this can slow down communication from milliseconds to seconds.
**Action:** Always implement terminator-aware JSON parsing. Only attempt `json.loads()` if the latest chunk (after `rstrip()`) ends with a valid JSON terminator like `}` or `]`.

## 2025-05-14 - Closure Integrity in Asynchronous Timers
**Learning:** When registering a callback in an event loop or timer (like `bpy.app.timers.register`), using a variable from an outer scope that changes (like a loop variable) can lead to race conditions or incorrect state being processed.
**Action:** Use default arguments in the callback definition (e.g., `def callback(cmd=command):`) to capture the current state of the variable at definition time.
