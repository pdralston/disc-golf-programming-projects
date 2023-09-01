import csv
import sys
import numpy
import pandas as pd
import warnings

from openpyxl import load_workbook


warnings.simplefilter(action='ignore', category=UserWarning)

FORMAT = "{0} <--> {1}"
CALI = "CALI: {0}"
OUTPUT_FILENAME = "./results.csv"
NAME_HEADER = "Name"
BRACKET_NAME_HEADER = "Bracket_Name"
PAID_HEADER = "Paid"
ACE_HEADER = "Ace"
WINS_HEADER = "Wins"
TEAMS_HEADER = "Teams"
TEAMS_HEADER_COL = 6
DEFAULT_EXCEL_NAME = "Putting_League_Stat_Tracker_2022.xlsm"


class Randomizer:
    __players = []
    __teams = []
    __rng = numpy.random.default_rng()

    def __init__(self, players):
        for player in players:
            self.__players.append(player)

    def randomize(self):
        while len(self.__players) >= 2:
            player_one = self.__players.pop()
            n = len(self.__players)
            index = self.__rng.integers(0, n, 1)[0]
            if index >= n:
                self.__teams.append(FORMAT.format(
                    player_one, self.__players.pop()))
            else:
                self.__teams.append(FORMAT.format(
                    player_one, self.__players[index]))
                self.__players[index] = self.__players[n-1]
                self.__players.pop()
        if len(self.__players) > 0:
            self.__teams.append(CALI.format(self.__players.pop()))
        return self.__teams

    def print_results(self):
        try:
            with open(OUTPUT_FILENAME, 'w', newline="") as outfile:
                writer = csv.writer(outfile)
                for team in self.__teams:
                    writer.writerow([team])
                    print(team)
        except BaseException as e:
            print("Shit Broke: \n\tOutfile {0}\n\t{1}\n".format(
                OUTPUT_FILENAME, e))
        else:
            print("Results saved to ./results.csv")
        return self.__teams


def main():
    if len(sys.argv) == 2:
        excel_filename = sys.argv[1]
    else:
        excel_filename = input("Enter excel filename (default = {0}): ".format(DEFAULT_EXCEL_NAME))
    if not excel_filename:
        excel_filename = DEFAULT_EXCEL_NAME
    current_record = pd.read_excel(excel_filename, sheet_name=0)
    randomizer = Randomizer(current_record[BRACKET_NAME_HEADER])
    randomizer.randomize()
    randomizer.print_results()
    input("Press Enter to close")


if __name__ == "__main__":
    main()
