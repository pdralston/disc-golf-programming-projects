import csv
import sys
import numpy

FORMAT = "{0} <--> {1}"
CALI = "CALI: {0}"
OUTPUT_FILENAME = "./results.csv"
NAME_HEADER = "Name"
BRACKET_NAME_HEADER = "Bracket_Name"
PAID_HEADER = "Paid"
ACE_HEADER = "Ace"
WINS_HEADER = "Wins"
TEAMS_HEADER = "Teams"


class Randomizer:
    __players = []
    __teams = []
    __rng = numpy.random.default_rng()

    def __init__(self, csv_file):
        with open(csv_file, 'r') as records:
            reader = csv.reader(records)
            # skip the header row
            next(reader)
            for row in reader:
                if not row[1]:
                    return
                self.__players.append(row[1])

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


def main():
    if len(sys.argv) < 2:
        print("Usage BagTag.py <infile>")
        return
    randomizer = Randomizer(sys.argv[1])
    randomizer.randomize()
    randomizer.print_results()


if __name__ == "__main__":
    main()
