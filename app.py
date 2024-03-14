from flask import Flask, request, jsonify, render_template
from ctransformers import AutoModelForCausalLM
import random

app = Flask(__name__)

# Initialisation du modèle
llms = {}
llms["mistral"] = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    gpu_layers=1,
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')
    llm = llms["mistral"]
    response = llm(user_message, stream=True, max_new_tokens=1000)
    
    message = ""
    for token in response:
        message += token

    return jsonify({'response': message})

def generate_mcq(contents: str, num_questions: int = 1, num_options: int = 2):
    llm = llms["mistral"]  # Accéder au modèle mistral dans le dictionnaire llms

    questions = []
    for _ in range(num_questions):
        response = llm(contents, stream=True, max_new_tokens=1000)  # Utiliser le modèle pour générer une réponse

        message = ""
        options = []
        for token in response:
            message += token
            options.append(token)
        question = f"Question: {message}\n"
        correct_option = options[-1]
        incorrect_options = options[:-1]
        options_all = [correct_option] + random.sample(incorrect_options, num_options - 1)
        questions.append({"question": question})
    return questions

@app.route('/qcm', methods=['POST'])
def qcm():
    data = request.get_json()
    user_message = data.get('message')
    contents = 'Give me a MCQ of 1 questions with 2 propositions each time and one correct answer on '+ str(user_message)
    mcqs = generate_mcq(contents)
    return jsonify({'mcqs': mcqs})



if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
