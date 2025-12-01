function abrirModal(titulo, conteudoHTML) {
    document.getElementById("modalTitulo").innerHTML = titulo;
    document.getElementById("modalConteudo").innerHTML = conteudoHTML;

    document.getElementById("modalOverlay").style.display = "flex";
}

function fecharModal() {
    document.getElementById("modalOverlay").style.display = "none";
}

// ==========================
// ALUNOS
// ==========================
async function carregarAlunos() {
    const r = await fetch("/gestao/dados/alunos");
    const dados = await r.json();

    let html = "<ul>";
    dados.forEach(a => {
        html += `
        <li>
            <div class="item-info">
                <strong>ID:</strong> ${a.id}<br>
                <strong>Nome:</strong> ${a.nome}<br>
                <strong>Email:</strong> ${a.email}<br>
                <strong>Status:</strong> ${a.status_pagamento}
            </div>
            <div class="item-botoes">
                <button class="btn-editar" onclick="editarAluno(${a.id})">Editar</button>
                <button class="btn-excluir" onclick="excluirAluno(${a.id})">Excluir</button>
            </div>
        </li>`;
    });
    html += "</ul>";

    abrirModal("Lista de Alunos", html);
}


// ==========================
// PROFESSORES
// ==========================
async function carregarProfessores() {
    const r = await fetch("/gestao/dados/professores");
    const dados = await r.json();

    let html = "<ul>";
    dados.forEach(p => {
        html += `
        <li>
            <div class="item-info">
                <strong>ID:</strong> ${p.id}<br>
                <strong>Nome:</strong> ${p.nome}<br>
                <strong>Email:</strong> ${p.email || "-" }<br>
                <strong>CREF:</strong> ${p.cref || "-" }<br>
                <strong>Identificador:</strong> ${p.identificador || "-"}<br>
                <strong>Ativo:</strong> ${p.ativo ? "Sim" : "Não"}<br>
                <strong>Estúdio ID:</strong> ${p.estudio_id || "-"}
            </div>
            <div class="item-botoes">
                <button class="btn-editar" onclick="editarProfessor(${p.id})">Editar</button>
                <button class="btn-excluir" onclick="excluirProfessor(${p.id})">Excluir</button>
            </div>
        </li>`;
    });
    html += "</ul>";

    abrirModal("Lista de Professores", html);
}

// ==========================
// ESTÚDIOS
// ==========================
async function carregarEstudios() {
    const r = await fetch("/gestao/dados/estudios");
    const dados = await r.json();

    let html = "<ul>";
    dados.forEach(e => {
        html += `
        <li>
            <div class="item-info">
                <strong>ID:</strong> ${e.id}<br>
                <strong>Nome:</strong> ${e.nome || "-"}<br>
                <strong>Endereço:</strong> ${e.endereco || "-"}<br>
                <strong>CEP:</strong> ${e.cep || "-"}<br>
                <strong>Telefone:</strong> ${e.telefone || "-"}<br>
                <strong>Email:</strong> ${e.email || "-"}<br>
                <strong>Capacidade Máxima:</strong> ${e.capacidade_maxima || "-"}
            </div>
            <div class="item-botoes">
                <button class="btn-editar" onclick="editarEstudio(${e.id})">Editar</button>
                <button class="btn-excluir" onclick="excluirEstudio(${e.id})">Excluir</button>
            </div>
        </li>`;
    });
    html += "</ul>";

    abrirModal("Lista de Estúdios", html);
}

// ==========================
// PAGAMENTOS ATRASADOS
// ==========================
async function carregarPagamentosAtrasados() {
    const r = await fetch("/gestao/dados/pagamentos_atrasados");
    const dados = await r.json();

    let html = "<ul>";
    dados.forEach(a => {
        html += `
        <li>
            <div class="item-info">
                <strong>ID:</strong> ${a.id}<br>
                <strong>Nome:</strong> ${a.nome || "-"}<br>
                <strong>Email:</strong> ${a.email || "-"}<br>
                <strong>Status:</strong> ${a.status_pagamento || "Atrasado"}
            </div>
        </li>`;
    });
    html += "</ul>";

    abrirModal("Pagamentos Atrasados", html);
}



