
# --- Imports ---

from flask import Flask, render_template, request, jsonify # Imports necessary components from the Flask web framework
import os # Imports the os module to handle environment variables and file paths
from markov import load_reviews, generate_text, tokenize, clean_text, order
import random

# --- Definitions ---

app = Flask(__name__)

csv_path = os.environ.get('csv_path', 'static/data/IMDB Dataset.csv')

# --- Model loading ---

print("\nLoading dataset and building model...")

chain_dictionary, starters, all_words = load_reviews(csv_path)

print("\nModel loaded.")

# --- Routes ---

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/generate', methods = ['POST'])

def generate():

    """
    Handles text generation requests.

    Arguments:
        None
    
    Returns:
        JSON response with generated text.

    """

    payload = request.get_json()
    text_input = payload.get('text', '')
    current_tokens = tokenize(clean_text(text_input))

    if not current_tokens:
        result = random.choice(starters)

    else:
        result = generate_text(chain_dictionary, starters, all_words, current_tokens)

    return jsonify({'result': result})

if __name__ == "__main__": # If the script is run directly:
    app.run(host = '127.0.0.1', port = 5000, debug = True) # Start the Flask server with given specifications