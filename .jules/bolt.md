## 2025-05-22 - Socket Communication Optimization
**Learning:** Quadratic buffer growth (`buffer += data`) and redundant JSON parsing of incomplete chunks are significant bottlenecks in Python socket servers.
**Action:** Always use a list to accumulate chunks (`chunks.append(data)`) and `b''.join(chunks)` for final assembly. Additionally, use a terminator check (like `data.rstrip()[-1:] in (b'}', b']')`) to avoid calling `json.loads` on every partial chunk.
