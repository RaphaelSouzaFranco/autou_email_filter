import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import openai
import re
import json
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

# Config OpenAI usando a nova interface
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NLP setup
nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))
stemmer = SnowballStemmer('portuguese')

def preprocess_text(text):
    # Remove caracteres especiais
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    # Remove stopwords e aplica stemming
    tokens = [stemmer.stem(word.lower()) for word in text.split() if word.lower() not in stop_words]
    return ' '.join(tokens)

def classify_email(text):
    prompt = (
        f"Você é um assistente especializado em classificar e-mails de trabalho.\n\n"
        f"Sua tarefa é classificar o email abaixo como **Produtivo** ou **Improdutivo**, "
        f"seguindo estas regras:\n"
        f"- **Produtivo:** emails que trazem informações importantes, tarefas, solicitações, decisões, resultados ou qualquer conteúdo que contribua para o trabalho.\n"
        f"- **Improdutivo:** emails irrelevantes, promocionais, triviais, pessoais, de spam ou que não agregam valor ao trabalho.\n\n"
        f"Para cada email, sugira uma **resposta curta e educada**, adequada ao contexto.\n\n"
        f"Exemplos de saída JSON correta:\n"
        f'{{"category": "Produtivo", "reply": "Obrigado, recebi sua mensagem e darei andamento."}}\n'
        f'{{"category": "Improdutivo", "reply": "Obrigado pelo envio, manterei em mente."}}\n\n'
        f"Email a classificar:\n{text}\n\n"
        f"Retorne **somente um JSON válido**, sem explicações ou textos adicionais, "
        f"no formato: {{\"category\": \"\", \"reply\": \"\"}}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content

        # Garante que o JSON seja válido
        result = json.loads(answer.replace("'", '"'))
        category = result.get('category', 'Improdutivo')
        reply = result.get('reply', 'Obrigado pelo contato.')

    except Exception as e:
        print("Erro ao processar OpenAI:", e)
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
