document.getElementById("predictBtn").addEventListener("click", async function () {

    // 1️⃣ Get values from form
    const weight = document.getElementById("weight").value;
    const fragility = document.getElementById("fragility").value;
    const category = document.getElementById("category").value;

    // 2️⃣ Basic validation
    if (!weight || !fragility || !category) {
        document.getElementById("error").innerText = "Please fill all required fields";
        return;
    }

    document.getElementById("error").innerText = "";

    // 3️⃣ Call backend API
    const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-KEY": "demo-key"
        },
        body: JSON.stringify({
            weight: parseFloat(weight),
            fragility: parseInt(fragility),
            material_type: category
        })
    });

    const data = await response.json();

    // 4️⃣ Show result
    const table = document.getElementById("resultTable");
    const tbody = table.querySelector("tbody");
    tbody.innerHTML = "";

    const row = `
        <tr>
            <td>1</td>
            <td>${data.recommended_material}</td>
            <td>${data.estimated_cost}</td>
            <td>${data.estimated_co2}</td>
            <td>${data.score}</td>
        </tr>
    `;

    tbody.innerHTML = row;
    table.style.display = "table";
});

