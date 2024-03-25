from flask import Flask, request, jsonify, render_template
import time  # Importer le module time

app = Flask(__name__)

# Predefined responses
responses = [
    "Hello, how can I help you today ?",
    "Great! Before we proceed, can I ask about your current level of understanding in mathematics? Please rate yourself on a scale of 1 to 10.",
    "To evaluate your understanding in mathematics, I will ask you a few questions. Let's start with a simple one: What is the value of 2 + 2?",
    "Correct! Let's move on to the next question. What is the square root of 16?",
    "Well done! What is the value of (3i+4)^2 ?",
    "That is not correct. Let's work on imaginary numbers. "
]

# Variable to keep track of the last response index
current_response_index = -1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    time.sleep(2)  # Introduit un délai de 2 secondes avant de traiter la requête
    global current_response_index
    # Update the index to get the next response, loop back to 0 if at the end
    current_response_index = (current_response_index + 1) % len(responses)
    # Get the next response
    next_response = responses[current_response_index]
    # Return the response in the desired format
    return jsonify({'response': next_response})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
