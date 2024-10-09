def get_pawn_moves(x, y, game, player, an_passant):
    allowed_moves = []
    move_dir = -1 if player == "White" else 1
    starting_row = 6 if player == "White" else 1

    if x == 0 or x == 7:
        return allowed_moves

    # Moving forwards one tile or two tiles
    if game[x + move_dir][y] == "":
        allowed_moves.append((x + move_dir, y))

        if x == starting_row and game[x + move_dir*2][y] == "":
            allowed_moves.append((x + move_dir * 2, y))

    # Hitting left and right
    left_side = y - 1
    if left_side >= 0 and enemy_on_tile(game[x + move_dir][left_side], player):
        allowed_moves.append((x + move_dir, y - 1))
        
    right_side = y + 1
    if right_side <= 7 and enemy_on_tile(game[x + move_dir][right_side], player):
        allowed_moves.append((x + move_dir, y + 1))

    # An passant rules
    an_passantable_piece = an_passant["White"] if player == "Black" else an_passant["Black"]
    if an_passantable_piece:
        enemy_piece_row, enemy_piece_col = an_passantable_piece[0], an_passantable_piece[1]
        if (x == starting_row + 3 * move_dir or x == starting_row + 4 * move_dir) and (enemy_piece_col == y + 1 or  enemy_piece_col == y - 1):
            allowed_moves.append((x + move_dir, enemy_piece_col))
            
    return allowed_moves

def get_rook_moves(x, y, game, player):
    allowed_moves = []

    def helper_func(row, col):
        if game[row][col] == "":
            allowed_moves.append((row, col))
            return False
        elif enemy_on_tile(game[row][col], player):
            allowed_moves.append((row, col))
            return True
        else:
            return True

    # Checks vertical range
    for row in reversed(range(0, x)):
        if helper_func(row, y):
            break

    for row in range(x + 1, 8):
        if helper_func(row, y):
            break

    # Check horizontal range
    for col in reversed(range(0, y)):
        if helper_func(x, col):
            break

    for col in range(y + 1, 8):
        if helper_func(x, col):
            break
    
    return allowed_moves

def get_bishop_moves(x, y, game, player):
    allowed_moves = []

    def helper_func(i_x, i_y):
        for i in range(0, 7):
            row = x + (i + 1) * i_x 
            col = y + (i + 1) * i_y
            if move_inside_play_area(row, col):    
                if game[row][col] == "":
                    allowed_moves.append((row, col))
                elif enemy_on_tile(game[row][col], player):
                    allowed_moves.append((row, col))
                    break
                else:
                    break
                
    helper_func(-1, -1)  # top-left
    helper_func(1, 1)    # bottom-right
    helper_func(-1, 1)   # top-right ?
    helper_func(1, -1)   # Bottom-left ? 

    return allowed_moves

def get_queen_moves(x, y, game, player):
    allowed_moves = get_rook_moves(x, y, game, player)
    for move in get_bishop_moves(x, y, game, player):
        allowed_moves.append(move)
    return allowed_moves

def get_knight_moves(x, y, game, player):
    allowed_moves = []

    def helper_func(add_x, add_y):
        row = x + add_x
        col = y + add_y
        if move_inside_play_area(row, col):
            move = (row, col)
            if game[row][col] == "" or enemy_on_tile(game[row][col], player):
                allowed_moves.append(move)
    helper_func(2, 1)
    helper_func(1, 2)
    helper_func(-2, 1)
    helper_func(-1, 2)
    helper_func(2, -1)
    helper_func(1, -2)
    helper_func(-2, -1)
    helper_func(-1, -2)
    return allowed_moves

def get_king_moves(x, y, game, player, pieces_moved):
    allowed_moves = []

    for row in range(x - 1, x + 2):
        right_move = (row, y + 1)
        mid_move = (row, y)
        left_move = (row, y - 1)

        moves = [right_move, mid_move, left_move]

        for move in moves:
            row, col = move[0], move[1]
            if move_inside_play_area(row, col):
                if game[row][col] == "" or enemy_on_tile(game[row][col], player):
                    allowed_moves.append(move)
        
    # Check castling rights
    if not pieces_moved[player]: # If king has not moved check right and left rooks and give castling move
        rook_right = f"{player}-right"
        rook_left = f"{player}-left"
        file = 7 if player == "White" else 0
        
        def empty_file(y):
            return game[file][y] == ""

        # Check castling rights for left and right side
        if not pieces_moved[rook_left] and empty_file(1) and empty_file(2) and empty_file(3):
            allowed_moves.append((file, 2))

        if not pieces_moved[rook_right] and empty_file(5) and empty_file(6):
            allowed_moves.append((file, 6))
    return allowed_moves

def move_inside_play_area(row, col):
    return row >= 0 and row <= 7 and col >= 0 and col <= 7

def enemy_on_tile(piece, player):
    return (player == "White" and piece != piece.lower()) or player == "Black" and piece == piece.lower() and piece != ""