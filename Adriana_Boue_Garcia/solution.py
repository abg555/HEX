from player import Player
from board import HexBoard
from collections import deque

class SmartPlayer(Player):
   def moves(self, hex_board: HexBoard) -> list:
      moves = []
      for i in range(hex_board.size):
         for j in range(hex_board.size):
            if hex_board.board[i][j] == 0:
               moves.append((i, j))
      return moves
   
   def aux(self, hex_board: HexBoard, player_id: int) -> int:
      cola = deque()
      distance = {}
      par= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
      impar = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]

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
            position = par
         else:
            position = impar

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
   
   def minimax(self, hex_board: HexBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
      rival = 3 - self.player_id
     
      if hex_board.check_connection(self.player_id) or hex_board.check_connection(rival) or depth == 0:
         return self.evaluate(hex_board)
      
      if is_maximizing:
         moves = self.moves(hex_board)
         for move in moves:
            new_board = hex_board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)
            score = self.minimax(new_board, depth - 1, False, alpha, beta)
            alpha = max(alpha, score)
            if beta <= alpha:
               break
         return alpha

      else:
         moves = self.moves(hex_board)
         for move in moves:
            new_board = hex_board.clone()
            new_board.place_piece(move[0], move[1], rival)
            score = self.minimax(new_board, depth - 1, True, alpha, beta)
            beta = min(beta, score)
            if beta <= alpha:
               break
         return beta
      
   def play(self, board: HexBoard) -> tuple:
      best_score = float('-inf')
      best_move = None
      moves = self.moves(board)

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
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   # def moves(self, hex_board: HexBoard) -> list:
   #    moves = []
   #    for i in range(hex_board.size):
   #       for j in range(hex_board.size):
   #          if hex_board.board[i][j] == 0:
   #             moves.append((i, j))
   #    return moves
   
   # def simulate_move(self, hex_board: HexBoard, move: tuple, player_id: int) -> HexBoard:
   #    new_hex_board = hex_board.clone()
   #    new_hex_board.place_piece(move[0], move[1], player_id)
   #    return new_hex_board
   
   # def evaluate(self, hex_board: HexBoard) -> float:
   #    rival = 3 - self.player_id
   #    if hex_board.check_connection(self.player_id):
   #       return 1.0
   #    elif hex_board.check_connection(rival):
   #       return -1.0
   #    else:
   #       return 0.0
      
   # def minimax(self, hex_board: HexBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
   #    rival = 3 - self.player_id
      
   #    if hex_board.check_connection(self.player_id):
   #       return 1.0
   #    elif hex_board.check_connection(rival):
   #       return -1.0
      
   #    if depth == 0:
   #       return self.evaluate(hex_board)
      
   #    if is_maximizing:
   #       moves =  self.moves(hex_board)
   #       for i in moves:
   #          new_board = self.simulate_move(hex_board, i, self.player_id)
   #          score = self.minimax(new_board, depth - 1, False, alpha, beta)
   #          alpha = max(alpha, score)
   #          if beta <= alpha:
   #              break
   #       return alpha
      
   #    else:
   #       moves = self.moves(hex_board)
   #       for i in moves:
   #          new_board = self.simulate_move(hex_board, i, 3 - self.player_id)
   #          score = self.minimax(new_board, depth - 1, True, alpha, beta)
   #          beta = min(beta, score)
   #          if beta <= alpha:
   #              break
   #       return beta

   # def play(self, board: HexBoard) -> tuple:
   #    best_move = None
   #    best_value = float('-inf')
   #    moves = self.moves(board)
   #    for move in moves:
   #       new_board = self.simulate_move(board, move, self.player_id)
   #       score = self.minimax(new_board, 3, False, float('-inf'), float('inf'))  
   #       if score > best_value:
   #          best_value = score   
   #          best_move = move
   #    return best_move