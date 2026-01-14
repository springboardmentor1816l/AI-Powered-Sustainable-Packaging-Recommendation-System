document
  .getElementById("productForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // -----------------------------
    // UI Elements
    // -----------------------------
    const errorDiv = document.getElementById("error");
    const resultDiv = document.getElementById("result");
    const scoreText = document.getElementById("recScore");

    errorDiv.innerText = "";
    resultDiv.classList.add("d-none");

    // -----------------------------
    // Read form values
    // -----------------------------
    const productName = document.getElementById("productName").value.trim();
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

    if (isNaN(weight) || weight <= 0) {
      errorDiv.innerText = "Weight must be greater than 0.";
      return;
    }

    if (isNaN(fragility) || fragility < 1 || fragility > 5) {
      errorDiv.innerText = "Fragility must be between 1 and 5.";
      return;
    }

    // -----------------------------
    // Payload (Backend-compatible + flexible)
    // -----------------------------
    const payload = {
      product_name: productName,
      product_category: category,
      weight_capacity_kg: weight,
      fragility_index: fragility,
      shipping_type: shipping
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

      /**
       * EXPECTED BACKEND RESPONSE FORMAT:
       * {
       *   prediction: number,
       *   material: string,
       *   cost: number,
       *   co2: number
       * }
       */

      // -----------------------------
      // Display result (UI feedback)
      // -----------------------------
      resultDiv.classList.remove("d-none");
      scoreText.innerText =
        "Suitability Score: " + result.prediction.toFixed(1) + "%";

      // -----------------------------
      // SAVE FOR results.html
      // -----------------------------
      const bestResult = {
        material: result.material || "AI Recommended Material",
        suitability_score: result.prediction,
        cost: result.cost || 0,
        co2: result.co2 || 0
      };

      localStorage.setItem(
        "best_result",
        JSON.stringify(bestResult)
      );

      localStorage.setItem(
        "product_input",
        JSON.stringify(payload)
      );

      // -----------------------------
      // SAVE HISTORY FOR analytics.html
      // -----------------------------
      const history =
        JSON.parse(localStorage.getItem("ecoPackHistory") || "[]");

      history.push({
        product_category: category,
        suitability_score: result.prediction,
        cost: result.cost || 0,
        co2: result.co2 || 0,
        timestamp: new Date().toISOString()
      });

      localStorage.setItem(
        "ecoPackHistory",
        JSON.stringify(history)
      );

    } catch (err) {
      errorDiv.innerText =
        err.message || "Backend connection failed.";
    }
  });
