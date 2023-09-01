import csv
import itertools
import sys
import numpy
import pandas as pd

BAG_TAG_TRACKER = "BagTags.xlsx"
NAME_COL = "Name"
PREV_TAG_COL = "Old_Tag"
SCORE_COL = "Round_Score"


class Player:

    def __init__(self, name, prev_tag, score):
        self.__name = name
        self.__prev_tag = sys.maxsize if pd.isna(prev_tag) else int(prev_tag)
        self.__score = sys.maxsize if pd.isna(score) else int(score)

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

    def __init__(self, current_registrants, bIsMonthly):
        self.__players = [Player(row[NAME_COL], row[PREV_TAG_COL], row[SCORE_COL])
                          for index, row in current_registrants.iterrows()]
        self.__available_tag_nums = [tag_num for tag_num in current_registrants[~current_registrants[PREV_TAG_COL].isnull(
        )][PREV_TAG_COL]] if bIsMonthly else numpy.arange(1, len(self.__players) + 1)

    def distribute(self):
        self.__available_tag_nums.sort()
        self.__players.sort()
        for new_tag, player in zip(self.__available_tag_nums, self.__players):
            player.new_tag = int(new_tag)

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
    if len(sys.argv) >= 2:
        excel_file = sys.argv[1]
    else:
        excel_file = input(
            "Enter excel filename (default = {0}): ".format(BAG_TAG_TRACKER))
    if not excel_file:
        excel_file = BAG_TAG_TRACKER
    if len(sys.argv) == 3:
        bIsMonthly = sys.argv[2].lower() in ("true", "t", "1")
    else:
        bIsMonthly = input(
            "Is this a monthly? T/F: ").lower() in ("true", "t", "1")

    current_registration = pd.read_excel(excel_file, sheet_name=0, usecols=[
                                         NAME_COL, PREV_TAG_COL, SCORE_COL])

    tagDistro = TagDistributor(
        current_registration[~current_registration[NAME_COL].isnull()], bIsMonthly)
    tagDistro.distribute()
    tagDistro.print_results()
    input("Press enter to close")


if __name__ == "__main__":
    main()
