import random
import pygame
 
pygame.init()

run = True

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Roee Swisa: 2048')
font = pygame.font.SysFont('Ariel', 24)



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


#מצייר את הרקע
def draw_board():
   pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
   pass



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


 
#המשחק הראשי
while run:
    screen.fill('grey')
    draw_board()
    draw_pieces(board_values)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    
    pygame.display.flip()
pygame.quit()
