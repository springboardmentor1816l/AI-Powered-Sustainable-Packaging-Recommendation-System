console.log("predict.js loaded");

const form = document.getElementById("predictForm");
const tableCard = document.getElementById("resultCard");
const table = document.getElementById("resultTable");
const tbody = table.querySelector("tbody");
const errorBox = document.getElementById("errorBox");
const loadingBox = document.getElementById("loading");

// Helper: validate number fields
function validateNumber(id, min = -Infinity, max = Infinity, required = true) {
    const el = document.getElementById(id);
    const val = el.value.trim();
    if (required && val === "") return `${id.replace("_", " ")} is required`;
    const num = Number(val);
    if (isNaN(num)) return `${id.replace("_", " ")} must be a number`;
    if (num < min || num > max) return `${id.replace("_", " ")} must be between ${min} and ${max}`;
    return null;
}

// Helper: validate select fields
function validateSelect(id) {
    const el = document.getElementById(id);
    if (!el.value) return `${id.replace("_", " ")} must be selected`;
    return null;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.innerText = "";
    tbody.innerHTML = "";
    tableCard.style.display = "none";

    // Validation
    const errors = [];

    // Text input
    if (!document.getElementById("product_name").value.trim()) {
        errors.push("Product Name is required");
    }

    // Select inputs
    ["product_category", "shipping_type"].forEach(id => {
        const err = validateSelect(id);
        if (err) errors.push(err);
    });

    // Numeric inputs
    const numericFields = [
        {id:"product_weight", min:0},
        {id:"fragility_score", min:0, max:1},
        {id:"moisture_sensitivity", min:0, max:1},
        {id:"thermal_sensitivity", min:0, max:1},
        {id:"expected_shelf_life_days", min:1},
        {id:"material_cost_per_kg", min:0},
        {id:"co2_emission_per_kg", min:0},
        {id:"biodegradability_percent", min:0, max:100},
        {id:"load_handling_score", min:0, max:1},
        {id:"sustainability_score", min:0, max:100}
    ];

    numericFields.forEach(f => {
        const err = validateNumber(f.id, f.min, f.max);
        if (err) errors.push(err);
    });

    // Show validation errors inline
    if (errors.length > 0) {
        errorBox.innerHTML = errors.map(e => `• ${e}`).join("<br>");
        return; // Stop submission
    }

    // Prepare payload
    const payload = {
        product_name: document.getElementById("product_name").value.trim(),
        product_category: document.getElementById("product_category").value,
        shipping_type: document.getElementById("shipping_type").value,
        product_weight: Number(document.getElementById("product_weight").value),
        fragility_score: Number(document.getElementById("fragility_score").value),
        moisture_sensitivity: Number(document.getElementById("moisture_sensitivity").value),
        thermal_sensitivity: Number(document.getElementById("thermal_sensitivity").value),
        expected_shelf_life_days: Number(document.getElementById("expected_shelf_life_days").value),
        material_cost_per_kg: Number(document.getElementById("material_cost_per_kg").value),
        co2_emission_per_kg: Number(document.getElementById("co2_emission_per_kg").value),
        biodegradability_percent: Number(document.getElementById("biodegradability_percent").value),
        load_handling_score: Number(document.getElementById("load_handling_score").value),
        sustainability_score: Number(document.getElementById("sustainability_score").value),
        hazardous_material_flag: Number(document.getElementById("hazardous_material_flag").value),
        recyclability_category: document.getElementById("recyclability_category").value,
        supplier_region: document.getElementById("supplier_region").value,
        material_type: document.getElementById("material_type").value
    };

    // Show loading
    loadingBox.style.display = "block";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-KEY": "ecopackai-secret-key"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("📥 API response:", data);

        // Hide loading
        loadingBox.style.display = "none";

        if (!Array.isArray(data) || data.length === 0) {
            errorBox.innerText = "No recommendations received from server.";
            return;
        }

        // Render results
        tbody.innerHTML = "";
        data.forEach((item, idx) => {
            const row = document.createElement("tr");
            if (idx === 0) row.classList.add("top"); // Highlight top

            row.innerHTML = `
                <td>${item.material_name || "-"}</td>
                <td>${item.predicted_cost || "-"}</td>
                <td>${item.co2_footprint?.toFixed(3) || "-"}</td>
                <td>${item.sustainability_score || "-"}</td>
                <td>${item.rank || "-"}</td>
            `;
            tbody.appendChild(row);
        });

        tableCard.style.display = "block";

    } catch (err) {
        console.error("❌ Error:", err);
        loadingBox.style.display = "none";
        errorBox.innerText = "Failed to fetch recommendations. Check console.";
    }
});
