#!/usr/bin/env python3

if __name__ == '__main__':
    import json
    from random import randint
    n = 10000
    out = [randint(0, n) for _ in range(0, n)]
    print(json.dumps(out))
