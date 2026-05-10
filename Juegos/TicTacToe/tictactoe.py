import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe") #titulo de la ventana
        self.window.geometry("400x600")  #tamaño de la ventana
        self.window.configure(bg="#111111") #color de fondo de la ventana
        
        self.player = "X" # El jugador siempre empieza con X
        self.bot = "O" # La computadora siempre juega con O
        self.board = [" " for _ in range(9)]
        self.vs_computer = True
        
        # Variables para almacenar los puntos y de quién es el turno
        self.score_x = 0
        self.score_o = 0
        self.current_turn = "X" # Variable para rastrear el turno actual (X o O)
        
        self.setup_menu()

    def setup_menu(self):
        self.clear_window()
        self.score_x = 0 # Reiniciar el puntaje cada vez que se regresa al menú
        self.score_o = 0
        
        title = tk.Label(self.window, text="TIC-TAC-TOE", font=("Urbanist", 24, "bold"), fg="#deff9a", bg="#111111")
        title.pack(pady=50)
        
        btn_pvp = tk.Button(self.window, text="Jugador vs Jugador", font=("Urbanist", 14), 
                           command=lambda: self.start_game(False), bg="#222", fg="#fff", width=20)
        btn_pvp.pack(pady=10)
        
        btn_pve = tk.Button(self.window, text="vs Computadora (IA)", font=("Urbanist", 14), 
                           command=lambda: self.start_game(True), bg="#222", fg="#fff", width=20)
        btn_pve.pack(pady=10)

        btn_exit = tk.Button(self.window, text="Salir", font=("Urbanist", 14), 
                            command=self.window.quit, bg="#222", fg="#fff", width=20)
        btn_exit.pack(pady=10, side="bottom")

    def start_game(self, computer_mode):
        self.vs_computer = computer_mode
        self.current_turn = "X" # La X siempre empieza cada nueva ronda
        self.clear_window()
        self.buttons = []
        
        # Etiqueta (Label) de Puntuación
        score_text = f"Jugador X: {self.score_x}   |   Jugador O: {self.score_o}"
        self.lbl_score = tk.Label(self.window, text=score_text, font=("Urbanist", 14, "bold"), fg="#ffffff", bg="#111111")
        self.lbl_score.pack(pady=10)

        
        
        # Frame para la cuadrícula
        grid_frame = tk.Frame(self.window, bg="#111111")
        grid_frame.pack(expand=True)
        
        for i in range(9):
            btn = tk.Button(grid_frame, text=" ", font=("Urbanist", 20, "bold"), width=5, height=2,
                           command=lambda i=i: self.on_click(i), bg="#222", fg="#deff9a")
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Etiqueta (Label) del Turno Actual
        self.lbl_turn = tk.Label(self.window, text="Turno de: X", font=("Urbanist", 16, "bold"), fg="#deff9a", bg="#111111")
        self.lbl_turn.pack(pady=10)

        # Botón para poder regresar al menú principal y cambiar de modo de juego
        btn_back = tk.Button(self.window, text="Volver al Menú", font=("Urbanist", 12), 
                           command=self.setup_menu, bg="#444", fg="#fff")
        btn_back.pack(pady=20)

    def on_click(self, i):
        if self.board[i] == " ": #si la posición está vacía, se puede hacer un movimiento
            # Hacemos el movimiento usando al jugador actual
            self.make_move(i, self.current_turn)
            
            # Si el juego no ha terminado...
            if not self.check_winner(self.board) and " " in self.board:
                # Cambiamos el turno al siguiente jugador
                self.current_turn = "O" if self.current_turn == "X" else "X"
                self.update_turn_label() # Actualizamos el texto en pantalla
                
                # Si estamos jugando contra la PC y le toca a la "O", la PC mueve
                if self.vs_computer and self.current_turn == self.bot:
                    self.window.after(100, self.computer_move) # Pequeña demora para que no parezca que la PC juega instantáneamente

    def update_turn_label(self):
        # Cambia el texto y el color del mensaje dependiendo de a quién le toque
        color = "#deff9a" if self.current_turn == "X" else "#ff9a9a"
        self.lbl_turn.config(text=f"Turno de: {self.current_turn}", fg=color)

    def make_move(self, i, char):
        self.board[i] = char
        # Colorear distinto si es X o O
        color = "#deff9a" if char == "X" else "#ff9a9a"
        self.buttons[i].config(text=char, state="disabled", disabledforeground=color)
        
        winner = self.check_winner(self.board)
        if winner:
            # Sumar un punto al ganador
            if winner == "X":
                self.score_x += 1
            else:
                self.score_o += 1
                
            messagebox.showinfo("Fin del juego", f"¡Ganó {winner}!")
            self.reset_board() # Reinicia el tablero pero mantiene los puntos
            
        elif " " not in self.board:
            messagebox.showinfo("Fin del juego", "¡Empate!")
            self.reset_board()

    def computer_move(self):
        best_score = -float('inf') # Empezamos con el peor puntaje posible (infinito negativo)
        move = -1 # Aquí guardaremos la posición de la mejor jugada

        for i in range(9):  # Para todas las casillas del tablero
            if self.board[i] == " ":        # 1. Busca una casilla vacía
                self.board[i] = self.bot    # 2. Imagina que pone una "O" ahí (la jugada de la computadora)
                score = self.minimax(self.board, 0, False)  # 3. Le pregunta a minimax: "¿Qué pasa si hago esto?" (evaluamos esa jugada)
                self.board[i] = " " # 4. Borra la "O" imaginaria para dejar todo como estaba
                if score > best_score:  # 5. Si el puntaje de esta jugada es mejor que el que teníamos, lo guardamos
                    best_score = score
                    move = i
        if move != -1:  # 6. Una vez que revisó todo, hace la jugada real en la mejor posición
            self.make_move(move, self.bot)
            
            # Después de que la IA juega, le devolvemos el turno al jugador X
            if not self.check_winner(self.board) and " " in self.board:
                self.current_turn = "X"
                self.update_turn_label()

    def minimax(self, board, depth, is_maximizing):
        # Algoritmo de Inteligencia Artificial (se mantiene igual)
        winner = self.check_winner(board)

        # --- CASOS BASE: ¿El juego ya terminó en esta simulación? ---
        if winner == self.bot: return 10 - depth        # ¡La PC gana! (Puntaje alto)
        if winner == self.player: return depth - 10     # ¡El humano gana! (Puntaje bajo)
        if " " not in board: return 0                   # Empate (Puntaje neutral)
        
        # --- TURNO DE LA COMPUTADORA (Trata de Maximizar el puntaje) ---
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.bot
                    # Se llama a sí misma, pero ahora le toca al humano (False)
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score) # Se queda con el puntaje más alto
            return best_score

        # --- TURNO DEL HUMANO (Trata de Minimizar el puntaje) ---
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.player
                    # Se llama a sí misma, pero ahora le toca a la PC (True)
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score) # Asume que el humano elegirá la peor opción para la PC
            return best_score

    def check_winner(self, b):
        #posiciones ganadoras en el tablero
        lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for l in lines:
            if b[l[0]] == b[l[1]] == b[l[2]] != " ": # si las posiciones son iguales y no están vacías, hay un ganador
                return b[l[0]] # devuelve el símbolo del ganador (X o O)
        return None

    def reset_board(self):
        # reinicia las casillas y no vuelva a cargar todo el menú, así no perdemos el puntaje.
        self.board = [" " for _ in range(9)]
        self.start_game(self.vs_computer)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()