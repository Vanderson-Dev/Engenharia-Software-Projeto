document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');

  form.addEventListener('submit', async function (event) {
    event.preventDefault(); // evita o envio tradicional do formulário

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validação simples
    if (!email || !password) {
      alert("Preencha todos os campos!");
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        alert("Login bem-sucedido!");

        // Armazena email e senha no localStorage para uso posterior
        localStorage.setItem("email", email);
        localStorage.setItem("senha", password);

        // Redireciona para o dashboard
        window.location.href = "../Dashboard/dashboard.html";
      } else {
        alert("E-mail ou senha inválidos.");
      }

    } catch (error) {
      console.error("Erro na conexão com o servidor:", error);
      alert("Erro na conexão com o servidor.");
    }
  });
});
