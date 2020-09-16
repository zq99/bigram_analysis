# ------------------------
# BIGRAM ANALYSIS PROJECT
# ------------------------
# This project builds a report of all the bigrams appearing in a file
# containing 9,000 of the most common words in english and works out
# the number of times they appear at different positions in a word

import csv
import logging

import pandas as pd

log = logging.getLogger("bigram analysis")
logging.basicConfig(level=logging.INFO)


class Bigram:
    def __init__(self, bigram, position):
        self.bigram = bigram
        self.position = position

    def get_start_letter(self):
        return self.bigram[0]

    def __hash__(self):
        return hash((self.bigram, self.position))

    def __eq__(self, other):
        return (self.bigram, self.position) == (other.bigram, other.position)

    def __ne__(self, other):
        return not (self == other)


def print_results(results):
    # used for debugging the output prior to exporting
    for o in results:
        print(o.position, o.bigram, results[o])


def get_percentage(count, total):
    return round((float(count) / total), 2) if total > 0 else 0


def export_to_csv(bigram_position_frequency, bigram_total):
    # exports the bigram_position_frequency dictionary into a csv
    # the keys in the bigram_position_frequency dictionary are bigram objects
    # the values in the bigram_position_frequency dictionary is the number of times that bigram occurs
    # in that position in a word

    if len(bigram_position_frequency) == 0:
        log.info("nothing to export")
        return
    file_name = "results.csv"

    try:
        with open(file_name, mode='w', newline='', encoding="utf-8")as f:
            export_writer = csv.writer(f, delimiter=',')
            export_writer.writerow(
                ["bigram", "position", "frequency", "total", "percentage"])

            for key in bigram_position_frequency:
                percentage = get_percentage(bigram_position_frequency[key], bigram_total[key.bigram])
                export_writer.writerow([key.bigram,
                                        key.position,
                                        bigram_position_frequency[key],
                                        bigram_total[key.bigram],
                                        percentage
                                        ])
            log.info("export complete")
    except PermissionError:
        log.error("unable to create export file")


def generate_bigram_analysis(filename):
    # iterates over all the words in the english word file
    # and extracts the bigrams from each position of the word

    bigram_position_frequency = {}
    bigram_frequency = {}
    words_df = pd.read_csv(filename)

    for row in words_df.iterrows():
        word = str(row[1].values[0])
        for n in range(0, len(word) - 1):
            bigram = word[n:n + 2]
            obj = Bigram(bigram, n + 1)

            # tracking by position in word
            if obj not in bigram_position_frequency:
                bigram_position_frequency[obj] = 1
            else:
                bigram_position_frequency[obj] = bigram_position_frequency[obj] + 1

            # tracking totals across all positions
            if obj.bigram not in bigram_frequency:
                bigram_frequency[obj.bigram] = 1
            else:
                bigram_frequency[obj.bigram] = bigram_frequency[obj.bigram] + 1

    export_to_csv(bigram_position_frequency, bigram_frequency)


if __name__ == '__main__':
    generate_bigram_analysis("english_words.csv")
