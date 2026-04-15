import timeit

d = {f"key_{i}": i for i in range(100)}
keys_to_check = [f"key_{i}" for i in range(110, 120)] # none present

def use_any():
    return any(k in d for k in keys_to_check)

def use_isdisjoint():
    return not d.keys().isdisjoint(keys_to_check)

# One present at the end
keys_to_check_present = [f"key_{i}" for i in range(95, 105)]

def use_any_present():
    return any(k in d for k in keys_to_check_present)

def use_isdisjoint_present():
    return not d.keys().isdisjoint(keys_to_check_present)

print("Not present:")
print(f"any: {timeit.timeit(use_any, number=1000000):.4f}s")
print(f"isdisjoint: {timeit.timeit(use_isdisjoint, number=1000000):.4f}s")

print("\nPresent at end:")
print(f"any: {timeit.timeit(use_any_present, number=1000000):.4f}s")
print(f"isdisjoint: {timeit.timeit(use_isdisjoint_present, number=1000000):.4f}s")
