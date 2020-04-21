import numpy as np
import pygame
import sys
import random
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (31, 154, 141)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
piece1 = 1
piece2 = 2


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(board)


def wining_move(board, piece):
    # check all the horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True
    # Check all vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True
    # Positive slope
    for c in range(3, COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c - 1] == piece and board[r + 2][c - 2] == piece and board[r + 3][
                c - 3] == piece:
                return True

    # Negative slope
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True


def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if (board[r][c] == 0):
                pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            if (board[r][c] == piece1):
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            if (board[r][c] == piece2):
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)


pygame.font.init()
board = create_board()
game_over = False

turn = random.randint(0, 1)
pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 6)
size = (width, height)

screen = pygame.display.set_mode(size)
myFont = pygame.font.SysFont("monospace", 30)
draw_board()
# ----------------------Minimax----------------------------------


# ---------------------Alpha Beta pruning-----------------------


# ---------------------- Main Program----------------------------

while not game_over:
    # Ask for Player 1 input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

                pygame.display.update()
            if turn == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)

            if turn == 0:
                posx = event.pos[0]
                col = math.floor(posx / SQUARESIZE)
                col = int(col)

                # print(col)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, piece1)
                    # print(row)
                    turn += 1
                    turn = turn % 2

            else:
                posx = event.pos[0]
                col = math.floor(posx / SQUARESIZE)
                col = int(col)
                # col=int(input("Player 2 Make your selection (0_6) :"))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, piece2)
                    turn += 1
                    turn = turn % 2
            print_board(board)

            if wining_move(board, 1):
                WinnerText = myFont.render("The winner is Player 1", True, YELLOW)
                screen.blit(WinnerText, (int(width / 3), int(SQUARESIZE / 2)))
                game_over = True
            if wining_move(board, 2):
                WinnerText = myFont.render("The winner is Player 2", True, RED)
                screen.blit(WinnerText, (int(width / 3), 0))

                game_over = True

    # turn+=1
    # turn=turn%2
    draw_board()
    pygame.display.update()
    if game_over:
        pygame.time.wait(3000)