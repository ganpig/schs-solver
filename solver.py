import pygame
from easygui import *
from math import *
from sys import exit


TITLE = 'GUI Solver v4.0'
SIZE = 500
UNIT = 20
RAD = 5


def solve(r0, A, Wr):
    tmp1 = r0 ** 2 - (A - 10) ** 2
    assert tmp1 >= 0
    tmp2 = sqrt(tmp1 * (tmp1 + 4 * Wr ** 2))
    tmp3 = 2 * Wr * (-A + r0 + 10)
    res = 2 * atan((tmp2 - tmp1) / tmp3)
    return res


if __name__ == '__main__':
    try:
        pygame.init()
        screen = pygame.display.set_mode((SIZE, SIZE))
        font = pygame.font.SysFont('Arial', UNIT, 1, 1)

        def drawPoint(r, t, name):
            print(f'{name}({r:.3},{t:.3})')
            x = r * cos(t)
            y = r * sin(t)
            xx = SIZE / 2 + UNIT * x
            yy = SIZE / 2 - UNIT * y
            pygame.draw.circle(screen, (255, 0, 0), (xx, yy), RAD)
            screen.blit(font.render(name, 1, (0, 0, 255)), (xx, yy))
            pygame.display.update()

        pygame.display.set_caption(TITLE)

        screen.fill((255, 255, 255))
        for i in range(1, 6):
            pygame.draw.circle(screen, (100, 100, 100),
                               (SIZE / 2, SIZE / 2), UNIT * 2 * i, 2)
        for i in range(6):
            t = i / 6 * pi
            x = 10 * cos(t)
            y = 10 * sin(t)
            xx = SIZE / 2 + UNIT * x
            yy = SIZE / 2 - UNIT * y
            pygame.draw.line(screen, (100, 100, 100),
                             (xx, yy), (SIZE - xx, SIZE - yy), 2)

        pygame.display.update()

        init = multenterbox('请设置起始点', TITLE, ['ρ0', 'θ0'], ['10', '0.96'])

        if not init:
            exit()

        r, t = map(float, init)

        drawPoint(r, t, '0')
        i = 1

        while True:
            args = textbox("请设置各点参数，每行两个以空格分隔的数表示 A' 与 Wr'\n修正后 A' 的取值范围为 (0, 20)，Wr' 的取值范围为 [-10, 10]",
                           TITLE, '16 9\n10 7\n4 -3')

            if not args:
                exit()

            for item in args.splitlines():
                item = item.strip()
                if not item:
                    continue
                A_, Wr_ = map(float, item.split())
                assert 0 < A_ < 20 and -10 <= Wr_ <= 10

                A = (A_ - 10) / 10 * r + 10
                p = (A + r + 10) / 2
                Wr_max = 2 * sqrt(p * (p - A) * (p - r) * (p - 10)) / r
                Wr = Wr_ * Wr_max / 10

                dt = solve(r, A, Wr)
                r = Wr / sin(dt)
                t -= dt
                t %= 2 * pi
                if t > pi:
                    t -= 2 * pi

                drawPoint(r, t, str(i))
                i += 1

            flag = True
            while flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        flag = False

    except Exception:
        exceptionbox(title=TITLE)
