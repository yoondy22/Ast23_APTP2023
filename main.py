import pygame
import copy


pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = [680, 680]  # 게임창 크기 [w, h]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Yoon's Omok")  # 게임창 이름

done = False
stone_board = [[0 for j in range(15)] for i in range(15)]  # 오목판 15*15 배열, 0=돌없음, 1=흑돌, 2=백돌
board_stack = [copy.deepcopy(stone_board)]
grid_size = 40  # 격자 한 칸의 가로세로 픽셀
stone_size = 17  # 돌의 반지름
order = 0  # 현재까지 놓인 돌의 개수
winner = 0  # 1=흑, 2=백
game_end = False

grid_origin_x = 60
grid_origin_y = 60


def check_omok(x, y):
    target_stone = stone_board[y][x]

    horizontal, vertical, upward_diagonal, downward_diagonal = 0, 0, 0, 0

    ## 가로 탐색
    # 좌방 탐색
    for i in range(1, 5):
        if x - i < 0 or stone_board[y][x - i] != target_stone:
            break
        horizontal += 1
    # 우방 탐색
    for i in range(1, 5):
        if x + i > 14 or stone_board[y][x + i] != target_stone:
            break
        horizontal += 1
    if horizontal >= 4:
        return target_stone

    ## 세로 탐색
    # 상방 탐색
    for i in range(1, 5):
        if y - i < 0 or stone_board[y - i][x] != target_stone:
            break
        vertical += 1
    # 하방 탐색
    for i in range(1, 5):
        if y + i > 14 or stone_board[y + i][x] != target_stone:
            break
        vertical += 1
    if vertical >= 4:
        return target_stone

    ## 우상향 대각선 탐색
    # 좌하방 탐색
    for i in range(1, 5):
        if x - i < 0 or y + i > 14 or stone_board[y + i][x - i] != target_stone:
            break
        upward_diagonal += 1
    # 우상방 탐색
    for i in range(1, 5):
        if x + i > 14 or y - i < 0 or stone_board[y - i][x + i] != target_stone:
            break
        upward_diagonal += 1
    if upward_diagonal >= 4:
        return target_stone

    ## 우하향 대각선 탐색
    # 좌상방 탐색
    for i in range(1, 5):
        if x - i < 0 or y - i < 0 or stone_board[y - i][x - i] != target_stone:
            break
        downward_diagonal += 1
    # 우하방 탐색
    for i in range(1, 5):
        if x + i > 14 or y + i > 14 or stone_board[y + i][x + i] != target_stone:
            break
        downward_diagonal += 1
    if downward_diagonal >= 4:
        return target_stone

    return 0


def put_black(x, y):  # 검은돌 착수
    global order

    if stone_board[y][x]:  # 돌이 이미 존재하면
        return  # 착수 불가

    stone_board[y][x] = 1
    order += 1
    board_stack.append(copy.deepcopy(stone_board))


def put_white(x, y):
    global order

    if stone_board[y][x]:
        return

    stone_board[y][x] = 2
    order += 1
    board_stack.append(copy.deepcopy(stone_board))


def draw_board():
    global game_end

    screen.fill(WHITE)  # Background color
    pygame.time.Clock().tick(60)  # FPS

    pygame.draw.rect(screen, (247, 201, 122), [20, 20, 640, 640], 0)  # 오목판

    # 격자
    for i in range(14):
        for j in range(14):
            pygame.draw.rect(screen, BLACK,
                             [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j, grid_size, grid_size], 1)
    pygame.draw.rect(screen, BLACK, [59, 59, 562, 562], 1)

    for i in range(15):
        for j in range(15):
            if stone_board[j][i] == 1:
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
            if stone_board[j][i] == 2:
                pygame.draw.circle(screen, WHITE, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 0)
                pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j], stone_size, 1)

    if winner == 1:
        font = pygame.font.SysFont("arial", 50, True, False)
        winning_text = font.render("BLACK WIN!", True, RED)
        screen.blit(winning_text, (190, 310))
        game_end = True

    if winner == 2:
        font = pygame.font.SysFont("arial", 50, True, False)
        winning_text = font.render("WHITE WIN!", True, RED)
        screen.blit(winning_text, (200, 310))
        game_end = True


if __name__ == "__main__":
    while not done:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼 누르면 게임창 종료
                done = True
            elif not game_end and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 클릭 & 좌클릭
                mouse_pos = pygame.mouse.get_pos()
                if 40 <= mouse_pos[0] <= 639 and 40 <= mouse_pos[1] <= 639:
                    x, y = (mouse_pos[0]-40)//40, (mouse_pos[1]-40)//40
                    if order % 2:
                        put_white(x, y)
                    else:
                        put_black(x, y)
                    winner = check_omok(x, y)

        pygame.display.flip()

    pygame.quit()
