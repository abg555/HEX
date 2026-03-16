from player import Player
from board import HexBoard
from collections import deque

class SmartPlayer(Player):
   def moves(self, hex_board: HexBoard) -> list:
      moves = set()
      even_rows = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]
      odd_rows= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
      for row in range(hex_board.size):
        for col in range(hex_board.size):
            if hex_board.board[row][col] != 0:
                if row % 2 == 0:
                    directions = even_rows
                else:
                    directions = odd_rows
                for x, y in directions:
                    new_row = row + x
                    new_col = col + y
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
            if board.board[row][col] != self.player_id:
                continue
            for dx,dy,gaps in bridge_patterns:
                new_row = row + dx
                new_col = col + dy
                if 0 <= new_row < board.size and 0 <= new_col < board.size:
                    if board.board[new_row][new_col] == self.player_id:
                        for x,y in gaps:
                            gr = row + x
                            gc = col + y
                            if 0 <= gr < board.size and 0 <= gc < board.size:
                                if board.board[gr][gc] == 0:
                                    bridges.add((gr,gc))
      return list(bridges)
   
   def aux(self, hex_board: HexBoard, player_id: int) -> int:
      cola = deque()
      distance = {} 
      even_rows = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]
      odd_rows= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
      if player_id == 1:
         for i in range(hex_board.size):
            if hex_board.board[i][0] == 1:
               cola.appendleft((i, 0))
               distance[(i, 0)] = 0
            elif hex_board.board[i][0] == 0:
               cola.append((i, 0))
               distance[(i,0)] = 1

      else:
         for i in range(hex_board.size):
            if hex_board.board[0][i] == 2:
               cola.appendleft((0, i))
               distance[(0, i)] = 0
            elif hex_board.board[0][i] == 0:
               cola.append((0, i))
               distance[(0, i)] = 1

      while cola:
         row,col = cola.popleft()

         if player_id == 1 and col == hex_board.size - 1:
            return distance[(row, col)]
         if player_id == 2 and row == hex_board.size - 1:
            return distance[(row, col)]
         
         if row % 2 == 0:
            position = even_rows
         else:
            position = odd_rows

         for (i,j) in position:
            new_row = row + i
            new_col = col + j

            if new_row >= 0 and new_col >= 0 and new_row < hex_board.size and new_col < hex_board.size:
               if hex_board.board[new_row][new_col] == (3 - player_id):
                  continue
               
               if hex_board.board[new_row][new_col] == 0:
                  new_distance = distance[(row, col)] + 1

                  if (new_row,new_col) not in distance or new_distance < distance[(new_row, new_col)]:
                     cola.append((new_row, new_col))
                     distance[(new_row, new_col)] = new_distance

               elif hex_board.board[new_row][new_col] == player_id:
                  new_distance = distance[(row, col)]

                  if (new_row,new_col) not in distance or new_distance < distance[(new_row, new_col)]:
                     cola.appendleft((new_row, new_col))
                     distance[(new_row, new_col)] = new_distance
      return 999            
   
   def evaluate(self, hex_board: HexBoard) -> int:
      rival = 3 - self.player_id
      if hex_board.check_connection(self.player_id):
         return 10000
      elif hex_board.check_connection(rival):
          return -10000
         
      my_distance = self.aux(hex_board, self.player_id)
      rival_distance = self.aux(hex_board, rival)
      return rival_distance - my_distance
   
   def evaluate_move(self, board, move):
      new_board = board.clone()
      new_board.place_piece(move[0], move[1], self.player_id)
      return self.evaluate(new_board)
   
   def minimax(self, hex_board: HexBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
      rival = 3 - self.player_id
     
      if hex_board.check_connection(self.player_id) or hex_board.check_connection(rival) or depth == 0:
         return self.evaluate(hex_board)
      

      moves = self.moves(hex_board)[:20]
      if is_maximizing:
         for move in moves:
            new_board = hex_board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)
            score = self.minimax(new_board, depth - 1, False, alpha, beta)
            alpha = max(alpha, score)
            if beta <= alpha:
               break
         return alpha

      else:
         for move in moves:
            new_board = hex_board.clone()
            new_board.place_piece(move[0], move[1], rival)
            score = self.minimax(new_board, depth - 1, True, alpha, beta)
            beta = min(beta, score)
            if beta <= alpha:
               break
         return beta
      
   def play(self, board: HexBoard) -> tuple:
      if all(cell == 0 for row in board.board for cell in row):
         center = board.size // 2
         return (center, center)
      
      best_score = float('-inf')
      best_move = None

      moves = set(self.moves(board))
      bridge_moves = self.bridge_moves(board)
      moves.update(bridge_moves)
      moves = list(moves)
      moves.sort(key=lambda m: self.evaluate_move(board,m), reverse= True)
      moves = moves[:15]

      if not moves:
         return None

      for move in moves:
         new_board = board.clone()
         new_board.place_piece(move[0], move[1], self.player_id)
         score = self.minimax(new_board, 2, False, float('-inf'), float('inf'))
         
         if score > best_score:
            best_score = score
            best_move = move
       
      return best_move
   
