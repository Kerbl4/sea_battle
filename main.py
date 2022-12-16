from random import randint

class BoardOutException(Exception):
    def __str__(self):
        return "You are firing out of the board!"

class SamePointException(Exception):
    def __str__(self):
        return "You've already fired the board here!"

class ShipOutOfBoard(Exception):
    def __str__(self):
        return "The ship is placed out of the board!"

class Board:
    """The sea battle game board."""
    def __init__(self, is_hidden=False, size=6):
        self.is_hidden = is_hidden
        self.size = size
        self.used_coords = []
        self.ship_list = []
        self.board_table = [["0" for i in range(size)] for i in range(size)]
        self.count = 0
    
    def __str__(self):
        """Prints the current state of a board table."""
        board_print = ""
        header = '    |'
        for i in range(1, self.size + 1):
            header += f" {i} |"
        board_print += header
        
        for i, row in enumerate(self.board_table):
            board_print += f"\n  {i + 1} | {' | '.join(row)} | "

        if self.is_hidden:
            board_print = board_print.replace("■", "0")
        return board_print

    def add_ship(self, ship):
        """Add ship to the table"""
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_coords:
                raise ShipOutOfBoard()
        for dot in ship.dots:
            self.board_table[dot.i][dot.j] = "■"
            self.used_coords.append(dot)
        
        self.ship_list.append(ship)
        self.hitbox(ship)
    
    def hitbox(self, ship, real=False):
        buffer = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for dot in ship.dots:
            for di, dj in buffer:
                cur = Dot(dot.i + di, dot.j + dj)
                if not (self.out(cur)) and cur not in self.used_coords:
                    if real:
                        self.board_table[cur.i][cur.j] = "."
                    self.used_coords.append(cur)

    def out(self, dot):
        return not ((0 <= dot.i < self.size) and (0<= dot.j < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        
        if dot in self.used_coords:
            raise SamePointException()
        
        self.used_coords.append(dot)
        
        for ship in self.ship_list:
            if ship.is_hit(dot):
                ship.hp -= 1
                self.board_table[dot.i][dot.j] = "X"
                if ship.hp == 0:
                    self.count += 1
                    self.hitbox(ship, real = True)
                    print("Ship has been destroyed!")
                    return False
                else:
                    print("Ship has been hit!")
                    return True
        
        self.board_table[dot.i][dot.j] = "."
        print("You've missed that one!")
        return False
    
    def start(self):
        self.used_coords = []

class Dot:
    """A dot a.k.a. cell in our game board."""
    def __init__(self, i, j):
        self.i = i
        self.j = j
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __repr__(self):
        return f"Dot: {self.i, self.j}"

class Ship:
    """The ship entity"""
    def __init__(self, length, bow_point, direction):
        self.length = length
        self.bow_point = bow_point
        self.direction = direction
        self.hp = length
    
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_i = self.bow_point.i 
            cur_j = self.bow_point.j

            if self.direction == 0:
                cur_i += i

            elif self.direction == 1:
                cur_j += i
            ship_dots.append(Dot(cur_i, cur_j))
        return ship_dots

    def is_hit(self, shot):
        return shot in self.dots

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
            except BoardOutException as error:
                print(error)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.i+1} {d.j+1}")
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
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.is_hidden = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except ShipOutOfBoard:
                    pass
        board.start()
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
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
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

game = Game()
game.start()