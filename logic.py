import piece_movements
# White = lowercase; Black = Uppercase
# Rook, kNight, Bishop, King, Queen, Soldier
game_at_start = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['s', 's', 's', 's', 's', 's', 's', 's'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
]

## TODO: pawn promotions
# King move restrictions so he can't move into illegal squares 
# Other piece restrictions so they cannot move out of kings way if it is threatened (most likely won't do this...)
##

kings_and_rooks_have_moved = {
    'White': False, # White king
    'Black': False, # Black king
    'White-left': False, # Rooks
    'White-right': False,
    'Black-left': False,
    'Black-right': False,
}
pieces_that_can_be_an_passanted = {
    'White': None,
    'Black': None
}

def check_for_king_and_rook_movements(piece, x, y):
    if piece.lower() == 'k':
        player = "White" if piece == piece.lower() else "Black"
        kings_and_rooks_have_moved[player] = True
    
    if piece.lower() == 'r':
        # Black rooks
        if x == 0 and y == 0:
            kings_and_rooks_have_moved['Black-left'] = True
        if x == 0 and y == 7:
            kings_and_rooks_have_moved['Black-right'] = True
        # White rooks
        if x == 7 and y == 0:
            kings_and_rooks_have_moved['White-left'] = True
        if x == 7 and y == 7:
            kings_and_rooks_have_moved['White-right'] = True

def check_for_castling(piece, from_y, to_y):
    if piece.lower() == 'k':
        player = get_player_from_piece(piece)
        file = 7 if player == "White" else 0
        rook = 'r' if player == "White" else "R"

        # Check left and right side for castling
        if from_y == 4 and to_y == 2:
            game[file][0] = ""
            game[file][3] = rook
        elif from_y == 4 and to_y == 6:
            game[file][7] = ""
            game[file][5] = rook

def check_for_an_passant(piece, from_x, from_y, to_x, to_y):
    player = get_player_from_piece(piece)

    # Remove old passants from memory
    if pieces_that_can_be_an_passanted[player]:
        pieces_that_can_be_an_passanted[player] = None
    # Add new passant possibilities to dictionary
    if piece.lower() == 's':
        start_file = 6 if player == "White" else 1
        movement = -2 if player == "White" else 2

        if from_x == start_file and to_x == from_x + movement:
            pieces_that_can_be_an_passanted[player] = (to_x, to_y)

    # Do the an passant move by removing the moved piece
    if game[to_x][to_y] == "" and from_y != to_y:

        row = 3 if player == "White" else 4
        game[row][to_y] = ""
    


def move_piece(from_x, from_y, to_x, to_y, game):
    # Get the value of the piece
    piece = game[from_x][from_y]

    check_for_king_and_rook_movements(piece, from_x, from_y)

    check_for_castling(piece, from_y, to_y)

    check_for_an_passant(piece, from_x, from_y, to_x, to_y)

    if piece:
        # Move the piece to new location
        game[from_x][from_y] = ""
        game[to_x][to_y] = piece

    return game

def get_valid_moves(x, y, game):
    piece = game[x][y]
    player = get_player_from_piece(piece)

    allowed_moves = []
    if piece.lower() == 's':
        allowed_moves = piece_movements.get_pawn_moves(x, y, game, player, pieces_that_can_be_an_passanted)
    elif piece.lower() == 'r':
        allowed_moves = piece_movements.get_rook_moves(x, y, game, player)
    elif piece.lower() == 'b':
        allowed_moves = piece_movements.get_bishop_moves(x, y, game, player)
    elif piece.lower() == 'n':
        allowed_moves = piece_movements.get_knight_moves(x, y, game, player)
    elif piece.lower() == 'q':
        allowed_moves = piece_movements.get_queen_moves(x, y, game, player)
    elif piece.lower() == 'k':
        allowed_moves = piece_movements.get_king_moves(x, y, game, player, kings_and_rooks_have_moved)

    # print(f"allowed moves for {piece}: {allowed_moves}")
    return allowed_moves


def valid_for_player(player, piece):
    return (player == "White" and piece == piece.lower() and piece != "") or (player == "Black" and piece != piece.lower())

def get_player_from_piece(piece):
    return "White" if piece == piece.lower() else "Black"

game = game_at_start.copy()