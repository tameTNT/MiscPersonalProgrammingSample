import argparse
import os
from pathlib import Path

import requests

session_id = 'session='


class DayOutOfRangeError(Exception):
    pass


class OnlineInputNotFoundError(Exception):
    pass


def get_aoc_input(year: int, day: int, save_file_bool=True, get_test=False) -> str:
    """
    Function returns the input data for a specific date of the yearly Advent of Code (AoC) challenge.
    Output of function to be used within a solutions program\n
    :param year: year to find input for
    :param day: day to find input for
    :param save_file_bool: boolean of whether to save a .txt file of the input if requested from server
    :param get_test: if True, returns test data instead of real puzzle data
    :return: a string of the AoC input for the year and day requested
    """

    onedrive_path = Path(os.environ['USERPROFILE'], 'OneDrive')

    if day > 25:
        raise DayOutOfRangeError("day argument out of range of available days.")

    target_path = onedrive_path / 'Python Programming' / 'Advent of Code' / f'{year}' / 'Inputs'
    target_path.mkdir(exist_ok=True)  # creates required Inputs directory structure if it does not yet exist
    main_path = target_path / f'Day{day}.txt'
    test_path = target_path / f'Day{day}test.txt'

    try:
        if not get_test:
            with main_path.open() as fobj:
                print('Input file already exists - returning...')
                input_data = fobj.read()
                fobj.close()
        else:
            with test_path.open() as fobj:
                print('Input file already exists - returning TEST file...')
                input_data = fobj.read()
                fobj.close()

    except FileNotFoundError:
        print('Input file does not already exist - requesting...')

        input_data = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'Cookie': session_id}).text

        if ' 404 ' in input_data or 'countdown' in input_data:
            raise OnlineInputNotFoundError(
                f"request url ('https://adventofcode.com/{year}/day/{day}/input') not valid (might be requesting it too early).")

        if save_file_bool:
            with main_path.open('w+') as fobj:
                fobj.write(input_data)
                fobj.close()
            with test_path.open('w+') as fobj:
                fobj.write('PASTE TEST DATA INSTEAD OF THIS')
                fobj.close()
            print(f'New input data file (and test file) created at {main_path} (and {test_path})')

    return input_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', metavar='YYYY', type=int, required=True)
    parser.add_argument('-d', '--day', metavar='DD', type=int, required=True)
    parser.add_argument('-nof', '--no-file', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    
    args = parser.parse_args()
    
    puzzle_input = get_aoc_input(year=args.year, day=args.day, save_file_bool=not args.no_file, get_test=args.test)
    print(f'Input preview (first 100 characters - actual length {len(puzzle_input)}):\n' + puzzle_input[:100])
