import numpy as np
import pygame
import sys
import math
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

rows = 3
cols = 3

piece1 = 1
piece2 = 2

depth = 0


def create_board(rows, cols):
    if (rows < 3 or cols < 3):
        print("Enter a select grid size  (3X3) is the minimum size")
    else:
        return np.zeros((rows, cols))


def is_valid_location(board, row, col):
    return board[row][col] == 0


def drop_piece(board, row, col, Player):
    board[row][col] = Player


def winning_move(board, Player):
    # Alignement horizontal
    for r in range(rows):
        for c in range(cols - 2):
            if board[r][c] == Player and board[r][c + 1] == Player and board[r][c + 2] == Player:
                return True

    # Alignement vertical
    for c in range(cols):
        for r in range(rows - 2):
            if board[r][c] == Player and board[r + 1][c] == Player and board[r + 2][c] == Player:
                return True

    # Alignement Diagonale positive:
    for r in range(2, rows):
        for c in range(cols - 2):
            if board[r][c] == Player and board[r - 1][c + 1] == Player and board[r - 2][c + 2] == Player:
                return True

    # Algnement Diagonale negative:
    for r in range(rows - 2):
        for c in range(cols - 2):
            if board[r][c] == Player and board[r + 1][c + 1] == Player and board[r + 2][c + 2] == Player:
                return True


def draw_board(board):
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE), 2)
            if (board[r][c] == piece1):
                pygame.draw.circle(screen, BLACK,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS,
                                   2)
            if (board[r][c] == piece2):
                x1 = int(c * SQUARESIZE + SQUARESIZE / 8)
                y1 = int(r * SQUARESIZE + SQUARESIZE / 8)
                x2 = int(c * SQUARESIZE + 7 * SQUARESIZE / 8)
                y2 = int(r * SQUARESIZE + 7 * SQUARESIZE / 8)
                x1b = int(c * SQUARESIZE + 7 * SQUARESIZE / 8)
                y1b = int(r * SQUARESIZE + SQUARESIZE / 8)
                x2b = int(c * SQUARESIZE + SQUARESIZE / 8)
                y2b = int(r * SQUARESIZE + 7 * SQUARESIZE / 8)

                pygame.draw.line(screen, BLACK, [x1, y1], [x2, y2], 2)
                pygame.draw.line(screen, BLACK, [x1b, y1b], [x2b, y2b], 2)


def show_winner(screen, piece):
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))

    pygame.display.update()

    if (piece == 1):
        myFont = pygame.font.SysFont("monospace", 17)
        WinnerText = myFont.render("The winner is Player O", True, BLACK)
        screen.blit(WinnerText, (int(SQUARESIZE / 2), int(cols / 2) * SQUARESIZE))
        pygame.display.update()

    else:
        myFont = pygame.font.SysFont("monospace", 17)
        WinnerText = myFont.render("The winner is Player X ", True, BLACK)
        screen.blit(WinnerText, (int(SQUARESIZE / 2), SQUARESIZE))
        pygame.display.update()


def show_equal():
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))

    pygame.display.update()

    myFont = pygame.font.SysFont("monospace", 17)
    EqualText = myFont.render("No one wins", True, BLACK)
    screen.blit(EqualText, (int(SQUARESIZE / 2), int(cols / 2) * SQUARESIZE))
    pygame.display.update()


# ---------------------------- MiniMax---------------------
def children_node(node, Player):
    children = []
    for r in range(rows):
        for c in range(cols):
            if is_valid_location(node, r, c):
                node_temp = node
                drop_piece(node_temp, r, c, Player)
                children.append(node_temp)
    return children


def is_terminal_node(node):
    board_full = True
    for r in range(rows):
        for c in range(cols):
            if is_valid_location(node, r, c):
                board_full = False
                break
    return winning_move(node, piece1) or winning_move(node, piece2) or board_full


def number_tows(board, Player):
    nb = 0

    # Horizontal tows
    for r in range(rows):
        for c in range(cols - 1):
            if board[r][c] == Player and board[r][c + 1]:
                nb += 1

    # Vertical tows
    for r in range(rows - 1):
        for c in range(cols):
            if board[r][c] == Player and board[r + 1][c]:
                nb += 1

    return nb


