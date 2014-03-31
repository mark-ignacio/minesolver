#coding=utf-8
from field import MinesweeperField, new_field, eight_directions

UNKNOWN = -1
FLAG = '⚐'
QUESTION = '?'


def simple_solve(known_field):
    modifications_made = False
    # solves exact/sure matches of "number is 2, unknown is 2"
    for y, row in enumerate(known_field):
        for x, cell in enumerate(row):
            # first strategy: count the number of unknown spaces
            if isinstance(cell, int) and cell > 0:
                unknown_cells = get_unknown_around(x, y, known_field)
                # if cell value ==len(unknown), flag them all!
                if cell == len(unknown_cells):
                    for ax, ay in unknown_cells:
                        known_field[ay][ax] = FLAG
                        modifications_made = True

    return modifications_made


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

    for x, y, val in revealed:
        known[y][x] = val

    while True:
        if not simple_solve(known):
            break

    print('\n Known Board')
    for row in reversed(known):
        print('\t'.join(str(x) for x in row))

    print('\nField')
    print(field)


def main():
    field = new_field(0)
    solve(field)


if __name__ == '__main__':
    main()