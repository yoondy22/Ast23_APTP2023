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


def check_omok():
    # 가로 체크
    for i in range(15):
        for j in range(10):
            if stone_board[i][j] and stone_board[i][j] == stone_board[i][j+1] == stone_board[i][j+2] == \
                    stone_board[i][j+3] == stone_board[i][j+4]:
                return stone_board[i][j]

    # 세로 체크
    for i in range(15):
        for j in range(10):
            if stone_board[j][i] and stone_board[j][i] == stone_board[j+1][i] == stone_board[j+2][i] == \
                    stone_board[j+3][i] == stone_board[j+4][i]:
                return stone_board[j][i]

    # / 대각선 체크

    # \ 대각선 체크

    return 0


def put_black(x, y):  # 검은돌 착수
    global order
    global game_end

    if stone_board[y][x]:  # 돌이 이미 존재하면
        return  # 착수 불가

    pygame.draw.circle(screen, BLACK, [grid_origin_x + grid_size * x, grid_origin_y + grid_size * y], stone_size, 0)
    stone_board[y][x] = 1
    order += 1

    if check_omok() == 1:
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

    if check_omok() == 2:
        font = pygame.font.SysFont("arial", 50, True, False)
        winning_text = font.render("WHITE WIN!", True, RED)
        screen.blit(winning_text, (200, 310))
        game_end = True


if __name__ == "__main__":

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

# test