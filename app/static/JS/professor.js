document.addEventListener("DOMContentLoaded", () => {

    let aulaSelecionada = null;

    // Função genérica para abrir o modal
    window.abrirModal = function (titulo, conteudoHTML, mostrarBotao = false) {
        document.getElementById("modalTitulo").innerText = titulo;
        document.getElementById("modalConteudo").innerHTML = conteudoHTML;

        const btn = document.getElementById("btnConfirmarPresenca");
        btn.style.display = mostrarBotao ? "block" : "none";

        document.getElementById("modalOverlay").style.display = "flex";
    };

    // Função para fechar modal
    window.fecharModalPresenca = function () {
        document.getElementById("modalOverlay").style.display = "none";
    };

    // ================================
    // 1. Abrir modal com lista de aulas
    // ================================
    window.abrirModalPresenca = function () {

        fetch("/professores/presencas/aulas")
            .then(res => res.json())
            .then(data => {

                if (data.length === 0) {
                    abrirModal("Aulas Disponíveis", "<p>Nenhuma aula disponível.</p>");
                    return;
                }

                let html = "";

                data.forEach(aula => {
                    html += `
                        <div class="aula-card" onclick="carregarAlunos(${aula.id})">
                            <strong>${aula.tipo_aula}</strong><br>
                            ${aula.data}<br>
                            ${aula.hora}<br>
                            Estúdio: ${aula.estudio}
                        </div>
                        <hr>
                    `;
                });

                abrirModal("Aulas Disponíveis", html);
            });
    };

    // ==========================================
    // 2. Carregar alunos dentro do mesmo modal
    // ==========================================
window.carregarAlunos = function (aula_id) {

    aulaSelecionada = aula_id;

    fetch(`/professores/presencas/aula/${aula_id}`)
        .then(res => res.json())
        .then(data => {

            let html = "";

            if (data.alunos.length === 0) {
                html = "<p>Nenhum aluno inscrito nesta aula.</p>";
            } else {
                data.alunos.forEach(item => {
                    html += `
                        <div class="aluno-item">
                            <label>
                                <input type="checkbox" class="presenca-checkbox" value="${item.agendamento_id}" ${item.presenca === "presente" ? "checked" : ""}>
                                ${item.nome}
                            </label>
                        </div>
                    `;
                });
            }

            abrirModal("Lista de Presença", html, true);
        });
};


    // ====================================================
    // 3. Botão de salvar presença
    // ====================================================
    document.getElementById("btnConfirmarPresenca").addEventListener("click", () => {

        const selecionados = [...document.querySelectorAll(".presenca-checkbox")]
            .filter(c => c.checked)
            .map(c => c.value);

        fetch("/professores/presencas/salvar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                aula_id: aulaSelecionada,
                presentes: selecionados
            })
        })
        .then(() => {
            alert("Presença registrada com sucesso!");
            fecharModalPresenca();
        });
    });

});
