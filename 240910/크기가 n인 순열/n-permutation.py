n = int(input())
used = [False] * n
path = []
array = []
for i in range(1,n+1):
    array.append(i)

def backtracking():
    if len(path) == len(array):
        print(*path)

    for i in range(n):
        if used[i]:
            continue
        used[i] = True
        path.append(array[i])

        backtracking()

        used[i] = False
        path.pop()
    
backtracking()