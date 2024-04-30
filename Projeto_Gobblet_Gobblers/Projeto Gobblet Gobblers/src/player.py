class Player:
    def __init__(self):
        self.identifier = ""  #   string
        self.name = ""  #   string
        self.symbol = None  # int
        self.small_pieces = 2  # int
        self.medium_pieces = 2  # int
        self.large_pieces = 2  # int
        self.turn = False  # bool
        self.winner = False  # bool
        self.selected_piece = 0  # int: 0 - no piece; 1 - small, 2 - medium, 3 - large

    def initialize(self, aSymbol, an_id, a_name):  # Name!!!!
        self.reset()
        self.identifier = an_id  #   string
        self.symbol = aSymbol  # int
        self.name = a_name  #   string

    def reset(self):
        self.identifier = ""  #   string
        self.name = ""  #   string
        self.symbol = None  # int
        self.small_pieces = 2  # int
        self.medium_pieces = 2  # int
        self.large_pieces = 2  # int
        self.turn = False  # bool
        self.winner = False  # bool
        self.selected_piece = 0  # int: 0 - no piece; 1 - small, 2 - medium, 3 - large

    def toogle_turn(self):
        if self.turn == False:
            self.turn = True
        elif self.turn == True:
            self.turn = False

    def get_turn(self):
        return self.turn

    def get_identifier(self):
        return self.identifier

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_winner(self):
        return self.winner

    def set_winner(self):
        self.winner = True

    def get_selected_piece(self):
        return self.selected_piece

    def set_selected_piece(self, size):
        self.selected_piece = size

    def give_piece(self, size):
        if size == 1:
            self.small_pieces -= 1
        elif size == 2:
            self.medium_pieces -= 1
        elif size == 3:
            self.large_pieces -= 1

    def has_piece(self, size):
        if size == 1:
            return self.small_pieces > 0
        elif size == 2:
            return self.medium_pieces > 0
        elif size == 3:
            return self.large_pieces > 0

    def get_piece_state(self):
        state = []
        state.append(self.small_pieces)  # int
        state.append(self.medium_pieces)  # int
        state.append(self.large_pieces)  # int
        state.append(self.selected_piece)  # int: 0 - no piece; 1 - small, 2 - medium, 3 - large
        return state
