import piece_movements
import copy
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
game = copy.deepcopy(game_at_start)

## TODO: better pawn promotions
# King move restrictions so he can't move into illegal squares 
# Other piece restrictions so they cannot move out of kings way if it is threatened (most likely won't do this...) 
# Checkmate checking
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

def init_new_game():
    # Reset values
    for key in kings_and_rooks_have_moved.keys():
        kings_and_rooks_have_moved[key] = False 
    for key in pieces_that_can_be_an_passanted.keys():
        pieces_that_can_be_an_passanted[key] = None
    return game_at_start



def check_for_king_and_rook_movements(piece, x, y):
    player = "White" if piece == piece.lower() else "Black"
    if piece.lower() == 'k':
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

def check_for_castling(piece, from_y, to_y, game):
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

def check_for_an_passant(piece, from_x, from_y, to_x, to_y, game):
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
    
def check_for_pawn_promotion(piece, to_x):
    # Checks for pawn promotion and returns queen if it promotes. Otherwise returns the same piece value it was given.
    if piece.lower() == 's' and (to_x == 0 or to_x == 7):
        player = get_player_from_piece(piece)
        piece = 'q' if player == "White" else 'Q'
        return piece
    return piece

def move_piece(from_x, from_y, to_x, to_y, game, check_special=True):
    # Get the value of the piece
    piece = game[from_x][from_y]

    # Special rules
    if check_special:
        check_for_king_and_rook_movements(piece, from_x, from_y)
        check_for_an_passant(piece, from_x, from_y, to_x, to_y, game)
        check_for_castling(piece, from_y, to_y, game)
    piece = check_for_pawn_promotion(piece, to_x) 

    if piece:
        # Move the piece to new location
        game[from_x][from_y] = ""
        game[to_x][to_y] = piece

    return game

def get_valid_moves(x, y, game, restrict=True):
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

    # Remove restricted moves. (moves that threaten the king)
    if restrict:
       restricted_moves = restrict_moves_based_on_king_safety(game, player, allowed_moves, x, y)
       for move in restricted_moves:
            if allowed_moves.count(move):
                allowed_moves.remove(move)
    
    
    return allowed_moves

def restrict_moves_based_on_king_safety(game_before_moving, player, allowed_moves, from_x, from_y):
    opponent = "White" if player == "Black" else "Black"
    restricted_moves = []

    # Remove castling rights from king if he is under attack
    if game[from_x][from_y].lower() == 'k' and check_for_checks(game, opponent) and from_y == 4:
        file = 7 if player == "White" else 0
        restricted_moves.append((file, 2))
        restricted_moves.append((file, 6))
        

    for move in allowed_moves:
        # If own king is in danger after moving a piece to a square; Make that move restricted
        # We need to create a deepcopy so the new game doesn't modify the old game
        game_after_moving = copy.deepcopy(game_before_moving)
        game_after_moving = move_piece(from_x, from_y, move[0], move[1], game_after_moving, check_special=False)

        if check_for_checks(game_after_moving, opponent):
            restricted_moves.append(move)
    return restricted_moves

def check_for_checks(game, player):
    # Gets every move of every player's piece and checks if opponent king is in danger

    for x in range(8):
        for y in range(8):
            piece = game[x][y]

            if piece == "": # Skip empty pieces
                pass
            elif get_player_from_piece(piece) == player: # Check your own pieces
                allowed_moves = get_valid_moves(x, y, game, restrict=False)
                for move in allowed_moves:
                        
                    if game[move[0]][move[1]].lower() == "k":
                        return True
    return False

def check_for_checkmate(game, player):
    game_after_moving = copy.deepcopy(game)
    for x in range(8):
        for y in range(8):
            piece = game[x][y]

            if piece == "": # Skip empty pieces
                pass
            elif get_player_from_piece(piece) != player: # Get every opponents piece and see if they can move
                allowed_moves = get_valid_moves(x, y, game_after_moving)
                if len(allowed_moves) > 0:
                    return False
    return True

def valid_for_player(player, piece):
    return (player == "White" and piece == piece.lower() and piece != "") or (player == "Black" and piece != piece.lower())

def get_player_from_piece(piece):
    return "White" if piece == piece.lower() else "Black"
