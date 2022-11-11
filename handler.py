import re
import json
import random

import load_model
import utils
from dictionaries import DICTIONARIES


def handler(event, context):
    print("Incoming event:")
    print(event)

    err_builder = utils.ErrorResponseBuilder(context.aws_request_id)

    request = json.loads(event['body'])
    if err := validate_input(request):
        return err_builder.format_error_response(err[0], err[1])
    
    model = request['model']
    N = request['N']
    M = request['M']

    P, symbols = load_model.load_model(model, N)

    new_words = list()
    for i in range(M):
        new_words.append(generate(P, symbols, N=N))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "words": new_words
        }, ensure_ascii=False)
    }

def validate_input(req):
    if req['model'] is None or not isinstance(req['model'], str) or req['model'] == "":
        return 400, "Model must be a string"
    if req['model'] not in DICTIONARIES:
        return 400, f"Model {req['model']} does not exist"
    return None

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
        # print(new_word)
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
    return "".join(new_word[N-1:-1])
