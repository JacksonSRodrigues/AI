from tic_tac_toe import TicTacToe, Player, Status, Result
from live_player import LivePlayer

board = TicTacToe()
board.add_new_player(LivePlayer('Jack', 'x'))
board.add_new_player(Player('Jill','o'))

def play_game(board):
    while board.status is not Status.Complete:
        print('-------------')
        p = board.next_player()
        print('Move for {}'.format(p.avatar))
        available_moves = board.available_moves()
        move = p.choose_move(available_moves) 
        board.make_move(p,move)
        board.visualize_state()

def test_live_player():
    board = TicTacToe()
    board.add_new_player(LivePlayer('Jack', 'x'))
    board.add_new_player(Player('Jill','o'))
    play_game(board)

test_live_player()

def test_board_statistics(p1,p2,test_count=100):
    draws = 0
    player1 = 0
    player2 = 0

    board = TicTacToe()
    board.add_new_player(p1)
    board.add_new_player(p2)

    for i in range(test_count):
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


#test_board_statistics(Player('Jack', 'x'),Player('Jill','o'))