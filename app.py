# 3. Backend API (app.py)
# This script runs on your local computer to serve the model.
# It forces the use of local files to avoid caching issues.

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# --- Main script ---
model_dir = "./coding_doubts_gpt_new"

# Check if the model directory and its contents exist
if not os.path.exists(model_dir) or not os.listdir(model_dir):
    print(f"Error: Model directory '{model_dir}' not found or is empty.")
    print("Please ensure you have run the fine-tuning script and the folder is present.")
    exit()

print(f"Loading the fine-tuned model from: {model_dir}")
try:
    # Force loading from the local directory, ignoring any remote cache
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True)
    print("Model loaded successfully.")
except OSError as e:
    print(f"Error loading model: {e}")
    print("Please check that the 'coding_doubts_gpt_new' folder contains the model files (like 'pytorch_model.bin' and 'config.json') and is not nested inside another folder.")
    exit()


app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'Question is required.'}), 400

    input_text = f"Question: {question} Answer:"
    inputs = tokenizer(input_text, return_tensors="pt")
    
    # Generate the answer with increased length for code snippets
    outputs = model.generate(inputs.input_ids, max_length=300, num_return_sequences=1) 
    
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Clean up the output to only show the answer part
    answer_text = answer.split("Answer:")[-1].strip()
    
    return jsonify({'question': question, 'answer': answer_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

