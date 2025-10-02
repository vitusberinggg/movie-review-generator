
# --- Imports ---

import csv # Imports the CSV module to handle CSV files
import random

# --- Definitions ---

order = 2 # Sets the amount of previous words to consider for suggesting the next word
csv_path = "\static\data\IMDB dataset.csv"

# --- Functions ---

def remove_html_tags(string):

    """
    Removes HTML tags ("<" and ">").

    Arguments:
        "string": The string to process.
    
    Returns:
        The string without HTML tags.
    """

    out = [] # Creates an empty list to hold the output characters
    inside_tags = False # Creates a variable to track if we are inside HTML tags and initializes its value to False

    for character in string: # For each character in the string:

        if character == '<': # If the character is a "<":
            inside_tags = True # Set "inside_tags" to True
            continue # Skip to the next character

        if character == '>': # If the character is a ">":
            inside_tags = False # Set "inside_tags" to False
            continue # Skip to the next character

        if not inside_tags: # If we are not inside HTML tags:
            out.append(character) # Add the character to the output list

    return "".join(out) # Join the characters in the output list into a single string and return it

def clean_text(string):

    """
    Cleans the text by converting to lowercase, removing HTML tags, and replacing non-alphanumeric characters with spaces.

    Arguments:
        "string": The string to clean.

    Returns:
        The cleaned string.
    """

    string = string.lower() # Converts the string to lowercase
    string = remove_html_tags(string) # Removes HTML tags by calling function "remove_html_tags"
    out = [] # Creates an empty list to hold the output characters

    for character in string: # For each character in the string:

        if character.isalnum(): # If the character is alphanumeric (a letter or a digit):
            out.append(character) # Add the character to the output list

        else: # Else:
            out.append(' ') # Add a space to the output list
    
    cleaned = "".join(out) # Joins the characters in the output list into a single string and assigns it to variable "cleaned"

    parts = cleaned.split() # Splits the cleaned string into parts based on whitespace

    return " ".join(parts) # Joins the parts with a single space and returns the result

def tokenize(string):

    """
    Tokenizes the string into words.
    
    Arguments:
        "string": The string to tokenize.
        
    Returns:
        A list of tokens (words).
    """

    if not string: # If the string is empty:
        return [] # Return an empty list
    
    return string.split() # Split the string into parts based on whitespace and returns the list of parts

def build_markov_chain(reviews, order = order):

    """
    Builds a Markov chain dictionary and a list of valid starting words.

    Arguments:
        "reviews": A list of reviews (strings).
        "order": The number of previous words to consider for suggesting the next word.
    
    Returns:
        "chain": {tuple(previous words): [possible next words]}
        "starters": list of starting words
    """

    chain = {} # Creates an empty dictionary to hold the Markov chain
    starters = [] # Creates an empty list to hold valid starting sequences
    all_words = [] # Creates an empty list to hold all words in the dataset

    for review in reviews: # For each review in the list of reviews:

        tokens = tokenize(clean_text(review)) # Clean and tokenize the review text

        starters.append(tokens[0]) # Add the first token as a starter
        all_words.extend(tokens) # Add all tokens to the list of all words

        for token_index in range(len(tokens) - order): # For each token index in the number of tokens - "order" (so we don't go out of bounds):

            key = tuple(tokens[token_index:token_index + order]) # Create a dictionary key from the current token and the next "order - 1" tokens
            next_word = tokens[token_index + order] # Get the next word after the key

            if key not in chain: # If the key is not already in the chain dictionary:
                chain[key] = [] # Create a new entry in it for this key

            chain[key].append(next_word) # Add the next word to the list of possible continuations for this key

    return chain, starters, all_words

def load_reviews(csv_path, order = order):

    """

    
    """

    reviews = []

    with open(csv_path, "r", encoding = "utf-8") as data: # Opens the CSV file in read mode with UTF-8 encoding

        reader = csv.reader(data) # Reads all lines from the file
        next(reader)

        for row in reader:
            if row:
                reviews.append(row[0])

    return build_markov_chain(reviews, order = order)

def generate_text(chain, starters, all_words, current_tokens):

    """
    Generates the next word based on the current tokens.

    Arguments:
        "chain": The Markov chain dictionary.
        "all_words": A list of all words in the dataset.
        "current_tokens": The current list of tokens (words).
        "order": The number of previous words to consider for suggesting the next word.
    
    Returns:

    """
    key = tuple(current_tokens[-order:]) # Creates a tuple from the last "order" tokens in "current_tokens" to use as a key

    if key in chain: # If the key exists in the chain dictionary:
        next_word = random.choice(chain[key]) # Randomly select one of the possible next words for this key

    else: # Else:
        next_word = random.choice(all_words) # Randomly select any word from the list of all words

    return next_word