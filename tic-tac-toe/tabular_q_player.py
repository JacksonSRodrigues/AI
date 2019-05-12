from board import Player, Board, Status, Result
import numpy as np

class TabularQPlayer(Player):

    def __init__(self,name,avatar):
        super().__init__(name,avatar)
        self.QTable = {}
        self.match_history = []

    def get_most_successfull_move(self, board: Board):
        moves = board.available_moves()
        predictions = self.QTable.get(board.hash_value())
        if predictions is None:
            predictions = np.full(len(moves), .6)
            self.QTable[board.hash_value()] = predictions
        
        return moves[np.argmax(predictions)], moves


    def choose_move(self,board: Board):
        selected_move, available_moves = self.get_most_successfull_move(board)
        self.match_history.append((board.hash_value(),selected_move,available_moves))
        return selected_move


    def evaluate_own_moves(self,board: Board):
        learning_rate = 0.90
        discount_rate = 0.95
        score = 0
        if board.status == Status.Complete:
            if board.result == Result.Draw:
               score = 0.5 
            elif board.winner == self:
                score = 1
            else:
                score = 0
  
        tmp_history = self.match_history[:]
        tmp_history.reverse()
        last_item = tmp_history.pop(0)
        last_hash, last_move, available_moves = last_item
        qvalues = self.QTable.get(last_hash)
        qvalues[available_moves.index(last_move)] = score
        last_state_max = max(qvalues)

        while len(tmp_history) > 0:
            last_item = tmp_history.pop(0)
            last_hash, last_move, available_moves = last_item
            qvalues = self.QTable.get(last_hash)
            prev_move_rate = qvalues[available_moves.index(last_move)]
            score = prev_move_rate*(1 - learning_rate) + learning_rate * discount_rate * last_state_max
            qvalues[available_moves.index(last_move)] = score
            
            last_state_max = max(qvalues)
            

    def game_did_complete(self,board: Board):
        self.evaluate_own_moves(board)
        self.reset()

    def reset(self):
        self.match_history = []