from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device="cuda")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()

    if 'message' not in data:
        return jsonify({'error': 'Missing "message" parameter'}), 400

    user_message = data['message']
    response = get_chatbot_response(user_message)

    return jsonify({'response': response})

def get_chatbot_response(user_message):
    messages = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ""}
    ]

    inputs = tokenizer.encode_plus(
        tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokenizer.mask_token)),
        **tokenizer.prepare_seq2seq_batch([m["content"] for m in messages], return_tensors="pt", truncation=True)
    )
    inputs["input_ids"] = inputs["input_ids"].to("cuda")

    outputs = model.generate(inputs["input_ids"], max_length=150, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
    chatbot_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return chatbot_response

if __name__ == '__main__':
    app.run(debug=True)
