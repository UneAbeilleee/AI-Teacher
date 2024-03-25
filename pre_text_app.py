from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import time
from anki2 import FlashcardCreator
app = Flask(__name__)

# Configuration de la base de données SQLite (remplacez 'sqlite:///test.db' par le chemin de votre base de données)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Champ pour le rôle de l'utilisateur

# Predefined responses
responses = [
    "Hello student, what's your name ?",
    "Nice to meet you Jack, which year are you ?",
    "Alright ! In what subject do you need help ?",
    "And what is your level in this subject ?",
    "Great, in this chat I will  help you learn the concepts of CNN ! Are you ready ?",
    """In a convolutional neural network (CNN), what is the purpose of the pooling layer?<br>
Choose the correct answer:<br>
A) To reduce overfitting by introducing dropout<br>
B) To increase the number of feature maps<br>
C) To reduce the spatial dimensions of the input volume<br>
D) To increase the non-linearity of the model""",
    "Correct ! In a convolutional neural network (CNN), the pooling layer is used to reduce the spatial dimensions (width and height) of the input volume, while retaining important information. This helps in reducing the computational complexity of the network and controlling overfitting by reducing the number of parameters. Common pooling operations include max pooling and average pooling, where the maximum or average value in each pooling window is taken, respectively. Do you want more ?",
    """What is the role of the convolutional layer in a Convolutional Neural Network (CNN)?<br>
Choose the correct answer:<br>
A) It reduces the dimensionality of the data by extracting important features<br>
B) It applies an activation function to introduce non-linearity into the model<br>
C) It combines local features of the data using filters to create activation maps<br>
D) It adjusts the model's weights by minimizing a loss function using optimization techniques.""",
    "False ! It combines local features of the data using filters to create activation maps. The convolutional layer's primary role is to extract meaningful features from the input data by convolving it with learnable filters, creating activation maps that represent different aspects of the input. This process forms the foundation for the CNN's ability to learn and understand complex visual patterns in tasks such as image recognition and object detection.",
    "My pleasure ! Tell me if you need more information about CNN !"
]

# Variable to keep track of the last response index
current_response_index = -1  # Start at -1 so the first request gives the first response (index 0)

# Dummy user data (replace this with a proper user authentication mechanism)
users = {
    "jack": {"password": "password123"},
    "jill": {"password": "abc123"}
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return redirect(url_for('chatbot'))
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Récupérer le rôle depuis le formulaire
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        else:
            new_user = User(username=username, password=password, role=role)  # Ajouter le rôle à l'utilisateur
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/chatbot')
def chatbot():
    return render_template('index.html')
import random

@app.route('/chatbot', methods=['POST'])
def chatbot_post():
    global current_response_index  # Declare global to modify the variable outside the local scope
    # Update the index to get the next response, loop back to 0 if at the end
    current_response_index = (current_response_index + 1) % len(responses)
    # Get the next response
    next_response = responses[current_response_index]
    # Return the response in the desired format
    time.sleep(random.randint(3,10))
    return jsonify({'response': next_response})

def generate_anki_flashcard(message):
    # Your Python code to generate an Anki flashcard
    # Usage example
    flashcard_creator = FlashcardCreator(deck_name='CNN Flashcards', deck_id=123456789)

    # Flashcard info
    question = "In a convolutional neural network (CNN), what is the purpose of the pooling layer?"
    options = [
        "A) To reduce overfitting by introducing dropout",
        "B) To increase the number of feature maps",
        "C) To reduce the spatial dimensions of the input volume",
        "D) To increase the non-linearity of the model"
    ]
    correct_option = "Correct! In a convolutional neural network (CNN), the pooling layer is used to reduce the spatial dimensions (width and height) of the input volume, while retaining important information. This helps in reducing the computational complexity of the network and controlling overfitting by reducing the number of parameters. Common pooling operations include max pooling and average pooling, where the maximum or average value in each pooling window is taken, respectively."

    # Creating the flashcard
    quiz_flashcard = flashcard_creator.create_quiz_flashcard(question, options, correct_option)

    # Adding the flashcard to the deck
    flashcard_creator.add_flashcard(quiz_flashcard)

    # Exporting the deck to a file
    flashcard_creator.export_deck('cnn_flashcards.apkg')
    # This is just a placeholder function for your actual implementation
    print(f"Generating Anki flashcard with message: {message}")
    return True

@app.route('/generate_flashcard', methods=['POST'])
def handle_generate_flashcard():
    data = request.json
    success = generate_anki_flashcard(data['message'])
    return jsonify({'response': "Great"})
    return jsonify({'success': success, 'message': 'Flashcard generation initiated'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)
