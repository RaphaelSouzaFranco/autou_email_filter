document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const textarea = document.getElementById("email_text");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // previne envio tradicional

    const emailText = textarea.value.trim();
    if (!emailText) {
      alert("Digite algum texto para o email!");
      return;
    }

    // Monta o JSON para a API da OpenAI
    const requestData = {
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: "Você é um assistente que classifica emails como Produtivo ou Improdutivo e sugere uma resposta adequada."
        },
        {
          role: "user",
          content: emailText
        }
      ],
      temperature: 0.5,
      max_tokens: 200
    };

    try {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${YOUR_OPENAI_API_KEY}`
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();
      const reply = data.choices[0].message.content;

      // Aqui você pode mostrar o resultado na tela
      alert("Resposta gerada:\n\n" + reply);

    } catch (err) {
      console.error("Erro na requisição OpenAI:", err);
      alert("Erro ao gerar resposta automática.");
    }
  });
});
