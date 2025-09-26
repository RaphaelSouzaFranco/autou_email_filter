# AutoU - Classificador de Emails

O **AutoU** é uma ferramenta web que classifica e-mails como **Produtivo** ou **Improdutivo** e sugere respostas automáticas apropriadas. Ele utiliza **Flask** no backend e consome a API da OpenAI para realizar a classificação.

# IMPORTANTE

**O deploy feito no Vercel leva um tempo até fazer a requisição ao backend hospedado no Render pela primeira tentativa de filtragem de mensagens. Após essa conexão feita, o processo torna-se mais rápido e eficiente**

---

## Demo

- Backend hospedado no Render: `https://autou-email-filter-7.onrender.com/`  
- Frontend hospedado no Vercel: `https://autou-email-filter-o4uj.vercel.app/`

---

## Funcionalidades

- Recebe texto do e-mail ou arquivo `.txt/.pdf`
- Processamento de linguagem natural (NLP) para limpeza do texto
- Classificação de e-mails em **Produtivo** ou **Improdutivo**
- Sugestão automática de resposta ao e-mail
- Interface moderna com efeito **glassmorphism** nos cards
- Integração segura com OpenAI API via backend (chave não exposta no frontend)
- Deploy backend no Render e frontend no Vercel

---

## Tecnologias Utilizadas

- Frontend: HTML, CSS (Glassmorphism), Bootstrap 5, JavaScript
- Backend: Python, Flask, Flask-CORS
- NLP: NLTK (stopwords, stemming)
- IA: OpenAI GPT-3.5 Turbo
- Hospedagem: Render (backend), Vercel (frontend)

---

## Estrutura do Projeto

```plaintext
autou_email_filter/
│
├─ backend/
│  ├─ app.py              # Backend em Flask
│  ├─ requirements.txt    # Dependências Python
│
├─ frontend/
│  ├─ index.html          # Página principal
│  ├─ results.html        # Página de resultados
│  ├─ styles/styles.css   # CSS personalizado
│  └─ scripts/openai_request.js # JS do frontend para interações
│
└─ README.md

```


