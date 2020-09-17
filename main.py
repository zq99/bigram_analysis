# ------------------------
# BIGRAM ANALYSIS PROJECT
# ------------------------
# This project builds a report of all the bigrams appearing in a file
# containing 9,000 of the most common words in english and works out
# the number of times they appear at different positions in a word

import csv
import logging

import pandas as pd

log = logging.getLogger("text analysis")
logging.basicConfig(level=logging.INFO)


class Bigram:
    def __init__(self, text, position):
        self.text = text
        self.position = position

    def get_start_letter(self):
        return self.text[0]

    def __hash__(self):
        return hash((self.text, self.position))

    def __eq__(self, other):
        return (self.text, self.position) == (other.text, other.position)

    def __ne__(self, other):
        return not (self == other)


def print_results(results):
    # used for debugging the output prior to exporting
    for o in results:
        print(o.position, o.text, results[o])


def get_percentage(count, total):
    return round((float(count) / total), 2) if total > 0 else 0


def export_to_csv(bigram_position_frequency, bigram_total):
    # exports the bigram_position_frequency dictionary into a csv
    # the keys in the bigram_position_frequency dictionary are text objects
    # the values in the bigram_position_frequency dictionary is the number of times that text occurs
    # in that position in a word

    if len(bigram_position_frequency) == 0 or len(bigram_total) == 0:
        log.warning("data missing or incomplete - nothing exported")
        return
    file_name = "results.csv"

    try:
        with open(file_name, mode='w', newline='', encoding="utf-8")as f:
            export_writer = csv.writer(f, delimiter=',')
            export_writer.writerow(
                ["text", "position", "frequency", "total", "percentage"])

            for key in bigram_position_frequency:
                percentage = get_percentage(bigram_position_frequency[key], bigram_total[key.text])
                export_writer.writerow([key.text,
                                        key.position,
                                        bigram_position_frequency[key],
                                        bigram_total[key.text],
                                        percentage
                                        ])
            log.info("export complete")
    except PermissionError:
        log.error("unable to create export file")


def get_ngram(word, n):
    return word[n:n + 2]


def generate_bigram_analysis(filename):
    # iterates over all the words in the english word file
    # and extracts the bigrams from each position of the word

    bigram_position_frequency = {}
    bigram_frequency = {}
    words_df = pd.read_csv(filename)

    for row in words_df.iterrows():
        word = str(row[1].values[0])
        for n in range(0, len(word) - 1):

            bigram = Bigram(get_ngram(word,n), n + 1)

            # tracking by position in word
            if bigram not in bigram_position_frequency:
                bigram_position_frequency[bigram] = 1
            else:
                bigram_position_frequency[bigram] += 1

            # tracking totals across all positions
            if bigram.text not in bigram_frequency:
                bigram_frequency[bigram.text] = 1
            else:
                bigram_frequency[bigram.text] += 1

    export_to_csv(bigram_position_frequency, bigram_frequency)


if __name__ == '__main__':
    generate_bigram_analysis("english_words.csv")
