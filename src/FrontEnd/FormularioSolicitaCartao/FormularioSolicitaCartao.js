// Seleção do tipo de cartão
document.querySelectorAll(".card-option").forEach((option) => {
  option.addEventListener("click", function () {
    document
      .querySelectorAll(".card-option")
      .forEach((opt) => opt.classList.remove("selected"));
    this.classList.add("selected");
    document.getElementById("cardType").value = this.getAttribute("data-value");
  });
});

// Mostrar/ocultar campo de "outro motivo"
document.getElementById("reason").addEventListener("change", function () {
  const otherReasonGroup = document.getElementById("otherReasonGroup");
  otherReasonGroup.style.display = this.value === "outro" ? "block" : "none";
  if (this.value !== "outro") {
    document.getElementById("otherReason").value = "";
  }
});

// Envio do formulário
document
  .getElementById("cardRequestForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const statusMessage = document.getElementById("statusMessage");
    statusMessage.style.display = "none";

    try {
      // Simulação de envio para o backend (substitua pela chamada real à API)
      const response = await sendToBackend(data);

      // Se chegou aqui, o envio foi bem-sucedido
      statusMessage.textContent =
        "Solicitação enviada com sucesso! Em breve entraremos em contato.";
      statusMessage.className = "status-message success";
      statusMessage.style.display = "block";

      // Limpar o formulário após o envio
      form.reset();
      document
        .querySelectorAll(".card-option")
        .forEach((opt) => opt.classList.remove("selected"));
      document.getElementById("cardType").value = "";
      document.getElementById("otherReasonGroup").style.display = "none";

      // Rolando a página para mostrar a mensagem de sucesso
      statusMessage.scrollIntoView({ behavior: "smooth" });
    } catch (error) {
      statusMessage.textContent =
        "Erro ao enviar solicitação. Por favor, tente novamente mais tarde.";
      statusMessage.className = "status-message error";
      statusMessage.style.display = "block";
      statusMessage.scrollIntoView({ behavior: "smooth" });
    }
  });

// Função para simular/envio para o backend Python
async function sendToBackend(data) {
  // Substitua esta parte pela chamada real à sua API Python
  console.log("Dados a serem enviados para o backend:", data);

  // Simulando uma requisição HTTP (substitua pelo seu endpoint real)
  const response = await fetch("http://localhost:5000/api/solicitar-cartao", {
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
