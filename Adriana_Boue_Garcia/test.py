from board import HexBoard
from solution import SmartPlayer
import random

class RandomPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def play(self, board):
        moves = []
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == 0:
                    moves.append((i, j))
        return random.choice(moves) if moves else None

def test_game():
    size = 11  # Puedes subirlo a 7 o 11
    board = HexBoard(size)
    p1 = SmartPlayer(1)
    p2 = RandomPlayer(2)
    
    turn = 1
    while True:
        current_player = p1 if turn == 1 else p2
        move = current_player.play(board)
        
        if move:
            board.place_piece(move[0], move[1], turn)
            print(f"Jugador {turn} mueve a {move}")
        
        if board.check_connection(turn):
            print(f"\n¡EL JUGADOR {turn} HA GANADO!")
            break
            
        turn = 3 - turn # Cambiar turno (1 -> 2, 2 -> 1)

if __name__ == "__main__":
    test_game()