def best_move(board):
    best_score = -100
    best_row = 0
    best_col = 0
    for r in range(rows):
        for c in range(cols):
            if is_valid_location(board, r, c):
                temp_board = board
                drop_piece(temp_board, r, c, piece2)
                score = minimaxx(temp_board)
                if score > best_score:
                    best_score = score
                    best_row = r
                    best_col = c

    return best_row, best_col


def heuristic_evalution(node):
    heuristic_value = 0
    if winning_move(node, piece2):
        heuristic_value = 400
    elif winning_move(node, piece1):
        heuristic_value = -400
    else:
        heuristic_value = 4 * number_tows(board, piece2) - 4 * number_tows(board, piece1)

    return heuristic_value


def minimaxx(board):
    return 1  # heuristic_evalution(board)


def minimax(node, depth, maximiziningPlayer):
    if depth == 0 or is_terminal_node(node):
        return heuristic_evalution(node)

    children = children_node(node, piece2)

    if maximiziningPlayer:  # Maximizing player
        value = -math.inf

        for child in children:
            valuen = minimax(child, depth - 1, False)
            if valuen > value:
                value = valuen
                return value
    else:
        value = math.inf

        for child in children:
            valuen = minimax(child, depth - 1, True)
            if valuen < value:
                value = valuen
                return value


# -----------------------Test AI---------------------------
def test_AI(board):
    Rows = []
    Cols = []
    for r in range(rows):
        for c in range(cols):
            if is_valid_location(board, r, c):
                Rows.append(r)
                Cols.append(c)
    row = random.choice(Rows)
    col = random.choice(Cols)
    return row, col


# ---------------------- Initializing ---------------------
# Displaying text
pygame.font.init()
myFont = pygame.font.SysFont("monospace", 60)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 3)
width = cols * SQUARESIZE
hight = rows * SQUARESIZE
size = (hight, width)
screen = pygame.display.set_mode(size)
screen.fill(WHITE)

game_over = False
turn = 1

board = create_board(rows, cols)
draw_board(board)

# ----------------------------- Main Loop ------------------------
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0:
                posx = event.pos[0]
                col = math.floor(posx / SQUARESIZE)
                col = int(col)
                posy = event.pos[1]
                row = math.floor(posy / SQUARESIZE)
                row = int(row)
                if is_valid_location(board, row, col):
                    drop_piece(board, row, col, piece1)
                    draw_board(board)
                    print(board)
                    turn += 1
                    turn = turn % 2
                    if winning_move(board, piece1):
                        show_winner(screen, piece1)
                        game_over = True
            else:
                row, col = best_move(board)
                if is_valid_location(board, row, col):
                    drop_piece(board, row, col, piece2)
                    pygame.time.wait(400)
                    draw_board(board)
                    print(board)
                    if winning_move(board, piece2):
                        show_winner(screen, piece2)
                        game_over = True
                    turn += 1
                    turn = turn % 2
        if is_terminal_node(board) and not winning_move(board, piece1) and not winning_move(board, piece2):
            show_equal()
            game_over = True
        pygame.display.update()
        if game_over:
            pygame.time.wait(2000)
            print(board)
"""
"""

"""
			else:
				# Human adversaire

				posx=event.pos[0]
				col=math.floor(posx/SQUARESIZE)
				col=int(col)

				posy=event.pos[1]
				row=math.floor(posy/SQUARESIZE)
				row=int(row)

				#print(col)

				#------ AI adversaire
				row,col=test_AI(board)


				if is_valid_location(board,row,col):
					drop_piece(board,row,col,piece2)
					#print(row)
					#pygame.display.update()
					draw_board(board)
					print(board)
					if winning_move(board,piece2):
						show_winner(screen,piece2)
						game_over=True

					turn+=1
					turn=turn%2
			if is_terminal_node(board) and not winning_move(board,piece1) and not winning_move(board,piece2):
					show_equal()
					game_over=True

			"""