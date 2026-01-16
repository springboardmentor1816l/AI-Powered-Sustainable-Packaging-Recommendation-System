document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const errorBox = document.getElementById("errorBox");
    const loadingOverlay = document.getElementById("loadingOverlay");

    errorBox.classList.add("d-none");

    // -------------------------
    // BUILD PAYLOAD
    // -------------------------
    const payload = {
        product_weight: Number(document.getElementById("product_weight").value),
        material_type: document.getElementById("material_type").value,
        recyclability_score: Number(document.getElementById("recyclability_score").value)
    };

    // -------------------------
    // CLIENT-SIDE VALIDATION
    // -------------------------
    if (
        payload.product_weight <= 0 ||
        !payload.material_type ||
        payload.recyclability_score < 0 ||
        payload.recyclability_score > 1
    ) {
        errorBox.innerText = "Please fill all required fields correctly.";
        errorBox.classList.remove("d-none");
        return;
    }

    // ✅ START SPINNER
    loadingOverlay.classList.remove("d-none");

    try {
        // -------------------------
        // API CALL
        // -------------------------
        const res = await fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": "ecopack-secret-key"
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Prediction failed");
        }

        if (!data.recommendations || data.recommendations.length === 0) {
            throw new Error("No recommendations returned from backend");
        }

        // -------------------------
        // STORE RESULTS
        // -------------------------
        localStorage.setItem(
            "latest_recommendations",
            JSON.stringify(data.recommendations)
        );

        if (data.product_id) {
            localStorage.setItem("last_product_id", data.product_id);
        }

        // ⏳ UX DELAY (FEELS NATURAL)
        setTimeout(() => {
            window.location.href = "/results.html";
        }, 900);

    } catch (err) {
        // ❌ STOP SPINNER ON ERROR
        loadingOverlay.classList.add("d-none");

        errorBox.innerText = err.message || "Backend not reachable.";
        errorBox.classList.remove("d-none");
        console.error("Prediction error:", err);
    }
});
