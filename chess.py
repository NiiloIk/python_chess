import logic
import tkinter as tk
from image_handler import get_image
CELL_SIZE = 80

class Chess():
    def __init__(self, canvas, cell_size):
        self.game = logic.game
        self.player_turn = "White"
        self.selected_square = (-1, -1) 
        self.allowed_moves = []
        self.canvas = canvas
        self.cell_size = cell_size
        self.rows = len(self.game)
        self.cols = len(self.game[0])
        self.checkmate = False
        
        self.images = self.load_images()
        self.canvas.pack()
        self.draw_board()
        canvas.bind("<Button-1>", self.click_board) # Modify this to make interactive

    def load_images(self):
        return {
            'S': get_image('S'),
            'B': get_image('B'),
            'N': get_image('N'),
            'R': get_image('R'),
            'Q': get_image('Q'),
            'K': get_image('K'),
            's': get_image('s'),
            'b': get_image('b'),
            'n': get_image('n'),
            'r': get_image('r'),
            'q': get_image('q'),
            'k': get_image('k')
        }

    def draw_board(self):
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = self.get_color(row, col)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                self.draw_piece(row, col, x1 + self.cell_size // 2, y1 + self.cell_size // 2)
                
                # Highlight allowed moves
                if self.allowed_moves and self.allowed_moves.count((row, col)):
                    i = 16
                    self.canvas.create_oval(x1+i, y1+i, x2-i, y2-i, fill="#887")
        if self.checkmate:
            print("Checkmate")
            x1 = self.cell_size * 2
            y1 = self.cell_size * 3
            x2 = self.cell_size * 6
            y2 = self.cell_size * 5
            text_x = self.cell_size * 4
            text_y = self.cell_size * 4
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#555", outline="black")
            self.canvas.create_text(text_x, text_y, text="checkmate", fill="black", font=('Helvetica 20 bold'))

    def get_color(self, row, col):
        if self.selected_square[0] == row and self.selected_square[1] == col:
            return  "Blue"
        elif row % 2 == 1:
            return "#bbb" if col % 2 == 1 else "#363"
        else:
            return "#363" if col % 2 == 1 else "#bbb"


    def draw_piece(self, x, y, pos_x, pos_y):
        piece = self.game[x][y]
        if piece:
            image = self.images.get(piece)
            if image:
                self.canvas.create_image(pos_x, pos_y, image=image)

    def click_board(self, event):
        # Get the cell that was clicked
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.click_event_handler(row, col)
    
    def click_event_handler(self, row, col):

        player = self.player_turn
        last_selected = self.selected_square
        former_piece = self.game[last_selected[0]][last_selected[1]] if last_selected[0] >= 0 else None # Return the value of former selected piece. 
        selected_piece = self.game[row][col]
        if self.checkmate:
            self.game = logic.init_new_game()
            self.checkmate = False
            self.selected_square = (-1, -1) 
            self.allowed_moves = []
            self.player_turn = "White"
        elif self.selected_square == (row, col):
            self.selected_square = (-1, -1)
            self.allowed_moves = []
        elif logic.valid_for_player(player, selected_piece): # Get valid moves for a given piece
            self.selected_square = (row, col)
            self.allowed_moves = logic.get_valid_moves(row, col, self.game)
        elif former_piece:
            # Check if the former selected square belongs to current player
            if logic.valid_for_player(player, former_piece) and self.allowed_moves.count((row, col)):
                # Move the piece to new position
                from_x, from_y = last_selected[0], last_selected[1]
                self.game = logic.move_piece(from_x, from_y, row, col, self.game)
                if logic.check_for_checkmate(self.game, player):
                    self.checkmate = True

                # Change the player after a move
                self.player_turn = "White" if player == "Black" else "Black"
                self.allowed_moves = []
                self.selected_square = (-1, -1)


        # Draw board after click
        self.draw_board()


def init_game():
    '''
    Initiates canvas.

    '''
    root = tk.Tk()
    root.title("Chess")

    canvas = tk.Canvas(root, width=CELL_SIZE * len(logic.game[0]), height=CELL_SIZE * len(logic.game[0]))

    # init the chess game
    app = Chess(canvas, CELL_SIZE)

    root.mainloop()


if __name__ == "__main__":
    init_game()