

class Board:
    """The sea battle game board."""
    def _init_(self):
        pass

    @property
    def board_table(self):
        """Creates a board canvas"""
        board_table = [["0" for i in range(6)] for i in range(6)]
        return board_table
    
    @property
    def ships_list(self):
        """List of the ships on the table"""
        ships_list = []
        return ships_list
    
    def print_board_table(self):
        """Prints the current state of a board table."""
        print()
        header = '    |'
        for i in range(1, 7):
            header += f" {i} |"
        
        print(header)
        for i, row in enumerate(self.board_table):
            row_str = f"  {i} | {' | '.join(row)} | "
            print(row_str)

class Dot:
    """A dot a.k.a. cell in our game board."""
    def __init__(self, i, j):
        self.x = i
        self.y = j
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __str__(self):
        return f"Dot:{self.i, self.j}"

class Ship:
    """The ship entity"""
    def __init__(self, length, bow_point, direction, hp):
        self.length = length
        self.bow_point = bow_point
        self.direction = direction
        self.hp = hp


sea_battle_board = Board()
sea_battle_board.print_board_table()