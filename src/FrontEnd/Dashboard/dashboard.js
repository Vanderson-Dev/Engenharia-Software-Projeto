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

// Gráfico de conversão de moedas
let moedasChart = null;

async function atualizarConversaoMoedas() {
  const email = localStorage.getItem("email");
  const senha = localStorage.getItem("senha");
  
  if (!email || !senha) return;
  
  try {
    const response = await fetch("http://localhost:5000/conversao-moedas", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, senha })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Atualizar valores textuais
      document.getElementById("valorUSD").textContent = data.conversoes.USD.toLocaleString("en-US", {
        style: "currency",
        currency: "USD"
      });
      
      document.getElementById("valorEUR").textContent = data.conversoes.EUR.toLocaleString("en-US", {
        style: "currency",
        currency: "EUR"
      });
      
      document.getElementById("valorGBP").textContent = data.conversoes.GBP.toLocaleString("en-US", {
        style: "currency",
        currency: "GBP"
      });
      
      // Atualizar hora da última atualização
      const agora = new Date();
      document.getElementById("horaAtualizacao").textContent = agora.toLocaleTimeString();
      
      // Criar ou atualizar gráfico
      const ctx = document.getElementById('graficoMoedas').getContext('2d');
      
      if (moedasChart) {
        moedasChart.data.datasets[0].data = [
          data.conversoes.USD,
          data.conversoes.EUR,
          data.conversoes.GBP
        ];
        moedasChart.update();
      } else {
        moedasChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Dólar (USD)', 'Euro (EUR)', 'Libra (GBP)'],
            datasets: [{
              label: 'Valor convertido',
              data: [
                data.conversoes.USD,
                data.conversoes.EUR,
                data.conversoes.GBP
              ],
              backgroundColor: [
                '#36a2eb',
                '#ff6384',
                '#ffcd56'
              ],
              borderColor: [
                '#36a2eb',
                '#ff6384',
                '#ffcd56'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: function(value) {
                    return value.toLocaleString('en-US', {
                      style: 'currency',
                      currency: 'USD'
                    });
                  }
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return context.dataset.label + ': ' + context.parsed.y.toLocaleString('en-US', {
                      style: 'currency',
                      currency: 'USD'
                    });
                  }
                }
              }
            }
          }
        });
      }
    }
  } catch (error) {
    console.error("Erro ao buscar conversão de moedas:", error);
  }
}

// Chamar a função quando a página carregar
document.addEventListener("DOMContentLoaded", function() {
  // ... código existente
  
  // Adicionar chamada para atualizar conversão de moedas
  atualizarConversaoMoedas();
  
  // Atualizar a cada 5 minutos
  setInterval(atualizarConversaoMoedas, 5 * 60 * 1000);
});