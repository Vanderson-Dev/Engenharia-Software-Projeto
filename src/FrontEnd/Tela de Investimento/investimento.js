document.addEventListener('DOMContentLoaded', function() {
    const email = localStorage.getItem('email') || 'seu_email@exemplo.com';
    const senha = localStorage.getItem('senha') || 'sua_senha';

    // Atualiza saldo ao carregar
    fetch('http://localhost:5000/saldo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
    })
    .then(res => res.json())
    .then(data => {
        if (data.saldo !== undefined) {
            document.getElementById('saldo-atual').textContent = `R$ ${data.saldo.toFixed(2)}`;
        } else {
            document.getElementById('saldo-atual').textContent = 'R$ 0,00';
        }
    });

    // Função para investir
    document.querySelectorAll('.btn-investir').forEach(btn => {
        btn.addEventListener('click', function() {
            const valor = parseFloat(document.getElementById('valor-investir').value);
            const tipo = btn.getAttribute('data-tipo');
            if (!valor || valor <= 0) {
                alert('Digite um valor válido para investir.');
                return;
            }
            fetch('http://localhost:5000/investir', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, senha, valor, tipo })
            })
            .then(res => res.json())
            .then(data => {
                if (data.erro) {
                    alert(data.erro);
                } else {
                    alert(data.descricao + '\nNovo saldo: R$ ' + data.novo_saldo.toFixed(2));
                    // Atualiza saldo na tela
                    document.getElementById('saldo-atual').textContent = `R$ ${data.novo_saldo.toFixed(2)}`;
                }
            });
        });
    });
});