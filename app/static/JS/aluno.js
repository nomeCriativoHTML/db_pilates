
document.getElementById("form-aluno").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/alunos/cadastrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Cadastro realizado com sucesso!");
            window.location.href = "/login";  // Redireciona após cadastro
        } else {
            alert("Erro: " + (result.error || "Tente novamente."));
        }

    } catch (err) {
        console.error(err);
        alert("Erro ao enviar cadastro.");
    }
});



// --- Máscara de Telefone ---
function mascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, '').slice(0, 11);

    if (valor.length <= 10) {
        // Formato (XX) XXXX-XXXX
        input.value = valor.replace(
            /^(\d{0,2})(\d{0,4})(\d{0,4})$/,
            (_, ddd, p1, p2) =>
                `${ddd ? '(' + ddd : ''}${p1 ? ') ' + p1 : ''}${p2 ? '-' + p2 : ''}`
        );
    } else {
        // Formato (XX) XXXXX-XXXX
        input.value = valor.replace(
            /^(\d{0,2})(\d{0,5})(\d{0,4})$/,
            (_, ddd, p1, p2) =>
                `${ddd ? '(' + ddd : ''}${p1 ? ') ' + p1 : ''}${p2 ? '-' + p2 : ''}`
        );
    }
}

// --- Máscara de CPF ---
function mascaraCPF(input) {
    let valor = input.value.replace(/\D/g, '').slice(0, 11);

    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    input.value = valor;
}

// Aplica máscara em todos inputs tipo telefone
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', e => mascaraTelefone(e.target));
});


// --- Identificador: CPF ou Outro ---
const identificadorInput = document.getElementById('identificador');
const tipoIdentificador = document.getElementById('tipo_identificador');

if (identificadorInput && tipoIdentificador) {

    identificadorInput.addEventListener('input', e => {
        let valor = e.target.value;

        if (tipoIdentificador.value === "cpf") {
            mascaraCPF(e.target);
        } else {
            // Apenas números, limite de 15 caracteres
            e.target.value = valor.replace(/\D/g, '').slice(0, 15);
        }
    });

    tipoIdentificador.addEventListener('change', () => {
        identificadorInput.value = "";
    });
}

// CPF direto no campo "cpf"
const cpfInput = document.getElementById('cpf');
if (cpfInput) {
    cpfInput.addEventListener('input', e => mascaraCPF(e.target));
}


const passwordInput = document.getElementById('senha');
const togglePassword = document.getElementById('togglePassword');

// Mostrar/ocultar senha
togglePassword.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;

    togglePassword.classList.toggle('fa-eye-slash');
});



