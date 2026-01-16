const data = JSON.parse(localStorage.getItem("latest_recommendations")) || [];

if (!data.length) {
    alert("No analytics data found. Please run prediction first.");
}

// ---------- HELPERS ----------
const avg = arr => arr.reduce((a,b)=>a+b,0)/arr.length;

// ---------- SUMMARY ----------
const avgCost = avg(data.map(d=>d.predicted_cost));
const avgCO2 = avg(data.map(d=>d.predicted_co2));
const avgScore = avg(data.map(d=>d.final_score));

const best = [...data].sort((a,b)=>a.rank-b.rank)[0];

// ---------- UPDATE STATS ----------
document.getElementById("bestMaterial").innerText = best["Packaging Type"];
document.getElementById("bestScore").innerText = `Sustainability: ${best.final_score.toFixed(2)}`;

document.getElementById("avgCost").innerText = `₹ ${avgCost.toFixed(2)}`;
document.getElementById("avgCO2").innerText = avgCO2.toFixed(2);
document.getElementById("avgScore").innerText = (100 - avgScore).toFixed(2);

// ---------- CHART CONFIG ----------
Chart.defaults.font.family = "Inter, system-ui";
Chart.defaults.color = "#444";

// ---------- LABELS ----------
const labels = data.map(d=>d["Packaging Type"]);

// ---------- COST ----------
new Chart(document.getElementById("costChart"),{
    type:"bar",
    data:{
        labels,
        datasets:[{
            label:"Predicted Cost",
            data:data.map(d=>d.predicted_cost),
            backgroundColor:"rgba(76,175,80,0.7)",
            hoverBackgroundColor:"#2e7d32"
        }]
    },
    options:{
        responsive:true,
        plugins:{
            tooltip:{enabled:true},
            zoom:{
                zoom:{wheel:{enabled:true},pinch:{enabled:true},mode:"x"},
                pan:{enabled:true,mode:"x"}
            }
        }
    }
});

// ---------- CO2 ----------
new Chart(document.getElementById("co2Chart"),{
    type:"bar",
    data:{
        labels,
        datasets:[{
            label:"Predicted CO₂",
            data:data.map(d=>d.predicted_co2),
            backgroundColor:"rgba(239,83,80,0.7)",
            hoverBackgroundColor:"#c62828"
        }]
    },
    options:{
        responsive:true,
        plugins:{
            zoom:{
                zoom:{wheel:{enabled:true},mode:"x"},
                pan:{enabled:true,mode:"x"}
            }
        }
    }
});
