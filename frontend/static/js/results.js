document.addEventListener("DOMContentLoaded", () => {
  const data = JSON.parse(localStorage.getItem("ecoResult"));
  if (!data) return;

  document.getElementById("prediction-text").innerHTML =
    "✅ Recommendation Generated Successfully";

  const tableBody = document.getElementById("result-table-body");

  tableBody.innerHTML = `
    <tr>
      <td>1</td>
      <td><strong>${data.recommended_material}</strong></td>
      <td>₹ ${Number(data.predicted_cost).toFixed(2)}</td>
      <td>${data.co2_impact} kg</td>
      <td><span class="badge bg-success">High</span></td>
    </tr>
  `;

  drawCharts(data.predicted_cost, data.co2_impact);
});