// --- CARREGAR PLANOS DINAMICAMENTE ---
async function carregarPlanos() {
    try {
        const response = await fetch("/planos/");
        if (!response.ok) throw new Error("Erro ao carregar planos.");

        const planos = await response.json();
        const container = document.getElementById("planosContainer");
        if (!container) return;
        container.innerHTML = "";

        planos.forEach(plano => {
            const card = document.createElement("div");
            card.className = "plano-card";
            card.onclick = () => abrirModalPlano(plano.id, "adquirir");

            card.innerHTML = `
                <h3>${plano.periodo}</h3>
                <p>Acesso a ${plano.frequencia} aulas por semana</p>
            `;

            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        alert("Erro ao carregar os planos. Tente novamente.");
    }
}

async function abrirModalPlano(planoId, modo = "adquirir") {
    // Fechar upgrade antes de abrir
    const modalUpgrade = document.getElementById("modalUpgrade");
    if (modalUpgrade) modalUpgrade.style.display = "none";

    try {
        const response = await fetch(`/planos/${planoId}`);
        if (!response.ok) throw new Error("Plano não encontrado.");

        const plano = await response.json();

        document.getElementById("modalTitulo").innerText = plano.periodo;
        document.getElementById("modalDescricao").innerText = `Acesso a ${plano.frequencia} aulas por semana`;
        document.getElementById("modalFrequencia").innerText = plano.frequencia;
        document.getElementById("modalValorMensal").innerText = plano.valor_mensal.toFixed(2);
        document.getElementById("modalValorTotal").innerText = plano.valor_total.toFixed(2);
        document.getElementById("modalCancelamento").innerText = plano.politica_cancelamento;

        const modal = document.getElementById("modalPlano");
        const btnAdquirir = document.querySelector(".btn-adquirir");

        if (modo === "detalhes") {
            btnAdquirir.style.display = "none";
        } else {
            btnAdquirir.style.display = "block";
            btnAdquirir.onclick = () => adquirirPlano(planoId);
        }

        modal.style.display = "flex";

    } catch (err) {
        console.error(err);
        alert("Erro ao carregar o plano.");
    }
}


function fecharModalPlano() {
    document.getElementById("modalPlano").style.display = "none";
}


// --- Adquirir ---
async function adquirirPlano(planoId) {
    const alunoId = document.body.dataset.alunoId;

    if (!alunoId) {
        alert("Aluno não identificado. Faça login novamente.");
        return;
    }

    try {
        const response = await fetch("/planos/assinar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                aluno_id: Number(alunoId),
                plano_id: Number(planoId)
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Plano assinado com sucesso!");
            window.location.reload();
        } else {
            alert("Erro: " + (result.detail || "Tente novamente."));
        }

    } catch (err) {
        console.error(err);
        alert("Erro ao assinar o plano. Tente novamente.");
    }
}

// --- Inicializa ---
document.addEventListener("DOMContentLoaded", () => {
    carregarPlanos();
});

async function abrirModalUpgrade() {
    try {
        const response = await fetch("/planos");
        const planos = await response.json();

        const lista = document.getElementById("listaPlanosUpgrade");
        lista.innerHTML = "";

        planos.forEach(p => {
            lista.innerHTML += `
                <div class="plano-upgrade-card">
                    <h3>${p.periodo}</h3>
                    <p><strong>Frequência:</strong> ${p.frequencia} aulas/semana</p>
                    <p><strong>Mês:</strong> R$ ${p.valor_mensal.toFixed(2)}</p>
                    <button onclick="abrirModalPlano(${p.id})">Ver detalhes</button>
                </div>
            `;
        });

        document.getElementById("modalUpgrade").style.display = "flex";

    } catch (err) {
        console.error("Erro ao carregar planos:", err);
        alert("Erro ao carregar planos.");
    }
}

function fecharModalUpgrade() {
    document.getElementById("modalUpgrade").style.display = "none";
}

window.addEventListener("click", (e) => {
    if (e.target === document.getElementById("modalUpgrade")) fecharModalUpgrade();
});

function abrirDetalhesPlano(id) {
    abrirModalPlano(id, "detalhes");
}

// ================================
// ABRIR MODAL DE DETALHES DA AULA
// ================================
function abrirModalAula(aulaId) {
    fetch(`/login/aluno/aula/${aulaId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar detalhes da aula");
            }
            return response.json();
        })
        .then(aula => {
            // Título do modal
            document.getElementById("modalAulaTitulo").textContent =
                `Aula de ${aula.tipo_aula} com ${aula.professor}`;

            // Conteúdo do modal
            document.getElementById("modalAulaConteudo").innerHTML = `
                <p><strong>Data:</strong> ${aula.data}</p>
                <p><strong>Hora:</strong> ${aula.hora}</p>
                <p><strong>Professor:</strong> ${aula.professor}</p>
                <p><strong>Estúdio:</strong> ${aula.estudio}</p>
                <p><strong>Tipo da Aula:</strong> ${aula.tipo_aula}</p>
                <p><strong>Vagas Restantes:</strong> ${aula.vagas_restantes}</p>
            `;

            // Configura o botão de confirmar presença
            const btn = document.getElementById("btnConfirmarPresenca");
            btn.onclick = function () {
                confirmarPresenca(aulaId);
            };

            // Exibe o modal
            document.getElementById("modalAula").style.display = "flex";
        })
        .catch(err => {
            alert("Erro: " + err.message);
        });
}

// ================================
// FECHAR MODAL
// ================================
function fecharModalAula() {
    document.getElementById("modalAula").style.display = "none";
}
// ================================
// CONFIRMAR PRESENÇA
// ================================
function confirmarPresenca(aulaId) {
    fetch(`/login/aluno/aula/confirmar/${aulaId}`, {  // <<--- endpoint correto
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            alert(data.message || "Inscrição confirmada com sucesso!");
            fecharModalAula();

            // Atualiza a página para refletir alterações
            window.location.reload();
        })
        .catch(err => {
            alert("Erro ao confirmar presença: " + err.message);
        });
}
