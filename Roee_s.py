import random
import pygame
import os 
pygame.init()
run = True

high_score_file = 'high_score.txt'
if not os.path.exists(high_score_file):
    with open(high_score_file, 'w') as file:
        file.write('0')
with open(high_score_file, 'r') as file:
    high_score = int(file.read())

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Roee Swisa: 2048')
font = pygame.font.SysFont('Ariel', 24)
game_over_font = pygame.font.SysFont('Ariel', 33)
letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                      'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
spawn_new = True
init_count = 0
direction = ''
score = 0
play_sound = True
merged_sound = 'C:\\Users\\ניצנים\\Documents\\project_Raz2048\\678742__cloud-10__martin-garrix-animals-drop-pluck-original.wav'
sound_effect = pygame.mixer.Sound(merged_sound)
game_over_music = 'C:\\Users\\ניצנים\\Documents\\project_Raz2048\\173859__jivatma07__j1game_over_mono.wav'
game_over_sound = pygame.mixer.Sound(game_over_music)
bg_music = 'C:\\Users\\ניצנים\\Documents\\project_Raz2048\\scott-buckley-permafrost(chosic.com).mp3'
Getting_name = font.render(f'You have made new high score enter your name: {score}', True, 'black')
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)


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
   score_text = font.render(f'Score: {score}', True, 'black')
   high_score_text = font.render(f'High Score: {high_score}', True, 'black')
   screen.blit(high_score_text, (10, 440))
   screen.blit(score_text, (10, 410))

#משרטט קוביות רנדמליות
def generate_new_pieces(board):
    count = 0
    full_board = True
    while any(0 in row for row in board):
        #כך עוד יש אפס איפשהו בלוח
        if count == 1:
            return board, full_board
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[col][row] == 0:
            #אם המיקום הרנדומלי שנבחר שווה לאפס נוסיף קוביה
            full_board = False
            count = 1
            if random.randint(1, 10) == 10:
                # במשחק יש סיכוי של עשרה אחוז לקבל ארבע במקום שתיים אז נבדוק את זה
                board[col][row] = 4   
            else:
                #אחרת יוצב שתיים
                board[col][row] = 2
        # אם הלוח לא מצא מקום ששווה לאפס זאת אומרת הלוח מלא
    return board, full_board


#מצייר את הקוביות
def draw_pieces(board):
    for i in range(4):
        for t in range(4):
            value = board[i][t]
            if value > 8:
                #אם הערך גדול משמונה צבע הטקסט יהיה כהה יותר כדי שהטקסט יראה טוב יותר
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                # אם הערך גדול או שווה ל2048 זה אומר שיש לו צבע מוגדר 
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [t * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
            # רק הערכים שגדולים מערך יוצגו
                value_len = len(str(value))
                font = pygame.font.SysFont('Ariel', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(t * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)


 #תור
def take_turn(direc, board):
    global score
    if direc == 'UP':
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4): 
            for j in range(4):
                shift = 0
                if i > 0:
                    #בודקים אם הוא בשורה האחרונה
                    for q in range(i):
                        #נבדוק כמה ריבועים אפשר לזוז
                        if board[q][j] == 0:
                            #אם הריבוע מעליו שווה לאפס זה אומר שאפשר לזוז עוד ריבוע אחד
                            shift += 1
                    if shift > 0:
                        #אם יש לריבוע לאן לזוז
                        board[i - shift][j] = board[i][j]
                        #נגדיר את המיקום החדש באמצעות המשתנה שיפט שמגדיר לנו כמה אנחנו יכולים לזוז 
                        board[i][j] = 0
                        #המיקום של הקוביה לפני התזוזה תשתנה לאפס
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                        and not merged[i - shift - 1][j]:
                        #אם הקוביה שווה לקוביה מעליה והיא והקוביה מעליה לא התמזגו 
                        sound_effect.play()
                        board[i - shift - 1 ][j] *= 2
                        #הקוביה תתמזג ותזוז למעלה למיקום של הקוביה שהתמזגה איתה והערך יהיה שווה פי שניים
                        score += board[i - shift - 1 ][j]
                        board[i - shift][j] = 0
                        #הקוביה במיקום הישן תהיה שווה לאפס
                        merged[i - shift - 1][j] = True
    elif direc == 'DOWN':
        merged = [[False for _ in range(4)] for _ in range(4)] 
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                        and not merged[2 - i + shift][j]:
                        sound_effect.play()
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i][j] = 0
                        merged[3 - i + shift][j] = True


    elif direc == 'LEFT':
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                    and not merged[i][j - shift]:
                    sound_effect.play()
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
      

    elif direc == 'RIGHT':
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <=3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                    and not merged[i][3 - j + shift]:
                        sound_effect.play()
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift]

    return board


#המשחק הראשי
while run:
    screen.fill('grey')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
#הפונקציה תכנס לבפנים אם אינט קונט קטן משתיים וזה רק רק בתחילת המשחק מכיוון שבתחילת המשחק אמורות להשתגר שתי קוביות רנדומליות ולא אחת
#ואם ספואן ניו שווה נכון והוא שווה לנכון רק אחרי שהשחקן מבצע תנועה אם השחקן לא ביצעה תנועה לא יהיו קוביות חדשות
        board_values, game_over = generate_new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if game_over:
        #אחרי שקראנו לפונקציה נבדוק אם המשחק נגמר
        if play_sound:
            #אם עדיין לא נגנו את הסאונד של סוף המשחק
            game_over_sound.play()
            play_sound = False
        if high_score < score:
            #אם הניקוד הנוכחי גבוה יותר מהניקוד הקודם
            high_score = score
            name = input("Enter your name:")
        with open(high_score_file, 'w') as file:
            file.write(str(high_score))
        game_over_text = game_over_font.render("Game over your final score: " + str(score), True, (20, 20, 0))
        screen.blit(game_over_text, (35, 180))


    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #אם נלחץ איקס נסגור את המסך
            run = False
        if event.type == pygame.KEYDOWN:
            #אם נלחץ כפתור ונבדוק איזה אחד מן הכפתורים נלחץ
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'



    pygame.display.flip()
pygame.quit()
