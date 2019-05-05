from board import Player, Status, Result
from tic_tac_toe import TicTacToe
from enum import Enum

LOSE=-1
DRAW=0
WIN=1


class MinMaxPlayer(Player):

    def __init__(self, name, avatar):
        super().__init__(name,avatar)
        self.cache = {}
        

    def min(self,board):
        """
        Minimize the Players Move, i.e this is to calculate the impact of opposite players counter move.
        So here we find the minimum of the possible values that the parent move can lead to. Lowest value being Loosing the game.
        """
        hash_value = board.hash_value()
        if hash_value in self.cache:
            return self.cache[hash_value]

        score = DRAW
        action = None

        # Check for the end of Game.
        if board.winner is not None:
            if self == board.winner:
                score = WIN
            else:
                score = LOSE
        else: # If Game is not finished by the last move, Lets check the possibilities, of the remaining moves.
            for next_move in board.available_moves(): 
                eval_board = self.board_copy(board) # Create a new copy of the board.
                eval_board.make_move(self._competing_player(eval_board),next_move) # Make the move, by Oppenent.
                next_score, _ = self.max(eval_board) # Calculate the result which can be achieved by our Counter move.
                if next_score < score or action is None: # Save the minimal Score yet, and the move.
                    score = next_score
                    action = next_move
                    self.cache[hash_value] = (next_score,next_move) # Cache for performance.
                if score == LOSE: # Stop iteration if the Opponents move leads us to faliure.
                    break
        return score, action



    def max(self, board:TicTacToe):
        """
        MMaximize the Players Move, i.e this is to calculate the maximum impact a player can male.
        So here we find the Maximum of the possible result that the parent move can lead to, even an opponent makes the move.
        """

        hash_value = board.hash_value()
        if hash_value in self.cache:
            return self.cache[hash_value]
            
        score = DRAW
        action = None

        # Check for the end of Game.
        if board.winner is not None:
            if self == board.winner:
                score = WIN
            else:
                score = LOSE
        else: # If Game is not finished by the last move, Lets check the possibilities, of the remaining moves.
            for next_move in board.available_moves():
                eval_board = self.board_copy(board) # Create a new copy of the board.
                eval_board.make_move(self,next_move) # Make a move as Self.
                next_score, _ = self.min(eval_board) # Calculate the score that can be lead by Opponents move.
                if next_score > score or action is None:
                    score = next_score
                    action = next_move
                    self.cache[hash_value] = (next_score,next_move) # Cache for performance
                if score == WIN: #Stop iteration if the move can lead to a WIN
                    break
        return score, action


    def choose_move(self,board: TicTacToe):
        """
        Choose a Move for Player, which Maximizes our winning Chance.
        """
        eval_board = self.board_copy(board)
        _, move = self.max(eval_board)
        return move

    def board_copy(self, board):
        """
        Make a copy of the board.
        """
        eval_board = TicTacToe(nodes=list(map(lambda row: list(row),board.nodes)))
        eval_board.players = list(board.players)
        eval_board.last_player = board.last_player
        eval_board.result = board.result
        eval_board.status = board.status
        eval_board.winner = board.winner
        return eval_board
        

    def _competing_player(self,board):
        """
        Find the opponent.
        """
        return list(filter(lambda p: p != self, board.players))[0]