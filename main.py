import pygame


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
stone_board = [[0 for j in range(15)] for i in range(15)]  # 오목판 15*15 배열, 0=돌없음, 1=검은돌, 2=흰돌
grid_size = 40  # 격자 한 칸의 가로세로 픽셀
stone_size = 17  # 돌의 반지름
order = 0  # 현재까지 놓인 돌의 개수
game_end = False


def check_omok(x, y):
    target_stone = stone_board[y][x]

    horizontal = 0
    vertical = 0
    upward_diagonal = 0
    downward_diagonal = 0

    ## 가로 탐색
    # 가로 좌방 탐색
    for i in range(1, 5):
        if x - i < 0 or stone_board[y][x - i] != target_stone:
            break
        horizontal += 1
    # 가로 우방 탐색
    for i in range(1, 5):
        if x + i > 14 or stone_board[y][x + i] != target_stone:
            break
        horizontal += 1
    if horizontal >= 4:
        return target_stone

    ## 세로 탐색
    # 세로 상방 탐색
    for i in range(1, 5):
        if y - i < 0 or stone_board[y - i][x] != target_stone:
            break
        vertical += 1
    # 세로 하방 탐색
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
    global game_end

    if stone_board[y][x]:  # 돌이 이미 존재하면
        return  # 착수 불가

    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * x, grid_origin_y + grid_size * y], stone_size, 0)
    stone_board[y][x] = 1
    order += 1

    if check_omok(x, y) == 1:
        font = pygame.font.SysFont("arial", 50, True, False)
        winning_text = font.render("BLACK WIN!", True, RED)
        screen.blit(winning_text, (190, 310))
        game_end = True


def put_white(x, y):
    global order
    global game_end

    if stone_board[y][x]:
        return

    pygame.draw.circle(screen, WHITE, [grid_origin_x + grid_size * x, grid_origin_y + grid_size * y], stone_size, 0)
    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * x, grid_origin_y + grid_size * y], stone_size, 1)
    stone_board[y][x] = 2
    order += 1

    if check_omok(x, y) == 2:
        font = pygame.font.SysFont("arial", 50, True, False)
        winning_text = font.render("WHITE WIN!", True, RED)
        screen.blit(winning_text, (200, 310))
        game_end = True


def start_screen():
    global done

    go_together = 0

    screen.fill(WHITE)

    title_font = pygame.font.SysFont("arial", 50, True, True)  # 제목 폰트
    title = title_font.render("OMOK GAME HAGI", True, BLACK)
    title_rect = title.get_rect()
    title_rect.center = (340,100)  # 제목 위치
    screen.blit(title, title_rect)

    menu_font=pygame.font.SysFont("arial", 35, True, True)  # play sole, together, exit 폰트

    pygame.draw.rect(screen, BLACK, [250, 300, 150, 50], 2)  # play sole
    play_sole = menu_font.render("play sole", True, BLACK)
    sole_rect = play_sole.get_rect()
    sole_rect.center = (320,320)
    screen.blit(play_sole, sole_rect)

    pygame.draw.rect(screen, BLACK, [225, 400, 200, 50], 2)  # play together
    play_together = menu_font.render("play together", True, BLACK)
    together_rect = play_together.get_rect()
    together_rect.center = (323, 420)
    screen.blit(play_together, together_rect)

    pygame.draw.rect(screen, BLACK, [250, 500, 150, 50], 2)  # EXIT
    Nagagi = menu_font.render("EXIT", True, BLACK)
    Nagagi_rect = Nagagi.get_rect()
    Nagagi_rect.center = (320, 525)
    screen.blit(Nagagi, Nagagi_rect)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if 225 <= mouse_pos[0] <= 425 and 400 <= mouse_pos[1] <= 450:  # play together 눌렀을 때
                    go_together = 1
                if 250 <= mouse_pos[0] <= 400 and 500 <= mouse_pos[1] <= 550:  # EXIT 눌렀을 때
                    done = True
        if go_together:  # 다음 화면으로 넘어가기
            break
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()

    screen.fill(WHITE)  # Background color
    pygame.time.Clock().tick(10)  # FPS

    pygame.draw.rect(screen, (247, 201, 122), [20, 20, 640, 640], 0)  # 오목판

    # 격자
    grid_origin_x = 60
    grid_origin_y = 60
    for i in range(14):
        for j in range(14):
            pygame.draw.rect(screen, BLACK,
                             [grid_origin_x + grid_size * i, grid_origin_y + grid_size * j, grid_size, grid_size], 1)
    pygame.draw.rect(screen, BLACK, [59, 59, 562, 562], 1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼 누르면 게임창 종료
                done = True
            elif not game_end and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 마우스 클릭 & 좌클릭
                mouse_pos = pygame.mouse.get_pos()
                if 40 <= mouse_pos[0] <= 639 and 40 <= mouse_pos[1] <= 639:
                    if order % 2:
                        put_white((mouse_pos[0]-40)//40, (mouse_pos[1]-40)//40)
                    else:
                        put_black((mouse_pos[0]-40)//40, (mouse_pos[1]-40)//40)
        pygame.display.flip()

    pygame.quit()
