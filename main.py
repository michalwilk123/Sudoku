import sys, pygame
from pygame.locals import *
import config
import functions as fn

# sudoku by Michal Wilk - 15.02.2020
def game_prep():
    global sudoku, player_sudoku
    sudoku = []
    player_sudoku = []
    sudoku = fn.create_puzzle()
    for row in sudoku: player_sudoku.append(row.copy())
    player_sudoku = fn.set_sudoku(player_sudoku, config.EASY_DIFF)

pygame.display.init()
pygame.font.init()
game_prep()

size = width, height = 600, 500
screen = pygame.display.set_mode(size)
bg = pygame.image.load("bg.png")

font = pygame.font.get_default_font()
font_obj = pygame.font.SysFont( font, config.SUDOKU_NUM_SIZE)
tile = font_obj.render( "sd", True, config.BLACK)
square = pygame.Rect(0, 0, config.TILE_WIDTH, config.TILE_HEIGHT)
wrong_num = []
highlight = { "x" : None, "y" : None}
spf = int(config.SPRITES_PER_SECOND * 1000)
game_over = False
timer_start = pygame.time.get_ticks()
time_in_sec = 0
clock_text = "00 : 00"

while True:
    pygame.time.wait(spf)

    # blitting the background
    screen.blit(bg, (0, 0))

    timer_stop = pygame.time.get_ticks()
    # blitting the numbers for the timer
    if timer_stop - timer_start >= 1000:
        time_in_sec += 1
        clock_text = fn.get_time_str(time_in_sec)
        timer_start = pygame.time.get_ticks()

    clock_textbox = font_obj.render(clock_text, True, config.BLACK)
    screen.blit(clock_textbox, (config.CLOCK_X, config.CLOCK_Y))

    #blitting clicked squares
    if highlight["x"] != None:
        square.left = fn.set_position(config.TILE_X_OFFSET, config.TILE_WIDTH,
            highlight["x"])
        square.top = fn.set_position(config.TILE_Y_OFFSET, config.TILE_HEIGHT,
            highlight["y"])
        screen.fill( config.GREY, square)

    #blitting squares for wrong_placed numbers
    if wrong_num:
        for item in wrong_num:
            square.left = fn.set_position(config.TILE_X_OFFSET,
                config.TILE_WIDTH, item[1])
            square.top = fn.set_position(config.TILE_Y_OFFSET,
                config.TILE_HEIGHT, item[0])
            screen.fill( config.RED, square)

    # blitting numbers into sudoku grid
    for i in range(len(player_sudoku)):
        y_pos = fn.set_position(config.VER_OFFSET, config.TILE_HEIGHT, i)
        for j in range(len(player_sudoku[i])):
            if player_sudoku[i][j] == 0: continue
            tile = font_obj.render(str(player_sudoku[i][j]), True, config.BLACK)
            x_pos = fn.set_position(config.HOR_OFFSET, config.TILE_WIDTH, j)
            screen.blit(tile,( x_pos, y_pos))

    # checking if game ended and waiting for ENTER key to reset the game
    while game_over:
        pygame.time.wait(spf)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                game_prep()
                game_over = False
                break

    # end menu
    if not wrong_num:
        if fn.check_win(player_sudoku):
            end_display = pygame.Rect(0, config.SCREEN_HEIGHT // 3,
                config.SCREEN_WIDTH, config.SCREEN_HEIGHT // 3)
            end_font = pygame.font.SysFont( font, config.MENU_FONT_SIZE)
            screen.fill( config.WHITE, end_display)
            text = ["YOU WON", "CLICK ENTER TO TRY AGAIN"]
            game_over = True
            for i in range(len(text)):
                end_message = end_font.render(text[i], True, config.BLACK)
                text_width, text_height = end_message.get_size()
                screen.blit(end_message, ((config.SCREEN_WIDTH - text_width) // 2, ((config.SCREEN_HEIGHT
                    - config.MENU_FONT_SIZE) // 2 + i * text_height)))

    # click and keyboard events
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()
            sudoku_num, sudoku_row = fn.click_detect(position)
            if sudoku_row < 9 and sudoku_num < 9:
                highlight = { "x" : sudoku_num, "y" : sudoku_row }

            # checking if reset or hint button was clicked
            if position[0] in range(config.RESET_BUTTON_X, config.RESET_BUTTON_X + config.RESET_BUTTON_WIDTH):
                if position[1] in range(config.RESET_BUTTON_Y, config.RESET_BUTTON_Y + config.RESET_BUTTON_HEIGHT):
                    clock_text = "00 : 00"
                    time_in_sec = 0
                    game_prep()

            if position[0] in range(config.HINT_BUTTON_X, config.HINT_BUTTON_X + config.HINT_BUTTON_WIDTH):
                if position[1] in range(config.HINT_BUTTON_Y, config.HINT_BUTTON_Y + config.HINT_BUTTON_HEIGHT):
                    x0 ,y0 = fn.get_hint(player_sudoku)
                    player_sudoku[y0][x0] = sudoku[y0][x0]
        if event.type == KEYDOWN:
            if event.key in (K_0, K_KP0): number_clicked = 0
            elif event.key in (K_1, K_KP1): number_clicked = 1
            elif event.key in (K_2, K_KP2): number_clicked = 2
            elif event.key in (K_3, K_KP3): number_clicked = 3
            elif event.key in (K_4, K_KP4): number_clicked = 4
            elif event.key in (K_5, K_KP5): number_clicked = 5
            elif event.key in (K_6, K_KP6): number_clicked = 6
            elif event.key in (K_7, K_KP7): number_clicked = 7
            elif event.key in (K_8, K_KP8): number_clicked = 8
            elif event.key in (K_9, K_KP9): number_clicked = 9
            else: break

            if highlight["x"] != None:
                w_coord = [highlight["y"], highlight["x"]]

                if number_clicked == 0 or fn.check_tile(number_clicked,
                    highlight["y"], highlight["x"], player_sudoku):
                    if w_coord in wrong_num:
                        wrong_num.remove(w_coord)
                else:
                    if w_coord not in wrong_num:
                        wrong_num.append(w_coord)
                player_sudoku[highlight["y"]][highlight["x"]] = number_clicked
        elif event.type == QUIT: sys.exit()

    pygame.display.flip()
