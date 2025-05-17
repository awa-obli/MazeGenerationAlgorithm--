"""
迷宫生成算法*3: prim(最小生成树); dfs(深度优先搜索); recursion(递归)
作者: awa
"""

import random
from maze_path_find import maze_path_stack, maze_path_queue

# 查找四个方向的匿名函数列表
dirs = [
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y + 1),
    lambda x, y: (x + 1, y),
    lambda x, y: (x, y - 1)
]


def initialize_maze(size):
    # 迷宫初始化
    rows, cols = size
    maze = [[0 if i not in {0, rows - 1} and j not in {0, cols - 1} else 2 for j in range(cols)] for i in range(rows)]
    # 初始化水平墙
    for i in range(2, rows - 1, 2):
        for j in range(1, cols - 1, 1):
            maze[i][j] = 1
    # 初始化竖直墙
    for i in range(1, rows - 1, 1):
        for j in range(2, cols - 1, 2):
            maze[i][j] = 1
    
    return maze


def generate_maze_prim(size):
    rows, cols = size
    # 迷宫初始化
    maze = initialize_maze(size)

    candidate_seq = {}  # 候选序列
    start_node = (random.randrange(1, rows - 1, 2), random.randrange(1, cols - 1, 2))  # 随机起始点（应保证在格点而非墙壁上）
    visited = set()  # 用于记录已访问格点的集合
    visited.add(start_node)  # 记录起始点

    def determine_walls_to_add(node):  # 查找四个方向的墙壁是否应添加至候选序列，并添加
        for dir_ in dirs:
            next_node = dir_(node[0], node[1])  # 获取该方向边
            if maze[next_node[0]][next_node[1]] == 1:  # 判断该边是否为内部墙壁
                candidate_seq[next_node] = dir_  # 将所有邻边墙壁添加到候选序列

    determine_walls_to_add(start_node)  # 将起始点的所有邻边添加到候选序列

    while candidate_seq:  # 若候选序列有值
        random_wall = random.choice(list(candidate_seq.keys()))
        connect_node = candidate_seq[random_wall](random_wall[0], random_wall[1])  # 调用候选者对应的匿名函数，找到连接格点
        if connect_node not in visited:
            maze[random_wall[0]][random_wall[1]] = 0  # 打通墙壁
            visited.add(connect_node)  # 记录连接格点
            determine_walls_to_add(connect_node)
        else:
            candidate_seq.pop(random_wall)
    return maze


def generate_maze_dfs(size):
    # 迷宫初始化
    maze = initialize_maze(size)

    start_node = (random.randrange(1, len(maze) - 1, 2), random.randrange(1, len(maze) - 1, 2))  # 随机起始点（应保证在格点而非墙壁上）
    stack = [start_node]  # 栈
    visited = set()  # 用于记录已访问格点的集合
    visited.add(start_node)  # 记录初始格点

    while stack:
        cur_node = stack[-1]
        random.shuffle(dirs)  # 打乱
        for dir_ in dirs:
            random_wall = dir_(cur_node[0], cur_node[1])  # 获取随机的边（墙）
            connect_node = dir_(random_wall[0], random_wall[1])  # 获取连接的格点
            if maze[random_wall[0]][random_wall[1]] == 1 and connect_node not in visited:  # 如果是内部墙壁且连接格点未访问
                maze[random_wall[0]][random_wall[1]] = 0  # 打通墙壁
                stack.append(connect_node)  # 进入下一格点（即连接格点），入栈
                visited.add(connect_node)  # 记录该格点
                break
        else:
            stack.pop()  # 无路，出栈
    else:  # 若所有格点都走完了,结束
        return maze


def generate_maze_partition(size):
    # 初始化迷宫
    rows, cols = size
    maze_finish = [[0 if i not in {0, rows - 1} and j not in {0, cols - 1} else 2 for j in range(cols)] for i in range(rows)]

    def recursion_partition(maze, row_start, row_end, col_start, col_end):
        # 检查子空间大小(子空间行列范围界限均为奇数，所以空间不足即start==end时)
        if row_end == row_start or col_end == col_start:
            return

        # 确保分割位置在偶数坐标
        partition_row = random.randrange(row_start + 1, row_end, 2)
        partition_col = random.randrange(col_start + 1, col_end, 2)

        # 建造墙（行）
        for i in range(col_start, col_end + 1):
            maze[partition_row][i] = 1

        # 建造墙（列）
        for i in range(row_start, row_end + 1):
            maze[i][partition_col] = 1

        # 在三面墙上打通 [我是天才:) => 横纵坐标一定要是奇数！否则在下一次十字分割（横纵为偶）时可能会被堵！！！]
        # (注意：1.randrange函数前闭后开：后要加一2.十字中间不可取，partition_row/col要减/加一)
        walls_to_be_chose = [
            (partition_row, random.randrange(col_start, partition_col, 2)),  # 左侧墙壁
            (partition_row, random.randrange(partition_col + 1, col_end + 1, 2)),  # 右侧墙壁
            (random.randrange(row_start, partition_row, 2), partition_col),  # 上侧墙壁
            (random.randrange(partition_row + 1, row_end + 1, 2), partition_col)  # 下侧墙壁
        ]
        random.shuffle(walls_to_be_chose)  # 打乱
        for i in range(3):  # 打通三面墙
            wall_to_be_connected = walls_to_be_chose[i]
            maze[wall_to_be_connected[0]][wall_to_be_connected[1]] = 0

        # 递归对四个子空间分割（不包括十字墙壁）
        recursion_partition(maze, row_start, partition_row - 1, col_start, partition_col - 1)  # 左上
        recursion_partition(maze, row_start, partition_row - 1, partition_col + 1, col_end)  # 右上
        recursion_partition(maze, partition_row + 1, row_end, col_start, partition_col - 1)  # 左下
        recursion_partition(maze, partition_row + 1, row_end, partition_col + 1, col_end)  # 右下

    recursion_partition(maze_finish, 1, rows - 2, 1, cols - 2)
    return maze_finish


'''🎉完结撒花🎉'''


def main():
    while True:
        try:
            func = [generate_maze_prim, generate_maze_dfs, generate_maze_partition][int(input('生成算法(1~3:1:prim;2:dfs;3:partition)：')) - 1]
            maze_size = input('大小({(m,n)|m,n∈2*x+1,x∈N*},Enter→默认)：')
            if maze_size != '':
                size_row = int(maze_size.split(',')[0].split('(')[1])
                size_col = int(maze_size.split(',')[1].split(')')[0])
                maze_size = (size_row, size_col)  # 迷宫的大小（2 * n + 1）
            else:
                maze_size = (51, 51)  # 默认值

            maze_output = func(maze_size)
        except ValueError:
            print('请输入整数/正确的取值大小')
            continue
        except IndexError:
            print('请输入指定范围内的数字/正确的格式')
            continue
        except RecursionError:
            print('请缩小迷宫尺寸或切换生成算法')
            continue
        except Exception as e:
            print(f'*未知错误*: {e}')
            continue
        else:
            # 打印迷宫
            print(maze_output)
            for row in range(len(maze_output)):
                for col in range(len(maze_output[0])):
                    if maze_output[row][col] == 0:
                        print('□', end='')
                    else:
                        print('■', end='')
                print()
            
            # 搜索路径
            end_point = (maze_size[0] - 2, maze_size[1] - 2)
            print(maze_path_stack(maze_output, (1, 1), end_point))

            # 重新生成
            whether_again = input('again?（Y:"Y"/"y";N:Enter→）')
            if whether_again == 'Y' or whether_again == 'y':
                continue
            else:
                break


if __name__ == '__main__':
    main()
