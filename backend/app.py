import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import openai
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from flask_cors import CORS

# Inicialização do Flask
app = Flask(
    __name__,
    template_folder="../frontend",   # pasta com index.html
    static_folder="../frontend",     # pasta com CSS/JS
    static_url_path="/frontend"
)

# Habilita CORS para aceitar requisições do frontend no Vercel
CORS(app)

# Config OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# NLP setup
nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))
stemmer = SnowballStemmer('portuguese')

def preprocess_text(text):
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    tokens = [word.lower() for word in text.split() if word.lower() not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

def classify_email(text):
    prompt = f"Classifique o email abaixo como Produtivo ou Improdutivo e sugira uma resposta curta apropriada:\n\n{text}\n\nFormato JSON: {{'category': '', 'reply': ''}}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    answer = response['choices'][0]['message']['content']
    try:
        result = eval(answer)
        category = result.get('category', 'Improdutivo')
        reply = result.get('reply', 'Obrigado pelo contato.')
    except:
        category = 'Improdutivo'
        reply = 'Obrigado pelo contato.'
    return category, reply

# Rota principal
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", error=None)

# Endpoint de classificação
@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    email_text = data.get("email_text", "").strip()
    if not email_text:
        return jsonify({"error": "Texto vazio"}), 400

    processed_text = preprocess_text(email_text)
    category, reply = classify_email(processed_text)

    return jsonify({"category": category, "reply": reply})

# Servir CSS/JS estáticos (opcional, só se precisar acessar direto)
@app.route('/frontend/<path:filename>')
def serve_frontend_file(filename):
    return send_from_directory('../frontend', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
