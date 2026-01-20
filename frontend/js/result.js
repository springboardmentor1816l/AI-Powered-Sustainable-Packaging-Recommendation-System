const data = JSON.parse(localStorage.getItem("prediction"));
console.log("Loaded prediction:", data);

if (!data || !data.ranked_materials) {
  alert("Invalid prediction data");
  throw new Error("Prediction missing");
}

const materials = data.ranked_materials;
const shipping = data.product.shipping_method;
const mlCategory = data.ml_recommendation;

// --------------------------------------------------
// 1️⃣ Choose BEST material safely
// --------------------------------------------------

// Strategy:
// - If ML label matches a material → use it
// - Else → use highest sustainability score

let selected =
  materials.find(m => m.material === mlCategory) ||
  materials.sort((a, b) => b.sustainability_score - a.sustainability_score)[0];

// --------------------------------------------------
// 2️⃣ Fill summary card
// --------------------------------------------------
document.getElementById("material").innerText = selected.material;
document.getElementById("cost").innerText = `₹ ${selected.predicted_cost}`;
document.getElementById("co2").innerText = `${selected.co2_impact} kg`;
document.getElementById("score").innerText = selected.sustainability_score;
document.getElementById("shipping").innerText = shipping;

// --------------------------------------------------
// 3️⃣ Prepare chart data
// --------------------------------------------------
const labels = materials.map(m => m.material);
const costData = materials.map(m => m.predicted_cost);
const co2Data = materials.map(m => m.co2_impact);
const scoreData = materials.map(m => m.sustainability_score);

const highlightIndex = labels.indexOf(selected.material);

// --------------------------------------------------
// 4️⃣ Cost Bar Chart
// --------------------------------------------------
new Chart(document.getElementById("costChart"), {
  type: "bar",
  data: {
    labels,
    datasets: [{
      label: "Cost (₹)",
      data: costData,
      backgroundColor: labels.map((_, i) =>
        i === highlightIndex ? "#2e7d32" : "#90caf9"
      )
    }]
  }
});

// --------------------------------------------------
// 5️⃣ CO₂ Pie Chart
// --------------------------------------------------
new Chart(document.getElementById("co2Chart"), {
  type: "pie",
  data: {
    labels,
    datasets: [{
      data: co2Data,
      backgroundColor: ["#81c784", "#ffb74d", "#e57373"]
    }]
  }
});

// --------------------------------------------------
// 6️⃣ Sustainability Radar Chart
// --------------------------------------------------
new Chart(document.getElementById("scoreChart"), {
  type: "radar",
  data: {
    labels,
    datasets: [{
      label: "Sustainability Score",
      data: scoreData,
      backgroundColor: "rgba(46,125,50,0.2)",
      borderColor: "#2e7d32"
    }]
  }
});

// --------------------------------------------------
// 7️⃣ Export CSV
// --------------------------------------------------
document.getElementById("exportCsv").onclick = () => {
  let csv = "Material,Cost,CO2,Sustainability\n";
  materials.forEach(m => {
    csv += `${m.material},${m.predicted_cost},${m.co2_impact},${m.sustainability_score}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ecopack_analysis.csv";
  a.click();
};

// --------------------------------------------------
// 8️⃣ Export PDF
// --------------------------------------------------
document.getElementById("exportPdf").onclick = () => {
  window.print();
};
