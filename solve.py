#coding=utf-8
from field import MinesweeperField, new_field, eight_directions

UNKNOWN = -1
FLAG = '⚐'
QUESTION = '?'


def simple_solve(num_flags, known_field):
    reveal_orders = set()
    # solves exact/sure matches of "number is 2, unknown is 2"
    for y, row in enumerate(known_field):
        for x, cell in enumerate(row):
            # first strategy: count the number of unknown spaces
            if isinstance(cell, int) and cell > 0:
                unknown_cells = get_unknown_around(x, y, known_field)
                flagged_cells = get_flags_around(x, y, known_field)

                # if enough cells are flagged, order all unknowns to be touched
                if cell == len(flagged_cells):
                    reveal_orders = reveal_orders.union(unknown_cells)

                # if cell - flagged == unknown, flag them all!
                elif cell - len(flagged_cells) == len(unknown_cells):
                    for ax, ay in unknown_cells:
                        known_field[ay][ax] = FLAG
                        num_flags += 1

    return num_flags, reveal_orders


def get_value_around(field, x, y, value):
    unknowns = set()
    for py, px in eight_directions(x, y):
        try:
            if field[py][px] == value:
                unknowns.add((px, py))
        except IndexError:
            continue
    return unknowns


def get_unknown_around(x, y, field):
    return get_value_around(field, x, y, UNKNOWN)


def get_flags_around(x, y, field):
    return get_value_around(field, x, y, FLAG)


def solve(field):
    assert isinstance(field, MinesweeperField)
    known = []
    for y in range(field.height):
        row = [UNKNOWN for i in range(field.width)]
        known.append(row)
    x, y = field.get_starting_position()
    revealed = field.reveal_cell(x, y)
    for rx, ry, val in revealed:
        known[ry][rx] = val

    reveal_orders = set()
    num_flags = 0
    solved = True
    while True:
        for x, y in reveal_orders:
            revealed = field.reveal_cell(x, y)

            for rx, ry, val in revealed:
                known[ry][rx] = val

        reveal_orders = set()
        if not reveal_orders:
            num_flags, reveal_orders = simple_solve(num_flags, known)
        if not reveal_orders:
            solved = num_flags == field.num_mines
            break

    print('\nKnown Board')
    for row in reversed(known):
        print('\t'.join(str(x) for x in row))

    print('\nField')
    print(field)
    if solved:
        print('\nBoard solved!')


def main():
    field = new_field(0)
    solve(field)


if __name__ == '__main__':
    main()