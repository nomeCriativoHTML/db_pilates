// --- Alternar formulários ao clicar nas categorias ---
document.querySelectorAll('.categoria-item').forEach(item => {
    item.addEventListener('click', () => {
        // Remove ativo de todos os botões
        document.querySelectorAll('.categoria-item').forEach(i => i.classList.remove('ativo'));
        // Adiciona ativo no clicado
        item.classList.add('ativo');

        // Oculta todos os formulários
        document.querySelectorAll('.formulario').forEach(f => f.classList.remove('ativo'));

        // Mostra o formulário correspondente (ex: data-form="aluno" => #form-aluno)
        const formId = `form-${item.dataset.tab}`;
        const form = document.getElementById(formId);
        if (form) form.classList.add('ativo');
    });
});

// --- Botão voltar ---
document.querySelector('.btn-voltar').addEventListener('click', () => window.history.back());

// --- Botão cancelar ---
document.querySelectorAll('.cancelar').forEach(btn => {
    btn.addEventListener('click', () => {
        if (confirm('Deseja cancelar o cadastro? Os dados não salvos serão perdidos.')) {
            window.location.href = '/home';
        }
    });
});

// --- Submit do formulário de aluno ---
document.getElementById('form-aluno').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    const payload = {
        nome: data.nome,
        cpf: data.cpf,
        email: data.email,
        senha: data.senha,
        telefone: data.telefone || null,
        data_nascimento: data.data_nascimento || null,
        status_pagamento: data.status_pagamento || 'pendente'
    };

    try {
        const response = await fetch('/alunos/cadastro/aluno', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Aluno cadastrado com sucesso!');
            this.reset();
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.error || 'Tente novamente.'));
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao cadastrar aluno. Verifique sua conexão.');
    }
});

// --- Submit do formulário de professor ---
document.getElementById('form-professor').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    const estudioId = data.estudio_id ? parseInt(data.estudio_id) : null;
    const ativo = data.ativo === 'on';

    const payload = {
        nome: data.nome,
        cref: data.cref,
        email: data.email,
        senha: data.senha,
        telefone: data.telefone || null,
        identificador: data.identificador || null,
        tipo_identificador: data.tipo_identificador || null,
        estudio_id: estudioId,
        ativo: ativo
    };

    if (!payload.nome || !payload.cref || !payload.email || !payload.senha) {
        alert('Preencha todos os campos obrigatórios!');
        return;
    }

    try {
        const response = await fetch('/professores/cadastro/professor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Professor cadastrado com sucesso!');
            this.reset();
            document.getElementById('ativo').checked = true;
        } else {
            alert('Erro: ' + (result.error || 'Tente novamente.'));
        }
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro ao cadastrar professor. Verifique sua conexão.');
    }
});

// --- Submit do formulário de estúdio ---
// --- Submit do formulário de estúdio ---
document.getElementById('form-estudio').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    // Montar payload para envio
    const payload = {
        nome: data.nome,
        endereco: data.endereco,
        cep: data.cep,
        telefone: data.telefone || null,
        email: data.email || null,
        capacidade_maxima: data.capacidade_maxima ? parseInt(data.capacidade_maxima) : 3
    };

    // Validação básica
    if (!payload.nome || !payload.endereco || !payload.cep) {
        alert('Preencha todos os campos obrigatórios!');
        return;
    }

    try {
        const response = await fetch('/estudios/cadastro/estudio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Estúdio cadastrado com sucesso!');
            this.reset();
        } else {
            alert('Erro: ' + (result.error || 'Tente novamente.'));
        }
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro ao cadastrar estúdio. Verifique sua conexão.');
    }
});

// --- Submit do formulário de atendimento (novo admin) ---
const formAtendimento = document.getElementById('form-atendimento');
if (formAtendimento) {
    formAtendimento.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

       const payload = {
            nome: data.nome,
            email: data.email,
            senha: data.senha,
            ativo: data.ativo === "true",
            tipo_admin: data.tipo_admin
        };


        try {
            const response = await fetch('/admins/cadastro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert('Administrador cadastrado com sucesso!');
                this.reset();
            } else {
                const error = await response.json();
                alert('Erro: ' + (error.error || 'Tente novamente.'));
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao cadastrar admin.');
        }
    });
}


// --- Máscaras CPF e Telefone ---
function mascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, '').slice(0, 11);
    if (valor.length <= 10) {
        input.value = valor.replace(/^(\d{0,2})(\d{0,4})(\d{0,4})$/, (_, ddd, p1, p2) =>
            `${ddd ? '(' + ddd : ''}${p1 ? ') ' + p1 : ''}${p2 ? '-' + p2 : ''}`
        );
    } else {
        input.value = valor.replace(/^(\d{0,2})(\d{0,5})(\d{0,4})$/, (_, ddd, p1, p2) =>
            `${ddd ? '(' + ddd : ''}${p1 ? ') ' + p1 : ''}${p2 ? '-' + p2 : ''}`
        );
    }
}

function mascaraCPF(input) {
    let valor = input.value.replace(/\D/g, '').slice(0, 11);
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
    valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
    valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = valor;
}

document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', e => mascaraTelefone(e.target));
});

const cpfInput = document.getElementById('cpf');
if (cpfInput) cpfInput.addEventListener('input', e => mascaraCPF(e.target));

const identificadorInput = document.getElementById('identificador');
const tipoIdentificador = document.getElementById('tipo_identificador');
if (identificadorInput && tipoIdentificador) {
    identificadorInput.addEventListener('input', e => {
        if (tipoIdentificador.value === 'cpf') mascaraCPF(e.target);
        else e.target.value = e.target.value.replace(/\D/g, '').slice(0, 15);
    });

    tipoIdentificador.addEventListener('change', () => (identificadorInput.value = ''));
}

// --- Carregar estúdios reais via API ---
async function carregarEstudios() {
    try {
        const response = await fetch('/estudios/'); // Faz a requisição para o endpoint de estúdios
        if (!response.ok) throw new Error('Falha ao carregar estúdios');

        const estudios = await response.json(); // Converte a resposta em JSON
        const select = document.getElementById('estudio_id');
        if (select) {
            // Limpa opções antigas, mantendo a primeira (placeholder)
            select.options.length = 1;

            estudios.forEach(estudio => {
                const option = document.createElement('option');
                option.value = estudio.id;       // valor do option = id do estúdio
                option.textContent = estudio.nome; // texto do option = nome do estúdio
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Erro ao carregar estúdios:', error);
    }
}

document.addEventListener('DOMContentLoaded', carregarEstudios);
