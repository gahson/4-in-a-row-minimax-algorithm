import pygame
from pygame.locals import *
from random import choice

def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

def possible_columns(s):
    return [col for col in range(7) if s[0][col] == ' ']

def check_winner(s):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if s[row][col] != ' ' and all(s[row][col + i] == s[row][col] for i in range(4)):
                return s[row][col]

    # Check vertical
    for row in range(3):
        for col in range(7):
            if s[row][col] != ' ' and all(s[row + i][col] == s[row][col] for i in range(4)):
                return s[row][col]

    # Check diagonal (/)
    for row in range(3):
        for col in range(4):
            if s[row][col] != ' ' and all(s[row + i][col + i] == s[row][col] for i in range(4)):
                return s[row][col]

    # Check diagonal (\)
    for row in range(3):
        for col in range(3, 7):
            if s[row][col] != ' ' and all(s[row + i][col - i] == s[row][col] for i in range(4)):
                return s[row][col]

    # Check for draw
    if all(s[0][col] != ' ' for col in range(7)):
        return '?'

    return None

def drop_piece(board, column, piece):
    for row in range(5, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = piece
            return True
    return False

def min_max(s, player, depth=5):
    moves = possible_columns(s)
    if player:
        best = [choice(moves), float('-inf')]
        mark = 'O'
    else:
        best = [choice(moves), float('inf')]
        mark = 'X'

    res = check_winner(s)
    if depth == 0 or res is not None:
        if res == 'O':
            return [choice(moves), 1]
        elif res == 'X':
            return [choice(moves), -1]
        else:
            return [choice(moves), 0]

    for move in moves:
        if s[0][move] != ' ':
            continue
        to_remove = None
        for row in range(5, -1, -1):
            if s[row][move] == ' ':
                s[row][move] = mark
                to_remove = row
                break

        score = min_max(s.copy(), not player, depth - 1)
        score[0] = move
        s[to_remove][move] = ' '

        if player:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score

    return best

def ai_move(board):
    move, _ = min_max(board.copy(), True)
    return move

def draw_board(screen, board):
    for row in range(6):
        for col in range(7):
            color = (255, 255, 255)  # White
            if board[row][col] == 'X':
                color = (255, 0, 0)  # Red
            elif board[row][col] == 'O':
                color = (255, 255, 0)  # Yellow
            pygame.draw.circle(screen, color, (col * 100 + 50, row * 100 + 50), 40)

def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Connect Four')
    font = pygame.font.Font(None, 74)

    board = create_board()
    running = True
    game_over = False

    # Allow player to choose who starts
    first_player = None
    while first_player not in ('X', 'O'):
        first_player = input("Who starts? Enter 'X' for you or 'O' for AI: ").strip().upper()

    current_player = first_player

    while running:
        screen.fill((0, 0, 255))  # Blue background
        draw_board(screen, board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN and not game_over and current_player == 'X':
                x, y = event.pos
                col = x // 100
                if drop_piece(board, col, current_player):
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                        if winner == '?':
                            text = font.render("Draw!", True, (0, 0, 0))
                        else:
                            if winner == 'X':
                                winner = "Player"
                            else:
                                winner = "Computer"
                            text = font.render(f"{winner} Wins!", True, (0, 0, 0))
                        screen.blit(text, (200, 250))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        board = create_board()
                        game_over = False
                        current_player = first_player
                    else:
                        current_player = 'O'

        if not game_over and current_player == 'O':
            col = ai_move(board)
            drop_piece(board, col, 'O')
            winner = check_winner(board)
            if winner:
                game_over = True
                if winner == '?':
                    text = font.render("Draw!", True, (0, 0, 0))
                else:
                    if winner == 'X':
                        winner = "Player"
                    else:
                        winner = "Computer"
                    text = font.render(f"{winner} Wins!", True, (0, 0, 0))
                screen.blit(text, (200, 250))
                pygame.display.flip()
                pygame.time.wait(3000)
                board = create_board()
                game_over = False
                current_player = first_player
            else:
                current_player = 'X'

    pygame.quit()

if __name__ == '__main__':
    main()
