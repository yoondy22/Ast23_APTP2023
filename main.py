import pygame
import copy


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen_size = [680 + 200, 680]  # 게임창 크기 [w, h]
grid_size = 40  # 격자 한 칸의 가로세로 픽셀
stone_size = 17  # 돌의 반지름
grid_origin_x, grid_origin_y = 60, 60
max_depth = 3
max_width = 3


board_stack = [[[0 for j in range(15)] for i in range(15)]]  # 오목판 15*15 배열, 0=무돌, 1=흑돌, 2=백돌, -1=금수
full_order = 0  # 최대로 놓인 돌의 개수
order = 0  # 현재까지 놓인 돌의 개수
winner = 0  # 1=흑, 2=백
game_end = False  # 승리 여부


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Yoon's Omok")  # 게임창 이름
pygame.time.Clock().tick(60)  # FPS


def start_screen():
    done = False

    screen.fill((255, 242, 214))  # Background color

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
            if event.type == pygame.QUIT:  # 닫기 버튼 누르면 게임창 종료
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 클릭 & 좌클릭
                mouse_pos = pygame.mouse.get_pos()

                if 310 <= mouse_pos[0] <= 569 and 200 <= mouse_pos[1] <= 269:  # 1player black
                    game_start(1)
                    return

                if 310 <= mouse_pos[0] <= 569 and 300 <= mouse_pos[1] <= 369:  # 1player white
                    game_start(2)
                    return

                if 310 <= mouse_pos[0] <= 569 and 400 <= mouse_pos[1] <= 469:  # 2 player
                    game_start(0)
                    return

                if 360 <= mouse_pos[0] <= 519 and 550 <= mouse_pos[1] <= 619:  # quit
                    done = True

        pygame.display.flip()

    pygame.quit()
    quit()


def game_start(mode):
    global full_order
    global order
    global winner
    global game_end

    done = False

    while not done:
        if order % 2 == 0 and not winner:
            check_forbidden_point(board_stack[order], order % 2 + 1)  # 흑 차례일 때 금수 판별
        else:
            reset_forbidden_point(board_stack[order])

        draw_board()  # 격자, 돌, WIN

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼 누르면 게임창 종료
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 클릭 & 좌클릭
                mouse_pos = pygame.mouse.get_pos()

                if not game_end and 40 <= mouse_pos[0] <= 639 and 40 <= mouse_pos[1] <= 639:  # 오목판
                    x, y = (mouse_pos[0] - 40) // 40, (mouse_pos[1] - 40) // 40
                    if mode == 0:
                        put_stone(order % 2 + 1, x, y)
                    else:
                        if mode == 2 and order == 0:
                            put_stone(1, 7, 7)
                        else:
                            if order % 2 == mode - 1:
                                put_stone(order % 2 + 1, x, y)
                            else:
                                x, y = AI(board_stack)
                    winner = is_omok(board_stack[order], board_stack[order][y][x], x, y)

                elif 700 <= mouse_pos[0] <= 769 and 410 <= mouse_pos[1] <= 479:  # undo
                    undo()

                elif 790 <= mouse_pos[0] <= 859 and 410 <= mouse_pos[1] <= 479:  # redo
                    redo()
                    if order > 0:
                        winner = is_omok(board_stack[order], board_stack[order][y][x], x, y)

                elif 700 <= mouse_pos[0] <= 769 and 500 <= mouse_pos[1] <= 569:  # undo all
                    undo_all()

                elif 790 <= mouse_pos[0] <= 859 and 500 <= mouse_pos[1] <= 569:  # redo all
                    redo_all()
                    if order > 0:
                        winner = is_omok(board_stack[order], board_stack[order][y][x], x, y)

                elif 700 <= mouse_pos[0] <= 859 and 590 <= mouse_pos[1] <= 659:  # home
                    for i in range(full_order):
                        board_stack.pop()
                    order, full_order, winner = 0, 0, 0
                    game_end = False

                    start_screen()

        pygame.display.flip()

    pygame.quit()
    quit()


