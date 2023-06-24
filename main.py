import pygame
import copy


pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = [680 + 200, 680]  # 게임창 크기 [w, h]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Yoon's Omok")  # 게임창 이름

stone_board = [[0 for j in range(15)] for i in range(15)]  # 오목판 15*15 배열, 0=돌없음, 1=흑돌, 2=백돌
board_stack = [copy.deepcopy(stone_board)]
grid_size = 40  # 격자 한 칸의 가로세로 픽셀
stone_size = 17  # 돌의 반지름
order = 0  # 현재까지 놓인 돌의 개수
full_order = 0
winner = 0  # 1=흑, 2=백
game_end = False
x, y = -1, -1
grid_origin_x, grid_origin_y = 60, 60


def start_screen():
    done = False

    screen.fill((255, 242, 214))

    title_font = pygame.font.SysFont("arial", 50, True, True)  # 제목 폰트

    title_text = title_font.render("GO", True, BLACK)
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (440, 100)  # 제목 위치
    screen.blit(title_text, title_text_rect)

    menu_font = pygame.font.SysFont("arial", 35, True, True)  # 1player, 2player, quit 폰트

    pygame.draw.rect(screen, BLACK, [310, 200, 260, 70], 0)  # 1player black
    player1_text = menu_font.render("1 player", True, WHITE)
    player1_text_rect = player1_text.get_rect()
    player1_text_rect.center = (440, 235)
    screen.blit(player1_text, player1_text_rect)

    pygame.draw.rect(screen, WHITE, [310, 300, 260, 70], 0)  # 1player white
    player1_text = menu_font.render("1 player", True, BLACK)
    player1_text_rect = player1_text.get_rect()
    player1_text_rect.center = (440, 335)
    screen.blit(player1_text, player1_text_rect)

    pygame.draw.rect(screen, (150, 150, 150), [310, 400, 260, 70], 0)  # 2player
    player2_text = menu_font.render("2 player", True, WHITE)
    player2_text_rect = player2_text.get_rect()
    player2_text_rect.center = (440, 435)
    screen.blit(player2_text, player2_text_rect)

    pygame.draw.rect(screen, BLACK, [360, 550, 160, 70], 3)  # quit
    quit_text = menu_font.render("Q U I T", True, BLACK)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = (440, 585)
    screen.blit(quit_text, quit_text_rect)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if 310 <= mouse_pos[0] <= 569 and 400 <= mouse_pos[1] <= 469:  # 2 player
                    player2_mode()
                    return

                if 360 <= mouse_pos[0] <= 519 and 550 <= mouse_pos[1] <= 619:  # quit
                    done = True

        pygame.display.flip()

    pygame.quit()
    quit()


def player2_mode():
    global order, full_order
    global winner
    global game_end
    global x, y

    done = False

    while not done:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼 누르면 게임창 종료
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 클릭 & 좌클릭
                mouse_pos = pygame.mouse.get_pos()

                if not game_end and 40 <= mouse_pos[0] <= 639 and 40 <= mouse_pos[1] <= 639:
                    x, y = (mouse_pos[0] - 40) // 40, (mouse_pos[1] - 40) // 40
                    if order % 2:
                        put_white(x, y)
                    else:
                        put_black(x, y)
                    winner = is_five(x, y)

                elif 700 <= mouse_pos[0] <= 769 and 410 <= mouse_pos[1] <= 479:
                    undo()

                elif 790 <= mouse_pos[0] <= 859 and 410 <= mouse_pos[1] <= 479:
                    redo()
                    winner = is_five(x, y)

                elif 700 <= mouse_pos[0] <= 769 and 500 <= mouse_pos[1] <= 569:
                    undo_all()

                elif 790 <= mouse_pos[0] <= 859 and 500 <= mouse_pos[1] <= 569:
                    redo_all()
                    winner = is_five(x, y)

                elif 700 <= mouse_pos[0] <= 859 and 590 <= mouse_pos[1] <= 659:
                    for i in range(full_order):
                        board_stack.pop()
                    order, full_order = 0, 0
                    winner = 0
                    game_end = False
                    start_screen()

        pygame.display.flip()

    pygame.quit()
    quit()


