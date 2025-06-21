document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // Impede envio tradicional do formulário

    // Coleta os dados do formulário
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Cria ou seleciona elemento de status (mensagem)
    let statusMessage = document.getElementById("statusMessage");
    if (!statusMessage) {
      statusMessage = document.createElement("div");
      statusMessage.id = "statusMessage";
      statusMessage.className = "status-message";
      form.appendChild(statusMessage);
    }

    statusMessage.style.display = "none";

    try {
      // Simula envio para o backend
      const response = await enviarParaBackend(data);

      statusMessage.textContent = "Cadastro realizado com sucesso!";
      statusMessage.className = "status-message success";
      statusMessage.style.display = "block";

      form.reset(); // Limpa os campos
      statusMessage.scrollIntoView({ behavior: "smooth" });
    } catch (error) {
      statusMessage.textContent = "Erro ao cadastrar. Tente novamente.";
      statusMessage.className = "status-message error";
      statusMessage.style.display = "block";
      statusMessage.scrollIntoView({ behavior: "smooth" });
    }
  });

  async function enviarParaBackend(data) {
    console.log("Dados a serem enviados:", data);

    const response = await fetch("http://localhost:5000/api/clientes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Erro na requisição");
    }

    return response.json();
  }
});
