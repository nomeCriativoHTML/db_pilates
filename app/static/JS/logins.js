const passwordInput = document.querySelector('#password');
const togglePassword = document.querySelector('.toggle-password');
const loginForm = document.getElementById('loginForm');
const userButtons = document.querySelectorAll(".user-btn");

let tipoLogin = null;

// Função para mostrar mensagens estilizadas
function showMessage(text, type = "success", duration = 3000) {
    const container = document.getElementById("message-container");
    container.innerHTML = `<div class="message ${type}">${text}</div>`;
    const messageEl = container.querySelector(".message");

    // Força animação
    setTimeout(() => messageEl.classList.add("show"), 10);

    // Sumir depois de X segundos
    setTimeout(() => {
        messageEl.classList.remove("show");
        setTimeout(() => container.innerHTML = "", 500);
    }, duration);
}

// Selecionar tipo de usuário
userButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        userButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        if (btn.id === "btnAluno") tipoLogin = "aluno";
        if (btn.id === "btnProfessor") tipoLogin = "professor";
        if (btn.id === "btnAdmin") tipoLogin = "admin";

        loginForm.setAttribute("action", `/login/${tipoLogin}`);
    });
});

// Mostrar/ocultar senha
togglePassword.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    togglePassword.classList.toggle('fa-eye-slash');
});

// Enviar login
loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    if (!tipoLogin) {
        showMessage("Escolha o tipo de usuário.", "error");
        return;
    }

    const email = document.getElementById('email').value;
    const password = passwordInput.value;

    if (!email || !password) {
        showMessage('Preencha todos os campos!', "error");
        return;
    }

    let endpoint = `/login/${tipoLogin}`;

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ email, password })
        });

        const result = await response.json();

        if (!response.ok) {
            showMessage(result.error || "Credenciais inválidas", "error");
            return;
        }

        showMessage(result.message || "Login realizado!", "success");

        // Redireciona após 1,5s para a rota correta
        setTimeout(() => {
            if (tipoLogin === "aluno") {
                window.location.href = "/login/aluno";
            } else if (tipoLogin === "professor") {
                window.location.href = "/login/professor/dashboard";
            } else if (tipoLogin === "admin") {
                window.location.href = "/login/admin";
            }
        }, 1500);

    } catch (error) {
        console.error("Erro ao fazer login:", error);
        showMessage("Erro inesperado. Tente novamente.", "error");
    }
});
