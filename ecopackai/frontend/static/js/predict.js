// ===============================
// SAFE DOM REFERENCES
// ===============================
const form = document.getElementById("productForm");
const scenarioSelect = document.getElementById("scenarioSelect");

const productNameEl = document.getElementById("product_name");

const categoryEl = document.getElementById("category");
const shippingEl = document.getElementById("shipping_type");
const materialEl = document.getElementById("material_type");
const packagingEl = document.getElementById("packaging_type");
const regionEl = document.getElementById("supplier_region");
const weightEl = document.getElementById("product_weight_kg");
const fragilityEl = document.getElementById("fragility_index");

// ===============================
// Scenario Auto-Fill Logic
// ===============================
if (scenarioSelect && form) {
    scenarioSelect.addEventListener("change", function () {
        const scenario = this.value;

        if (scenario === "best") {
            productNameEl.value = "Eco-friendly Food Item";
            categoryEl.value = "Food";
            shippingEl.value = "Road";
            materialEl.value = "PLA";
            packagingEl.value = "Box";
            regionEl.value = "Asia";
            weightEl.value = 0.5;
            fragilityEl.value = 0.1;
        }

        if (scenario === "worst") {
            productNameEl.value = "Electronic Gadget";
            categoryEl.value = "Electronics";
            shippingEl.value = "Air";
            materialEl.value = "Paper";
            packagingEl.value = "Pouch";
            regionEl.value = "Europe";
            weightEl.value = 10;
            fragilityEl.value = 1.0;
        }

        if (scenario === "manual") {
            const selectedScenario = scenarioSelect.value;
            form.reset();
            scenarioSelect.value = selectedScenario; // ✅ keep scenario
        }
    });
}

// ===============================
// Form Submit + Backend Call
// ===============================
if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Clear previous errors
        document.querySelectorAll(".text-danger").forEach(el => el.textContent = "");

        let valid = true;

        const product_name = productNameEl.value.trim();
        const category = categoryEl.value;
        const shipping_type = shippingEl.value;
        const material_type = materialEl.value;
        const packaging_type = packagingEl.value;
        const supplier_region = regionEl.value;
        const product_weight_kg = weightEl.value;
        const fragility_index = fragilityEl.value;

        // ===============================
        // VALIDATION
        // ===============================
        if (!product_name) {
            document.getElementById("errorProductName").textContent = "Product name required";
            valid = false;
        }
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
            document.getElementById("errorFragility").textContent = "Fragility must be between 0 and 1";
            valid = false;
        }

        if (!valid) return;

        // ===============================
        // FINAL PAYLOAD (Backend Schema)
        // ===============================
        const payload = {
            product_name: product_name,
            category: category,
            shipping_type: shipping_type,
            material_type: material_type,
            packaging_type: packaging_type,
            supplier_region: supplier_region,
            product_weight_kg: parseFloat(product_weight_kg),
            fragility_index: parseFloat(fragility_index)
        };

        console.log("Payload being sent to backend:", payload);

        // ===============================
        // API CALL
        // ===============================
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (!res.ok) {
                throw new Error("Backend error");
            }
            return res.json();
        })
        .then(data => {
            console.log("ML Response:", data);

            // Preserve product name for results & exports
            data.product_name = product_name;

            localStorage.setItem("ecoResult", JSON.stringify(data));
            window.location.href = "results.html";
        })
        .catch(err => {
            alert("Backend error. Please check server.");
            console.error(err);
        });
    });
}

