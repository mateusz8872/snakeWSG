import tkinter as tk
import time
import random
import sys
import math
####################################################################################################################
# PARAMETRY GRY
# startowe zmienne
game_over = False
score = 0
lives = 1
# okno gry
snake_window = tk.Tk()
# rozmiary okna gry
win_x, win_y = 800, 800
game_window_dimensions = [win_x, win_y]
snake_window.geometry(str(win_x) + "x" + str(win_y))
# blokada zmiany rozmiarów okna gry
snake_window.resizable(0, 0)
# tytuł gry
snake_window.title("Snake")
# obsługa zamkniecia okna gry
snake_window.protocol("WM_DELETE_WINDOW", sys.exit)
# okno gry: bd - tło; highlightthickness - obramowanie
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

# rozmiary segmentu weża
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]

# początkowa pozycja głowy weża, lista definująca ogon - wąż 1
snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
snake_tail = []

# początkowa pozycja głowy weża, lista definująca ogon - wąż 2
snake2_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2 - 5]
snake2_tail = []

# kierunek ruchu weża 1 [x,y]
snake_move_dir = [1, 0]
snake_moved_in_this_frame = False

# kierunek ruchu weża 2 [x,y]
snake2_move_dir = [1, 0]

# parametry gry - ilość wyświetleń/sec
wps = 10
####################################################################################################################
# FUNKCJE GRY
####################################################################################################################
# wypełnianie pola na siatce
def createGridItem(coords, hexcolor):
    snake_canvas.create_rectangle((coords[0]) * snake_scale, (coords[1]) * snake_scale, (coords[0] + 1) * snake_scale, (coords[1] + 1) * snake_scale, fill=hexcolor, outline="#222222", width=3)

# losowanie pozycji jabłka
def generateAppleCoords():
    global snake_tail, snake2_tail

    while True:
        x = random.randint(1, game_dimensions[0] - 2)   
        y = random.randint(1, game_dimensions[1] - 2) 

        apple_coords = [x, y]

        # jabłko nie może być na żadnym wężu
        if apple_coords not in snake_tail and apple_coords not in snake2_tail:
            return apple_coords


# wyniki
def show_game_over():
    global game_over
    game_over = True

    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="black")

    snake_canvas.create_text(win_x//2, win_y//2 - 50,
                             text="KONIEC GRY",
                             fill="red", font=("Arial", 40, "bold"))

    snake_canvas.create_text(win_x//2, win_y//2,
                             text=f"Wynik: {score}",
                             fill="white", font=("Arial", 30))

    snake_canvas.create_text(win_x//2, win_y//2 + 80,
                             text="Naciśnij R aby zagrać ponownie",
                             fill="yellow", font=("Arial", 20))

# restart
def restart_game():
    global snake_coords, snake_tail, snake_move_dir
    global snake2_coords, snake2_tail, snake2_move_dir
    global apple_coords, score, lives, game_over

    # reset węża 1
    snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
    snake_tail = []
    snake_move_dir = [1, 0]

    # reset węża 2
    snake2_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2 - 5]
    snake2_tail = []
    snake2_move_dir = [1, 0]

    # reset reszty
    apple_coords = generateAppleCoords()
    score = 0
    lives = 1
    game_over = False
    global snake_moved_in_this_frame
    snake_moved_in_this_frame = False

# gra
def gameloop():
    global wps, snake_moved_in_this_frame
    global snake_tail, snake_coords, snake_move_dir
    global snake2_tail, snake2_coords, snake2_move_dir
    global apple_coords, score, lives, game_over

    if game_over:
        return

    snake_window.after(1000 // wps, gameloop)

    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="white", width=5)

    # dodanie głowy węża 1
    snake_tail.append([snake_coords[0], snake_coords[1]])
    snake_coords[0] += snake_move_dir[0]
    snake_coords[1] += snake_move_dir[1]    

    # dodanie głowy węża 2
    snake2_tail.append([snake2_coords[0], snake2_coords[1]])
    snake2_coords[0] += snake2_move_dir[0]
    snake2_coords[1] += snake2_move_dir[1]

    # kolizja ze ścianą – oba węże
    for x, y in (snake_coords, snake2_coords):
        if x < 0 or x >= game_dimensions[0] or y < 0 or y >= game_dimensions[1]:
            show_game_over()
            return


    snake_moved_in_this_frame = False

    # kolizja głowy węża 1 z ogonem
    for segment in snake_tail[:-1]:
        if segment == snake_coords:
            show_game_over()
            return

    # kolizja głowy węża 2 z ogonem
    for segment in snake2_tail[:-1]:
        if segment == snake2_coords:
            show_game_over()
            return

    # kolizja głowy węża 1 z ogonem węża 2
    for segment in snake2_tail:
        if segment == snake_coords:
            show_game_over()
            return

    # kolizja głowy węża 2 z ogonem węża 1
    for segment in snake_tail:
        if segment == snake2_coords:
            show_game_over()
            return


    # wyswietlanie weza 1
    for segment in snake_tail:
        createGridItem(segment, "#00ff00")

    # wyswietlanie weza 2
    for segment in snake2_tail:
        createGridItem(segment, "#00aaff")

    # wyświetlenie jabłka
    createGridItem(apple_coords, "#ff0000")

    # jeżeli jabłko zjedzone
    snake1_ate = (snake_coords == apple_coords)
    snake2_ate = (snake2_coords == apple_coords)

    # jeśli któryś zjadł – nowe jabłko
    if snake1_ate or snake2_ate:
        score += 1
        if score % 25 == 0:
            lives += 1
        apple_coords = generateAppleCoords()

    # wydłużanie ogonów osobno
    if not snake1_ate:
        snake_tail.pop(0)

    if not snake2_ate:
        snake2_tail.pop(0)


    # HUD – wyświetlanie wyniku i żyć
    snake_canvas.create_text(60, 20, text=f"Jabłka: {score}", fill="white", font=("Arial", 16))
    snake_canvas.create_text(60, 50, text=f"Życia: {lives}", fill="white", font=("Arial", 16))

# obsługa klawiatury
def key(e):
    global snake_move_dir, snake_moved_in_this_frame, snake2_move_dir, game_over

    # restart gry
    if e.keysym.lower() == "r":
        if game_over:
            restart_game()
            gameloop()
        else:
            restart_game()
        return

    if not snake_moved_in_this_frame:
        snake_moved_in_this_frame = True

        # wąż 1 – strzałki
        if e.keysym == "Left" and snake_move_dir[0] != 1:
            snake_move_dir = [-1, 0]
        elif e.keysym == "Right" and snake_move_dir[0] != -1:
            snake_move_dir = [1, 0]
        elif e.keysym == "Up" and snake_move_dir[1] != 1:
            snake_move_dir = [0, -1]
        elif e.keysym == "Down" and snake_move_dir[1] != -1:
            snake_move_dir = [0, 1]
        else:
            snake_moved_in_this_frame = False

    # wąż 2 – WSAD
    if e.keysym == "a" and snake2_move_dir[0] != 1:
        snake2_move_dir = [-1, 0]
    elif e.keysym == "d" and snake2_move_dir[0] != -1:
        snake2_move_dir = [1, 0]
    elif e.keysym == "w" and snake2_move_dir[1] != 1:
        snake2_move_dir = [0, -1]
    elif e.keysym == "s" and snake2_move_dir[1] != -1:
        snake2_move_dir = [0, 1]


####################################################################################################################
# 1 losowanie jabłka
apple_coords = generateAppleCoords()

snake_window.bind("<KeyPress>", key)
gameloop()
snake_window.mainloop()
