n = int(input())
used = [False] * (n+1)
path = []

def backtracking():
    if len(path) == n:
        print(*path)

    for i in range(1, n+1):
        if used[i]:
            continue
        used[i] = True
        path.append(i)

        backtracking()

        used[i] = False
        path.pop()
    
backtracking()