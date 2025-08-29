document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('transacoes-tbody');

    const clienteIdParaTeste = 1;

    async function carregarExtrato() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/extrato/${clienteIdParaTeste}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Não foi possível carregar o extrato.');
            }
            
            const transacoes = await response.json();
            renderizarTransacoes(transacoes);

        } catch (error) {
            tbody.innerHTML = `<tr><td colspan="4" class="no-transacoes">${error.message}</td></tr>`;
        }
    }

    function renderizarTransacoes(transacoes) {
    
        tbody.innerHTML = '';

        if (transacoes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="no-transacoes">Nenhuma transação encontrada.</td></tr>';
            return;
        }

        transacoes.forEach(t => {
            const tr = document.createElement('tr');

        
            const isCredito = t.tipo.includes('deposito') || t.tipo.includes('recebida');
            const valorClasse = isCredito ? 'credito' : 'debito';
            const valorPrefixo = isCredito ? '+' : '-';

            tr.innerHTML = `
                <td>${t.data_formatada}</td>
                <td>${t.descricao || '-'}</td>
                <td style="text-transform: capitalize;">${t.tipo.replace(/_/g, ' ')}</td>
                <td class="valor ${valorClasse}">${valorPrefixo} ${parseFloat(t.valor).toFixed(2)}</td>
            `;
            tbody.appendChild(tr);
        });
    }


    carregarExtrato();
});
