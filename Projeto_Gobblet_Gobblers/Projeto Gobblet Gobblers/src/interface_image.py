class InterfaceImage:
    def __init__(self):
        super().__init__()
        self.message = ""
        self.map = []
        for y in range(3):
            column = []
            for x in range(3):
                column.append(0)
            self.map.append(column)
        self.selected_position = [3, 3]
        self.player1_pieces = [2, 2, 2, 0]
        self.player2_pieces = [2, 2, 2, 0]

    def get_message(self):
        return self.message

    def setMessage(self, text):
        self.message = text

    def getValue(self, line, column):
        return self.map[(line - 1)][(column - 1)]

    def setValue(self, line, column, value):
        self.map[(line - 1)][(column - 1)] = value

    def get_selected_position(self):
        return self.selected_position

    def set_selected_position(self, an_array):
        self.selected_position = an_array

    def get_player1_pieces(self):
        return self.player1_pieces

    def set_player1_pieces(self, an_array):
        self.player1_pieces = an_array

    def get_player2_pieces(self):
        return self.player2_pieces

    def set_player2_pieces(self, an_array):
        self.player2_pieces = an_array
