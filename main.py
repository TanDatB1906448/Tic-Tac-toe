import pygame
import algorithm

pygame.init()

screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Tic Tac Toe")

WHITE = (255, 255, 255)
C948E99 = (148, 142, 153) #Grey
C3a6186 = (58, 97, 134)  #Blue
C89253e = (137, 37, 62) #purple
BLACK = (0, 0, 0)
WIN_COLOR = WHITE
BACKGROUND = C948E99
HOME_BG = C948E99
X_COLOR = C3a6186
O_COLOR = C89253e

BI = pygame.image.load('Image\LoveCouple.jpg')
BG_IMG = pygame.transform.scale(BI,(600,700))

font_normal = pygame.font.Font("Font\EmotionEngine.otf", 30)
font_gamename = pygame.font.Font("Font\EmotionEngine.otf", 100)
font_moving = pygame.font.SysFont("sans", 180)
font_score = pygame.font.Font("Font\EmotionEngine.otf", 25)
font_turning_lable = pygame.font.Font("Font\EmotionEngine.otf", 40)
font_gamename.bold = True
font_turning_lable.bold = True
text_x = font_moving.render("X", True, X_COLOR)
text_o = font_moving.render("O", True, O_COLOR)

vsPlayer = 1
vsAI_easy = 2
vsAI_hard = 3
home = True
win = 0
showboard = False
running = True


gameState = {
    'board': [[None, None, None], [None, None, None], [None, None, None]],
    'remain': 9,
    'score': {'x': 0, 'y': 0, 'tie': 0},
    'mode': 1,
    'currentPlayer': 'X'
}

# def returnHome():
#     global home
#     home = True

def textObject(text, font, color):
    text = font.render(text, True, color)
    return text, text.get_rect()

def winningAnimations():
    s = pygame.Surface((500,500))  # the size of your rect
    s = pygame.transform.scale(BI,(500,500))
    s.set_alpha(230)                # alpha level
    s.fill(BLACK)           # this fills the entire surface
    if win == 1:
        screen.blit(s, (50,100))
    if algorithm.wins(gameState["board"], 'X'):
        textWin, textWR = textObject("X wins!", font_gamename, C3a6186)
    elif algorithm.wins(gameState["board"], 'O'):
        textWin, textWR = textObject("O wins!", font_gamename, C89253e)
    else:
        textWin, textWR = textObject("Tie!", font_gamename, BLACK)
    textWR.center = (300, 300)
    screen.blit(textWin, textWR)
    drawAButton1(screen, 100, 450, 170, 50, "Next game", C3a6186, C89253e, lambda: startGame(gameState["mode"]))
    drawAButton1(screen, 300, 450, 170, 50, "Return", C3a6186, C89253e, lambda: showHome())
    global showboard
    showboard = False

    pygame.display.flip()
    pygame.time.delay(50)

def switchPlayer():
    global gameState
    gameState["currentPlayer"] = "X" if gameState["currentPlayer"] == "O" else "O"

def makeMove(x, y):
    if gameState["currentPlayer"] == "X":
        board_surface.blit(text_x, (x * 170 + 40, y * 170 - 20))
        gameState['board'][x][y] = "X"
    else:
        board_surface.blit(text_o, (x * 170 + 40, y * 170 - 20))
        gameState['board'][x][y] = "O"
    switchPlayer()
    gameState["remain"] -= 1
    if algorithm.wins(gameState["board"], 'X'):
        gameState["score"]['x'] += 1
    elif algorithm.wins(gameState["board"], 'O'):
        gameState["score"]['y'] += 1
    elif gameState["remain"] == 0:
        gameState["score"]['tie'] += 1
    drawBoard()

def makeAIMove():
    if gameState["mode"] == vsAI_hard:
        AIsMove = algorithm.minimax(gameState["board"], gameState["remain"], 1, -99999, 99999)
        makeMove(AIsMove[1], AIsMove[2])
    elif gameState["mode"] == vsAI_easy:
        AIsMove = algorithm.CMove(gameState["board"])
        makeMove(AIsMove[0], AIsMove[1])
    

def checkMove():
    mouse_x, mouse_y =pygame.mouse.get_pos()
    mouse_x = (mouse_x - 45) // 175
    mouse_y = (mouse_y - 145) // 175

    if 0 <= mouse_x <= 2 and 0 <= mouse_y <= 2 and gameState['board'][mouse_x][mouse_y] is None:
        makeMove(mouse_x, mouse_y)
    else:
        return

def reset():
    global gameState, board_surface, board_bg

    gameState["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    # gameState["score"] = {'x': 0, 'y': 0, 'tie': 0}
    gameState["remain"] = 9
    gameState["currentPlayer"] = 'X'

    board_surface = pygame.Surface((510, 510))
    board_bg = pygame.Surface((510, 510))
    board_bg.set_alpha(50)
    board_bg.fill(BLACK)
    board_surface.fill(BACKGROUND)
    # pygame.draw.rect(board_surface, BLACK, (0, 0, 510, 510), 2)
    pygame.draw.line(board_surface, BLACK, (170, 5), (170, 505), 2)
    pygame.draw.line(board_surface, BLACK, (340, 5), (340, 505), 2)
    pygame.draw.line(board_surface, BLACK, (5, 170), (505, 170), 2)
    pygame.draw.line(board_surface, BLACK, (5, 340), (505, 340), 2)

def startGame(gm):
    global gameState, home, win
    win = 0
    gameState["mode"] = gm
    home = False
    reset()
    # pygame.time.delay(50)
    drawBoard()


def drawAButton(surface, x, y, w, h, text, active_color, inactive_color, funct):
    button = pygame.Rect(x, y, w, h)

    # pygame.draw.rect(screen, WIN_COLOR, (x, y, w, h))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button.collidepoint(mouse):
        pygame.draw.rect(surface, active_color, (x + 1, y + 1, w - 2, h - 2))
        if text is not None:
            lable, text_r = textObject(text, font_normal, WHITE)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)
        if click[0] == 1 and funct is not None:
            pygame.time.delay(200)
            funct()
    else:
        pygame.draw.rect(surface, active_color, (x + 1, y + 1, w - 2, h - 2), 2, 0)
        if text is not None:
            lable, text_r = textObject(text, font_normal, BLACK)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)