def draw_board():
    global game_end

    screen.fill(WHITE)  # Background color

    pygame.draw.rect(screen, (247, 201, 122), [20, 20, 640, 640], 0)  # 좌측 오목판
    pygame.draw.rect(screen, (221, 221, 221), [680, 0, 200, 680], 0)  # 우측 메뉴판

    # 격자
    for i in range(14):
        for j in range(14):
            pygame.draw.rect(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j, grid_size, grid_size], 1)
    pygame.draw.rect(screen, BLACK, [59, 59, 562, 562], 1)

    # 중간점
    dot_size = 5
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 3, grid_origin_y + grid_size * 3], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 3, grid_origin_y + grid_size * 11], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 7, grid_origin_y + grid_size * 7], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 11, grid_origin_y + grid_size * 3], dot_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * 11, grid_origin_y + grid_size * 11], dot_size, 0)

    # 돌, 금수
    for i in range(15):
        for j in range(15):
            if board_stack[order][j][i] == 1:
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
            if board_stack[order][j][i] == 2:
                pygame.draw.circle(screen, WHITE, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 1)
            if order % 2 == 0 and board_stack[order][j][i] == -1:
                pygame.draw.circle(screen, RED, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], 6, 0)

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

    if order % 2 == 0:
        pygame.draw.circle(screen, BLACK, [730, 50], stone_size, 0)
    else:
        pygame.draw.circle(screen, WHITE, [730, 50], stone_size, 0)
        pygame.draw.circle(screen, BLACK, [730, 50], stone_size, 1)

    if winner:
        font = pygame.font.SysFont("arial", 30, True, False)
        winning_text = font.render("WIN!", True, RED)
        winning_text_rect = winning_text.get_rect()
        winning_text_rect.center = (805, 50)
        screen.blit(winning_text, winning_text_rect)
        game_end = True


def put_stone(stone_color, x, y):  # 검은돌 착수
    global order
    global full_order

    stone_board = copy.deepcopy(board_stack[order])

    if stone_board[y][x]:  # 돌이 이미 존재하면
        return  # 착수 불가

    put_stone_sound = pygame.mixer.Sound("put_stone.mp3")
    put_stone_sound.play()

    for i in range(full_order - order):
        board_stack.pop()

    order += 1
    full_order = order

    stone_board[y][x] = stone_color  # 착수
    board_stack.append(copy.deepcopy(stone_board))


def is_omok(stone_board, stone_color, x, y):
    for direction in range(4):  # 4방향 탐색
        stone_cnt = 1

        for side in [-1, 1]:  # 2방향 탐색
            cur_x = x + get_move(direction)[0] * side
            cur_y = y + get_move(direction)[1] * side

            while 0 <= cur_x < 15 and 0 <= cur_y < 15 and stone_board[cur_y][cur_x] == stone_color:
                stone_cnt += 1
                cur_x += get_move(direction)[0] * side
                cur_y += get_move(direction)[1] * side

        if stone_cnt >= 5:
            return stone_board[y][x]

    return False


def check_forbidden_point(stone_board, stone_color):
    for i in range(15):
        for j in range(15):
            if stone_board[j][i] == 0 and is_forbidden_point(copy.deepcopy(stone_board), stone_color, i, j):
                stone_board[j][i] = -1


def is_forbidden_point(stone_board, stone_color, x, y):
    if stone_color == 1:
        reset_forbidden_point(stone_board)

    # 오목을 위한 금수는 거짓 금수
    for direction in range(4):
        if is_five(stone_board, stone_color, x, y, direction):
            return False

    # 33, 44, 6목
    if is_double_three(stone_board, stone_color, x, y) or is_double_four(stone_board, stone_color, x, y) or is_six(stone_board, stone_color, x, y):
        return True

    return False


