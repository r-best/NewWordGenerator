import os
import json

from pathlib import Path

from ..dictionary import Dictionary

FOLDERPATH = os.path.dirname(os.path.abspath(__file__))

class CMUDict(Dictionary):
    def _compute(self):
        """Loads the CMUDict dataset and transforms it from ARPAbet to IPA

        To do: Just write the transformed version to a file so you're not
        doing it every time, Bobby, that's just inefficient.
        """
        self.phonetics = list()
        self.words = list()
        arpa_to_ipa = load_ARPA_to_IPA_table()
        with open(os.path.join(FOLDERPATH, "./CMUDict-0.7b/cmudict-0.7b"), 'r') as fp:
            for line in fp.readlines():
                if line.startswith(';;;'): continue # Skip comment lines
                token, arpa = line.strip().split('  ')
                arpa = arpa.split(' ')
                for i,symbol in enumerate(arpa):
                    if symbol not in arpa_to_ipa:
                        print(f"ARPAbet symbol {symbol} not found in IPA translation table! (word: {token})")
                        continue
                    arpa[i] = arpa_to_ipa[symbol]
                self.words.append(token)
                self.phonetics.append(" ".join(arpa))

def load_ARPA_to_IPA_table():
    """Reads `cmudict_ARPAbet_to_IPA.csv` to create a mapping
    of ARPAbet symbols to their corresponding IPA notation
    """
    ret = dict()
    with open(os.path.join(FOLDERPATH, "./cmudict_ARPAbet_to_IPA.csv"), 'r', encoding='UTF-8') as fp:
        fp.readline() # Skip header line
        for line in fp.readlines():
            line = line.strip().split(',')
            ret[line[0]] = line[1]
    return ret