async function excluirAluno(id) {
    if (!confirm("Tem certeza que deseja excluir este aluno?")) return;

    const r = await fetch(`/gestao/aluno/${id}`, { method: "DELETE" });
    const res = await r.json();

    alert(res.mensagem || res.erro);

    fecharModal();
}

async function excluirProfessor(id) {
    if (!confirm("Tem certeza que deseja excluir este professor?")) return;

    const r = await fetch(`/gestao/professor/${id}`, { method: "DELETE" });
    const res = await r.json();

    alert(res.mensagem || res.erro);

    fecharModal();
}

async function excluirEstudio(id) {
    if (!confirm("Tem certeza que deseja excluir este estúdio?")) return;

    const r = await fetch(`/gestao/estudio/${id}`, { method: "DELETE" });
    const res = await r.json();

    alert(res.mensagem || res.erro);

    fecharModal();
}

function abrirModalEdicaoAluno(aluno) {
    const html = `
        <label>Nome:</label>
        <input id="editNome" class="modal-input" value="${aluno.nome}">
        
        <label>Email:</label>
        <input id="editEmail" class="modal-input" value="${aluno.email}">
        
        <label>CPF:</label>
        <input id="editCpf" class="modal-input" value="${aluno.cpf}">
        
        <label>Status Pagamento:</label>
        <select id="editStatus" class="modal-input">
            <option value="pendente" ${aluno.status_pagamento === "pendente" ? "selected" : ""}>Pendente</option>
            <option value="pago" ${aluno.status_pagamento === "pago" ? "selected" : ""}>Pago</option>
            <option value="atrasado" ${aluno.status_pagamento === "atrasado" ? "selected" : ""}>Atrasado</option>
        </select>

        <button class="btnSalvar" onclick="salvarEdicaoAluno(${aluno.id})">Salvar</button>
    `;

    abrirModal("Editar Aluno", html);
}

