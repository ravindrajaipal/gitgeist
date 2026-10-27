let presetsData = [];

function renderArtifact(item) {
  document.getElementById("commit-meta").innerHTML = `
    <strong>Commit:</strong> <code>${item.commit_hash}</code> &middot;
    <strong>Author:</strong> ${item.author} &middot;
    <strong>Date:</strong> <code>${item.date}</code><br/>
    <strong>File:</strong> <code>${item.file_path}</code> &middot;
    <strong>Message:</strong> ${item.message}
  `;
  document.getElementById("suspicious-line").textContent = item.suspicious_line;
  document.getElementById("seance-whisper").innerHTML = item.seance.whisper;
  document.getElementById("seance-source").textContent = item.seance.source;

  const risk = item.forecast.haunting_risk_pct;
  const [low, high] = item.forecast.range_10_90_pct;
  document.getElementById("risk-number").textContent = `${risk}%`;
  document.getElementById("risk-range").textContent = `Calibrated 10–90% Range: ${low}% – ${high}% (${item.forecast.model_backend})`;
  document.getElementById("risk-bar").style.width = `${Math.min(100, risk)}%`;
  document.getElementById("forecast-severity").textContent = item.forecast.severity;

  const driverList = document.getElementById("driver-list");
  driverList.innerHTML = "";
  item.forecast.top_drivers.forEach((d) => {
    const li = document.createElement("li");
    li.textContent = `⚡ ${d}`;
    driverList.appendChild(li);
  });

  document.getElementById("deleted-code").textContent = item.deleted_code;
  document.getElementById("ofrenda-tribute").textContent = item.ofrenda.tribute;
}

async function loadPresets() {
  const res = await fetch("/api/presets");
  const data = await res.json();
  presetsData = data.presets;
  document.getElementById("backend-pill").textContent = `⚡ Offline-First: Gemma 3 + ${data.forecaster_backend}`;

  const container = document.getElementById("preset-buttons");
  container.innerHTML = "";
  presetsData.forEach((item, idx) => {
    const btn = document.createElement("button");
    btn.className = `preset-card ${idx === 0 ? "active" : ""}`;
    btn.innerHTML = `
      <div><strong>#${item.commit_hash}</strong> (${item.forecast.haunting_risk_pct}% Risk)</div>
      <div style="font-size:0.84rem;color:#a59cc8;margin-top:0.25rem;">${item.message}</div>
    `;
    btn.onclick = () => {
      document.querySelectorAll(".preset-card").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      renderArtifact(item);
    };
    container.appendChild(btn);
  });

  if (presetsData.length > 0) {
    renderArtifact(presetsData[0]);
  }
}

document.getElementById("scan-repo-btn").addEventListener("click", async () => {
  const res = await fetch("/api/scan-local");
  const data = await res.json();
  if (data.artifacts && data.artifacts.length > 0) {
    presetsData = data.artifacts;
    renderArtifact(presetsData[0]);
  }
});

document.getElementById("custom-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    commit_hash: document.getElementById("f-hash").value,
    author: document.getElementById("f-author").value,
    commit_hour: parseInt(document.getElementById("f-hour").value, 10),
    cyclomatic_delta: parseFloat(document.getElementById("f-cyclo").value),
    days_since_last_touch: parseInt(document.getElementById("f-days").value, 10),
    test_coverage_pct: parseFloat(document.getElementById("f-cov").value),
    cpu_temp_spike_c: parseFloat(document.getElementById("f-temp").value),
    files_touched: parseInt(document.getElementById("f-files").value, 10),
    suspicious_line: document.getElementById("f-line").value,
    deleted_code: document.getElementById("f-deleted").value,
  };
  const res = await fetch("/api/seance", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  renderArtifact({
    ...data.artifact,
    forecast: data.forecast,
    seance: data.seance,
    ofrenda: data.ofrenda,
  });
});

loadPresets();
