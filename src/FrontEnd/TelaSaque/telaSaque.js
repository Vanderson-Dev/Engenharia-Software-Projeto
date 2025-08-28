document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('saque-form');

  form.addEventListener('submit', async function (event) {
    event.preventDefault(); // evita envio tradicional do formulário

    const valor = parseFloat(document.getElementById('valor').value);
    const senha = document.getElementById('senha').value;

    // ⚠️ Pegando CPF do usuário logado
    // Substitua isso pela forma que você armazena o CPF no login (localStorage, sessionStorage, etc.)
    const cpf = localStorage.getItem("cpf"); 
    if (!cpf) {
      alert("Usuário não logado. Faça login novamente.");
      return;
    }

    // Valida campos
    if (!valor || !senha) {
      alert("Preencha todos os campos!");
      return;
    }

    if (valor <= 0) {
      alert("O valor do saque deve ser maior que zero!");
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/saque', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, valor, senha })
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        alert(data.message);
        window.location.href = "../Home/home.html"; // redireciona para o menu/home
      } else {
        alert(data.message || "Não foi possível realizar o saque.");
      }

    } catch (error) {
      console.error("Erro na conexão com o servidor:", error);
      alert("Erro na conexão com o servidor.");
    }
  });
});