async function salvarEdicaoAluno(id) {
    const nome = document.getElementById("editNome").value;
    const email = document.getElementById("editEmail").value;
    const cpf = document.getElementById("editCpf").value;
    const status_pagamento = document.getElementById("editStatus").value;

    const payload = {
        nome,
        email,
        cpf,
        status_pagamento
    };

    const r = await fetch(`/gestao/aluno/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const res = await r.json();
    alert(res.mensagem || res.erro);

    fecharModal();
}

async function editarAluno(id) {
    const r = await fetch(`/gestao/dados/alunos`);
    const dados = await r.json();

    // Buscar aluno pelo ID
    const aluno = dados.find(a => a.id === id);

    if (!aluno) {
        alert("Aluno não encontrado!");
        return;
    }

    abrirModalEdicaoAluno(aluno);
}


function abrirModalEdicaoProfessor(professor) {
    const html = `
        <label>Nome:</label>
        <input id="editProfNome" class="modal-input" value="${professor.nome || ""}">

        <label>Email:</label>
        <input id="editProfEmail" class="modal-input" value="${professor.email || ""}">

        <label>CREF:</label>
        <input id="editProfCref" class="modal-input" value="${professor.cref || ""}">

        <label>Identificador:</label>
        <input id="editProfIdentificador" class="modal-input" value="${professor.identificador || ""}">

        <label>Tipo Identificador:</label>
        <select id="editProfTipoIdentificador" class="modal-input">
            <option value="cpf" ${professor.tipo_identificador === "cpf" ? "selected" : ""}>CPF</option>
            <option value="cref" ${professor.tipo_identificador === "cref" ? "selected" : ""}>CREF</option>
        </select>

        <label>Ativo:</label>
        <input id="editProfAtivo" type="checkbox" ${professor.ativo ? "checked" : ""}>

        <label>ID do Estúdio:</label>
        <input id="editProfEstudio" type="number" class="modal-input" value="${professor.estudio_id || ""}">

        <button class="btnSalvar" onclick="salvarEdicaoProfessor(${professor.id})">Salvar</button>
    `;

    abrirModal("Editar Professor", html);
}


async function salvarEdicaoProfessor(id) {
    let payload = {
        nome: document.getElementById("editProfNome").value,
        email: document.getElementById("editProfEmail").value,
        cref: document.getElementById("editProfCref").value,
        identificador: document.getElementById("editProfIdentificador").value,
        tipo_identificador: document.getElementById("editProfTipoIdentificador").value,
        ativo: document.getElementById("editProfAtivo").checked,
        estudio_id: document.getElementById("editProfEstudio").value
            ? Number(document.getElementById("editProfEstudio").value)
            : undefined
    };

    // Remove campos vazios ou indefinidos
    payload = Object.fromEntries(
        Object.entries(payload).filter(([_, v]) => v !== "" && v !== undefined)
    );

    const r = await fetch(`/gestao/professor/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const res = await r.json();
    alert(res.mensagem || res.erro);

    fecharModal();
}


async function editarProfessor(id) {
    const r = await fetch(`/gestao/dados/professores`);
    const dados = await r.json();

    const professor = dados.find(p => p.id === id);

    if (!professor) {
        alert("Professor não encontrado!");
        return;
    }

    abrirModalEdicaoProfessor(professor);
}


//FUNÇÃO PARA ABRIR MODAL DO ESTUDIO
function abrirModalEdicaoEstudio(estudio) {
    const html = `
        <label>Nome:</label>
        <input id="editEstNome" class="modal-input" value="${estudio.nome || ""}">

        <label>Endereço:</label>
        <input id="editEstEndereco" class="modal-input" value="${estudio.endereco || ""}">

        <label>CEP:</label>
        <input id="editEstCep" class="modal-input" value="${estudio.cep || ""}">

        <label>Telefone:</label>
        <input id="editEstTelefone" class="modal-input" value="${estudio.telefone || ""}">

        <label>Email:</label>
        <input id="editEstEmail" class="modal-input" value="${estudio.email || ""}">

        <label>Capacidade Máxima:</label>
        <input type="number" id="editEstCapacidade" class="modal-input" value="${estudio.capacidade_maxima || ""}">

        <button class="btnSalvar" onclick="salvarEdicaoEstudio(${estudio.id})">Salvar</button>
    `;

    abrirModal("Editar Estúdio", html);
}

//FUNÇÃO PARA SALVAR EDIÇÃO DO ESTUDIO
async function salvarEdicaoEstudio(id) {
    const payload = {
        nome: document.getElementById("editEstNome").value,
        endereco: document.getElementById("editEstEndereco").value,
        cep: document.getElementById("editEstCep").value,
        telefone: document.getElementById("editEstTelefone").value,
        email: document.getElementById("editEstEmail").value,
        capacidade_maxima: Number(document.getElementById("editEstCapacidade").value)
    };

    const r = await fetch(`/gestao/estudio/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const res = await r.json();
    alert(res.mensagem || res.erro);

    fecharModal();
}

//FUNÇÃO EDITAR ESTUDIO ID
async function editarEstudio(id) {
    const r = await fetch(`/gestao/dados/estudios`);
    const dados = await r.json();

    const estudio = dados.find(e => e.id === id);

    if (!estudio) {
        alert("Estúdio não encontrado!");
        return;
    }

    abrirModalEdicaoEstudio(estudio);
}

async function carregarAgenda() {
    const hoje = new Date().toISOString().split("T")[0];

    let horarios = [];

    try {
        const r = await fetch(`/agendas/dia/${hoje}`);
        
        // Se der erro 404, não quebra
        if (!r.ok) {
            console.warn("Nenhum horário encontrado para hoje.");
        } else {
            horarios = await r.json();
        }

    } catch (e) {
        console.error("Erro ao buscar horários:", e);
    }

    // --- Mesmo com erro, abrimos o modal! ---
    let html = `
        <button class="btnAdicionar" onclick="abrirModalCadastrarAgenda()">+ Novo horário</button>
        <ul>
    `;

    if (horarios.length === 0) {
        html += `<p>Nenhum horário cadastrado para hoje.</p>`;
    } else {
        horarios.forEach(h => {
            if (h.bloqueado) {
                html += `
                <li>
                    <div class="item-info">
                        <strong>${h.hora}</strong> — <span style="color:red;">BLOQUEADO</span><br>
                        <strong>Motivo:</strong> ${h.motivo_bloqueio}
                    </div>
                    <div class="item-botoes">
                        <button class="btn-editar" onclick="desbloquearHorario(${h.id})">Desbloquear</button>
                        <button class="btn-excluir" onclick="excluirHorario(${h.id})">Excluir</button>
                    </div>
                </li>`;
            } else {
                html += `
                <li>
                    <div class="item-info">
                        <strong>${h.hora}</strong> — ${h.tipo_aula}<br>
                        <strong>Professor:</strong> ${h.professor_id}<br>
                        <strong>Estúdio:</strong> ${h.estudio_id}<br>
                        <strong>Status:</strong> Disponível
                    </div>
                    <div class="item-botoes">
                        <button class="btn-editar" onclick="editarHorario(${h.id})">Editar</button>
                        <button class="btn-excluir" onclick="excluirHorario(${h.id})">Excluir</button>
                        <button class="btn-bloquear" onclick="abrirModalBloqueio(${h.id})">Bloquear</button>
                    </div>
                </li>`;
            }
        });
    }

    html += "</ul>";

    abrirModal("Agenda do Dia", html);
}


async function abrirModalCadastrarAgenda() {
    const professores = await fetch("/professores/").then(r => r.json());
    const estudios = await fetch("/estudios/").then(r => r.json());

    let opcoesProfessores = "";
    professores.forEach(p => {
        opcoesProfessores += `<option value="${p.id}">${p.nome}</option>`;
    });

    let opcoesEstudios = "";
    estudios.forEach(e => {
        opcoesEstudios += `<option value="${e.id}">${e.nome}</option>`;
    });

    const html = `
        <label>Data:</label>
        <input id="agdData" class="modal-input" type="date">

        <label>Hora:</label>
        <input id="agdHora" class="modal-input" type="time">

        <label>Estúdio:</label>
        <select id="agdEstudio" class="modal-input">
            ${opcoesEstudios}
        </select>

        <label>Professor:</label>
        <select id="agdProfessor" class="modal-input">
            ${opcoesProfessores}
        </select>

        <label>Tipo de Aula:</label>
        <input id="agdTipo" class="modal-input" type="text">

        <button class="btnSalvar" onclick="salvarNovaAgenda()">Salvar</button>
    `;

    abrirModal("Novo Horário", html);
}



async function salvarNovaAgenda() {
    const payload = {
        data: document.getElementById("agdData").value,
        hora: document.getElementById("agdHora").value,
        estudio_id: Number(document.getElementById("agdEstudio").value),
        professor_id: Number(document.getElementById("agdProfessor").value),
        tipo_aula: document.getElementById("agdTipo").value
    };

    const r = await fetch("/agendas/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const j = await r.json();
    alert(j.message || j.error);

    fecharModal();
}
function abrirModalBloqueio(id) {
    const html = `
        <label>Motivo do bloqueio:</label>
        <input id="motivoBloqueio" class="modal-input" type="text">

        <button class="btnSalvar" onclick="bloquearHorario(${id})">Bloquear</button>
    `;

    abrirModal("Bloquear Horário", html);
}


async function desbloquearHorario(id) {
    const r = await fetch(`/agendas/${id}/desbloquear`, {
        method: "PATCH"
    });

    const j = await r.json();
    alert(j.message || "Agenda desbloqueada com sucesso!");

    fecharModal();
}


async function excluirHorario(id) {
    if (!confirm("Excluir horário?")) return;

    const r = await fetch(`/agendas/${id}`, {
        method: "DELETE"
    });

    alert("Horário excluído.");
    fecharModal();
}


async function carregarTodasAgendas() {
    let agendas = [];

    try {
        const r = await fetch("/gestao/dados/agendas");
        agendas = await r.json();
    } catch (err) {
        console.error("Erro ao carregar agendas:", err);
        agendas = [];
    }

    let html = `
        <button class="btnAdicionar" onclick="abrirModalCadastrarAgenda()">+ Nova agenda</button>
        <table class="tabela-lista">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Hora</th>
                    <th>Professor</th>
                    <th>Estúdio</th>
                    <th>Tipo</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
    `;

    agendas.forEach(a => {
        html += `
        <tr>
            <td>${a.data}</td>
            <td>${a.hora}</td>
            <td>${a.professor_id}</td>
            <td>${a.estudio_id}</td>
            <td>${a.tipo_aula ?? "-"}</td>
            <td>${a.bloqueado ? "<span style='color:red;'>BLOQUEADO</span>" : "Ativo"}</td>
            <td>
                ${
                    !a.bloqueado
                    ? `<button class="btn-bloquear" onclick="abrirModalBloqueio(${a.id})">Bloquear</button>`
                    : `<button class="btn-desbloquear" onclick="desbloquearHorario(${a.id})">Desbloquear</button>`
                }
                <button class="btn-editar" onclick="editarHorario(${a.id})">Editar</button>
                <button class="btn-excluir" onclick="excluirHorario(${a.id})">Excluir</button>
            </td>
        </tr>
        `;
    });

    html += `</tbody></table>`;

    abrirModal("Todas as Agendas", html);
}

async function bloquearHorario(id) {
    const motivo = document.getElementById("motivoBloqueio").value;

    if (!motivo || motivo.trim() === "") {
        alert("Informe o motivo do bloqueio.");
        return;
    }

    const r = await fetch(`/agendas/${id}/bloquear`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ motivo })
    });

    const j = await r.json();

    if (!r.ok) {
        alert(j.detail || "Erro ao bloquear horário.");
        return;
    }

    alert("Horário bloqueado com sucesso!");

    fecharModal();

    // recarrega a agenda atual
    carregarAgenda();
}


async function editarHorario(id) {
    try {
        const r = await fetch(`/agendas/${id}`);
        const agenda = await r.json();

        // Carregar listas
        const professores = await fetch("/professores/").then(r => r.json());
        const estudios = await fetch("/estudios/").then(r => r.json());

        let opcoesProfessores = "";
        professores.forEach(p => {
            opcoesProfessores += `
                <option value="${p.id}" ${p.id === agenda.professor_id ? "selected" : ""}>
                    ${p.nome}
                </option>`;
        });

        let opcoesEstudios = "";
        estudios.forEach(e => {
            opcoesEstudios += `
                <option value="${e.id}" ${e.id === agenda.estudio_id ? "selected" : ""}>
                    ${e.nome}
                </option>`;
        });

        const html = `
            <label>Data:</label>
            <input id="editData" class="modal-input" type="date" value="${agenda.data}">

            <label>Hora:</label>
            <input id="editHora" class="modal-input" type="time" value="${agenda.hora}">

            <label>Estúdio:</label>
            <select id="editEstudio" class="modal-input">
                ${opcoesEstudios}
            </select>

            <label>Professor:</label>
            <select id="editProfessor" class="modal-input">
                ${opcoesProfessores}
            </select>

            <label>Tipo de Aula:</label>
            <input id="editTipo" class="modal-input" type="text" value="${agenda.tipo_aula ?? ""}">

            <button class="btnSalvar" onclick="atualizarHorario(${id})">Salvar Alterações</button>
        `;

        abrirModal("Editar Horário", html);

    } catch (err) {
        console.error(err);
        alert("Erro ao carregar dados da agenda.");
    }
}



async function atualizarHorario(id) {
    const payload = {
        data: document.getElementById("editData").value,
        hora: document.getElementById("editHora").value,
        estudio_id: Number(document.getElementById("editEstudio").value),
        professor_id: Number(document.getElementById("editProfessor").value),
        tipo_aula: document.getElementById("editTipo").value
    };

    try {
        const r = await fetch(`/agendas/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const j = await r.json();

        if (!r.ok) {
            alert(j.detail || "Erro ao atualizar horário.");
            return;
        }

        alert("Horário atualizado com sucesso!");

        fecharModal();
        carregarAgenda(); // atualiza a lista
    } catch (err) {
        console.error(err);
        alert("Erro ao atualizar horário.");
    }
}

