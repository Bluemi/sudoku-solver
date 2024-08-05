#!/usr/bin/env python3
import argparse
from pathlib import Path

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description='Solve sudoku puzzles')
    parser.add_argument('input_file', type=Path, help='The file to parse')

    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.input_file, 'r') as f:
        field = read_field(f)

    while np.min(field) == 0:
        print(field)
        print()
        possibilities = get_possibilities(field)
        n_possibilities = np.sum(possibilities, axis=-1)
        indices = field == 0
        min_n_possibilities = np.min(n_possibilities[indices])
        # print('possibilities[indices]:', n_possibilities[indices], sep='\n')
        # print('shape:', n_possibilities[indices].shape)
        # print(min_n_possibilities)

        if min_n_possibilities == 0:
            raise ValueError('Got a field without valid numbers')
        elif min_n_possibilities == 1:
            # print('n_possibilities:', n_possibilities, sep='\n')
            # print('n_possibilities == min_n_possibilities:', n_possibilities == min_n_possibilities, sep='\n')
            # print('where(n_possibilities == min_n_possibilities):', np.where(n_possibilities == min_n_possibilities), sep='\n')

            for y, x in zip(*np.where(n_possibilities == min_n_possibilities)):
                number = np.nonzero(possibilities[y, x])[0][0] + 1
                field[y, x] = number
        else:
            raise ValueError('ambiguous field')

    print(field)


def read_field(reader) -> np.ndarray:
    field = np.zeros((9, 9), dtype=np.uint8)
    y = 0
    while y < 9:
        line = reader.readline()
        x = 0
        found_something_in_line = False
        for c in line:
            if c in '0123456789':
                field[y, x] = int(c)
                x += 1
                found_something_in_line = True
            elif c in '-_.':
                x += 1
                found_something_in_line = True
        if found_something_in_line:
            y += 1
    return field


def get_possibilities(field: np.ndarray) -> np.ndarray:
    possibilities = np.ones((9, 9, 9), dtype=np.uint8)

    # exclude by known items
    for x in range(9):
        for y in range(9):
            if field[y, x] != 0:
                current_number = field[y, x]

                # in the same row / column the number is not possible anymore
                possibilities[y, :, current_number-1] = 0
                possibilities[:, x, current_number-1] = 0

                # in the same field, the number is not possible anymore
                x_field_index = x // 3
                y_field_index = y // 3
                possibilities[
                    y_field_index*3:(y_field_index+1)*3,
                    x_field_index*3:(x_field_index+1)*3,
                    current_number-1
                ] = 0

                # at the field itself only the known item is possible
                possibilities[y, x] = 0
                possibilities[y, x, current_number-1] = 1

    return possibilities


if __name__ == '__main__':
    main()

