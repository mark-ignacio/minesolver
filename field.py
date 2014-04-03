from random import randint
import logging

MINE = '*'


class LostGameException(Exception):
    pass


class MinesweeperField(object):
    def __init__(self, width, height, num_mines):
        field = []

        if num_mines > width * height:
            raise ValueError('Too many mines to be placed')

        # make the board
        for i in range(height):
            row = []
            for j in range(width):
                row.append(0)
            field.append(row)

        self._field = field
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self._generate_mines()
        self._mark_board()

        # utility
        self.touched = set()

    def __getitem__(self, row):
        return self._field[row]

    def __str__(self):
        field = []
        for row in self[::-1]:
            field.append('\t'.join(str(x) for x in row))

        return '\n'.join(field)

    def _generate_mines(self):
        positions = self._generate_mine_positions(self.width, self.height, self.num_mines)
        for x, y in positions:
            self._field[y][x] = MINE

    def _mark_board(self):
        board = self._field
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                # skip mine
                if val == MINE:
                    continue

                adjacent_mines = 0
                pairs = eight_directions(x, y)
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

    def get_starting_position(self):
        for y, row in enumerate(self):
            for x, cell in enumerate(row):
                if cell == 0:
                    return x, y

    def reveal_cell(self, x, y):
        cell_value = self[y][x]
        revealed = {(x, y, cell_value)}

        if cell_value == MINE:
            raise LostGameException('Touched a mine!')
        elif cell_value > 0:
            return revealed
        elif cell_value == 0:
            # reveal cells by DFS in eight directions
            return self._reveal_cell_dfs(x, y, revealed)

    def _reveal_cell_dfs(self, x, y, revealed):
        assert (x >= 0 and y >= 0)
        try:
            cell_value = self[y][x]
        except IndexError:
            return revealed

        logging.debug('Touching ({},{}) - {}'.format(x, y, cell_value))

        # only recurse if this isn't next to anything
        if cell_value == 0:
            pairs = eight_directions(x, y)
            logging.debug('Probing pairs: {}'.format(pairs))
            for py, px in pairs:
                try:
                    revealed_tuple = (px, py, self[py][px])
                except IndexError:
                    continue

                if not revealed_tuple in revealed:
                    revealed.add(revealed_tuple)
                    revealed = self._reveal_cell_dfs(px, py, revealed)
                else:
                    logging.debug('Already went to ({}, {})'.format(px, py))
        # elif cell_value == MINE:
        #     raise ValueError('Touched a mine during DFS!')
        else:
            revealed.add((x, y, cell_value))

        return revealed


def new_field(difficulty):
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


def eight_directions(x, y):
    pairs = [
        (y, x + 1),
        (y + 1, x),
        (y + 1, x + 1)
    ]

    if x > 0:
        pairs.extend((
            (y, x - 1),
            (y + 1, x - 1),
        ))

    if y > 0:
        if x > 0:
            pairs.append((y - 1, x - 1))

        pairs.extend((
            (y - 1, x),
            (y - 1, x + 1),
        ))

    return sorted(pairs, key=lambda k: k[0])


if __name__ == '__main__':
    print('Medium Board')
    print(new_field(1))
