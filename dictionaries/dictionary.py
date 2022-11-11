import os
import abc
import json
from typing import Tuple, List

FOLDERPATH = os.path.dirname(os.path.abspath(__file__))

class Dictionary(metaclass=abc.ABCMeta):
    """
    """
    words = None
    phonetics = None

    def __init__(self, recompute=False) -> None:
        self._precomputed_file_path = os.path.join(FOLDERPATH, type(self).__name__, "precomputed-IPA.json")
        if recompute or not os.path.isfile(self._precomputed_file_path):
            self.recompute()
        else:
            self._load()
    
    def recompute(self) -> None:
        """Performs 
        """
        self._compute()
        self._save()

    def _load(self) -> None:
        with open(os.path.join(self._precomputed_file_path), 'r', encoding='UTF-8') as fp:
            data = json.load(fp)
            self.phonetics = data["phonetics"]
            self.words = data["words"]
    
    def _save(self):
        with open(os.path.join(self._precomputed_file_path), 'w', encoding='UTF-8') as fp:
            json.dump({
                "phonetics": self.phonetics,
                "words": self.words
            }, fp, ensure_ascii=False)
    
    def _compute(self):
        return None


