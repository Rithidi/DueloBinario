class Position:
    def __init__(self):
        self.small_occupant = None  # size = 1 points a player
        self.medium_occupant = None  # size = 2 points a player
        self.large_occupant = None  # size = 3 points a player

    def store(self, a_player, size):
        if size == 1 and self.get_biggest_size() < 1:
            self.small_occupant = a_player
        elif size == 2 and self.get_biggest_size() < 2:
            self.medium_occupant = a_player
        elif size == 3 and self.get_biggest_size() < 3:
            self.large_occupant = a_player

    def remove(self, size):
        if size == 1 and self.get_biggest_size() == 1:
            self.small_occupant = None
        elif size == 2 and self.get_biggest_size() == 2:
            self.medium_occupant = None
        elif size == 3 and self.get_biggest_size() == 3:
            self.large_occupant = None

    def inform_empty(self):
        return self.small_occupant == None and self.medium_occupant == None and self.large_occupant == None

    def occupied(self):
        return not (self.inform_empty())

    def get_biggest_size(self):
        bigger = 0
        if self.large_occupant != None:
            bigger = 3
        elif self.medium_occupant != None:
            bigger = 2
        elif self.small_occupant != None:
            bigger = 1
        return bigger

    def get_biggest_occupant(self):
        bigger = None
        if self.large_occupant != None:
            bigger = self.large_occupant
        elif self.medium_occupant != None:
            bigger = self.medium_occupant
        elif self.small_occupant != None:
            bigger = self.small_occupant
        return bigger

    def same_player(self, p1, p2):
        if self.occupied() and p1.occupied() and p2.occupied():
            return (self.get_biggest_occupant() is p1.get_biggest_occupant()) and (
                self.get_biggest_occupant() is p2.get_biggest_occupant()
            )
        else:
            return False

    def belongs_to(self, a_player):
        if self.inform_empty():
            return False
        else:
            return self.get_biggest_occupant() is a_player
