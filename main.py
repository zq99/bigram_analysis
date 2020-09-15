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


def export(results):
    # exports the results dictionary into a csv
    # the keys in the results dictionary are bigram objects
    # the values in the results dictionary is the number of times that bigram occurs
    # in that position in a word

    if len(results) == 0:
        log.info("nothing to export")
        return
    file_name = "results.csv"
    with open(file_name, mode='w', newline='', encoding="utf-8")as f:
        export_writer = csv.writer(f, delimiter=',')
        export_writer.writerow(
            ["bigram", "position", "frequency"])

        for key in results:
            export_writer.writerow([key.bigram, key.position, results[key]])


def generate_bigram_analysis():
    # iterates over all the words in the english word file
    # and extracts the bigrams from each position of the word

    unique = {}
    words_df = pd.read_csv("english_words.csv")

    for row in words_df.iterrows():
        word = str(row[1].values[0])
        for n in range(0, len(word) - 1):
            bigram = word[n:n + 2]
            bigram_object = Bigram(n + 1, bigram)
            if bigram_object not in unique:
                unique[bigram_object] = 1
            else:
                unique[bigram_object] = unique[bigram_object] + 1

    export(unique)


if __name__ == '__main__':
    generate_bigram_analysis()
