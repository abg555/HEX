class HexBoard:
    
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)

    def clone(self) -> "HexBoard":
        copy = HexBoard(self.size)
        for i in range(self.size):
            for j in range(self.size):
                copy.board[i][j] = self.board[i][j]
        return copy        

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if row >= 0 and row < self.size and col >= 0 and col < self.size and self.board[row][col] == 0:
            self.board[row][col] = player_id
        else:
            return False
        return True

    def check_connection(self, player_id: int) -> bool:
        visited = set()
        stack = []
        par= [(-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,1)]
        impar = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1)]
        if player_id == 1:
            for i in range(self.size):
                if self.board[i][0] == player_id:
                    stack.append((i, 0))
                    visited.add((i,0))
        else:
            for i in range(self.size):
                if self.board[0][i] == player_id:
                    stack.append((0, i))
                    visited.add((0,i))
        while stack:
            (row,col) = stack.pop()
            if player_id == 1 and col == self.size - 1:
                return True
            if player_id == 2 and row == self.size-1:
                return True
            if row % 2 == 0:
                 position = par
            else:
                position = impar
            for (i,j) in position:
                new_row = row + i
                new_col = col + j
                if (new_row,new_col) not in visited and new_row >= 0 and new_col >= 0 and new_row < self.size and new_col < self.size and self.board[new_row][new_col] == player_id:
                    stack.append((new_row,new_col))
                    visited.add((new_row,new_col))
        return False
                

        

        



