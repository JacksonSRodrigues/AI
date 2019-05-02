from board import Player, Status, Result
from tic_tac_toe import TicTacToe
from enum import Enum

LOSE=-1
DRAW=0
WIN=1


class MinMaxPlayer(Player):

    def __init__(self, name, avatar):
        self.cache = {}
        super().__init__(name,avatar)

    def min(self,board):
        print('--------min--------------')
        hash_value = board.hash_value()
        if hash_value in self.cache:
            return self.cache[hash_value]

        score = DRAW
        action = None

        # For handling the cases win happende on last move
        print(board.winner)
        if board.winner is not None:
            if self == board.winner:
                score = WIN
            else:
                score = LOSE
        else:
            print('e',board.winner)
            for next_move in board.available_moves():
                eval_board = self.board_copy(board)
                print('<<',next_move, eval_board.available_moves())
                eval_board.make_move(self._competing_player(board),next_move) 
                board.visualize_state()
                next_score, _ = self.max(eval_board)
                self.cache[hash_value] = (next_score,next_move)
                if next_score > score or action is None:
                    score = next_score
                    action = next_move
                if score == LOSE:
                    break 
        return score, action

    def max(self, board:TicTacToe):
        print('-----------max-------------')
        hash_value = board.hash_value()
        if hash_value in self.cache:
            return self.cache[hash_value]
            
        score = DRAW
        action = None

        # For handling the cases win happende on last move
        if board.winner is not None:
            if self == board.winner:
                score = WIN
            else:
                score = LOSE
        else:
            print("-- {}".format(board.available_moves()))
            for next_move in board.available_moves():
                #print(next_move)
                eval_board = self.board_copy(board)
                eval_board.make_move(self,next_move)
                print(next_move,eval_board.available_moves())
                board.visualize_state()
                next_score, _ = self.min(eval_board)
                #print(next_move,next_score)
                self.cache[hash_value] = (next_score,next_move)
                if next_score < score or action is None:
                    score = next_score
                    action = next_move
                if score == WIN:
                    break
        return score, action

    def choose_move(self,board: TicTacToe):
        eval_board = self.board_copy(board)
        _, move = self.max(eval_board)
        return move

    def board_copy(self, board):
        eval_board = TicTacToe(nodes=list(board.nodes))
        eval_board.players = list(board.players)
        return eval_board

    def _competing_player(self,board):
        return list(filter(lambda p: p != self, board.players))[0]

    def did_win(self,board):
        is_winner = False
        if board.status == Status.Complete and board.winner == self:
            is_winner = True
        return is_winner

    def did_lose(self,board):
        is_loser = False
        if board.status == Status.Complete and board.winner != self and board.status != Result.Draw:
            is_loser = True
        return is_loser