import csv
import pandas as pd
import numpy as np

DEFAULT_FILE = "Doubles_Records.xlsx"
NAME_COL = "Name"
POOL_COL = "Pool"
A_POOL = "A"
B_POOL = "B"
TEAM_FORMAT = "{0} <==> {1}"
RESULTS = "Teams.csv"


def balance(a_players, b_players):
    len_a = len(a_players)
    len_b = len(b_players)
    if len_a == len_b:
        return a_players, b_players
    isEven = (len_a + len_b) % 2 == 0
    if isEven:
        if len_a > len_b:
            b_players, a_players = evenBalance(a_players, b_players)
            return a_players, b_players
        return evenBalance(b_players, a_players)
    else:
        return oddBalance(a_players, b_players)


def evenBalance(bigger_group, smaller_group):
    shift_amt = (len(bigger_group) - len(smaller_group)) // 2
    return shift(shift_amt, smaller_group, bigger_group)


def oddBalance(a_players, b_players):
    rng = np.random.default_rng()
    len_a, len_b = len(a_players), len(b_players)
    total_players = len_a + len_b
    if len_a > len_b:
        shift_amt = len_a - 1 - (total_players // 2)
        b_players, a_players = shift(shift_amt, b_players, a_players)
        return a_players, b_players
    shift_amt = len_b - (total_players // 2)
    return shift(shift_amt, a_players, b_players)


def shift(shift_amt, shift_to, shift_from):
    rng = np.random.default_rng()
    to_shift = rng.choice(shift_from, shift_amt, replace=False)
    return np.append(shift_to, to_shift), np.setdiff1d(shift_from, to_shift)


def randomize(a_players, b_players):
    if len(a_players) != len(b_players):
        b_players = np.append(b_players, "Cali")
    np.random.shuffle(a_players)
    np.random.shuffle(b_players)

    teams = np.column_stack((a_players, b_players))
    return teams


def print_results(teams):
    try:
        with open(RESULTS, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            print("<====TEAMS====>")
            counter = 0
            for team in teams:
                if counter == 2:
                    counter = 0
                    print()
                writer.writerow([team[0], "<==>", team[1]])
                print(TEAM_FORMAT.format(team[0], team[1]))
                counter = counter + 1
    except BaseException as e:
        print("Shit Broke: \n\tOutfile {0}\n\t{1}\n".format(RESULTS, e))
    else:
        print(f"\nResults saved to {RESULTS}.")


def main():
    excel_filename = (
        input(f'Enter excel file name (Default = "{DEFAULT_FILE}"): ') or DEFAULT_FILE
    )
    players = pd.read_excel(excel_filename, sheet_name=0, usecols=[NAME_COL, POOL_COL])
    a_players, b_players = balance(
        players[players[POOL_COL].isin(["A", "a"])][NAME_COL].to_numpy(),
        players[players[POOL_COL].isin(["B", "b"])][NAME_COL].to_numpy(),
    )
    print_results(randomize(a_players, b_players))
    input("Enter to close: ")


if __name__ == "__main__":
    main()
