from tic_tac_toe import TicTacToe, Player, Status, Result

board = TicTacToe()
board.add_new_player(Player('Jack', 'x'))
board.add_new_player(Player('Jill','o'))

def play_game(board):
    while board.status is not Status.Complete:
        print('----  {}'.format(board.status))
        print(board.available_moves())
        p = board.next_player()
        available_moves = board.available_moves()
        move = p.choose_move(available_moves) 
        print('Move made by {}'.format(p.avatar))
        board.make_move(p,move)
        board.visualize_state()

draws = 0
player1 = 0
player2 = 0


for i in range(100):
    print('Game {}'.format(i))
    board.reset()
    play_game(board)
    if board.result == Result.Draw:
        draws += 1
    else:
        if board.players.index(board.winner) == 0:
            player1 += 1
        else:
            player2 += 1


print('Draws: {}   Player 1 Won: {}     Player 2 Won: {}'.format(draws,player1,player2))
