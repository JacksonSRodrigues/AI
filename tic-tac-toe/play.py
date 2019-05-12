from tic_tac_toe import TicTacToe, Player, Status, Result
from live_player import LivePlayer
from min_max_player import MinMaxPlayer
from tabular_q_player import TabularQPlayer
from battle_ground import BattleGround
import time

board = TicTacToe()
board.add_new_player(LivePlayer('John Doe', 'x'))
board.add_new_player(Player('Jean Doe','o'))

def play_game(board):
    while board.status is not Status.Complete:
        print('-------------')
        print(board.hash_value())
        p = board.next_player()
        print('Move for {}'.format(p.avatar))
        move = p.choose_move(board) 
        board.make_move(p,move)
        board.visualize_state()
        if board.status == Status.Complete:
            print('------------------------')
            if board.result == Result.Draw:
                print('We have a DRAW')
            else:
                print('{}({}) WON'.format(p.name,p.avatar))
            print('------------------------')
        

def test_live_player():
    board = TicTacToe()
    board.add_new_player(LivePlayer('Jack', 'x'))
    board.add_new_player(MinMaxPlayer('Jill','o'))
    play_game(board)

#test_live_player()

def test_board_statistics(p1,p2,test_count=1000):
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


#test_board_statistics(Player('Jack', 'x'), Player('Jill','o'),10)
#test_board_statistics(Player('Jack', 'x'),MinMaxPlayer('Jill','o'),10)
#test_board_statistics(MinMaxPlayer('Jack', 'x'),MinMaxPlayer('Jill','o'),10)


def test_Q_player():
    board = TicTacToe()
    battle_ground = BattleGround(board)
    tq_player = TabularQPlayer('Jack', 'x')
    battle_ground.join(tq_player)
    battle_ground.add_listener(tq_player)
    battle_ground.join(MinMaxPlayer('Jill','o'))
    battle_ground.start_battle()

#test_Q_player()


def test_tq_board_statistics(test_count=3000):
    print('Testing TQ')
    draws = 0
    player1 = 0
    player2 = 0

    board = TicTacToe()
    battle_ground = BattleGround(board)
    battle_ground.join(MinMaxPlayer('Min Max Player','o'))
    tq_player = TabularQPlayer('Tabular Q Player', 'x')
    battle_ground.join(tq_player)
    battle_ground.add_listener(tq_player)
    

    for i in range(test_count):
        print('Game {}'.format(i))
        board.reset()
        battle_ground.start_battle()
        if board.result == Result.Draw:
            draws += 1
        else:
            if board.players.index(board.winner) == 0:
                player1 += 1
            else:
                player2 += 1
    time.sleep(1)

    print('Draws: {}   Player 1 Won: {}     Player 2 Won: {}'.format(draws,player1,player2))

test_tq_board_statistics()