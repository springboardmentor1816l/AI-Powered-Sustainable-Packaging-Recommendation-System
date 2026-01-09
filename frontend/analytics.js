// Same kind of data as backend response (NO dataset needed)
const recommendations = [
  { material: "Molded Pulp", cost: 45, co2: 1.2, score: 0.92 },
  { material: "Corrugated Board", cost: 30, co2: 1.8, score: 0.81 }
];

function drawCharts() {
  const labels = recommendations.map(r => r.material);

  new Chart(document.getElementById("costChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Cost",
        data: recommendations.map(r => r.cost)
      }]
    }
  });

  new Chart(document.getElementById("co2Chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "CO₂ Footprint",
        data: recommendations.map(r => r.co2)
      }]
    }
  });

  new Chart(document.getElementById("scoreChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Sustainability Score",
        data: recommendations.map(r => r.score)
      }]
    }
  });
}

drawCharts();

// CSV export
function exportCSV() {
  let csv = "Material,Cost,CO2,Score\n";
  recommendations.forEach(r => {
    csv += `${r.material},${r.cost},${r.co2},${r.score}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "ecopackai_analytics.csv";
  link.click();
}
