document.addEventListener("DOMContentLoaded", async () => {
  const tbody = document.getElementById("transacoes-tbody");
  const email = localStorage.getItem("email");
  const senha = localStorage.getItem("senha");

  if (!email || !senha) {
    tbody.innerHTML = `<tr><td colspan="4">Você precisa estar logado para ver o extrato.</td></tr>`;
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/extrato", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });

    const data = await response.json();

    if (!response.ok || !data.transacoes) {
      tbody.innerHTML = `<tr><td colspan="4">Erro ao carregar extrato.</td></tr>`;
      return;
    }

    if (data.transacoes.length  ===0) {
      tbody.innerHTML = `<tr><td colspan="4">Nenhuma transação encontrada.</td></tr>`;
      return;
    }

    tbody.innerHTML = "";
    data.transacoes.forEach(transacao => {
      const linha = document.createElement("tr");

      const dataFormatada = new Date(transacao.created_at).toLocaleDateString("pt-BR");
      const valorFormatado = parseFloat(transacao.amount).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
      });

      linha.innerHTML = `
        <td>${dataFormatada}</td>
        <td>${transacao.description || "-"}</td>
        <td>${transacao.type}</td>
        <td>${valorFormatado}</td>
      `;

      tbody.appendChild(linha);
    });
  } catch (error) {
    console.error("Erro ao buscar extrato:", error);
    tbody.innerHTML = `<tr><td colspan="4">Erro de conexão com o servidor.</td></tr>`;
  }
});
