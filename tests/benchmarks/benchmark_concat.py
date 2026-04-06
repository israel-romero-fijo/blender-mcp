import time

def slow_concat(n):
    s = ""
    start = time.time()
    for i in range(n):
        s += "a"
    return time.time() - start

def fast_concat(n):
    l = []
    start = time.time()
    for i in range(n):
        l.append("a")
    s = "".join(l)
    return time.time() - start

def main():
    n = 1000000
    t1 = slow_concat(n)
    t2 = fast_concat(n)
    print(f"Slow concat (+=): {t1:.4f}s")
    print(f"Fast concat (join): {t2:.4f}s")
    print(f"Improvement: {(t1-t2)/t1*100:.2f}%")

if __name__ == "__main__":
    main()
