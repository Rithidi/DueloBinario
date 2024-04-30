from pyexpat.errors import XML_ERROR_UNDEFINED_ENTITY
import position
import player
from location import Location
from interface_image import InterfaceImage
import math

# 	Board matchStatus
# 1 - no match (initial state)
# 2 - finished match (game with winner - no tied game)
# 3 - your turn, match in progress AND NOT move occurring (waiting first action)
# 4 - your turn, match in progress AND move occurring (waiting second action)
# 5 - NOT your turn, match in progress - waiting move
# 6 - match abandoned by opponent

class Board:
    def __init__(self):
        super().__init__()
        self.local_player = player.Player()
        self.remote_player = player.Player()
        self.local_player.initialize(1, "Red player", "Red player")
        self.remote_player.initialize(2, "Blue player", "Blue player")
        self.match_status = 1
        self.selected_location = None
        self.regular_move = True
        self.first_local_action = None
        self.second_local_action = None
        self.positions = []
        for y in range(3):
            column = []
            for x in range(3):
                column.append(position.Position())
            self.positions.append(column)

    def get_match_status(self):
        return self.match_status

    def get_status(self):
        interface_image = InterfaceImage()
        #       message
        turn_player = self.get_turn_player()
        if not self.regular_move:
            interface_image.setMessage(turn_player.get_name() + ", jogada irregular")
        else:
            if self.match_status == 1:
                interface_image.setMessage("Gobblet Gobblers")
            elif self.match_status == 2:
                interface_image.setMessage("Vencedor: " + self.get_winner_name())
            elif self.match_status == 3:
                interface_image.setMessage(turn_player.get_name() + ", selecione peça ou posição")
            elif self.match_status == 4:
                interface_image.setMessage(turn_player.get_name() + ", selecione posição destino")
            elif self.match_status == 5:
                interface_image.setMessage("Aguardando lance do adversário: " + self.remote_player.get_name())
            elif self.match_status == 6:
                interface_image.setMessage("Adversário abandonou a partida")
                #    pieces
        player1_pieces = self.local_player.get_piece_state()
        interface_image.set_player1_pieces(player1_pieces)
        player2_pieces = self.remote_player.get_piece_state()
        interface_image.set_player2_pieces(player2_pieces)

        #    selected board position
        if self.selected_location != None:
            selected_position = []
            selected_position.append(self.selected_location.get_line())
            selected_position.append(self.selected_location.get_column())
            interface_image.set_selected_position(selected_position)
            #    board positions (3x3)
        for y in range(3):
            for x in range(3):
                value = self.positions[x][y].get_biggest_size()
                if self.positions[x][y].get_biggest_occupant() is self.remote_player:
                    value += 3
                interface_image.setValue(x, y, value)
                #    return status
        return interface_image

    def select_board_place(self, grid_line, grid_column):  #   grid_line 0 to 2, grid_column 0 to 6
        move_to_send = {}
        if self.match_status == 3:  #   match in progress AND NOT move occurring -> select piece or origin
            if grid_column >= 2 and grid_column <= 4:  #   position area (2 to 4)
                self.select_origin(grid_line, grid_column)
            else:  #   piece area (0, 1, 5 and 6)
                self.select_piece(grid_line, grid_column)
        elif self.match_status == 4:  #   match in progress AND move occurring -> select destination
            move_to_send = self.select_destination(grid_line, grid_column)
        return move_to_send

    def receive_move(self, a_move):
        grid_line1 = int(a_move["first_action_line"])
        grid_column1 = int(a_move["first_action_column"])
        grid_line2 = int(a_move["second_action_line"])
        grid_column2 = int(a_move["second_action_column"])
        if self.match_status == 5:
            if grid_column1 >= 2 and grid_column1 <= 4:  #   position area (2 to 4)
                self.select_origin(grid_line1, grid_column1)
            else:  #   piece area (0, 1, 5 and 6)
                self.select_piece(grid_line1, (grid_column1 + 5))
            self.select_destination(grid_line2, grid_column2)

    def receive_withdrawal_notification(self):
        self.match_status = 6  #  match abandoned by opponent

    def start_match(self, players, local_id):
        playerA_name = players[0][0]
        playerA_id = players[0][1]
        playerA_order = players[0][2]
        playerB_name = players[1][0]
        playerB_id = players[1][1]
        self.local_player.reset()
        self.remote_player.reset()
        self.local_player.initialize(1, playerA_id, playerA_name)
        self.remote_player.initialize(2, playerB_id, playerB_name)
        if playerA_order == "1":
            self.local_player.toogle_turn()
            self.match_status = 3  #    waiting piece or origin selection (first action)
        else:
            self.remote_player.toogle_turn()
            self.match_status = 5  #    waiting remote action

    def reset_game(self):
        self.local_player = player.Player()
        self.remote_player = player.Player()
        self.local_player.initialize(1, "Red player", "Red player")
        self.remote_player.initialize(2, "Blue player", "Blue player")
        self.match_status = 1
        self.selected_location = None
        self.regular_move = True
        self.positions = []
        for y in range(3):
            column = []
            for x in range(3):
                column.append(position.Position())
            self.positions.append(column)

    def select_origin(self, grid_line, grid_column):
        turn_player = self.get_turn_player()
        self.regular_move = self.positions[grid_line][grid_column - 2].belongs_to(turn_player)
        if self.regular_move:
            self.selected_location = Location(grid_line, grid_column - 2)
            self.first_local_action = Location(grid_line, grid_column)
            self.match_status = 4  #   move occurring (waiting second action)

    def select_piece(self, grid_line, grid_column):
        turn_player = self.get_turn_player()
        self.regular_move = True
        if (turn_player is self.local_player and grid_column > 1) or (
            turn_player is self.remote_player and grid_column < 5
        ):
            self.regular_move = False
        if self.regular_move:
            self.regular_move = turn_player.has_piece(3 - grid_line)  # 3-grid_line is the size value
        if self.regular_move:
            turn_player.set_selected_piece(3 - grid_line)
            self.first_local_action = Location(grid_line, grid_column)
            self.match_status = 4  #   move occurring (waiting second action)

    def select_destination(self, grid_line, grid_column):
        move_to_send = {}
        if grid_column < 2 or grid_column > 4:  # outside position area (board area) - irregular
            self.match_status = 3  #    waiting piece or origin selection (first action)
            self.regular_move = False
        else:
            turn_player = self.get_turn_player()
            clicked_position = self.positions[grid_line][grid_column - 2]
            clicked_size = clicked_position.get_biggest_size()
            selected_position = None
            if self.selected_location == None:  #    there is a selected piece
                selected_piece_size = turn_player.get_selected_piece()
            else:  #    there is a selected position
                selected_line = self.selected_location.get_line()
                selected_column = self.selected_location.get_column()
                selected_position = self.positions[selected_line][selected_column]
                selected_piece_size = selected_position.get_biggest_size()
            if selected_piece_size <= clicked_size:  # piece does not fit in the destination - irregular
                self.match_status = 3  #    waiting piece or origin selection (first action)
                self.regular_move = False
            else:  # selected piece fits in the destination
                reachable = True
                if selected_position != None:
                    reachable = self.adjacent_to_selected_location(grid_line, grid_column - 2)
                if not reachable:
                    self.match_status = 3  #    waiting piece or origin selection (first action)
                    self.regular_move = False
                else:  #    reachable destination AND REGULAR MOVE
                    self.second_local_action = Location(grid_line, grid_column)
                    move_to_send["first_action_line"] = str(self.first_local_action.get_line())
                    move_to_send["first_action_column"] = str(self.first_local_action.get_column())
                    move_to_send["second_action_line"] = str(self.second_local_action.get_line())
                    move_to_send["second_action_column"] = str(self.second_local_action.get_column())
                    if selected_position != None:
                        selected_position.remove(selected_piece_size)
                    else:
                        turn_player.give_piece(selected_piece_size)
                    clicked_position.store(turn_player, selected_piece_size)
                    finished = self.evaluate_match_finish()
                    if finished:
                        move_to_send["match_status"] = "finished"
                        self.match_status = 2  #    finished match / no move occurring
                    else:
                        move_to_send[
                            "match_status"
                        ] = "next"  # 'next' (pass the turn to the next player) or 'progress' (match in progress)
                        self.local_player.toogle_turn()
                        self.remote_player.toogle_turn()
                        if self.local_player.get_turn():
                            self.match_status = 3  #    waiting piece or origin selection (first action)
                        else:
                            self.match_status = 5  #    waiting remote move
                        # no move occurring
        self.clear_selections()
        return move_to_send

    def get_turn_player(self):
        if self.local_player.get_turn():
            return self.local_player
        elif self.remote_player.get_turn():
            return self.remote_player
        else:
            return None

    def get_winner_name(self):
        if self.local_player.get_winner():
            return self.local_player.get_name()
        elif self.remote_player.get_winner():
            return self.remote_player.get_name()
        else:
            return None

    def adjacent_to_selected_location(self, clicked_line, clicked_column):
        selected_line = self.selected_location.get_line()
        selected_column = self.selected_location.get_column()
        x_dif = int(math.fabs(selected_line - clicked_line))
        y_dif = int(math.fabs(selected_column - clicked_column))
        return (x_dif == 1 and y_dif == 1) or ((x_dif == 0 and y_dif == 1) or (x_dif == 1 and y_dif == 0))

    def clear_selections(self):
        self.selected_location = None
        self.local_player.set_selected_piece(0)
        self.remote_player.set_selected_piece(0)
        self.first_local_action = None
        self.second_local_action = None

    def evaluate_match_finish(self):
        turn_player = self.get_turn_player()
        local_player_may_win = False
        remote_player_may_win = False
        for x in range(3):
            line = []
            for y in range(3):
                line.append(self.positions[x][y])
            if line[0].same_player(line[1], line[2]):
                if line[0].get_biggest_occupant() is self.local_player:
                    local_player_may_win = True
                else:
                    remote_player_may_win = True
        for y in range(3):
            column = []
            for x in range(3):
                column.append(self.positions[x][y])
            if column[0].same_player(column[1], column[2]):
                if column[0].get_biggest_occupant() is self.local_player:
                    local_player_may_win = True
                else:
                    remote_player_may_win = True
        for z in range(2):
            diagonal = []
            diagonal.append(self.positions[2 * z][0])
            diagonal.append(self.positions[1][1])
            diagonal.append(self.positions[2 - 2 * z][2])
            if diagonal[0].same_player(diagonal[1], diagonal[2]):
                if diagonal[0].get_biggest_occupant() is self.local_player:
                    local_player_may_win = True
                else:
                    remote_player_may_win = True
        if local_player_may_win or remote_player_may_win:
            if local_player_may_win and not turn_player is self.local_player:
                self.local_player.set_winner()
            elif remote_player_may_win and not turn_player is self.remote_player:
                self.remote_player.set_winner()
            elif local_player_may_win:
                self.local_player.set_winner()
            elif remote_player_may_win:
                self.remote_player.set_winner()
            return True
        else:
            return False
