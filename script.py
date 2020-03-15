import os
import random


def load_ARPA_to_IPA_table():
    """Reads `cmudict_ARPAbet_to_IPA.csv` to create a mapping
    of ARPAbet symbols to their corresponding IPA notation
    """
    ret = dict()
    with open("./cmudict_ARPAbet_to_IPA.csv", 'r', encoding='UTF-8') as fp:
        fp.readline() # Skip header line
        for line in fp.readlines():
            line = line.strip().split(',')
            ret[line[0]] = line[1]
    return ret


def load_cmudict():
    """Loads the CMUDict dataset and transforms it from ARPAbet to IPA

    To do: Just write the transformed version to a file so you're not
    doing it every time, Bobby, that's just inefficient.
    """
    X = list()
    Y = list()
    arpa_to_ipa = load_ARPA_to_IPA_table()
    with open("./CMUDict-0.7b/cmudict-0.7b", 'r') as fp:
        for line in fp.readlines():
            if line.startswith(';;;'): continue # Skip comment lines
            token, arpa = line.strip().split('  ')
            arpa = arpa.split(' ')
            for i,symbol in enumerate(arpa):
                if symbol not in arpa_to_ipa:
                    print(f"ARPAbet symbol {symbol} not found in IPA translation table! (word: {token})")
                    continue
                arpa[i] = arpa_to_ipa[symbol]
            Y.append(token)
            X.append(" ".join(arpa))
    return X, Y

def build_model(X, N=2):
    """Runs through the given list of examples of IPA word
    representations, and builds a probability distribution
    of how often a symbol is to occur based on some (N-1)
    symbols appearing before it (ngram model)
    """
    ngrams = dict()
    n1grams = dict()
    symbols = set()
    for word in X:
        if len(word) < N: continue

        word = f"<start> {word} <end>"

        # Move along the word with a sliding window, incrementing
        # the probabilities of the ngrams you find as you go
        word = word.split()
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
    
    return P, list(symbols)

def generate(P, symbols, N=2):
    """Takes in the probability distribution obtained from
    build_model and creates a new word from it
    """
    new_word = list()

    # Put N "<start>" tags at start of new word to
    # make indices work out properly
    for i in range(N-1):
        new_word.append("<start>")
    
    # Pull new tokens from the probability distribution
    # randomly until you get an "<end>" token
    while("<end>" not in new_word):
        rand = random.random()
        counter = 0

        # Get last (N-1) symbols in word
        lastN1Symbols = " ".join(new_word[-(N-1):])
        
        for i in range(len(symbols)):
            # Skip this symbol if it doesn't exist or has probability 0
            if lastN1Symbols not in P or \
                symbols[i] not in P[lastN1Symbols] or\
                P[lastN1Symbols][symbols[i]] == 0:
                continue
            # Increment the counter by the symbol's probability
            # and use the one that makes the sum cross the random number
            counter += P[lastN1Symbols][symbols[i]]
            if counter > rand:
                new_word.append(symbols[i])
                break
    return "".join(new_word[1:-1])


if __name__ == "__main__":
    X, _ = load_cmudict()
    P, symbols = build_model(X)
    while(True):
        input("Press enter to generate a new word:")
        print(generate(P, symbols))
