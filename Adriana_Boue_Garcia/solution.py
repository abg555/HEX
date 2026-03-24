from player import Player
from board import HexBoard
from collections import deque
import time

class SmartPlayer(Player):
   def moves(self, hex_board: HexBoard) -> list:
      moves = set()
      even_rows = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]
      odd_rows= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
      
      for row in range(hex_board.size):
        for col in range(hex_board.size):
            if hex_board.board[row][col] != 0:
                directions = even_rows if row % 2 == 0 else odd_rows
                for x, y in directions:
                    new_row, new_col = row + x, col + y
                    if 0 <= new_row < hex_board.size and 0 <= new_col < hex_board.size:
                        if hex_board.board[new_row][new_col] == 0:
                            moves.add((new_row, new_col))

      if not moves:
          return [(hex_board.size // 2, hex_board.size // 2)]
      return list(moves)
   
   def bridge_moves(self, board: HexBoard):
      bridges = set()
      bridge_patterns = [
        (1, 1, [(0,1),(1,0)]),
        (1,-1, [(0,-1),(1,0)]),
        (-1,1,[(0,1),(-1,0)]),
        (-1,-1,[(0,-1),(-1,0)])]
      for row in range(board.size):
         for col in range(board.size):
            if board.board[row][col] == self.player_id:
                for dx, dy, gaps in bridge_patterns:
                    nr, nc = row + dx, col + dy
                    if 0 <= nr < board.size and 0 <= nc < board.size:
                        if board.board[nr][nc] == self.player_id:
                            for x, y in gaps:
                                gr, gc = row + x, col + y
                                if 0 <= gr < board.size and 0 <= gc < board.size:
                                    if board.board[gr][gc] == 0:
                                        bridges.add((gr, gc))
      return list(bridges)
   
   def aux(self, hex_board: HexBoard, player_id: int) -> int:
      cola = deque()
      distance = {} 
      even_rows = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]
      odd_rows= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
      
      size = hex_board.size
      if player_id == 1:
         for i in range(size):
            if hex_board.board[i][0] == 1:
               cola.appendleft((i, 0)); distance[(i, 0)] = 0
            elif hex_board.board[i][0] == 0:
               cola.append((i, 0)); distance[(i, 0)] = 1
      else:
         for i in range(size):
            if hex_board.board[0][i] == 2:
               cola.appendleft((0, i)); distance[(0, i)] = 0
            elif hex_board.board[0][i] == 0:
               cola.append((0, i)); distance[(0, i)] = 1

      while cola:
         row, col = cola.popleft()
         if (player_id == 1 and col == size - 1) or (player_id == 2 and row == size - 1):
            return distance[(row, col)]
         
         directions = even_rows if row % 2 == 0 else odd_rows
         for i, j in directions:
            nr, nc = row + i, col + j
            if 0 <= nr < size and 0 <= nc < size:
               if hex_board.board[nr][nc] == (3 - player_id): continue
               
               cost = 0 if hex_board.board[nr][nc] == player_id else 1
               new_dist = distance[(row, col)] + cost
               if (nr, nc) not in distance or new_dist < distance[(nr, nc)]:
                  distance[(nr, nc)] = new_dist
                  if cost == 0: cola.appendleft((nr, nc))
                  else: cola.append((nr, nc))
      return 999            
   
   def evaluate(self, hex_board: HexBoard) -> int:
      rival = 3 - self.player_id
      if hex_board.check_connection(self.player_id): return 10000
      if hex_board.check_connection(rival): return -10000
         
      my_dist = self.aux(hex_board, self.player_id)
      rival_dist = self.aux(hex_board, rival)
      return (rival_dist * 2) - my_dist 
   
   def minimax(self, hex_board: HexBoard, depth: int, is_max: bool, alpha: float, beta: float) -> float:
      rival = 3 - self.player_id
      if depth == 0 or hex_board.check_connection(self.player_id) or hex_board.check_connection(rival):
         return self.evaluate(hex_board)
      
      mvs = self.moves(hex_board)[:12]
      if is_max:
         for m in mvs:
            nb = hex_board.clone(); nb.place_piece(m[0], m[1], self.player_id)
            alpha = max(alpha, self.minimax(nb, depth - 1, False, alpha, beta))
            if beta <= alpha: break
         return alpha
      else:
         for m in mvs:
            nb = hex_board.clone(); nb.place_piece(m[0], m[1], rival)
            beta = min(beta, self.minimax(nb, depth - 1, True, alpha, beta))
            if beta <= alpha: break
         return beta
      
   def play(self, board: HexBoard) -> tuple:
      if all(c == 0 for r in board.board for c in r):
         return (board.size // 2, board.size // 2)
      
      rival = 3 - self.player_id
      all_moves = self.moves(board)
      for m in all_moves:
          test_b = board.clone()
          test_b.place_piece(m[0], m[1], self.player_id)
          if test_b.check_connection(self.player_id): return m
      for m in all_moves:
          test_b = board.clone()
          test_b.place_piece(m[0], m[1], rival)
          if test_b.check_connection(rival): return m

      mvs = list(set(all_moves) | set(self.bridge_moves(board)))
      mvs.sort(key=lambda m: self.evaluate(board), reverse=True) 
      mvs = mvs[:15]

      best_score = float('-inf')
      best_move = mvs[0]

      for m in mvs:
         nb = board.clone()
         nb.place_piece(m[0], m[1], self.player_id)
         score = self.minimax(nb, 2, False, float('-inf'), float('inf'))
         if score > best_score:
            best_score = score
            best_move = m
       
      return best_move