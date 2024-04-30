class Location:
    def __init__(self, a_line, a_column):
        super().__init__()
        self.line = a_line
        self.column = a_column

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column
