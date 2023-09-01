import csv
import itertools
import sys
import numpy


class Player:

    def __init__(self, name, prev_tag, score):
        self.__name = name
        self.__prev_tag = int(prev_tag)
        self.__score = int(score) if score.isnumeric() else sys.maxsize

    @property
    def name(self):
        return self.__name

    @property
    def prev_tag(self):
        return self.__prev_tag

    @property
    def score(self):
        return self.__score

    """
    A player should get a lower tag if their score is lower
    If the scores are equal than use the prev_tag to determine
    who gets the lower tag
    """

    def __lt__(self, other):
        if self.score == other.score:
            if not self.prev_tag:
                return False
            if not other.prev_tag:
                return True
            return self.prev_tag < other.prev_tag
        return self.score < other.score


class TagDistributor:
    __available_tag_nums = []
    __players = []

    def __init__(self, csv_file, bIsMonthly):
        with open(csv_file, 'r') as records:
            reader = csv.reader(records)
            # skip the header row
            header = next(reader)
            self.name_col = header.index("Name")
            self.prev_tag_col = header.index("Old_Tag")
            self.score_col = header.index("Round_Score")
            for row in reader:
                prev_tag = int(row[self.prev_tag_col]
                               ) if row[self.prev_tag_col] else sys.maxsize
                if bIsMonthly:
                    self.__available_tag_nums.append(prev_tag)
                self.__players.append(
                    Player(row[self.name_col], prev_tag, row[self.score_col]))
            if not bIsMonthly:
                self.__available_tag_nums = numpy.arange(
                    1, len(self.__players) + 1)

    def distribute(self):
        self.__available_tag_nums.sort()
        self.__players.sort()
        for new_tag, player in zip(self.__available_tag_nums, self.__players):
            player.new_tag = new_tag

    def print_results(self):
        filename = "./results.csv"
        try:
            with open(filename, 'w', newline="") as outfile:
                writer = csv.writer(outfile)
                print("Player".ljust(30), "| Round Score |", "New Tag\n")
                writer.writerow(["Player_Name", "Total_Score", "New_Tag"])
                for player in self.__players:
                    writer.writerow(
                        [
                            player.name,
                            player.score,
                            player.new_tag
                        ]
                    )
                    print(player.name.ljust(30),
                          "{0}".format(player.score).center(14),
                          "{0}".format(player.new_tag).center(7))
        except BaseException as e:
            print("Shit Broke: \n\tOutfile {0}\n\t{1}\n".format(filename, e))
        else:
            print("Results saved to ./results.csv")


def main():
    if len(sys.argv) < 3:
        print("Usage BagTag.py <infile> <bIsMonthly>")
        return
    bIsMonthly = sys.argv[2].lower() in ("true", "t", "1")
    tagDistro = TagDistributor(sys.argv[1], bIsMonthly)
    tagDistro.distribute()
    tagDistro.print_results()


if __name__ == "__main__":
    main()
