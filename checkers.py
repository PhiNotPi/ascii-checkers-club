class Checker:
    """The checkers piece."""

    # constants (Checker._____)
    PLAYER_ONE = 'one'
    PLAYER_TWO = 'two'

    # constructor
    def __init__(self, player):
        """Constructs a new checkers piece."""
        self.player = player
        self.king = False

    @staticmethod
    def character(piece):
        """Returns the character for a piece (' ' (a space), x, o, X, or O)."""
        if piece is None: return ' '
        char = 'o' if piece.player == Checker.PLAYER_ONE else 'x'
        return char.upper() if piece.king else char

class Board:
    """The board on which the checkers lie."""

    # constructor
    def __init__(self):
        """Constructs a new, normal set up board."""
        self.data = []
        self.data.extend(Board.start_rows(Checker.PLAYER_ONE))
        self.data.extend(Board.empty_rows(2))
        self.data.extend(Board.start_rows(Checker.PLAYER_TWO))

    @staticmethod
    def start_rows(player):
        """The configuration of pieces that the game starts with."""
        r1, r2, r3 = [], [], []
        for _ in range(4):
            r1.extend([None, Checker(player)] if player == Checker.PLAYER_ONE else [Checker(player), None])
            r2.extend([None, Checker(player)] if player == Checker.PLAYER_TWO else [Checker(player), None])
            r3.extend([None, Checker(player)] if player == Checker.PLAYER_ONE else [Checker(player), None])
        return [r1, r2, r3]

    @staticmethod
    def empty_rows(count):
        """Returns an amount of empty rows."""
        return [[None] * 8 for _ in range(count)]

    def render(self):
        """Returns an ASCII representation of the board."""
        s = '   A B C D E F G H \n'
        for n, row in enumerate(self.data):
            s += '  +-+-+-+-+-+-+-+-+\n'
            s += '%i |%s|\n' % (n, '|'.join([Checker.character(p) for p in row]))
        s += '  +-+-+-+-+-+-+-+-+'
        return s

    def move(self, player, from_coords, to_coords):
        """
        Given a player that is moving, and A0-style coordinates for from and to, moves the piece.
        Returns a string (error message) if move failed, None otherwise.
        TODO jumping and capturing
        TODO keep count of captured pieces
        """
        
        while not is_coord(from_coords) or not is_coord(to_coords):
            new_move = input('Player %s, enter move (for example, A0 B1 to move the piece at A0 to B1): ' % player).split(' ')
            from_coords, to_coords = new_move[0], new_move[1]
        
        from_y, from_x = 'ABCDEFGH'.index(from_coords[0]), int(from_coords[1])
        to_y, to_x = 'ABCDEFGH'.index(to_coords[0]), int(to_coords[1])

        from_piece = self.data[from_x][from_y]
        to_piece = self.data[to_x][to_y]

        # first check to see if there's a piece in `from`
        if from_piece is None: return 'There is no piece there!'
        # and check to see if it's that player's
        if from_piece.player != player: return 'That\'s not your piece!'
        # check to see if `to` is an open space
        if to_piece is not None: return 'There\'s already a piece in that space!'
        # check to see if piece is moving forwards
        dx = to_x - from_x
        forwards = dx > 0 if from_piece.player == Checker.PLAYER_ONE else dx < 0
        if not forwards and not from_piece.king: return 'You can\'t move backwards!'

        # check to see if the move is diagonal
        adx, ady = abs(from_x - to_x), abs(from_y - to_y)
        if adx == ady == 1:
            self.data[to_x][to_y], self.data[from_x][from_y] = from_piece, None
            return None
        elif adx == ady == 2:
            jumped_x, jumped_y = (from_x + to_x)//2, (from_y + to_y)//2
            jumped_piece = self.data[jumped_x][jumped_y]
            if jumped_piece is None:
                return 'You can\'t jump over nothing!'
            elif jumped_piece.player == player:
                return 'You can\'t jump over yourself!'
            else:
                self.data[to_x][to_y], self.data[from_x][from_y] = self.data[from_x][from_y], None
                self.data[jumped_x][jumped_y] = None
                return None
        else:
            return 'That\'s not a diagonal move!'

def is_coord(coord):
    return coord[0] in 'ABCDEFG' and coord[1] in '01234567'

def ask_for_move(player, board):
    """Ask the player for a move, and move there, given a board."""
    move = input('Player %s, enter move (for example, A0 B1 to move the piece at A0 to B1): ' % player).split(' ')
    message = board.move(player, move[0], move[1])
    while message is not None:
        move = input(message + ' Please try again: ').split(' ')
        message = board.move(player, move[0], move[1])

if __name__ == '__main__':
    players = input('Enter number of players (1 or 2): ')
    while players not in ['1', '2']:
        players = input('Invalid number of players. Try again: ')

    if players == '1':
        print('AI not implemented yet. So... I\'ll just... do nothing')
    else:
        board = Board()
        while True:
            print(board.render())
            ask_for_move(Checker.PLAYER_ONE, board)
            print(board.render())
            ask_for_move(Checker.PLAYER_TWO, board)