def draw_board():
    global game_end

    screen.fill(WHITE)  # Background color
    pygame.time.Clock().tick(60)  # FPS

    pygame.draw.rect(screen, (247, 201, 122), [20, 20, 640, 640], 0)  # 좌측 오목판
    pygame.draw.rect(screen, (221, 221, 221), [680, 0, 200, 680], 0)  # 우측 메뉴판

    # 격자
    for i in range(14):
        for j in range(14):
            pygame.draw.rect(screen, BLACK,
                             [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j, grid_size, grid_size], 1)
    pygame.draw.rect(screen, BLACK, [59, 59, 562, 562], 1)

    dot_size = 5
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 3, grid_origin_y + grid_size * 3], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 3, grid_origin_y + grid_size * 11], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 7, grid_origin_y + grid_size * 7], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 11, grid_origin_y + grid_size * 3], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 11, grid_origin_y + grid_size * 11], dot_size, 0)

    for i in range(15):
        for j in range(15):
            if board_stack[order][j][i] == 1:
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
            if board_stack[order][j][i] == 2:
                pygame.draw.circle(screen, WHITE, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 1)

    sequence_control_font = pygame.font.SysFont("arial", 15, True, False)

    pygame.draw.rect(screen, (190, 255, 190), [700, 410, 70, 70], 0)
    undo_text = sequence_control_font.render("Undo", True, BLACK)
    undo_text_rect = undo_text.get_rect()
    undo_text_rect.center = (735, 445)
    screen.blit(undo_text, undo_text_rect)

    pygame.draw.rect(screen, (190, 255, 190), [790, 410, 70, 70], 0)
    redo_text = sequence_control_font.render("Redo", True, BLACK)
    redo_text_rect = redo_text.get_rect()
    redo_text_rect.center = (825, 445)
    screen.blit(redo_text, redo_text_rect)

    pygame.draw.rect(screen, (190, 255, 190), [700, 500, 70, 70], 0)
    undo_all_text = sequence_control_font.render("Undo All", True, BLACK)
    undo_all_text_rect = undo_all_text.get_rect()
    undo_all_text_rect.center = (735, 535)
    screen.blit(undo_all_text, undo_all_text_rect)

    pygame.draw.rect(screen, (190, 255, 190), [790, 500, 70, 70], 0)
    redo_all_text = sequence_control_font.render("Redo All", True, BLACK)
    redo_all_text_rect = redo_all_text.get_rect()
    redo_all_text_rect.center = (825, 535)
    screen.blit(redo_all_text, redo_all_text_rect)

    quit_font = pygame.font.SysFont("arial", 30, True, False)

    pygame.draw.rect(screen, WHITE, [700, 590, 160, 70], 0)
    pygame.draw.rect(screen, BLACK, [700, 590, 160, 70], 3)
    home_text = quit_font.render("H O M E", True, BLACK)
    home_text_rect = home_text.get_rect()
    home_text_rect.center = (780, 625)
    screen.blit(home_text, home_text_rect)

    if winner:
        font = pygame.font.SysFont("arial", 50, True, False)
        if winner == 1:
            winning_text = font.render("BLACK WIN!", True, RED)
        else:
            winning_text = font.render("WHITE WIN!", True, RED)
        winning_text_rect = winning_text.get_rect()
        winning_text_rect.center = (340, 340)
        screen.blit(winning_text, winning_text_rect)
        game_end = True


def put_black(x, y):  # 검은돌 착수
    global stone_board
    global order
    global full_order

    stone_board = copy.deepcopy(board_stack[order])

    if stone_board[y][x]:  # 돌이 이미 존재하면
        return  # 착수 불가

    put_stone_sound = pygame.mixer.Sound("put_stone.mp3")
    put_stone_sound.play()

    stone_board[y][x] = 1

    for i in range(full_order - order):
        board_stack.pop()

    order += 1
    full_order = order
    board_stack.append(copy.deepcopy(stone_board))


def put_white(x, y):
    global stone_board
    global order
    global full_order

    stone_board = copy.deepcopy(board_stack[order])

    if stone_board[y][x]:
        return

    put_stone_sound = pygame.mixer.Sound("put_stone.mp3")
    put_stone_sound.play()

    stone_board[y][x] = 2

    for i in range(full_order - order):
        board_stack.pop()

    order += 1
    full_order = order
    board_stack.append(copy.deepcopy(stone_board))


def is_five(x, y):
    for i in range(4):  # 4방향 탐색
        stone_cnt = 1

        for j in range(-1, 2, 2):  # 방향별 양쪽 탐색
            cur_x, cur_y = x, y

            for k in range(4):  # 최대 4칸 이동
                cur_x += [-1, -1, 0, 1][i] * j
                cur_y += [0, -1, -1, -1][i] * j

                if cur_x < 0 or cur_x > 14 or cur_y < 0 or cur_y > 14:
                    break
                if board_stack[order][cur_y][cur_x] != board_stack[order][y][x]:
                    break

                stone_cnt += 1

        if stone_cnt >= 5:
            return board_stack[order][y][x]

    return 0


def undo():
    global order
    global winner
    global game_end
    if order > 0:
        order -= 1
    winner = 0
    game_end = 0


def redo():
    global order
    if order < full_order:
        order += 1


def undo_all():
    global order
    global winner
    global game_end
    order = 0
    winner = 0
    game_end = 0


def redo_all():
    global order
    order = full_order


if __name__ == "__main__":
    start_screen()
