from flask import Flask, request, jsonify, render_template
from ctransformers import AutoModelForCausalLM

app = Flask(__name__)

# Initialisation du modèle
llms = {}
llms["mistral"] = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    gpu_layers=1, # Ajustez ce nombre selon la disponibilité et les capacités de votre GPU
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')

    # Assurez-vous que llms["mistral"] est initialisé correctement avant d'utiliser cette fonction
    llm = llms["mistral"]

    # Génération de la réponse. Vous devrez peut-être adapter cette partie pour qu'elle fonctionne avec votre modèle spécifique.
    # La méthode de génération pourrait différer. Vérifiez la documentation de votre modèle pour les détails exacts.
    response = llm(user_message, stream=True, max_new_tokens=1000)
    
    message = ""
    for token in response:
        message += token

    return jsonify({'response': message})

if __name__ == '__main__':
    app.run(debug=True)
