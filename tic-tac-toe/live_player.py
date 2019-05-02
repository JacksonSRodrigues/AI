from board import Player

class LivePlayer(Player):

    def __init__(self, name, avatar):
        super().__init__(name,avatar)

    def choose_move(self,board):
        valid_moves = board.available_moves()
        print(valid_moves)
        recieved_valid_move = False
        move = None
        while not recieved_valid_move:
            user_input = input('Enter your Move from Above : ')
            move = tuple(map(int, user_input.split(',')))
            if move in valid_moves:
                recieved_valid_move = True
            else:
                print('Invalid Move!')
        return move

