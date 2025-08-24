// Aguarda o HTML ser completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', function () {

    // Seleciona o formulário e o elemento de mensagem
    const form = document.querySelector('form');
    const statusMessage = document.getElementById('status-message'); // Simplificado para pegar o div que já existe no HTML

    // Adiciona um "escutador" para o evento de submissão do formulário
    form.addEventListener('submit', async function (event) {
        // Impede que a página recarregue
        event.preventDefault();

        // Esconde mensagens antigas antes de uma nova tentativa
        statusMessage.textContent = '';
        statusMessage.className = 'status-message';

        // Coleta todos os dados dos campos do formulário
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            // **MUDANÇA 1: URL correta da nossa API**
            const response = await fetch('http://127.0.0.1:5000/api/cadastrar-cliente', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            // Pega a resposta do servidor em formato JSON
            const result = await response.json();

            // Se a resposta do servidor não for 'ok' (ex: erro 409), ele entra no 'catch'
            if (!response.ok) {
                // **MUDANÇA 2: Usa a mensagem de erro vinda do back-end**
                throw new Error(result.error || 'Erro ao processar a solicitação.');
            }

            // **MUDANÇA 3: Usa a mensagem de sucesso vinda do back-end**
            statusMessage.textContent = result.message;
            statusMessage.className = 'status-message success';
            form.reset(); // Limpa o formulário

        } catch (error) {
            // Exibe a mensagem de erro (que foi jogada pelo 'throw' acima)
            statusMessage.textContent = error.message;
            statusMessage.className = 'status-message error';
        }
    });
});