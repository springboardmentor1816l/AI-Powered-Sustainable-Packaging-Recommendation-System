console.log("predict.js loaded");

const form = document.getElementById("predictForm");
const errorBox = document.getElementById("errorBox");
const loadingBox = document.getElementById("loading");
const tbody = document.querySelector("#resultTable tbody");

const costChartCanvas = document.getElementById("costChart");
const co2ChartCanvas = document.getElementById("co2Chart");
const sustainabilityChartCanvas = document.getElementById("sustainabilityChart");

let latestResults = [];
let costChart, co2Chart, sustainabilityChart;

/* ---------- Validation ---------- */
function vNum(id, min=0, max=Infinity) {
    const v = document.getElementById(id).value;
    if (v === "" || isNaN(v)) return `${id} invalid`;
    if (+v < min || +v > max) return `${id} out of range`;
    return null;
}

/* ---------- Submit ---------- */
form.addEventListener("submit", async e => {
    e.preventDefault();
    errorBox.innerHTML = "";
    loadingBox.style.display = "block";

    const errors = [
        !product_name.value && "Product name required",
        vNum("product_weight",0),
        vNum("fragility_score",0,1),
        vNum("moisture_sensitivity",0,1),
        vNum("thermal_sensitivity",0,1),
        vNum("expected_shelf_life_days",1),
        vNum("material_cost_per_kg",0),
        vNum("co2_emission_per_kg",0),
        vNum("biodegradability_percent",0,100),
        vNum("load_handling_score",0,1),
        vNum("sustainability_score",0,100)
    ].filter(Boolean);

    if (errors.length) {
        loadingBox.style.display = "none";
        errorBox.innerHTML = errors.map(e=>`• ${e}`).join("<br>");
        return;
    }

    const payload = Object.fromEntries(
        [...document.querySelectorAll("input,select")].map(i => [i.id, isNaN(i.value)?i.value:+i.value])
    );

    const res = await fetch("http://127.0.0.1:5000/predict", {
        method:"POST",
        headers:{"Content-Type":"application/json","X-API-KEY":"ecopackai-secret-key"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    loadingBox.style.display = "none";

    latestResults = data;
    tbody.innerHTML = "";

    data.forEach((r,i)=>{
        const tr = document.createElement("tr");
        if (i===0) tr.classList.add("top");
        tr.innerHTML = `<td>${r.material_name}</td><td>${r.predicted_cost}</td><td>${r.co2_footprint}</td><td>${r.sustainability_score}</td><td>${r.rank}</td>`;
        tbody.appendChild(tr);
    });

    document.getElementById("resultCard").style.display="block";
    document.getElementById("analyticsCard").style.display="block";

    renderCharts(data);
});

/* ---------- Charts ---------- */
function renderCharts(d){
    const labels = d.map(x=>x.material_name);
    costChart?.destroy(); co2Chart?.destroy(); sustainabilityChart?.destroy();

    costChart = new Chart(costChartCanvas,{type:"bar",data:{labels,datasets:[{label:"Cost",data:d.map(x=>x.predicted_cost)}]}});
    co2Chart = new Chart(co2ChartCanvas,{type:"bar",data:{labels,datasets:[{label:"CO₂",data:d.map(x=>x.co2_footprint)}]}});
    sustainabilityChart = new Chart(sustainabilityChartCanvas,{type:"bar",data:{labels,datasets:[{label:"Sustainability",data:d.map(x=>x.sustainability_score)}]}});
}

/* ---------- Export ---------- */
exportCSV.onclick = () => {
    let csv = "Material,Cost,CO2,Sustainability,Rank\n";
    latestResults.forEach(r=>csv+=`${r.material_name},${r.predicted_cost},${r.co2_footprint},${r.sustainability_score},${r.rank}\n`);
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([csv]));
    a.download="EcoPackAI.csv"; a.click();
};

exportPDF.onclick = () => {
    const pdf = new jspdf.jsPDF();
    pdf.text("EcoPackAI Sustainability Report",10,10);
    let y=25;
    latestResults.forEach(r=>{pdf.text(`${r.rank}. ${r.material_name} | CO₂:${r.co2_footprint}`,10,y); y+=10;});
    pdf.save("EcoPackAI_Report.pdf");
};
