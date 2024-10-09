from PIL import Image, ImageTk

black_pawn = Image.open("images/black_pawn.png")
black_bishop = Image.open("images/black_bishop.png")
black_knight = Image.open("images/black_knight.png")
black_rook = Image.open("images/black_rook.png")
black_queen = Image.open("images/black_queen.png")
black_king = Image.open("images/black_king.png")

white_pawn = Image.open("images/white_pawn.png")
white_bishop = Image.open("images/white_bishop.png")
white_rook = Image.open("images/white_rook.png")
white_knight = Image.open("images/white_knight.png")
white_queen = Image.open("images/white_queen.png")
white_king = Image.open("images/white_king.png")


def get_image(piece):
    def get_picture(piece):
      match piece:
        case 'S':
              return black_pawn
        case 'B':
              return black_bishop
        case 'N':
              return black_knight
        case 'R':
              return black_rook
        case 'Q':
              return black_queen
        case 'K':
              return black_king
            
        case 's':
              return white_pawn
        case 'b':
              return white_bishop
        case 'n':
              return white_knight
        case 'r':
              return white_rook
        case 'q':
              return white_queen
        case 'k':
              return white_king
           
    img = get_picture(piece).resize((60, 60))
    
    return ImageTk.PhotoImage(img)
