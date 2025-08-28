document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("saque-form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const valorInput = document.getElementById("valor");
    const senhaInput = document.getElementById("senha");

    const valor = parseFloat(valorInput.value);
    const senha = senhaInput.value;
    const email = localStorage.getItem("email"); // Recupera o e-mail do usuário logado

    if (!email) {
      alert("E-mail não encontrado. Faça login novamente.");
      return;
    }

    if (isNaN(valor) || valor < 10) {
      alert("O valor do saque deve ser de no mínimo R$10.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/saque", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ valor, email, senha })
      });

      const resultado = await response.json();

      if (response.ok) {
        alert(resultado.mensagem || "Saque realizado com sucesso!");
        valorInput.value = "";
        senhaInput.value = "";
      } else {
        alert("Erro: " + (resultado.mensagem || "Não foi possível realizar o saque."));
      }
    } catch (error) {
      console.error("Erro ao conectar com o servidor:", error);
      alert("Erro de conexão com o servidor.");
    }
  });
});
