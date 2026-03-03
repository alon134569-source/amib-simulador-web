let pyodide = null;
let currentIndex = 0;
let totalQuestions = 0;

const el = (id) => document.getElementById(id);

function setHidden(id, hidden) {
  el(id).classList.toggle("hidden", hidden);
}

function setProgress(pct) {
  el("bar").style.width = `${pct}%`;
}

async function loadPy() {
  setHidden("loader", false);
  setHidden("setup", true);
  setHidden("quiz", true);
  setHidden("results", true);

  el("loaderStatus").textContent = "Cargando Pyodide…";
  setProgress(10);

  pyodide = await loadPyodide({
    stdout: (msg) => console.log(msg),
    stderr: (msg) => console.error(msg),
  });

  setProgress(35);
  el("loaderStatus").textContent = "Cargando código Python del simulador…";

  const pyCode = await fetch("simulator.py").then(r => r.text());
  await pyodide.runPythonAsync(pyCode);

  setProgress(70);
  el("loaderStatus").textContent = "Inicializando banco de preguntas…";

  const areas = pyodide.runPython("init_bank()");
  const jsAreas = areas.toJs(); // esto está OK porque es lista, no dict

  // Cargar temas
  const topicSel = el("topic");
  topicSel.innerHTML = "";
  jsAreas.forEach(a => {
    const opt = document.createElement("option");
    opt.value = a;
    opt.textContent = a;
    topicSel.appendChild(opt);
  });

  setProgress(100);
  el("loaderStatus").textContent = "Listo.";
  setTimeout(() => {
    setHidden("loader", true);
    setHidden("setup", false);
  }, 200);
}

function renderQuestion(q) {
  el("areaPill").textContent = q.area;
  el("progressText").textContent = `${q.i + 1}/${q.n}`;
  el("qText").textContent = q.text;

  const form = el("choices");
  form.innerHTML = "";

  q.choices.forEach((c, idx) => {
    const label = document.createElement("label");
    label.className = "choice";
    label.innerHTML = `
      <input type="radio" name="choice" value="${idx}" />
      <strong>${["A","B","C","D"][idx]})</strong> ${c}
    `;
    form.appendChild(label);
  });
}

function getSelectedChoice() {
  const checked = document.querySelector('input[name="choice"]:checked');
  if (!checked) return null;
  return parseInt(checked.value, 10);
}

async function start(mode, topic) {
  currentIndex = 0;
  const cmd = `start_quiz(${JSON.stringify(mode)}, ${JSON.stringify(topic || "")})`;
  totalQuestions = pyodide.runPython(cmd);

  setHidden("setup", true);
  setHidden("results", true);
  setHidden("quiz", false);

  const q = JSON.parse(pyodide.runPython(`get_question_json(${currentIndex})`));
  renderQuestion(q);
}

async function next(saveAsSkip=false) {
  const choice = saveAsSkip ? -1 : getSelectedChoice();
  if (!saveAsSkip && choice === null) {
    alert("Selecciona una opción o usa Saltar.");
    return;
  }

  pyodide.runPython(`answer_question(${currentIndex}, ${choice})`);

  currentIndex += 1;
  if (currentIndex >= totalQuestions) {
    await finish();
    return;
  }

  const q = JSON.parse(pyodide.runPython(`get_question_json(${currentIndex})`));
  renderQuestion(q);
}

function renderResults(summary) {
  el("scorePct").textContent = `${summary.pct.toFixed(2)}%`;
  el("scoreRaw").textContent = `${summary.correct}/${summary.total}`;
  el("scoreScale").textContent = `${summary.scale}`;

  // Desglose por área
  const byArea = el("byArea");
  byArea.innerHTML = "";
  const areas = Object.keys(summary.by_area).sort();
  areas.forEach(a => {
    const row = document.createElement("div");
    row.className = "rowline";
    const v = summary.by_area[a];
    row.innerHTML = `<div>${a}</div><div><strong>${v.correct}/${v.total}</strong> (${v.pct.toFixed(2)}%)</div>`;
    byArea.appendChild(row);
  });

  // Incorrectas
  const wrongs = el("wrongs");
  wrongs.innerHTML = "";
  if (!summary.wrongs || summary.wrongs.length === 0) {
    wrongs.innerHTML = `<div class="muted">¡Sin errores! 🔥</div>`;
    return;
  }

  summary.wrongs.forEach((w, idx) => {
    const box = document.createElement("div");
    box.className = "wrong";
    const your = (w.your === -1) ? "Saltada" : ["A","B","C","D"][w.your];
    const cor = ["A","B","C","D"][w.correct];

    const list = w.choices.map((c, i) => {
      const letter = ["A","B","C","D"][i];
      const mark = (i === w.correct) ? " ✅" : "";
      return `<div class="${i===w.correct ? 'ok':''}">${letter}) ${c}${mark}</div>`;
    }).join("");

    box.innerHTML = `
      <div class="muted">#${idx+1} • ${w.area}</div>
      <div style="margin:6px 0 10px 0;"><strong>${w.text}</strong></div>
      <div style="display:grid;gap:6px;margin-bottom:10px;">${list}</div>
      <div class="ans"><strong>Tu respuesta:</strong> ${your}</div>
      <div class="ok"><strong>Correcta:</strong> ${cor}</div>
      <div class="muted" style="margin-top:8px;"><strong>Explicación:</strong> ${w.explanation}</div>
    `;
    wrongs.appendChild(box);
  });
}

async function finish() {
  const summary = JSON.parse(pyodide.runPython("finish_json()"));

  setHidden("quiz", true);
  setHidden("results", false);

  renderResults(summary);
}

function bindUI() {
  const modeSel = el("mode");
  const topicRow = el("topicRow");

  function refreshTopicVisibility() {
    topicRow.classList.toggle("hidden", modeSel.value !== "topic");
  }
  refreshTopicVisibility();
  modeSel.addEventListener("change", refreshTopicVisibility);

  el("startBtn").addEventListener("click", () => {
    const mode = modeSel.value;
    const topic = el("topic").value;
    start(mode, topic);
  });

  el("nextBtn").addEventListener("click", () => next(false));
  el("skipBtn").addEventListener("click", () => next(true));
  el("quitBtn").addEventListener("click", () => finish());
  el("restartBtn").addEventListener("click", () => {
    setHidden("results", true);
    setHidden("setup", false);
  });
}

window.addEventListener("load", async () => {
  bindUI();
  await loadPy();
});