def is_double_three(stone_board, stone_color, x, y):
    double_three_cnt = 0

    stone_board[y][x] = 1

    for direction in range(4):
        if is_open_three(stone_board, stone_color, x, y, direction):
            double_three_cnt += 1

    stone_board[y][x] = 0

    if double_three_cnt >= 2:
        return True

    return False


def is_double_four(stone_board, stone_color, x, y):
    double_four_cnt = 0

    stone_board[y][x] = 1

    for direction in range(4):
        if count_open_four(stone_board, stone_color, x, y, direction) == 2:
            double_four_cnt += 2
        elif is_four(stone_board, stone_color, x, y, direction):
            double_four_cnt += 1

    stone_board[y][x] = 0

    if double_four_cnt >= 2:
        return True

    return False


def is_six(stone_board, stone_color, x, y):
    for direction in range(4):
        if count_stone(stone_board, stone_color, x, y, direction) > 5:
            return True

    return False


def is_open_three(stone_board, stone_color, x, y, direction):
    for side in [-1, 1]:
        empty_xy = find_empty_point(stone_board, stone_color, x, y, direction, side)
        if empty_xy:
            stone_board[empty_xy[1]][empty_xy[0]] = stone_color

            if count_open_four(stone_board, stone_color, empty_xy[0], empty_xy[1], direction) == 1:
                if stone_color == 1 and not is_forbidden_point(copy.deepcopy(stone_board), stone_color, empty_xy[0], empty_xy[1]):
                    stone_board[empty_xy[1]][empty_xy[0]] = 0
                    return True
                if stone_color == 2:
                    stone_board[empty_xy[1]][empty_xy[0]] = 0
                    return True

            stone_board[empty_xy[1]][empty_xy[0]] = 0

    return False


def count_open_four(stone_board, stone_color, x, y, direction):
    open_four_cnt = 0

    for direction_ in range(4):
        if is_five(stone_board, stone_color, x, y, direction_):
            return open_four_cnt

    for side in [-1, 1]:
        empty_xy = find_empty_point(stone_board, stone_color, x, y, direction, side)
        if empty_xy:
            if is_five(stone_board, stone_color, empty_xy[0], empty_xy[1], direction):
                open_four_cnt += 1

    if open_four_cnt == 2:
        if count_stone(stone_board, stone_color, x, y, direction) == 4:
            open_four_cnt = 1
    else:
        open_four_cnt = 0

    return open_four_cnt


def is_four(stone_board, stone_color, x, y, direction):
    for side in [-1, 1]:
        empty_xy = find_empty_point(stone_board, stone_color, x, y, direction, side)
        if empty_xy:
            if is_five(stone_board, stone_color, empty_xy[0], empty_xy[1], direction):
                return True

    return False


def is_five(stone_board, stone_color, x, y, direction):
    if count_stone(stone_board, stone_color, x, y, direction) == 5:
        return True

    return False


def count_stone(stone_board, stone_color, x, y, direction):
    stone_cnt = 1

    for side in [-1, 1]:
        cur_x = x + get_move(direction)[0] * side
        cur_y = y + get_move(direction)[1] * side

        while 0 <= cur_x < 15 and 0 <= cur_y < 15 and stone_board[cur_y][cur_x] == stone_color:
            stone_cnt += 1
            cur_x += get_move(direction)[0] * side
            cur_y += get_move(direction)[1] * side

    return stone_cnt


def find_empty_point(stone_board, stone_color, x, y, direction, side):
    cur_x = x + get_move(direction)[0] * side
    cur_y = y + get_move(direction)[1] * side

    while 0 <= cur_x < 15 and 0 <= cur_y < 15 and stone_board[cur_y][cur_x] == stone_color:
        cur_x += get_move(direction)[0] * side
        cur_y += get_move(direction)[1] * side

    if 0 <= cur_x < 15 and 0 <= cur_y < 15 and stone_board[cur_y][cur_x] == 0:
        return cur_x, cur_y

    return None


