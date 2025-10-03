
# --- Imports ---

import random
import pickle
from generate_chain_dictionary import order, pickle_path

# --- Functions ---

def generate_text(chain_dictionary, all_words, current_tokens):

    """
    Generates the next word based on the current tokens.

    Arguments:
        "chain_dictionary": The chain dictionary.
        "all_words": A list of all words in the dataset.
        "current_tokens": The current list of tokens (words).
        "order": The number of previous words to consider for suggesting the next word.
    
    Returns:

    """

    key = tuple(current_tokens[-order:]) # Creates a tuple from the last "order" tokens in "current_tokens" to use as a key

    if key in chain_dictionary: # If the key exists in the chain dictionary:
        next_word = random.choice(chain_dictionary[key]) # Randomly select one of the possible next words for this key

    else: # Else:
        next_word = random.choice(all_words) # Randomly select any word from the list of all words

    return next_word

def load_model():

    """
    Loads the chain dictionary, the starters, and all words from the pickle file.

    Arguments:
        None
    
    Returns:
        The loaded file.
    """

    with open(pickle_path, "rb") as file: # Opens the pickle file in read-binary mode
        return pickle.load(file) # Loads and returns the contents of the file