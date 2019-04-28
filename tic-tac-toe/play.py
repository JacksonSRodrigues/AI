from tic_tac_toe import TicTacToe, Player, Status 
import random

board = TicTacToe()
board.add_new_player(Player('Jack', 'x'))
board.add_new_player(Player('Jill','o'))
while board.status is not Status.Complete:
    print('----  {}'.format(board.status))
    print(board.available_moves())
    p = board.next_player()
    available_moves = board.available_moves()
    move = random.choice(available_moves)
    print('Move made by {}'.format(p.avatar))
    board.make_move(p,move)
    board.visualize_state()


