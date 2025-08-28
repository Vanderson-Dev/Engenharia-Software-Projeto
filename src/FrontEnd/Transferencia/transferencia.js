document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const cpf_destino = document.getElementById("cpf-destino").value;
    const valor = parseFloat(document.getElementById("valor").value);
    const email = localStorage.getItem("email");
    const senha = localStorage.getItem("senha");

    if (!email || !senha) {
      alert("Faça login novamente.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/transferencia", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, senha, cpf_destino, valor })
      });

      const resultado = await response.json();

      if (response.ok) {
        alert(resultado.mensagem);
        form.reset();
      } else {
        alert("Erro: " + resultado.mensagem);
      }
    } catch (error) {
      console.error("Erro ao conectar com o servidor:", error);
      alert("Erro de conexão.");
    }
  });
});
