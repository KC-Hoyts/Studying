from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y+1
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class BoardWrongSize(Exception):
    def __str__(self):
        return "(!) Некорректные размеры поля (!)\n"

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
    
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, board_width, board_height):
        self.generated_status = False
        self.board_width = board_width
        self.board_height = board_height
        self.header = []

        self.hid = False
        
        self.count = 0
        
        self.field = []
        
        self.busy = []
        self.ships = []
    #=======================================
    def show_board(self):
        if self.generated_status == False:
            try:
                # проверка корректности размеров поля
                if self.board_width not in range(6,11) or self.board_height not in range(6,10):
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

    def board_generation(self):
            # Вывод номеров столбцов. Начало
        for h in range(self.board_width + 1):
            if h == 0:
                self.header.append(" ")
            else:
                self.header.append(h)
        #print(*self.header, sep=" | ")
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

        #for element in self.field:
            #print(*element, sep=" | ")
        # Вывод номеров строк и поля. Конец
        #==================================
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)
            
    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    

    
    def out(self, d):
        return not((0<= d.x < self.board_height) and (0<= d.y < self.board_width))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    
    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):

    def ask(self):
        d = Dot(randint(0, 10), randint(1, 10))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

class Game:
    def __init__(self, height1, width1):
        self.height1 = height1
        self.width1 = width1

        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]

        board = Board(self.width1, self.height1)
        board.show_board()

        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, board.board_height), randint(0, board.board_width)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    
    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board.show_board())
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board.show_board())
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()
            
h_size = int(input("Введите высоту поля: "))
w_size = int(input("Введите ширину поля: "))
g = Game(h_size, w_size)
g.start()