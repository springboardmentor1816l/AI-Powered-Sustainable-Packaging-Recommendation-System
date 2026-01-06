document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("productName").value.trim();
    const category = document.getElementById("category").value;
    const weight = parseFloat(document.getElementById("weight").value);
    const fragility = parseInt(document.getElementById("fragility").value);
    const shipping = document.getElementById("shipping").value;

    const errorMsg = document.getElementById("errorMsg");
    errorMsg.style.color = "red";

    // Validation
    if (!name || !category || !shipping) {
        errorMsg.textContent = "All fields are required.";
        return;
    }

    if (isNaN(weight) || weight <= 0) {
        errorMsg.textContent = "Weight must be greater than 0.";
        return;
    }

    if (fragility < 1 || fragility > 10) {
        errorMsg.textContent = "Fragility must be between 1 and 10.";
        return;
    }

    // If validation passes
    errorMsg.style.color = "green";
    errorMsg.textContent = "Validation successful. Ready to send to API.";

    // Prepared payload (for backend later)
    const payload = {
        product_name: name,
        category: category,
        product_weight: weight,
        fragility_index: fragility,
        shipping_type: shipping
    };

    console.log("Validated Payload:", payload);
});
