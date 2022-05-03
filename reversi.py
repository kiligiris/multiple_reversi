
DIR = [ # [y, x]
    [-1, 0], # upper
    [-1, 1], # upper_right
    [ 0, 1], # right
    [ 1, 1], # lower_right
    [ 1, 0], # lower
    [ 1,-1], # lower_left
    [ 0,-1], # left
    [-1,-1], # upper_left
]
EMPTY = 0

class reversi():
    def __init__(self, num=18):
        self.turns = 0
        self.current_num = 1
        self.is_end = False
        # プレイ人数を設定
        if num <= 2:
            self.num = 2
        elif num <= 8:
            self.num = 8
        else:
            self.num = 18
        self.size = int((self.num / 2) ** 0.5) * 8
        # boardの初期化
        self.board = [[0 for i in range(self.size)] for _ in range(self.size)]
        pnum = 1
        for i in range(3, self.size, 8):
            for j in range(3, self.size, 8):
                self.board[i][j] = pnum
                self.board[i+1][j+1] = pnum
                pnum += 1
                self.board[i+1][j] = pnum
                self.board[i][j+1] = pnum
                pnum += 1
        
        # 各プレイヤーが打てるか
        self.can_put = [True] * self.num
        
        self.maxturn = self.size * self.size - self.num * 2
        # 打てる座標リストの初期化
        self.init_cml()
    
    
    def move(self, y, x):
        if not (y, x) in self.cml:
            return False
        dirs = self.cmil[self.cml.index((y, x))]
        self.reverse(y, x, dirs)
        self.turns += 1
        self.current_num = self.current_num % self.num + 1
        
        self.init_cml()
        
        # 置けるところがない && ゲームオーバーでない間スキップする
        while not self.cml and not self.isgameover():
            self.can_put[self.current_num - 1] = False
            self.skip()

        if self.cml:
            self.can_put[self.current_num - 1] = True
        
        return True
    
    def reverse(self, y, x, dirs):
        self.board[y][x] = self.current_num
        for dir, cnt in dirs:
            inc = DIR[dir]
            yt = y + inc[0]
            xt = x + inc[1]
            for _ in range(cnt):
                self.board[yt][xt] = self.current_num
                yt += inc[0]
                xt += inc[1]
    
    # 石のおける場所とひっくり返る方向、枚数を更新
    def init_cml(self):
        cml = []
        cmil = []
        for i in range(self.size):
            for j in range(self.size):
                cm = self.can_move(i, j)
                if cm:
                    cml.append((i, j))
                    cmil.append(cm)
        self.cml = tuple(cml)
        self.cmil = tuple(cmil)
                
    # return ((DIR_num, cnt),・・・)
    def can_move(self, y, x):
        movable = []
        board = self.board
        num = self.current_num
        if board[y][x] != EMPTY:
            return ()
        for d in range(len(DIR)):
            yt = y + DIR[d][0]
            xt = x + DIR[d][1]
            if not self.within(yt, xt):
                continue
            if board[yt][xt] == EMPTY or board[yt][xt] == num:
                continue
            cnt = 1
            yt += DIR[d][0]
            xt += DIR[d][1]
            while self.within(yt, xt) and board[yt][xt] != EMPTY:
                if board[yt][xt] == num:
                    movable.append((d, cnt))
                    break
                cnt += 1
                yt += DIR[d][0]
                xt += DIR[d][1]
        return tuple(movable)
    # 範囲内か
    def within(self, y, x):
        return 0 <= y < self.size and 0 <= x < self.size
    
    # 置けない場合のスキップ処理
    def skip(self):
        if self.cml or self.is_end:
            return False
        
        self.current_num = self.current_num % self.num + 1
        self.init_cml()
        return True
    
    def isgameover(self):
        if self.is_end:
            return True
        if self.turns >= self.maxturn:
            self.is_end = True
            return True
        if not any(self.can_put):
            self.is_end = True
            return True
        return False
    
    # 各プレイヤーの駒が存在する数を返す
    def count_num(self):
        res = [0] * self.num
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    res[self.board[i][j] - 1] += 1
        return res
    
    def victory(self):
        ma = 0
        idxs = []
        cnts = self.count_num()
        for i, cnt in enumerate(cnts):
            if cnt > ma:
                idxs = [i]
                ma = cnt
            elif cnt == ma:
                idxs.append(i)
        return idxs
    
    
if __name__ == "__main__":
    
    def print_b(board):
        for bd in board:
            st = ""
            for b in bd:
                b = str(b)
                if len(b) == 1:
                    st += "  " + b
                else:
                    st += " " + b
            print(st)
        print("-" * 10)
        
    
    r = reversi(16)
    while not r.is_end: 
        print(f"{r.turns}ターン目")
        print(f"{r.current_num}のターン")
        print(r.count_num())
        print_b(r.board)
        print(r.cml)
        print("スペース区切りで「2 4」のように入力してください")
        y, x = map(int, input().split())
        #y, x = r.cml[0]
        f = r.move(y, x)
        if not f:
            print("そこにはおけません")
    print(r.maxturn)
    print(r.turns)
    print(r.count_num())
    print_b(r.board)
    v = r.victory()
    txt = "勝者は、" + str(v.pop(0) + 1)
    while v:
        txt += "番と、" + str(v.pop(0) + 1)
    txt += "番です。"
    print(txt)