from random import randint

MINE = 9

class MinesweeperField(object):
    def __init__(self, width, height, num_mines):
        board = []

        if num_mines > width * height:
            raise ValueError('Too many mines to be placed')

        # make the board
        for i in range(height):
            row = []
            for j in range(width):
                row.append(0)
            board.append(row)

        self.board = board
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self._generate_mines()
        self._mark_board()

    def __getitem__(self, row):
        return self.board[row]

    def _generate_mines(self):
        positions = self._generate_mine_positions(self.width, self.height, self.num_mines)
        for x, y in positions:
            self.board[y][x] = MINE

    def _mark_board(self):
        board = self.board
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                # skip mine
                if val == MINE:
                    continue

                adjacent_mines = 0
                pairs = (
                    (y - 1, x - 1),
                    (y - 1, x),
                    (y - 1, x + 1),
                    (y, x - 1),
                    (y, x + 1),
                    (y + 1, x - 1),
                    (y + 1, x),
                    (y + 1, x + 1)
                )
                for rindex, cindex in pairs:
                    try:
                        if board[rindex][cindex] == MINE:
                            adjacent_mines += 1
                    except IndexError:
                        pass

                # set current to adjacent number
                row[x] = adjacent_mines

    @staticmethod
    def _generate_mine_positions(width, height, num_mines):
        mines = set()
        windex = width - 1
        hindex = height - 1
        for i in range(num_mines):
            while True:
                coord = randint(0, windex), randint(0, hindex)
                if not coord in mines:
                    mines.add(coord)
                    break

        return mines


def new_board(difficulty):
    assert isinstance(difficulty, int)
    if difficulty == 0:
        args = (9, 9, 10)
    elif difficulty == 1:
        args = (16, 16, 40)
    elif difficulty == 2:
        args = (30, 16, 99)
    else:
        raise ValueError('Difficulty has to be in range [0, 2]')

    return MinesweeperField(*args)

if __name__ == '__main__':
    print('Medium Board')
    for row in new_board(1).board:
        print('\t'.join(str(x) for x in row))
