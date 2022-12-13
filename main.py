class Board:
    """The sea battle game board."""
    def _init_(self):
        pass

    @property
    def board_table(self):
        """Creates a board canvas"""
        board_table = [["0" for i in range(6)] for i in range(6)]
        return board_table
    
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
    def __init__(self, x, y):
        self.x = x
        self.y = y


sea_battle_board = Board()
sea_battle_board.print_board_table()