import heapq
import sys

INF = float('inf')
MAX_N =2000
MAX_ID = 30000

input = sys.stdin.readline

N, M = 0,0
A= [] #邻接矩阵
D= [] # 最短路径收藏
isMade = [] 
isCancel = []
S = 0 #出发地

#旅行商品定义 id 收入 目的地 利润(거리)
class Package:
    def __init__(self, id, revenue, dest, profit):
        self.id = id 
        self.revenue = revenue
        self.dest = dest
        self.profit = profit

    #优先序列，基于利润排序，利润相同则按照id排序
    def __lt__(self,other):
        if self.profit == other.profit:
            return self.id < other.id
        return self.profit > other.profit
    

pq = [] # 优先序列初始化，用来存储package对象

#dijkstra算法 最短路径
#从起始城市S 到所有其他城市的最短路径

def dijkstra():
    global D
    #初始化了一个距离数组D
    D = [INF] * N
    # visit 数组用于标记某个城市的最短路径是否已经找到
    visit = [False] * N
    #起始城市到自己的距离为0
    D[S] = 0
    
    #寻找未访问的最小距离城市， 从未访问的城市中找到一个到起始城市距离最小的城市
    for _ in range(N):
        # v是最小距离城市的索引id
        v = -1
        #minDist 最小距离
        minDist = INF
        for j in range(N):
            if not visit[j] and minDist > D[j]:
                v = j
                minDist = D[j]
        if v == -1:
            break
        #更新临近城市的距离
        #一旦找到了最小距离的城市v，就将其标记为已访问
        visit[v] = True
        #遍历所有城市，如果j是v的邻居(两者之间有直线连接且距离不是无限大)
        #并且从S到j的当前记录距离 大于 从S 到v再到j的距离，就更新D[j]
        for j in range(N):
            if A[v][j] != INF and D[j] > D[v] + A[v][j]:
                D[j] = D[v] + A[v][j]


#根据输入构建城市间的距离矩阵A
def buildLand(n,m,arr):
    #n是城市的数量，m是给定边的数量，arr是包含所有边的数据的数组
    global A, N, M
    N,M = n,m
    A = [[INF]*N for _ in range(N)]

    for i in range(N):
        #每个城市到自己的距离设为0
        A[i][i] = 0
    #对于每条边
    for i in range(M):
        #(城市u 到城市v 的权重是w)
        #每条边由三部分组成，起始城市u，到达城市v，和距离权重w
        #当i = 0时，代码从数组arr的第0，1，2个位置获取第一条边的信息
        #当i = 1时，第3，4，5 位置获取......
        #因为输入数据通常以这种连续的方式提供边的信息。
        #如果你有一组边的信息，将它们平铺在一个单一的列表中，每三个元素组成一组可以很方便地表示一条边。
        #这是处理图数据的一种常见方式，特别是在解决涉及城市和道路的问题时。
        u,v,w = arr[i*3], arr[i*3+1], arr[i*3 +2]
        #由于可能有多条边连接同两个城市，所以每次存储两个城市的最小距离
        A[u][v] = min(A[u][v], w)
        A[v][u] = min(A[v][u], w)

#添加新的旅行产品
def addPackage(id, revenue, dest):
    isMade[id] = True
    #利润 = 收入-最短路径成本
    profit = revenue - D[dest]
    #将此产品以Package类的实例形式加入到优先队列pq中
    #heapq: 确保列表的第一个元素始终是堆中的最小元素(当使用最小堆时)
    #适用于需要频繁访问和移除最小元素，如优先队列中
    heapq.heappush(pq, Package(id, revenue, dest, profit))

#取消旅行产品
def cancelPackage(id):
    if isMade[id]:
        isCancel[id] = True

#从优先队列中选择并销售最优旅行产品
def sellPackage():
    while pq: #确保只要是队列中有元素，就继续执行
        #查看堆顶元素，检查顶部元素是否符合销售条件
        p = pq[0] 
        # 如果堆顶元素利润<0, 则中断循环，函数返回-1， 队列顶部产品已不适合销售
        if p.profit < 0:
            break
        # 如果顶部产品利润不为负，移除堆顶元素
        heapq.heappop(pq)
        #如果产品未被取消，返回产品id，表示成功销售
        #如果产品已被取消，则继续循环，查看下一个产品
        if not isCancel[p.id]:
            return p.id
    return -1

#更改起始城市 S 并重新计算所有已存在的旅行产品的最短路径和利润。
def changeStart(param):
    global S
    #更新全局变量 S, 表示旅行产品的起始城市
    S = param
    #重新计算最短路径
    dijkstra()
    #临时存储现有产品
    temp_packages = []
    # 循环移除并存储当前优先队列中的所有产品
    #这样做是为了清空队列，并允许根据新的最短路径数据重新计算利润。
    while pq:
        #从优先队列中弹出产品并添加到临时列表中。
        temp_packages.append(heapq.heappop(pq))
    # 遍历临时存储的产品列表
    for p in temp_packages:
        #对于每个产品，
        #根据其ID、收入和目的地重新计算利润，
        #并将其重新添加到优先队列中。
        addPackage(p.id, p.revenue,p.dest)

#根据提供的命令执行相应的操作
def main():
    global isCancel,isMade
    #读取第一行输入，表示接下来要处理的查询数量
    Q = int(input())
    #分别初始化跟踪旅行产品是否已经被创建和是否已经被取消的状态数组。
    isMade = [False] * MAX_ID
    isCancel = [False] * MAX_ID

    #处理查询
    for _ in range(Q):
        #读取每个查询的数据，分割并转换为整数列表
        query = list(map(int,input().split()))
        #提取查询的类型
        T = query[0]
        #对于类型为100的查询，
        #调用 buildLand 函数来构建城市间的地图
        #并执行 dijkstra 函数计算最短路径
        if T == 100:
            buildLand(query[1],query[2],query[3:])
            dijkstra()
        #对于类型为200的查询，调用 addPackage 函数来添加一个新的旅行产品
        elif T == 200:
            id, revenue, dest = query[1],query[2],query[3]
            addPackage(id, revenue,dest)
        #对于类型为300的查询，调用 cancelPackage 函数来取消一个旅行产品
        elif T == 300:
            id = query[1]
            cancelPackage(id)
        # 对于类型为400的查询，调用 sellPackage 函数
        #打印返回的产品ID（如果有产品成功销售）
        elif T == 400:
            print(sellPackage())
        #对于类型为500的查询，调用 changeStart 函数来更改起始城市
        elif T == 500:
            changeStart(query[1])

if __name__=="__main__":
    main()