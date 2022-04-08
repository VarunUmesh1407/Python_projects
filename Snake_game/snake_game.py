import curses
from random import randint

# setup window

curses.initscr()
window = curses.newwin(20, 60, 0, 0)  # y,x
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)
window.nodelay(True)  # -1

# snake and food
snake = [(4, 10), (4, 9), (4, 8)]
food = (10, 20)
window.addch(food[0], food[1], '*')
# game logic
score = 0
ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    window.addstr(0, 2, 'Score' + str(score) + ' ')
    window.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)  # speed increases as the snake grows

    previous_key = key
    event = window.getch()
    key = event if event != -1 else previous_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = previous_key

    # calculate next co-ordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x))  # append 0(n)

    # check snake hitting the border and game over
    if y == 0 or y == 19:
        break
    if x == 0 or x == 59:
        break

    # snake over itself
    if snake[0] in snake[1:]:
        break

    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))
            if food in snake:
                food = ()
        window.addch(food[0], food[1], '*')
    else:
        # move snake
        last = snake.pop()
        window.addch(last[0], last[1], ' ')

    window.addch(snake[0][0], snake[0][1], '=')

curses.endwin()
print(f"FINAL SCORE= {score}")
