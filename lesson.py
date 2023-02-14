from random import randint
# Интерфейс приложения должен представлять собой консольное окно с двумя полями 6х6
# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже ходил.
# Для представления корабля опишите класс Ship с конструктором,
# принимающим в себя набор точек (координат) на игровой доске.
# Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
# Корабли должны находится на расстоянии минимум одной клетки друг от друга.
# Корабли на доске должны отображаться знаками - ■, пустые клетки - О, X - повреждение, T - промах
# На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей:
# 	1 корабль на 3 клетки;
# 	2 корабля на 2 клетки;
# 	4 корабля на одну клетку.
# Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение
# Если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения
# ___________
# Возможные классы:
# Корабль, доска, ячейка, выстрел,
# внутренняя логика - случайное расположение кораблей в пределах доски, проверка попадания, проверка уничтожения,
# (попадание, промах), вычисление победителя, (ВСЕ ДЕЙСТВИЯ КАК ДЛЯ ИГРОКА, ТАК И ДЛЯ ИИ)
# внешняя логика - ввод данных пользователем, отображение ячеек доски при разных событиях, вывод сообщений, вывод ошибок
# _______________________________________________________________________________________________________
# Начало кода
class BoardWrongSize(Exception):
    def __str__(self):
        return "(!) Некорректные размеры поля (!)\n"

# Внутренняя логика

class Board:
    def __init__(self):
        self.board_width = 0
        self.board_height = 0
        self.header = []
        self.field = []
        self.generated_status = False

    def show_board(self):
        if self.generated_status == False:
            try:
                self.board_width = int(input("Type board width: "))
                self.board_height = int(input("Type board height: "))
                # проверка корректности размеров поля
                if self.board_width not in range(2,11) or self.board_height not in range(2,10):
                    raise BoardWrongSize
            except BoardWrongSize as v:
                print(v, "Попробуйте ввести иные размеры.")
                self.show_board()
            else:
                self.board_generation()
                self.generated_status = True
        else:
            print(*self.header, sep=" | ")
            for element in self.field:
                print(*element, sep=" | ")

    # высота height не более 9, ширина width не более 10
    # а также высота и ширина не менее 2
    def board_generation(self):
            # Вывод номеров столбцов. Начало
        for h in range(self.board_width + 1):
            if h == 0:
                self.header.append(" ")
            else:
                self.header.append(h)
        print(*self.header, sep=" | ")
            # Вывод номеров столбцов. Конец

            # Вывод номеров строк и поля. Начало
        for el in range(self.board_height + 1):
            if el == 0:
                pass
            else:
                self.field.append([el])

        for y in self.field:
            while len(y) <= self.board_width:
                y.append("o")

        for element in self.field:
            print(*element, sep=" | ")
        # Вывод номеров строк и поля. Конец

class Ship(Board): # класс для создания корабля
    def __init__(self):
        super().__init__()
        self.length = 0
        self.nose_dot = []
        self.orientation = randint(0, 1)
        self.ship_life = 0

        # self.ship_one_1 = None
        # self.ship_one_2 = None
        # self.ship_one_3 = None
        # self.ship_one_4 = None
        # self.ship_two_1 = None
        # self.ship_two_2 = None
        # self.ship_two_3 = None
        # self.ship_three_1 = None
        # self.ship_three_2 = None
        # self.ship_four_1 = None

    def ship_generation(self):
        if self.board_width * self.board_height < 9:
            for y in self.field:
                if self.nose_dot[1] == y[0]:
                    for ind_x, data in enumerate(y):
                        if self.nose_dot[0] == ind_x:
                            y[ind_x] = "■"
        else:
            print("Размер поля больше, чем необходимо для данного корабля")

    def dot_check(self):
        pass


# == Для выстрела ==
# print(f'board_field[0] = {board.field[0]}')
# print(f'board_field[1] = {board.field[1]}')
# print(f'board_field[2] = {board.field[2]}')
# dot = (int(input("Столбец: ")), int(input("Строка: ")))
# print(f'Объявили точку {dot}, dot[0] (x) = {dot[0]}, dot[1] (y) = {dot[1]}')
#
# input("continue")
# for y in board.field:
#     print(f'y = {y}')
#     if dot[1] == y[0]:
#         for ind_x, data in enumerate(y):
#             if dot[0] == ind_x:
#                 y[ind_x] = "T"

game = Ship()  # вывод поля
print("До первого создания и вывода:")
game.show_board()
print("1 раз создали и вывели.")
input("==continue?==")

game.length = 1
game.nose_dot = [2, 2]
game.ship_generation()
game.show_board()



input("==continue?==")

game.show_board()
print("Вывод с изменениями")





# a = 10
# print(list(range(a)))