def drawAButton1(surface, x, y, w, h, text, active_color, inactive_color, funct):
    button = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, active_color, (x, y, w, h))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button.collidepoint(mouse):
        pygame.draw.rect(surface, active_color, (x + 2, y + 2, w - 4, h - 4))
        if text is not None:
            lable, text_r = textObject(text, font_normal, WHITE)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)
        if click[0] == 1 and funct is not None:
            pygame.time.delay(200)
            funct()
    else:
        pygame.draw.rect(surface, inactive_color, (x + 1, y + 1, w - 2, h - 2))
        if text is not None:
            lable, text_r = textObject(text, font_normal, WHITE)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)

def drawAButton2(surface, x, y, w, h, text, active_color, inactive_color, bg_color, funct):
    button = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, bg_color, (x, y, w, h))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if button.collidepoint(mouse):
        # pygame.draw.rect(surface, active_color, (x + 2, y + 2, w - 4, h - 4))
        if text is not None:
            lable, text_r = textObject(text, font_normal, active_color)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)
        if click[0] == 1 and funct is not None:
            pygame.time.delay(200)
            funct()
    else:
        # pygame.draw.rect(surface, inactive_color, (x + 1, y + 1, w - 2, h - 2))
        if text is not None:
            lable, text_r = textObject(text, font_normal,inactive_color)
            text_r.center = (x + w/2, y + h/2)
            screen.blit(lable, text_r)

def quitGame():
    global running
    running = False

def continueGame():
    global home
    home = False
    if win != 0:
        startGame(gameState["mode"])

def showHome():
    global home
    home = True

def drawHome():
    screen.fill(HOME_BG)
    screen.blit(BG_IMG, (0, 0))
    text_tictactoe, text_r = textObject("Tic-Tac-Toe", font_gamename, BLACK)
    text_r.center = (300, 300)

    screen.blit(text_tictactoe, text_r)

    drawAButton(screen, 22, 400, 170, 50, "VS Player", BLACK, WHITE, lambda: startGame(vsPlayer))
    drawAButton(screen, 214, 400, 170, 50, "VS AI - Easy", BLACK, WHITE, lambda: startGame(vsAI_easy))
    drawAButton(screen, 406, 400, 170, 50, "VS AI - Hard", BLACK, WHITE,lambda: startGame(vsAI_hard))
    yQuit = 0
    if gameState["score"]["x"] > 0 or gameState["score"]["y"] > 0 or gameState["score"]["tie"] > 0 or gameState["remain"] < 9:
        drawAButton(screen, 214, 500, 170, 50, "Continue", BLACK, WHITE, lambda: continueGame())
        yQuit = 1
    drawAButton(screen, 214, yQuit * 70 + 500, 170, 50, "Quit", BLACK, WHITE, lambda: quitGame())
    pygame.display.flip()

def drawBoard():
    screen.fill(BACKGROUND)
    
    text_score = font_score.render("PlayerX: %d    PlayerO: %d    Tie: %d" % (gameState['score']['x'], gameState['score']['y'], gameState['score']['tie']), True, BLACK)
    turn = font_turning_lable.render("%s's turn!" % (gameState["currentPlayer"]), True, X_COLOR)
    screen.blit(text_score, (5, 15))
    pygame.draw.line(screen, BLACK, (0, 45), (360, 45), 1)
    screen.blit(turn, (210, 70))

    drawAButton2(screen, 500, 10, 100, 50, "Home", C3a6186, C89253e, BACKGROUND, lambda: showHome())

    screen.blit(board_bg, (45, 145))
    screen.blit(board_surface, (45, 145))

    text_x, text_rx = textObject("X", font_moving, BLACK)
    text_o, text_ro = textObject("O", font_moving, BLACK)

    pygame.display.flip()

clock = pygame.time.Clock()

def main():
    global win, showboard, running

    while running:
        # clock.tick(30)

        if algorithm.finished(gameState["board"]) or gameState["remain"] == 0:
            if win == 1:
                win = 2
            elif win == 0:
                win = 1

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and home == False:
                if gameState["remain"] != 0 and algorithm.finished(gameState["board"]) == False:
                    checkMove()

        if (gameState["mode"] > vsPlayer) and gameState["currentPlayer"] == "O" and gameState["remain"] != 0 and algorithm.finished(gameState["board"]) == False:
            makeAIMove()
            
        if home:
            drawHome()
        elif win > 0:
            winningAnimations()
        else:
            drawBoard()

    pygame.quit()

if __name__ == "__main__":
    main()
