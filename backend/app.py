from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
from googletrans import Translator
import fitz  # PyMuPDF for PDF text extraction

app = Flask(__name__)
CORS(app)

# Load T5 model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)
translator = Translator()

# Function to summarize text
def summarize_with_t5(text, language='en', max_length=200, min_length=5):
    if language != 'en':
        text = translator.translate(text, dest='en').text
    input_text = "summarize: " + text
    input_tokenized = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_tokenized, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    if language != 'en':
        summary = translator.translate(summary, dest=language).text
    return summary

# Endpoint for text summarization
@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    user_input = data['text']
    selected_language = data.get('language', 'en')
    summary_length = data.get('length', 'short')

    # Define summary length parameters
    length_params = {
        'short': {'max_length': 50, 'min_length': 5},
        'medium': {'max_length': 100, 'min_length': 10},
        'detailed': {'max_length': 200, 'min_length': 70}
    }
    params = length_params.get(summary_length, {'max_length': 100, 'min_length': 5})
    
    # Generate summary
    summary = summarize_with_t5(user_input, language=selected_language, **params)
    return jsonify({'summary': summary,"length":params})

# Endpoint for PDF text extraction
@app.route('/api/extract-pdf', methods=['POST'])
def extract_pdf():
    file = request.files['file']
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Please upload a PDF.'}), 400

    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
