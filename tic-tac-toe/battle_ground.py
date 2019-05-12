from board import Board, Player, Status, Result

class BattleGround:

    def __init__(self, board: Board):
        self.board = board
        self.listeners = []

    def join(self,player: Player):
        self.board.add_new_player(player)

    def start_battle(self):
        board = self.board
        while board.status is not Status.Complete:
            #print('-------------')
            #print(board.hash_value())
            p = board.next_player()
            #print('Move for {}'.format(p.avatar))
            move = p.choose_move(board) 
            board.make_move(p,move)
            #board.visualize_state()
            if board.status == Status.Complete:
                print('------------------------')
                if board.result == Result.Draw:
                    print('We have a DRAW')
                else:
                    print('{}({}) WON'.format(p.name,p.avatar))
                print('------------------------')
                self.notify_listeners()

    def add_listener(self, listner):
        self.listeners.append(listner)

    def remove_listener(self, listner):
        self.listeners.remove(listner)

    def notify_listeners(self):
        for listener in self.listeners:
            listener.game_did_complete(self.board)