// URL base da API
const API_URL = 'http://localhost:5000';

// Função para carregar os produtos na tabela
async function carregarProdutos() {
    try {
        const response = await fetch(`${API_URL}/produtos`);
        const produtos = await response.json();
        
        const tabela = document.querySelector('#saida table');
        // Limpa a tabela mantendo apenas o cabeçalho
        while (tabela.rows.length > 1) {
            tabela.deleteRow(1);
        }
        
        produtos.forEach(produto => {
            const row = tabela.insertRow();
            row.innerHTML = `
                <td><input type="radio" name="selecao" value="${produto.id}"></td>
                <td>${produto.nome}</td>
                <td>${produto.quantidade}</td>
                <td>R$ ${produto.preco.toFixed(2)}</td>
                <td>${produto.largura || ''}</td>
                <td>${produto.profundidade || ''}</td>
                <td>${produto.altura || ''}</td>
            `;
        });
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
    }
}

// Função para adicionar um novo produto
async function adicionarProduto() {
    const produto = {
        nome: document.getElementById('nome').value,
        quantidade: parseInt(document.getElementById('quantidade').value),
        preco: parseFloat(document.getElementById('preco').value),
        descricao: document.getElementById('descricao').value,
        largura: parseFloat(document.getElementById('largura').value),
        profundidade: parseFloat(document.getElementById('profundidade').value),
        altura: parseFloat(document.getElementById('altura').value)
    };

    try {
        const response = await fetch(`${API_URL}/produtos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produto)
        });
        
        if (response.ok) {
            limparFormulario();
            carregarProdutos();
            alert('Produto adicionado com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao adicionar produto:', error);
        alert('Erro ao adicionar produto');
    }
}

// Função para excluir um produto
async function excluirProduto() {
    const radioSelecionado = document.querySelector('input[name="selecao"]:checked');
    if (!radioSelecionado) {
        alert('Selecione um produto para excluir');
        return;
    }

    const id = radioSelecionado.value;
    try {
        const response = await fetch(`${API_URL}/produtos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            carregarProdutos();
            alert('Produto excluído com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao excluir produto:', error);
        alert('Erro ao excluir produto');
    }
}

// Função para editar um produto
async function editarProduto() {
    const radioSelecionado = document.querySelector('input[name="selecao"]:checked');
    if (!radioSelecionado) {
        alert('Selecione um produto para editar');
        return;
    }

    const id = radioSelecionado.value;
    const produto = {
        nome: document.getElementById('nome').value,
        quantidade: parseInt(document.getElementById('quantidade').value),
        preco: parseFloat(document.getElementById('preco').value),
        descricao: document.getElementById('descricao').value,
        largura: parseFloat(document.getElementById('largura').value),
        profundidade: parseFloat(document.getElementById('profundidade').value),
        altura: parseFloat(document.getElementById('altura').value)
    };

    try {
        const response = await fetch(`${API_URL}/produtos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produto)
        });
        
        if (response.ok) {
            limparFormulario();
            carregarProdutos();
            alert('Produto atualizado com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao atualizar produto:', error);
        alert('Erro ao atualizar produto');
    }
}

// Função auxiliar para limpar o formulário
function limparFormulario() {
    document.getElementById('nome').value = '';
    document.getElementById('quantidade').value = '';
    document.getElementById('preco').value = '';
    document.getElementById('descricao').value = '';
    document.getElementById('largura').value = '';
    document.getElementById('profundidade').value = '';
    document.getElementById('altura').value = '';
}

// Adiciona os event listeners aos botões
document.getElementById('btnEnviar').addEventListener('click', adicionarProduto);
document.getElementById('btnExcluir').addEventListener('click', excluirProduto);
document.getElementById('btnEditar').addEventListener('click', editarProduto);

// Carrega os produtos ao iniciar a página
carregarProdutos();