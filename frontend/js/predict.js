document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // ----------------------------
    // Get form values
    // ----------------------------
    const name = document.getElementById("productName").value.trim();
    const category = document.getElementById("category").value;
    const weight = parseFloat(document.getElementById("weight").value);
    const fragility = parseInt(document.getElementById("fragility").value);
    const shipping = document.getElementById("shipping").value;

    const errorMsg = document.getElementById("errorMsg");
    const apiError = document.getElementById("apiError");
    const loadingMsg = document.getElementById("loadingMsg");

    errorMsg.textContent = "";
    apiError.textContent = "";

    // ----------------------------
    // Client-side validation
    // ----------------------------
    if (!name || !category || !shipping) {
        errorMsg.textContent = "All fields are required.";
        return;
    }

    if (isNaN(weight) || weight <= 0) {
        errorMsg.textContent = "Weight must be greater than 0.";
        return;
    }

    if (isNaN(fragility) || fragility < 1 || fragility > 10) {
        errorMsg.textContent = "Fragility must be between 1 and 10.";
        return;
    }

    // ----------------------------
    // Prepare payload for backend
    // ----------------------------
    const payload = {
        product_name: name,
        category: category,
        product_weight_kg: weight,
        fragility_index: fragility / 10, // Convert 1-10 to 0-1 decimal
        shipping_type: shipping
    };

    // ----------------------------
    // Call Flask /predict API
    // ----------------------------
    loadingMsg.style.display = "block";

    fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Prediction API failed");
        }
        return response.json();
    })
    .then(data => {
        loadingMsg.style.display = "none";

        // Add product information to the response for analytics
        data.product_info = {
            product_name: name,
            category: category,
            product_weight_kg: weight,
            fragility_index: fragility / 10,
            shipping_type: shipping
        };

        // Store response for results page and analytics
        localStorage.setItem("recommendationData", JSON.stringify(data));

        // Redirect to results page
        window.location.href = "results.html";
    })
    .catch(error => {
        loadingMsg.style.display = "none";
        apiError.textContent =
            "Failed to fetch recommendations. Please try again.";
        console.error(error);
    });
});
