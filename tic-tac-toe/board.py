from enum import Enum
import types
import random

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
        self.last_player = None

    def available_moves(self):
        return []

    def max_players(self):
        return 2

    def min_players(self):
        return 1

    def add_new_player(self, player):
        if len(self.players) < self.max_players():
            self.players.append(player)
        else:
            raise Exception('Players have reached the limit')

    def next_player(self):
        player = None
        if len(self.players) > 0:
            try:
                player_index = (self.players.index(self.last_player) + 1) % len(self.players)
                player = self.players[player_index]
            except:
                player = self.players[0]
        return player


    def is_move_valid(self,move):
        return False

    def save_move(self,player,move):
        return True

    def make_move(self,player,move):
        self.status = Status.InProgress
        if not self.is_move_valid(move):
            raise Exception('Invalid Move')
        else:
            self.last_player = player
            self.save_move(player,move)

        result = self.evaluate_result(player)
        if result != Result.Invalid:
            print('Game Over !!')
            self.status = Status.Complete
            self.result = result

    def evaluate_result(self,player):
        return Result.Invalid

    def visualize_state(self):
        return ""


class TicTacToe(Board):

    def __init__(self):
        self.nodes = [[' ' for c in range(3)] for r in range(3)]
        self.winning_states = [
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)],
            [(0,1),(1,1),(2,1)],
            [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)],
            [(0,2),(1,1),(2,0)]]

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

    def moves_by_player(self,player):
        moves = []
        for r in range(len(self.nodes)):
            row = self.nodes[r]
            for c in range(len(row)):
                column = row[c]
                if type(column) is tuple and column[0] == player:
                    moves.append((r,c))
        return moves

    def evaluate_result(self,player):
        result = Result.Invalid
        moves = self.moves_by_player(player)

        for w_state in self.winning_states:
            matches = set(w_state).intersection(set(moves)) #[i for i,j in zip(w_state,moves) if i == j]
            if len(matches) >= 3:
                result = Result.Won
                break
        
        if result == Result.Invalid and len(self.available_moves()) == 0:
            result = Result.Draw

        return result

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
