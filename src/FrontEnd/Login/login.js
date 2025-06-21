
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

   fetch('http://127.0.0.1:5000/login', { // URL do backend Flask
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password }) // envia dados no formato JSON
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("Login bem-sucedido!");
        window.location.href = "../Dashboard/dashboard.html";
      } else {
        alert("E-mail ou senha inválidos.");
      }
    })
    .catch(error => {
      console.error('Erro:', error);
      alert("Erro na conexão com o servidor.");
    });
  });
});
