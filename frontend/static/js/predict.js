document
  .getElementById("predictionForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log("Submit clicked");

    const form = e.target;

    // Let browser show validation UI
    if (!form.checkValidity()) {
      form.classList.add("was-validated");
      return;
    }

    const payload = {
      product_name: document.getElementById("product_name").value,
      category: document.getElementById("category").value,
      product_weight: parseFloat(
        document.getElementById("product_weight").value
      ),
      fragility_index: parseFloat(
        document.getElementById("fragility_index").value
      ),
      shipping_type: document.getElementById("shipping_type").value,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.error || "Prediction failed");

      // Save result and go to results page
      localStorage.setItem("ecoResult", JSON.stringify(data));
      window.location.href = "results.html";
    } catch (error) {
      alert("❌ " + error.message);
      console.error(error);
    }
  });