def reset_forbidden_point(stone_board):
    for i in range(15):
        for j in range(15):
            if stone_board[j][i] == -1:
                stone_board[j][i] = 0


def get_move(direction):
    return [-1, -1, 0, 1][direction], [0, -1, -1, -1][direction]


def undo():
    global order
    global winner
    global game_end

    if order > 0:
        order -= 1
    winner = 0
    game_end = False


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
    game_end = False


def redo_all():
    global order

    order = full_order


def AI(board_stack):
    global order
    global full_order

    depth = 0
    coord = dfs(copy.deepcopy(board_stack[order]), depth + 1)
    stone_board = copy.deepcopy(board_stack[order])
    stone_board[coord[1]][coord[0]] = order % 2 + 1
    board_stack.append(stone_board)
    order += 1
    full_order = order

    return coord[0], coord[1]


def dfs(stone_board, depth):
    weighted_board = [stone_board]
    weighted_board.append(copy.deepcopy(stone_board))

    for i in range(15):
        for j in range(15):
            weighted_board[1][j][i] = 0

    if (order + depth) % 2 == 0:
        check_forbidden_point(weighted_board[0], 1)
    else:
        reset_forbidden_point(weighted_board[0])

    for i in range(15):
        for j in range(15):
            for k in [1, 2]:
                if weighted_board[0][j][i] == 0:
                    weighted_board[0][j][i] = (order + depth + k) % 2 + 1

                    five_cnt = 0
                    for direction in range(4):
                        if is_five(copy.deepcopy(weighted_board[0]), weighted_board[0][j][i], i, j, direction):
                            five_cnt += 1
                    weighted_board[1][j][i] += (-k/2 + 2) * 1000 * five_cnt
                    if five_cnt:
                        weighted_board[0][j][i] = 0
                        continue

                    open_four_cnt = 0
                    for direction in range(4):
                        open_four_cnt += count_open_four(copy.deepcopy(weighted_board[0]), weighted_board[0][j][i], i, j, direction)
                    weighted_board[1][j][i] += (-k/2 + 2) * 300 * open_four_cnt * open_four_cnt

                    open_three_cnt = 0
                    for direction in range(4):
                        open_three_cnt += is_open_three(copy.deepcopy(weighted_board[0]), weighted_board[0][j][i], i, j, direction)
                    weighted_board[1][j][i] += (k/2 + 0.5) * 200 * open_three_cnt * open_three_cnt

                    four_cnt = 0
                    for direction in range(4):
                        four_cnt += is_four(copy.deepcopy(weighted_board[0]), weighted_board[0][j][i], i, j, direction)
                    weighted_board[1][j][i] += 250 * four_cnt

                    two_cnt = 0
                    for direction in range(4):
                        if 2 <= count_stone(copy.deepcopy(weighted_board[0]), weighted_board[0][j][i], i, j, direction) <= 3:
                            two_cnt += 1
                    weighted_board[1][j][i] += 60 * two_cnt

                    weighted_board[0][j][i] = 0

    max_list = [-1 for i in range(max_width)]
    max_xy_list = [(-1, -1) for i in range(max_width)]
    for k in range(max_width):
        max = -1
        for i in range(15):
            for j in range(15):
                if max < weighted_board[1][j][i]:
                    max = weighted_board[1][j][i]
                    max_list[k] = max
                    max_xy_list[k] = (i, j)
                    weighted_board[1][j][i] = 0

        if depth == max_depth:
            return max

        max_list[k] += (-1) * dfs(copy.deepcopy(weighted_board[0]), depth + 1)

    if depth == 1:
        max = max_idx = -1
        for i in range(max_width):
            if max < max_list[i]:
                max = max_list[i]
                max_idx = i
        return max_xy_list[max_idx]
    else:
        return sum(max_list) / max_width


if __name__ == "__main__":
    start_screen()

