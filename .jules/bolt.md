## 2026-05-06 - Verification of Memory vs. Codebase State
**Learning:** Memory entries may claim an optimization is present (e.g., terminator-aware parsing in both server and addon), but the actual codebase may still contain bottlenecks in one or more components. In this case, 'addon.py' was still using inefficient string concatenation and lacked the terminator check.
**Action:** Always use targeted 'sed' or 'read_file' to verify the exact implementation of hot paths before finalizing an optimization plan, regardless of what historical memory suggests.
