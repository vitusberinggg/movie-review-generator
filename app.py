
# --- Imports ---

from flask import Flask, render_template, request, jsonify # Imports necessary components from the Flask web framework
from markov import load_reviews, generate_text, tokenize, clean_text
import random

# --- Filepath ---

csv_path = "data/IMDB Dataset.csv"

# --- Model loading ---

print("\nLoading dataset and building model...")

chain_dictionary, starters, all_words = load_reviews(csv_path)

print("\nModel loaded.")

# --- Routes ---

app = Flask(__name__)

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/generate", methods = ["POST"])

def generate():

    """
    Handles text generation requests.

    Arguments:
        None
    
    Returns:
        JSON response with generated text.

    """

    payload = request.get_json() # Takes the POST request data and converts it from a JSON string to a dictionary
    text_input = payload.get("text", "") # Retrieves the value associated with the key "text" from the created payload dictionary, and if that key isn't found, returns an empty string

    current_tokens = tokenize(clean_text(text_input)) # Cleans and tokenizes the text with given functions and puts the result in "current_tokens"

    if not current_tokens: # If "current_tokens" is empty
        result = random.choice(starters) # Set "result" to a random starter word

    else: # Else:
        result = generate_text(chain_dictionary, all_words, current_tokens) # Call function "generate_text" and set "result" to whatever it returns

    return jsonify({"result": result}) # Creates a dictionary with key "result" and value "result", converts it into a JSON string and returns it to browser

if __name__ == "__main__": # If the script is run directly:
    app.run(host = "0.0.0.0", port = 5000, debug = True) # Start the Flask server with given specifications