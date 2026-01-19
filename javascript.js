let recommendations = [];
let costChart, co2Chart, scoreChart;

/* SECTION NAVIGATION */
function showSection(id) {
  document.querySelectorAll(".section").forEach(sec => {
    sec.style.display = "none";
  });
  document.getElementById(id).style.display = "block";
  window.scrollTo(0, 0);
}

/* DEFAULT LOAD */
showSection("homeSection");

/* FORM SUBMIT */
document.getElementById("productForm").addEventListener("submit", function (e) {
  e.preventDefault();

  recommendations = [
    { material: "Molded Pulp", cost: 210.50, co2: 2.10, score: 95.20 },
    { material: "Mushroom (Mycelium) Packaging", cost: 235.00, co2: 1.90, score: 96.00 },
    { material: "PLA (Polylactic Acid)", cost: 175.87, co2: 3.49, score: 91.69 },
    { material: "Recycled Cardboard", cost: 194.74, co2: 5.91, score: 90.55 }
  ];

  recommendations.sort((a, b) => b.score - a.score);

  document.getElementById("bestMaterial").innerText = recommendations[0].material;
  document.getElementById("bestScore").innerText = "Score: " + recommendations[0].score;

  document.getElementById("avgCost").innerText =
    "₹" + (recommendations.reduce((s, r) => s + r.cost, 0) / recommendations.length).toFixed(2);

  document.getElementById("avgCO2").innerText =
    (recommendations.reduce((s, r) => s + r.co2, 0) / recommendations.length).toFixed(2) + " kg";

  document.getElementById("avgScore").innerText =
    (recommendations.reduce((s, r) => s + r.score, 0) / recommendations.length).toFixed(2);

  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";

  recommendations.forEach((r, i) => {
    tbody.innerHTML += `
      <tr>
        <td>${i + 1}</td>
        <td>${r.material}</td>
        <td>₹${r.cost}</td>
        <td>${r.co2}</td>
        <td>${r.score}</td>
      </tr>`;
  });

  document.getElementById("resultTable").classList.remove("d-none");

  showSection("analyticsSection");
  setTimeout(drawCharts, 200);
});

/* CHARTS */
function drawCharts() {
  const labels = recommendations.map(r => r.material);

  if (costChart) costChart.destroy();
  if (co2Chart) co2Chart.destroy();
  if (scoreChart) scoreChart.destroy();

  costChart = new Chart(costChartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Cost (₹)",
        data: recommendations.map(r => r.cost),
        backgroundColor: "#8fb996"
      }]
    }
  });

  co2Chart = new Chart(co2ChartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "CO₂ (kg)",
        data: recommendations.map(r => r.co2),
        backgroundColor: "#88e397"
      }]
    }
  });

  scoreChart = new Chart(scoreChartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Sustainability Score",
        data: recommendations.map(r => r.score),
        backgroundColor: "#29ac55"
      }]
    }
  });
}

/* EXPORT CSV */
function exportCSV() {
  let csv = "Material,Cost,CO2,Score\n";
  recommendations.forEach(r => {
    csv += `${r.material},${r.cost},${r.co2},${r.score}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "EcoPackAI_Report.csv";
  link.click();
}

/* EXPORT PDF */
function exportPDF() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  doc.text("EcoPackAI Sustainability Report", 14, 15);

  doc.autoTable({
    startY: 25,
    head: [["Material", "Cost", "CO₂", "Score"]],
    body: recommendations.map(r => [r.material, r.cost, r.co2, r.score])
  });

  doc.save("EcoPackAI_Report.pdf");
}

  window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) {
      navbar.style.background = "#2e7d32";
    } else {
      navbar.style.background = "rgba(34, 139, 34, 0.75)";
    }
  });

