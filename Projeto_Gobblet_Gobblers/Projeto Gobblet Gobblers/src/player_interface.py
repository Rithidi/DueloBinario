from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from board import Board
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor


class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.main_window = Tk()  # instanciar Tk
        self.fill_main_window()  # organização e preenchimento da janela
        self.board = Board()  # tratamento do domínio do problema
        game_state = self.board.get_status()
        self.update_gui(game_state)
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        self.main_window.mainloop()  # abrir a janela

    def fill_main_window(self):
        # Título, ícone, dimensionamento e fundo da janela
        self.main_window.title("Gobblet Gobblers")
        self.main_window.iconbitmap("src/images/icon.ico")
        self.main_window.geometry("1280x720")
        self.main_window.resizable(False, False)
        self.main_window["bg"] = "gold3"

        # Criação de 2 frames e organização da janela em um grid de 2 linhas e 1 coluna,
        # sendo que table_frame ocupa a linha superior e message_frame, a inferior
        self.table_frame = Frame(self.main_window, padx=100, pady=40, bg="gold3")
        self.table_frame.grid(row=0, column=0)
        self.message_frame = Frame(self.main_window, padx=0, pady=10, bg="gold3")
        self.message_frame.grid(row=1, column=0)

        # Definição de 2 imagens para o preenchimento inicial
        self.an_image = PhotoImage(file="src/images/yellow_square.png")  # pyimage1
        self.logo = PhotoImage(file="src/images/logo.png")  # pyimage2

        # Preenchimento de table_frame com 21 imagens iguais, organizadas em 3 linhas e 7 colunas
        self.board_view = []
        for y in range(7):
            a_column = []  # 	column
            for x in range(3):
                aLabel = Label(self.table_frame, bd=0, image=self.an_image)
                aLabel.grid(row=x, column=y)
                aLabel.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_board_place(event, a_line, a_column)
                )
                a_column.append(aLabel)
            self.board_view.append(a_column)

        # Preenchimento de message_frame com 1 imagem com logo (label) e 1 label com texto,
        # organizadas em 1 linha e 2 colunas
        self.logo_label = Label(self.message_frame, bd=0, image=self.logo)
        self.logo_label.grid(row=0, column=0)
        self.message_label = Label(self.message_frame, bg="gold3", text=" Gobblet Gobblers", font="arial 30")
        self.message_label.grid(row=0, column=1)

        # Criação de um menu para o programa
        # Criar a barra de menu (menubar) e adicionar à janela:
        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar
        # Adicionar menu(s) à barra de menu:
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")
        # Adicionar itens de menu a cada menu adicionado à barra de menu:
        self.menu_file.add_command(label="Iniciar jogo", command=self.start_match)
        self.menu_file.add_command(label="Restaurar estado inicial", command=self.start_game)

    def select_board_place(self, event, line, column):
        match_status = self.board.get_match_status()
        if match_status == 3 or match_status == 4:
            move_to_send = self.board.select_board_place(line, column)
            game_state = self.board.get_status()
            self.update_gui(game_state)
            if bool(move_to_send):
                self.dog_server_interface.send_move(move_to_send)

    def receive_move(self, a_move):
        self.board.receive_move(a_move)
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def start_match(self):
        match_status = self.board.get_match_status()
        if match_status == 1:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                start_status = self.dog_server_interface.start_match(2)
                code = start_status.get_code()
                message = start_status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                else:  #    (code=='2')
                    players = start_status.get_players()
                    local_player_id = start_status.get_local_id()
                    self.board.start_match(players, local_player_id)
                    game_state = self.board.get_status()
                    self.update_gui(game_state)
                    messagebox.showinfo(message=start_status.get_message())

    def receive_start(self, start_status):
        self.start_game()  #    use case reset game
        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self.board.start_match(players, local_player_id)
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def start_game(self):
        match_status = self.board.get_match_status()
        if match_status == 2 or match_status == 6:
            self.board.reset_game()
            game_state = self.board.get_status()
            self.update_gui(game_state)

    def receive_withdrawal_notification(self):
        self.board.receive_withdrawal_notification()
        game_state = self.board.get_status()
        self.update_gui(game_state)

    def update_gui(self, game_state):
        self.update_menu_status()
        self.message_label["text"] = game_state.get_message()
        self.image_to_draw = []
        cont = 0
        for column in range(7):
            for line in range(3):
                image_id = self.get_image_id(game_state, line, column)
                self.image_to_draw.append(PhotoImage(file=image_id))
                self.board_view[column][line]["imag"] = self.image_to_draw[cont]
                cont += 1

    def update_menu_status(self):
        match_status = self.board.get_match_status()
        if match_status == 2 or match_status == 6:
            self.menu_file.entryconfigure("Restaurar estado inicial", state="normal")
        else:
            self.menu_file.entryconfigure("Restaurar estado inicial", state="disabled")
        if match_status == 1:
            self.menu_file.entryconfigure("Iniciar jogo", state="normal")
        else:
            self.menu_file.entryconfigure("Iniciar jogo", state="disabled")

    def get_image_id(self, match_status, line, column):
        if column == 0 or column == 1:  #   red pieces space
            player1_pieces = match_status.get_player1_pieces()
            if line == 0:
                if player1_pieces[2] == 2 or (player1_pieces[2] == 1 and column == 0):
                    if player1_pieces[3] == 3 and column == 0:
                        return "src/images/pecaVGs.png"
                    else:
                        return "src/images/pecaVG.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 1:
                if player1_pieces[1] == 2 or (player1_pieces[1] == 1 and column == 0):
                    if player1_pieces[3] == 2 and column == 0:
                        return "src/images/pecaVMs.png"
                    else:
                        return "src/images/pecaVM.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 2:
                if player1_pieces[0] == 2 or (player1_pieces[0] == 1 and column == 0):
                    if player1_pieces[3] == 1 and column == 0:
                        return "src/images/pecaVPs.png"
                    else:
                        return "src/images/pecaVP.png"
                else:
                    return "src/images/pecaSem.png"

        elif column == 5 or column == 6:  #   blue pieces space
            player2_pieces = match_status.get_player2_pieces()
            if line == 0:
                if player2_pieces[2] == 2 or (player2_pieces[2] == 1 and column == 6):
                    if player2_pieces[3] == 3 and column == 6:
                        return "src/images/pecaAGs.png"
                    else:
                        return "src/images/pecaAG.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 1:
                if player2_pieces[1] == 2 or (player2_pieces[1] == 1 and column == 6):
                    if player2_pieces[3] == 2 and column == 6:
                        return "src/images/pecaAMs.png"
                    else:
                        return "src/images/pecaAM.png"
                else:
                    return "src/images/pecaSem.png"
            elif line == 2:
                if player2_pieces[0] == 2 or (player2_pieces[0] == 1 and column == 6):
                    if player2_pieces[3] == 1 and column == 6:
                        return "src/images/pecaAPs.png"
                    else:
                        return "src/images/pecaAP.png"
                else:
                    return "src/images/pecaSem.png"
        else:  #   board space
            selected_position = match_status.get_selected_position()
            selected_line = selected_position[0]
            selected_column = selected_position[1]
            if match_status.getValue(line, column - 2) == 6:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAGs.png"
                else:
                    return "src/images/posAG.png"
            if match_status.getValue(line, column - 2) == 5:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAMs.png"
                else:
                    return "src/images/posAM.png"
            if match_status.getValue(line, column - 2) == 4:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posAPs.png"
                else:
                    return "src/images/posAP.png"
            if match_status.getValue(line, column - 2) == 3:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVGs.png"
                else:
                    return "src/images/posVG.png"
            if match_status.getValue(line, column - 2) == 2:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVMs.png"
                else:
                    return "src/images/posVM.png"
            if match_status.getValue(line, column - 2) == 1:
                if selected_line == line and selected_column == column - 2:
                    return "src/images/posVPs.png"
                else:
                    return "src/images/posVP.png"
            else:
                return "src/images/posSem.png"
