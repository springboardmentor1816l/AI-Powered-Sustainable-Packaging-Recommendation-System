const API_URL = "http://localhost:5000/api/predict";
const API_KEY = "ecopackai-secret-key";

let lastRecommendations = [];
const form = document.getElementById("productForm");
const loader = document.getElementById("loader");
const resultsCard = document.getElementById("results-card");
const tbody = document.getElementById("results-body");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  loader.classList.remove("d-none");
  resultsCard.classList.add("d-none");

  const payload = [{
    product_name: product_name.value,
    category: category.value,
    product_weight: parseFloat(product_weight.value),
    fragility_index: parseInt(fragility_index.value),
    shipping_type: shipping_type.value
  }];

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    lastRecommendations = data.recommendations;
    tbody.innerHTML = "";
    data.recommendations.forEach(r => {
      tbody.innerHTML += `
        <tr>
          <td>${r.rank}</td>
          <td>${r.material_name}</td>
          <td>$${r.predicted_cost.toFixed(2)}</td>
          <td>${r.predicted_co2.toFixed(3)}</td>
          <td>${(r.sustainability_score * 100).toFixed(1)}%</td>
        </tr>`;
    });

    loader.classList.add("d-none");
    resultsCard.classList.remove("d-none");

  } catch (err) {
    alert(err.message);
    loader.classList.add("d-none");
  }
});

function exportCSV() {
  if (!lastRecommendations.length) {
    alert("No data to export");
    return;
  }

  const headers = [
    "Rank",
    "Material Name",
    "Predicted Cost",
    "Predicted CO2",
    "Sustainability Score"
  ];

  const rows = lastRecommendations.map(r => [
    r.rank,
    r.material_name,
    r.predicted_cost.toFixed(3),
    r.predicted_co2.toFixed(4),
    r.sustainability_score.toFixed(4)
  ]);

  let csvContent =
    headers.join(",") + "\n" +
    rows.map(r => r.join(",")).join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "EcoPackAI_Recommendations.csv";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function exportPDF() {
  if (!lastRecommendations.length) {
    alert("No data to export");
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("EcoPackAI – Sustainability Recommendation Report", 14, 20);

  doc.setFontSize(11);
  doc.text("Generated using AI-driven packaging analysis", 14, 28);

  const tableData = lastRecommendations.map(r => [
    r.rank,
    r.material_name,
    `$${r.predicted_cost.toFixed(2)}`,
    r.predicted_co2.toFixed(3),
    `${(r.sustainability_score * 100).toFixed(1)}%`
  ]);

  doc.autoTable({
    startY: 35,
    head: [[
      "Rank",
      "Material",
      "Cost ($)",
      "CO₂",
      "Sustainability"
    ]],
    body: tableData,
    theme: "striped",
    headStyles: { fillColor: [46, 204, 113] },
    styles: { fontSize: 10 }
  });

  doc.save("EcoPackAI_Recommendations.pdf");
}

