import os
import json

from dictionaries import DICTIONARIES

FOLDERPATH = os.path.dirname(os.path.abspath(__file__))

LOADED_DICTIONARIES = dict()

def load_model(model_name, N=2, force_rebuild=False):
    """Runs through the given list of examples of IPA word
    representations, and builds a probability distribution
    of how often a symbol is to occur based on some (N-1)
    symbols appearing before it (ngram model)
    """
    PREBUILT_FILEPATH = os.path.join(FOLDERPATH, "prebuilt-models", model_name, f"prebuilt-{model_name}-N{N}.json")
    
    # If we don't want to force rebuild and the prebuilt file exists, load it from disk
    if not force_rebuild and os.path.isfile(PREBUILT_FILEPATH):
        with open(PREBUILT_FILEPATH, 'r', encoding='UTF-8') as fp:
            data = json.load(fp)
        return data['P'], data['symbols']
    
    # Else, we build the model from scratch

    # Load the dictionary from disk if it's not already
    if model_name not in LOADED_DICTIONARIES:
        LOADED_DICTIONARIES[model_name] = DICTIONARIES[model_name]()

    ngrams = dict()
    n1grams = dict()
    symbols = set()
    symbols.add("<start>")
    for word in LOADED_DICTIONARIES[model_name].phonetics:
        if len(word) < N: continue

        # Move along the word with a sliding window, incrementing
        # the probabilities of the ngrams you find as you go
        word = word.split()
        word = ["<start>"]*(N-1) + word + ["<end>"]*(N-1)
        for i in range(N-2, len(word)):
            # Increment frequency of this index's (N-1)-gram
            # i.e. the N-1 symbols preceding this index
            n1gram = " ".join(word[i-(N-2):i+1])
            if n1gram not in n1grams:
                n1grams[n1gram] = 0
            n1grams[n1gram] += 1
            
            # Increment frequency of this index's N-gram
            # i.e. the (N-1)-gram plus this index's symbol
            ngram = f"{word[i-N+1]} {n1gram}"
            if ngram not in ngrams:
                ngrams[ngram] = 0
            ngrams[ngram] += 1

            # Add this symbol to the dictionary
            symbols.add(word[i])
    
    # Construct probability distribution from ngram frequencies
    # by going through (N-1)-grams and checking the probability
    # of each symbol occurring after it
    P = dict()
    for n1gram in n1grams:
        P[n1gram] = dict()
        for symbol in symbols:
            ngram = f"{n1gram} {symbol}"
            if ngram in ngrams:
                P[n1gram][symbol] = ngrams[ngram] / n1grams[n1gram]
    
    symbols = list(symbols)
    os.makedirs(os.path.dirname(PREBUILT_FILEPATH), exist_ok=True)
    with open(PREBUILT_FILEPATH, 'w', encoding='UTF-8') as fp:
        json.dump({
            "P": P,
            "symbols": symbols
        }, fp, ensure_ascii=False)
    return P, symbols
