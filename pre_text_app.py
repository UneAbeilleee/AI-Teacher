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
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
db.create_all()

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Signup successful'})
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
