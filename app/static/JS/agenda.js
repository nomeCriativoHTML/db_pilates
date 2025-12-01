
document.querySelectorAll(".ver-menu button").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".ver-menu button").forEach(b => b.classList.remove("ativo"));
    btn.classList.add("ativo");
    alert(`Visualização: ${btn.textContent}`);
  });
});

document.querySelectorAll(".dia-semana button").forEach(day => {
  day.addEventListener("click", () => {
    document.querySelectorAll(".dia-semana button").forEach(d => d.classList.remove("ativo"));
    day.classList.add("ativo");
  });
});


document.querySelectorAll(".btn-agendar").forEach(btn => {
  btn.addEventListener("click", () => {
    alert("Aula agendada com sucesso!");
  });
});

document.querySelectorAll(".btn-detalhes").forEach(btn => {
  btn.addEventListener("click", () => {
    alert("Abrindo detalhes da aula...");
  });
});
