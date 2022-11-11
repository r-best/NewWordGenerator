from typing import Dict

from .dictionary import Dictionary
from .CMUDict import CMUDict


DICTIONARIES: Dict[str, Dictionary] = {
    "CMUDict": CMUDict
}
