## 2026-05-16 - Terminator-aware JSON parsing in socket receiver loops
**Learning:** Attempting to parse JSON from every network chunk in a socket receiver loop introduces O(N²) overhead as the payload grows. Using a simple terminator check (`chunk.rstrip().endswith((b'}', b']'))`) avoids redundant `json.loads` calls and significantly improves performance for large payloads.
**Action:** Always implement terminator-aware parsing in socket receiver loops handling JSON, and combine with list-based chunk accumulation to avoid quadratic string concatenation.
