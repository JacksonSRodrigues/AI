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
    Lost = 3

class Player:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar

    def choose_move(self, board):
        valid_moves = board.available_moves()
        if len(valid_moves) <= 0:
            raise Exception('No Valid moves available')
        return random.choice(valid_moves)


class Board:

    def __init__(self):
        self.status = Status.NotStarted
        self.result = Result.Invalid
        self.players = []
        self.last_player = None
        self.winner = None

    def reset(self):
        self.status = Status.NotStarted
        self.result = Result.Invalid
        self.last_player = None
        self.winner = None

    def hash_value(self):
        pass

    def one_dimensional_representation(self):
        pass

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
            if result == Result.Won:
                self.winner = player


    def evaluate_result(self,player):
        return Result.Invalid


    def visualize_state(self):
        return ""
