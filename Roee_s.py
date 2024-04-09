import random
import pygame
 
pygame.init()

run = True

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Roee Swisa: 2048')
font = pygame.font.SysFont('Ariel', 24)
spawn_new = True
init_count = 0
direction = ''


colors = {0: (204, 192, 179), 
          2: (238, 228, 218), 
          4: (237, 224, 200), 
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False

#מצייר את הרקע
def draw_board():
   pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
   pass

#משרטט קוביות רנדמליות
def generate_new_pieces(board):
    count = 0
    full_board = True
    while any(0 in row for row in board):
        if count == 1:
            return board, full_board
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[col][row] == 0:
            full_board = False
            count = 1
            if random.randint(1, 10) == 10:
                board[col][row] = 4   
            else:
                board[col][row] = 2
    return board, full_board


#מצייר את הקוביות
def draw_pieces(board):
    for i in range(4):
        for t in range(4):
            value = board[i][t]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [t * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.SysFont('Ariel', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(t * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)


 #תור
def take_turn(direc, board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0 :
                
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[ i - shift][j] = board[i][j]
                        board[i][j] = 0
      

    elif direc == 'DOWN':
        pass

    elif direc == 'LEFT':
        pass

    elif direc == 'RIGHT':
        pass












#המשחק הראשי
while run:
    screen.fill('grey')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = generate_new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.K_UP:
            direction = 'UP'
        elif event.type == pygame.K_DOWN:
            direction = 'DOWN'
        elif event.type == pygame.K_LEFT:
            direction = 'LEFT'
        elif event.type == pygame.K_RIGHT:
            direction = 'RIGHT'
        
    
    pygame.display.flip()
pygame.quit()
