from enum import Enum
import types

class Status(Enum):
    NotStarted = 0
    InProgress = 1
    Complete = 2
    

class Result(Enum):
    Invalid = 0
    Won = 1
    Draw = 2

class Player:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar


class Board:

    def __init__(self):
        self.status = Status.NotStarted
        self.result = Result.Invalid
        self.players = []

    def available_moves(self):
        return []

    def max_players(self):
        return 2

    def min_players(self):
        return 1

    def add_new_player(self, player):
        if self.players.count() < self.max_players():
            self.players.append(player)
        else:
            raise Exception('Players have reached the limit')

    def is_move_valid(self,move):
        return False

    def save_move(self,player,move):
        return True

    def make_move(self,player,move):
        if not self.is_move_valid(move):
            raise Exception('Invalid Move')
        else:
            self.save_move(player,move)

    def evaluate_result(self):
        return Result.Invalid

    def visualize_state(self):
        return ""


class TicTacToe(Board):

    def __init__(self):
        self.nodes = [[' ' for c in range(3)] for r in range(3)]
        super().__init__()

    def available_moves(self):
        moves = []
        for r in range(len(self.nodes)):
            row = self.nodes[r]
            for c in range(len(row)):
                column = row[c]
                if type(column) is not tuple:
                    moves.append((r,c))

        return moves

    def is_move_valid(self, move):
        [row, column] = move
        if type(self.nodes[row][column]) is not tuple:
            return True 
        return False

    def save_move(self, player, move):
        [row, column] = move
        self.nodes[row][column] = (player,move)
        return True

    def evaluate_result(self):
        return Result.Invalid

    def visualize_state(self):
        for row in range(len(self.nodes)):
            row_data = self.nodes[row]
            print('|{}|{}|{}|'.format(self.translate_node(row_data[0]), self.translate_node(row_data[1]), self.translate_node(row_data[2])))
            #print('-------')

    def translate_node(self,node):
        if type(node) is tuple:
            return node[0].avatar
        else:
            return node




p1 = Player('Jack', 'x')
p2 = Player('Jill', 'o')
board = TicTacToe()
print(board.available_moves())
board.make_move(p1,(1,1))
print(board.available_moves())
board.make_move(p2,(2,1))
print(board.available_moves())
board.visualize_state()
