from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Predefined responses
responses = [
    "Hello Jack, how can I help you today ?",
    "Great, in this chat I will  help you learn the concepts of CNN ! Are you ready ?",
    """In a convolutional neural network (CNN), what is the purpose of the pooling layer?<br>
Choose the correct answer:<br>
A) To reduce overfitting by introducing dropout<br>
B) To increase the number of feature maps<br>
C) To reduce the spatial dimensions of the input volume<br>
D) To increase the non-linearity of the model""",
    "Correct ! In a convolutional neural network (CNN), the pooling layer is used to reduce the spatial dimensions (width and height) of the input volume, while retaining important information. This helps in reducing the computational complexity of the network and controlling overfitting by reducing the number of parameters. Common pooling operations include max pooling and average pooling, where the maximum or average value in each pooling window is taken, respectively."
]

# Variable to keep track of the last response index
current_response_index = -1  # Start at -1 so the first request gives the first response (index 0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    global current_response_index  # Declare global to modify the variable outside the local scope
    # Update the index to get the next response, loop back to 0 if at the end
    current_response_index = (current_response_index + 1) % len(responses)
    # Get the next response
    next_response = responses[current_response_index]
    # Return the response in the desired format
    return jsonify({'response': next_response})

# Other parts of your Flask app remain unchanged

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
