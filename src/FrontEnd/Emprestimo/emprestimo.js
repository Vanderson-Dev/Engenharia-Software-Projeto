document.getElementById("loan-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const valor = parseFloat(document.getElementById("valor").value);
  const juros = parseFloat(document.getElementById("juros").value) / 100;
  const parcelas = parseInt(document.getElementById("parcelas").value);

  if (isNaN(valor) || isNaN(juros) || isNaN(parcelas) || parcelas <= 0) {
    document.getElementById("resultado").innerHTML = "Preencha todos os campos corretamente!";
    return;
  }

  // Fórmula de cálculo de parcela (Tabela Price)
  const parcela = valor * (juros * Math.pow(1 + juros, parcelas)) / (Math.pow(1 + juros, parcelas) - 1);
  const total = parcela * parcelas;

  document.getElementById("resultado").innerHTML = `
    <p><strong>Valor do Empréstimo:</strong> R$ ${valor.toFixed(2)}</p>
    <p><strong>Taxa de Juros:</strong> ${(juros * 100).toFixed(2)}% ao mês</p>
    <p><strong>Parcelas:</strong> ${parcelas}x de R$ ${parcela.toFixed(2)}</p>
    <p><strong>Total a Pagar:</strong> R$ ${total.toFixed(2)}</p>
  `;
});
