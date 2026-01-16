const data = JSON.parse(localStorage.getItem("latest_recommendations")) || [];
const tbody = document.getElementById("resultBody");

if (!data.length) {
    tbody.innerHTML = "<tr><td colspan='6'>No data available</td></tr>";
    throw new Error("No data");
}

// ---------------- TABLE ----------------
data.forEach(item => {
    const tr = document.createElement("tr");
    if (item.rank === 1) tr.classList.add("table-success");

    tr.innerHTML = `
        <td>${item["Packaging Type"]}</td>
        <td>${item["Material Type"]}</td>
        <td>${item.predicted_cost}</td>
        <td>${item.predicted_co2}</td>
        <td>${item.final_score}</td>
        <td>${item.rank}</td>
    `;
    tbody.appendChild(tr);
});

// ---------------- SUMMARY ----------------
const avg = arr => arr.reduce((a,b)=>a+b,0)/arr.length;

document.getElementById("bestMaterial").innerText = data[0]["Packaging Type"];
document.getElementById("bestScore").innerText =
    `Score: ${data[0].final_score.toFixed(2)}`;

document.getElementById("avgCost").innerText =
    "₹ " + avg(data.map(d=>d.predicted_cost)).toFixed(2);

document.getElementById("avgCO2").innerText =
    avg(data.map(d=>d.predicted_co2)).toFixed(2);

document.getElementById("avgScore").innerText =
    (100 - avg(data.map(d=>d.final_score))).toFixed(2);

// ---------------- CHARTS ----------------
const labels = data.map(d=>d["Packaging Type"]);

new Chart(costChart,{
    type:"bar",
    data:{
        labels,
        datasets:[{
            label:"Cost",
            data:data.map(d=>d.predicted_cost),
            backgroundColor:"rgba(76,175,80,0.7)"
        }]
    },
    options:{plugins:{zoom:{zoom:{wheel:{enabled:true}},pan:{enabled:true}}}}
});

new Chart(co2Chart,{
    type:"bar",
    data:{
        labels,
        datasets:[{
            label:"CO₂",
            data:data.map(d=>d.predicted_co2),
            backgroundColor:"rgba(239,83,80,0.7)"
        }]
    },
    options:{plugins:{zoom:{zoom:{wheel:{enabled:true}},pan:{enabled:true}}}}
});
