document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Clear errors
    document.querySelectorAll(".text-danger").forEach(el => el.textContent = "");

    let valid = true;

    const category = document.getElementById("category").value;
    const shipping_type = document.getElementById("shipping_type").value;
    const material_type = document.getElementById("material_type").value;
    const packaging_type = document.getElementById("packaging_type").value;
    const supplier_region = document.getElementById("supplier_region").value;
    const product_weight_kg = document.getElementById("product_weight_kg").value;
    const fragility_index = document.getElementById("fragility_index").value;

    if (!category) {
        document.getElementById("errorCategory").textContent = "Category required";
        valid = false;
    }
    if (!shipping_type) {
        document.getElementById("errorShipping").textContent = "Shipping type required";
        valid = false;
    }
    if (!material_type) {
        document.getElementById("errorMaterial").textContent = "Material required";
        valid = false;
    }
    if (!packaging_type) {
        document.getElementById("errorPackaging").textContent = "Packaging required";
        valid = false;
    }
    if (!supplier_region) {
        document.getElementById("errorRegion").textContent = "Region required";
        valid = false;
    }
    if (!product_weight_kg || product_weight_kg <= 0) {
        document.getElementById("errorWeight").textContent = "Weight must be > 0";
        valid = false;
    }
    if (fragility_index === "" || fragility_index < 0 || fragility_index > 1) {
        document.getElementById("errorFragility").textContent = "Fragility must be 0–1";
        valid = false;
    }

    if (!valid) return;

    // FINAL PAYLOAD (MATCHES ML EXACTLY)
    const payload = {
        category: category,
        shipping_type: shipping_type,
        material_type: material_type,
        packaging_type: packaging_type,
        supplier_region: supplier_region,
        product_weight_kg: parseFloat(product_weight_kg),
        fragility_index: parseFloat(fragility_index)
    };

    // Send to backend
    console.log("Payload being sent to backend:", payload);

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response from backend:", data);

        localStorage.setItem("ecoResult", JSON.stringify(data));
        window.location.href = "results.html";
    })
    .catch(err => {
        alert("Backend error. Check server.");
        console.error(err);
    });
});
