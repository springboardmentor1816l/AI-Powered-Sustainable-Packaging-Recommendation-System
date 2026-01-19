let costChart = null;
let co2Chart = null;

function drawCharts(predictedCost, co2Impact) {
  const costCtx = document.getElementById("costChart").getContext("2d");
  const co2Ctx = document.getElementById("co2Chart").getContext("2d");

  if (costChart) costChart.destroy();
  if (co2Chart) co2Chart.destroy();

  costChart = new Chart(costCtx, {
    type: "bar",
    data: {
      labels: ["Predicted Cost"],
      datasets: [
        {
          label: "Cost (₹)",
          data: [predictedCost],
          borderWidth: 1,
        },
      ],
    },
  });

  co2Chart = new Chart(co2Ctx, {
    type: "bar",
    data: {
      labels: ["CO₂ Impact"],
      datasets: [
        {
          label: "CO₂ (kg)",
          data: [co2Impact],
          borderWidth: 1,
        },
      ],
    },
  });
}
