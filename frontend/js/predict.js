document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predictForm");

    if (!form) {
        console.error("predictForm not found");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // =========================
        // Read values from form
        // =========================
        const productName = document.getElementById("productName").value.trim();
        const category = document.getElementById("category").value;
        const weight = parseFloat(document.getElementById("weight").value);
        const fragility = parseInt(document.getElementById("fragility").value);
        const shipping = document.getElementById("shipping").value;

        // =========================
        // Frontend validation
        // =========================
        if (!productName || !category || !shipping) {
            alert("Please fill all required fields");
            return;
        }

        if (isNaN(weight) || weight <= 0) {
            alert("Weight must be greater than 0");
            return;
        }

        if (isNaN(fragility) || fragility < 1 || fragility > 5) {
            alert("Fragility index must be between 1 and 5");
            return;
        }

        // =========================
        // Payload (MATCHES BACKEND)
        // =========================
        const payload = {
            category: category,
            weight: weight,
            fragility: fragility,
            shipping_type: shipping
        };

        try {
            // Optional: user feedback
            console.log("Sending payload:", payload);

            const response = await fetch("http://localhost:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-API-KEY": "ecopackai-secret"
                },
                body: JSON.stringify(payload)
            });

            // =========================
            // Handle API response
            // =========================
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API error ${response.status}: ${errorText}`);
            }

            const result = await response.json();
            console.log("Prediction result:", result);

            // =========================
            // Store result for result.html
            // =========================
            localStorage.setItem(
                "predictionResult",
                JSON.stringify(result)
            );

            // =========================
            // Redirect to results page
            // =========================
            window.location.href = "result.html";

        } catch (error) {
            console.error("Prediction failed:", error);
            alert("Failed to get prediction from server. Please try again.");
        }
    });
});
