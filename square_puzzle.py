#コード変更完了
from heapq import heappush, heappop
from random import shuffle
import time

class sBoard():
    def __init__(self, board_list, distance, parent):
        self._array = board_list
        self.heuristic = calc_heuristic(self._array)
        self.distance = distance
        self.cost = self.distance + self.heuristic
        self.parent = parent
        self.hashvalue = hash(tuple(self._array))

    def _getsBoard(self):
        return self._array

    def __hash__(self):
        return self.hashvalue

    def __eq__(self,other):
        return self._array == other._array

    def __lt__(self, other):
        return self._array < other._array

def astar():
    queue = []
    dist_dic = {}       # 初期盤面からの手数
    visited = {}        # 訪問済みnode；過去の盤面

    #スタートとゴールの作成
    start = sBoard(init_board, 0, None)
    end = sBoard(goal_board, 10000, None)

    # openリストの初期値を追加
    heappush(queue, (start.cost, start))
    No = 0                                              # debug
    # ゴールに到達するまで新しい盤面を探索する
    while len(queue) > 0:
        No += 1                                         # debug
        # open-listからコスト最小の探索済みnode（盤面）を取り出す
        now_tuple = heappop(queue)
        now_board = now_tuple[1]
        if now_board._array == goal_board or now_board._array == goal_board2:

            # ゴールを発見
            end = now_board
            break

        # ピースのない位置へ入ることのできる隣接座標
        index = now_board._array.index(0)
        x, y = XY_coord(index)
        coord_next_OK = coord_next(x, y)

        # 次のnodeを探索；ピースのない位置へスライドを試行
        for coord in coord_next_OK:
            next_board = now_board._array[:]
            next_index = coord[0] * board_size + coord[1]
            next_board[index],next_board[next_index] = next_board[next_index],next_board[index]

            new_sboard = sBoard(next_board, now_board.distance+1, now_board)
            new_distance = new_sboard.cost

            if tuple(new_sboard._array) not in visited or \
                    new_distance < dist_dic[new_sboard]:
                dist_dic[new_sboard] = new_distance

                visited[tuple(new_sboard._array)] = new_sboard
                new_sboard.parent = now_board
                heappush(queue, (new_sboard.cost, new_sboard))
    var = end
    sol = []
    while var != start:
        sol = sol + [var._getsBoard()]
        var = var.parent
    sol = sol + [var._getsBoard()]

    #スタートからゴールへ向かうように調整
    sol.reverse()
    return sol, No

def calc_heuristic(array):
    #ゴールまでのコスト推定値を求める
    board_list = array
    same = board_size * board_size
    manhattan_distance = 0

    for var in board_list:
        #正解配置と一致しないマスの数
        x, y = XY_coord(var)
        if goal_board.index(var) != board_list.index(var):
            same -= 1
        
        #マンハッタン距離
        pos = goal_board.index(var)
        goal_board_x, goal_board_y = XY_coord(pos)
        x, y = XY_coord(board_list.index(var))
        manhattan_distance += abs(x-goal_board_x) + abs(y-goal_board_y)
        
    if heuristic_type == 0:
        heuristic = 0
    elif heuristic_type == 1:
        heuristic = same
    elif heuristic_type == 2:
        heuristic = manhattan_distance
    
    return mul_heuristic * heuristic

def coord_next(x, y):
    #ピースのない位置へスライドできる隣接マスのXY座標のリストを返す
    coord_next_OK = [[x, y]]
    # right
    if(x+1 < board_size):
        coord_next_OK.append([x+1, y])
    # left
    if(x-1 >= 0):
        coord_next_OK.append([x-1, y])
    # down
    if(y-1 >= 0):
        coord_next_OK.append([x, y-1])
    # up
    if(y+1 < board_size):
        coord_next_OK.append([x, y+1])

    return coord_next_OK


def XY_coord(index):
    #盤面配列からx,y座標を返す(商と余り)
    x = index // board_size
    y = index % board_size
    return x, y

def draw_board(board):
    #盤面を各行に分割
    string_board = ""
    for i in range(board_size):
        for j in range(board_size):
            string_board += "{:^3s}".format(str(board[board_size * i + j]))
        string_board += "\n"
    
    print(string_board, end="")
    return

def draw_process(sol):
    separator = ""
    for i in range(len(sol)):
        draw_board(sol[i])
        if i != len(sol) - 1:
            print("{:^9s}".format("↓"))
        else:
            print("\n fin.")
    return

def main():
    global heuristic_type, board_size, init_board, goal_board, goal_board2, mul_heuristic

    mul_heuristic = 1
    heuristic_type = 2
    board_size = 3

    #盤面の大きさに応じた初期盤面の設定(今回は、8パズル,15パズルのみ対応)
    if board_size == 3:
        init_board  = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        goal_board  = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        goal_board2 = [1, 2, 3, 4, 5, 6, 8, 7, 0]
    elif board_size == 4:
        init_board  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        goal_board  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        goal_board2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0]
    else:
        raise ValueError("board_size must be 3 or 4.")
    
    shuffle(init_board)

    sol, visit = astar()
    return sol, visit


if __name__ == '__main__':
    start = time.time()
    
    sol, visit = main()
    print("[init_board]")
    draw_board(init_board)
    print("\n")
    print("heuristic_type:    h{}".format(heuristic_type))
    print("solving_length:    {}".format(len(sol)))
    print("visiting_nodes:    {}".format(visit))
   
    process_time = time.time() - start
    print("executing_time:    {} sec".format(round(process_time, 3)))
    print("-------------")
    print("[process]")
    draw_process(sol)