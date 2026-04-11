## 2025-05-15 - [Initial Setup]
**Learning:** Found quadratic JSON parsing overhead in both server and addon when receiving large payloads (e.g., textures, generated models).
**Action:** Implemented check for JSON terminators ('}' or ']') before calling `json.loads()` to avoid unnecessary parsing attempts on partial data.
