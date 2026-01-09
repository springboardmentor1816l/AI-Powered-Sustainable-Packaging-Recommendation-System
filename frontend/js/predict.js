document
  .getElementById("productForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const errorDiv = document.getElementById("error");
    const resultDiv = document.getElementById("result");
    const scoreText = document.getElementById("recScore");

    errorDiv.innerText = "";
    resultDiv.classList.add("d-none");

    // -----------------------------
    // Read form values
    // -----------------------------
    const productName = document.getElementById("productName").value;
    const category = document.getElementById("category").value;
    const weight = parseFloat(document.getElementById("weight").value);
    const fragility = parseInt(document.getElementById("fragility").value);
    const shipping = document.getElementById("shipping").value;

    // -----------------------------
    // Validation
    // -----------------------------
    if (!productName || !category || !shipping) {
      errorDiv.innerText = "All fields are required.";
      return;
    }

    if (weight <= 0) {
      errorDiv.innerText = "Weight must be greater than 0.";
      return;
    }

    if (fragility < 1 || fragility > 5) {
      errorDiv.innerText = "Fragility must be between 1 and 5.";
      return;
    }

    // -----------------------------
    // Payload (MATCHES BACKEND)
    // -----------------------------
    const payload = {
      material_type: "glass",
      industry_use_case: category,
      source_type: "recycled",

      weight_capacity_kg: weight,
      strength_mpa: 30 + fragility * 2,
      recyclability_percent: 70,
      biodegradability_percent: 20,

      co2_emission_kg_per_kg:
        shipping === "International" ? 2.0 : 1.2,

      co2_impact_index:
        shipping === "International" ? 0.8 : 0.5,

      cost_efficiency_index: 0.8,
      cost_per_kg: 1.5,
      recyclability_category: "high",

      fragility_index: fragility
    };

    try {
      // -----------------------------
      // Call backend API
      // -----------------------------
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": "supersecret123"
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Prediction failed");
      }

      // -----------------------------
      // Display result (STEP 3)
      // -----------------------------
      resultDiv.classList.remove("d-none");
      scoreText.innerText =
        "Suitability Score: " + result.prediction + "%";

      // Save for future steps
      localStorage.setItem("prediction", JSON.stringify(result));
      localStorage.setItem("product_name", productName);

    } catch (err) {
      errorDiv.innerText =
        err.message || "Backend connection failed.";
    }
  });
