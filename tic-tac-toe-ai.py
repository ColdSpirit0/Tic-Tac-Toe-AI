import os
import random

# инициализация данных
empty_cell = " "
player_symbols = ["X", "O"]
numpad_table = [6, 7, 8, 3, 4, 5, 0, 1, 2]

current_player = 0
field = [empty_cell] * 9

ai_player = 1
ai_difficulty = 0
ai_difficulty_names = ["Очень легкая", "Средняя", "Максимальная"]

# функция выбора сложности
def difficulty_choose():
    # очистка поля
    os.system("cls")
	
    # вывод списка сложностей
    for k, v in enumerate(ai_difficulty_names):
        print(k+1, v, sep=") ")

    while True:
        user_input = input("Выберите сложность компьютера: ")

        # проверяем, что ввод это число
        if user_input.isdigit():
            user_input = int(user_input) - 1

            # проверяем, что ввод в диапазоне возможных сложностей
            if user_input in range(3):
                global ai_difficulty
                ai_difficulty = user_input
                break

def get_opponent(player):
    if player is 0:
        return 1
    else:
        return 0

def init():
    global current_player
    global field

    current_player = 0
    field = [empty_cell] * 9

def draw():
    # очистка поля
    os.system("cls")

    for line in range(3):
        print(field[line * 3 : (line + 1)*3])

def is_tie(field):
    return empty_cell not in field

def is_win(field):
    # этап 1: по-горизонали
    for line in range(3):
        symbols = field[line * 3 : (line + 1)*3]

        if symbols[0] != empty_cell:
            if symbols[0] == symbols[1] == symbols[2]:
                return True

    # этап 2: по-вертикали
    for column in range(3):
        symbols = field[column::3]

        if symbols[0] != empty_cell:
            if symbols[0] == symbols[1] == symbols[2]:
                return True

    # этап 3: по-диагонали
    if field[4] != empty_cell:

        if field[2] == field[4] == field[6]:
            return True

        if field[0] == field[4] == field[8]:
            return True

    return False

# функции ИИ
def get_empty_cells(field):
    # получить индексы свободных ячеек
    index = 0
    empty_cells = []

    for cell in field:
        if cell == empty_cell:
            empty_cells.append(index)

        index += 1

    return empty_cells

def minmax(field, player, steps = None):

    empty_cells = get_empty_cells(field)
    best_cell = None

    if player is ai_player:
        # если компьютер, будем вычислять максимальное
        minmax_score = -10
    else:
        # если человек, будем вычислять минимальное
        minmax_score = 10

    for cell in empty_cells:
        branch_field = field.copy()
        branch_field[cell] = player_symbols[player]
        score = 0

        # если кто-то победил, считаем результат
        if is_win(branch_field):
            # победа компьютера дает ему 1
            if player is ai_player:
                score = 1
            # победа игрока дает -1
            else:
                score = -1
        # если ничья 0
        elif is_tie(branch_field):
            score = 0
        # если игра продолжается, вычисляем все следующие ходы
        # или несколько ходов
        else:
            if steps is not None:
                if steps > 0:
                    score = minmax(branch_field, get_opponent(player), steps - 1) [0]
                else:
                    score = 0
            else:
                score = minmax(branch_field, get_opponent(player)) [0]

        # вычисляем минмакс
        if player is ai_player:
            # если компьютер, будем вычислять максимальное
            if score > minmax_score:
                minmax_score = score
                best_cell = cell
        else:
            # если человек, будем вычислять минимальное
            if score < minmax_score:
                minmax_score = score
                best_cell = cell

    return minmax_score, best_cell

def ai_step_easy():
    # получить случайное среди свободных
    return random.choice(get_empty_cells(field))

# итерация игровых циклов
def game_update():
    global current_player

    # если ходит компьютер
    if current_player is ai_player:
        # самая легкая сложность, компьютер делает случайные шаги
        if ai_difficulty is 0:
            user_input = ai_step_easy()

        # средняя сложность, компьютер видит на 2 шага вперед
        elif ai_difficulty is 1:
            user_input = minmax(field, current_player, 1) [1]

        # максимальная сложность, компьютер видит все шаги
        elif ai_difficulty is 2:
            user_input = minmax(field, current_player) [1]

    else:
        # отрисовка поля
        draw()

        # вывод информации
        print("Ходит игрок " + str(current_player + 1))

        while True:
            # считываем ввод
            user_input = input("Введите номер ячейки: ")

            # проверяем ввод на валидность
            is_valid = False

            # проверяем, что это число
            if user_input.isdigit():
                # преобразовываем в удобный для работы формат
                user_input = int(user_input) - 1

                # проверяем, что число в диапазоне от 0 до 8
                # преобразовываем номер ячейки в реальный
                # проверяем, что ячейка на поле пустая в этом месте
                if user_input in range(9):
                    user_input = numpad_table[user_input]

                    if field[user_input] is empty_cell:
                        break

    # обработка ввода
    field[user_input] = player_symbols[current_player]

    # сообщение о выигрыше
    match_end = False
    if is_win(field):
        draw()
        if current_player is 0:
            print("Вы победили, поздравляем!")
        else:
            print("Компьютер победил!")
        match_end = True;
    # проверяем на ничью
    elif is_tie(field):
        draw()
        print("Ничья!")
        match_end = True;

    if match_end:
        while True:
            yes_no = input("Хотите сыграть снова? (y/n)")

            if yes_no is "n":
                return True
            elif yes_no is "y":
                return False

    # меняем игрока
    current_player = get_opponent(current_player)


# основная логика игры
while True:
    init()

    # перед игрой выбираем сложность
    difficulty_choose()

    exit = None
    while exit is None:
        exit = game_update()

    if exit is True:
        break
