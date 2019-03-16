import argparse
import os
import pandas as pd
import re


class QnA_Engine:
    """A class for a Q & A Lookup Table"""

    def __init__(self, filename):
        self._filename = os.path.abspath(filename)
        self._df = pd.read_csv(self._filename)


    def respond_to_question(self, txt):
        txt = txt.lower()
        for row in self._df.iterrows():
            idx, data = row
            regex = data['Question']
            m = re.search(regex, txt)
            if m is not None:
                answer = data['Answer']
                break
            else:
                answer = None
        return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='')
    parser.add_argument('-q', '--question', default='')
    args = parser.parse_args()

    if os.path.isfile(args.filename):
        QAE = QnA_Engine(args.filename)
        if len(args.question) > 0:
            answer = QAE.respond_to_question(args.question)
            print(answer)
