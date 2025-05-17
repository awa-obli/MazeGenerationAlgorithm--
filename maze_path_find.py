"""迷宫寻路算法"""
from collections import deque

maze_ = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

dirs = [
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y + 1),
    lambda x, y: (x + 1, y),
    lambda x, y: (x, y - 1)
]


def maze_path_stack(maze, start, finish):  # 深度优先搜索
    stack = [(start[0], start[1])]
    maze[start[0]][start[1]] = 3
    while len(stack) > 0:
        cur_node = stack[-1]
        if cur_node == (finish[0], finish[1]):
            n = 0  # 打印路径
            for p in stack:
                n += 1
                print(n, '.', p, sep='', end=',')
            return True
        for dir_ in dirs:
            next_node = dir_(cur_node[0], cur_node[1])
            if maze[next_node[0]][next_node[1]] == 0:
                stack.append(next_node)
                maze[next_node[0]][next_node[1]] = 3  # 3为路径标记
                break
        else:
            stack.pop()
    else:
        return False


def maze_path_stack_2(maze, start, finish):  # 不会更改迷宫内容的版本
    stack = [(start[0], start[1])]
    visited = set()
    visited.add((start[0], start[1]))
    while len(stack) > 0:
        cur_node = stack[-1]
        if cur_node == (finish[0], finish[1]):
            n = 0  # 打印路径
            for p in stack:
                n += 1
                print(n, '.', p, sep='', end=',')
            return True
        for dir_ in dirs:
            next_node = dir_(cur_node[0], cur_node[1])
            if maze[next_node[0]][next_node[1]] == 0:
                if next_node not in visited:
                    stack.append(next_node)
                    visited.add(next_node)
                    break
        else:
            remove_path = stack.pop()
    else:
        return False


def maze_path_queue(maze, start, finish):  # 广度优先搜索
    queue = deque()
    queue.append((start[0], start[1], -1))  # 队列（第三个元素表示‘是哪个位置的格点让它来的，以便打印路径’）
    path = []
    maze[start[0]][start[1]] = 3
    while len(queue) > 0:
        cur_node = queue.popleft()
        path.append(cur_node)
        if cur_node[0] == finish[0] and cur_node[1] == finish[1]:
            print_path(path)
            return True
        for dir_ in dirs:
            next_node = dir_(cur_node[0], cur_node[1])
            if maze[next_node[0]][next_node[1]] == 0:
                queue.append((next_node[0], next_node[1], len(path) - 1))
                maze[next_node[0]][next_node[1]] = 3  # 3为路径标记
    else:
        return False


def print_path(path):  # 倒推打印路径
    cur_node = path[-1]
    real_path = []
    while cur_node[2] != -1:
        real_path.append(cur_node[:2])
        cur_node = path[cur_node[2]]  # 倒推上一格点
    real_path.append(cur_node[:2])
    real_path.reverse()

    n = 0  # 反向正序打印
    for p in real_path:
        n += 1
        print(n, '.', p, sep='', end=',')



if __name__ == '__main__':
    print(f'\n{maze_path_stack(maze_, (1, 1), (8, 8))}')
    for i in maze_:
        print(i)

