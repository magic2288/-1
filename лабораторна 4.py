from tkinter import *
# імпортуємо рандом для відскоку м'ячика
import random
# настройки вікна
WIDTH = 900
HEIGHT = 300

# очки для кодного гравця
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# рахунок швидкості
INITIAL_SPEED = 20


# настройка ракеток
# ширина ракетки
PAD_W = 10
PAD_H = 100
# радіус м'яча
BALL_RADIUS = 40
#швидкість м'яча
# горизонтально
BALL_X_CHANGE = 20
# вертикально
BALL_Y_CHANGE = 0
# вікно
root = Tk()
root.title("Пінг-понг :)")
# canvas
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#DDA0DD")
c.pack()
# елементи ігрового поля
# ліва лінія
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# права лінія
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
# лінія, що розділяє ігрове поле
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")
# м'яч
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="#FFE4C4")
# ракетки
# ліва ракетка
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="#FFF0F5")
# права ракетка
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="#FFF0F5")

# текст очків
p_1_text = c.create_text(WIDTH - WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font ='Calibri 23',
                         fill = 'white')
p_2_text = c.create_text(WIDTH/6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font ='Calibri 23',
                         fill = 'white')
# швидкість ракеток
PAD_SPEED = 20
# швидкість лівої ракетки
LEFT_PAD_SPEED = 0
# швидкість правої ракетки
RIGHT_PAD_SPEED = 0

# швидкість м'яча з кожним ударом
BALL_SPEED_UP = 1.00
# максимальна швидкість м'яча
BALL_MAX_SPEED = 30
# початкова швидкість м'яча по горизонталі
BALL_X_SPEED = 20
# початкова швидкість м'яча по вертикалі
BALL_Y_SPEED = 20
# відстань до правого краю
right_line_distance = WIDTH - PAD_W
# рахунок
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
#Респаун
def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)


# відскок м'яча від ракеток
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':
        BALL_Y_SPEED =random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

# функції для руху м'яча
def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot)/2
    # вертикальний відскок
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH/2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > WIDTH/2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')
# функція руху ракеток
def move_pads():
    PADS = {LEFT_PAD:LEFT_PAD_SPEED,
            RIGHT_PAD:RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1]<0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3]>HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
# викликає сама себе (рекурсія)
    root.after(30, main)

# фокус на канвас (реакція на клавіші)
c.focus_set()
# Обробка нажимань
def moveent_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == 'Up':
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 'Down':
        RIGHT_PAD_SPEED = PAD_SPEED
# прив'язка до канваса
c.bind("<KeyPress>", moveent_handler)
# клавіші не нажаті
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0
c.bind("<KeyRelease>")
# Запуск
main()

# Запуск вікна
root.mainloop()
