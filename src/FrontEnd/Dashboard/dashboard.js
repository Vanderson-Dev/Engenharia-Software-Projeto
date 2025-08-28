document.addEventListener("DOMContentLoaded", async function () {
  const saldoSpan = document.querySelector(".valor");
  const saudacao = document.querySelector("header h1");
  const email = localStorage.getItem("email");
  const senha = localStorage.getItem("senha");

  if (!email || !senha) {
    saldoSpan.textContent = "Erro ao carregar saldo.";
    saudacao.textContent = "Bem-vindo ao Banco Digital";
    return;
  }

  // Buscar nome
  try {
    const nomeResponse = await fetch("http://localhost:5000/nome", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, senha })
    });

    const nomeData = await nomeResponse.json();

    if (nomeResponse.ok && nomeData.nome) {
      saudacao.textContent = `Olá, ${nomeData.nome}`;
    } else {
      saudacao.textContent = "Bem-vindo ao Banco Digital";
    }
  } catch (error) {
    console.error("Erro ao buscar nome:", error);
    saudacao.textContent = "Bem-vindo ao Banco Digital";
  }

  // Buscar saldo
  try {
    const saldoResponse = await fetch("http://localhost:5000/saldo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, senha })
    });

    const saldoData = await saldoResponse.json();

    if (saldoResponse.ok && saldoData.saldo !== undefined) {
      const saldoFormatado = parseFloat(saldoData.saldo).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
      });
      saldoSpan.textContent = saldoFormatado;
    } else {
      saldoSpan.textContent = "Erro ao carregar saldo.";
    }
  } catch (error) {
    console.error("Erro ao buscar saldo:", error);
    saldoSpan.textContent = "Erro de conexão.";
  }
});
