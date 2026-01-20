console.log("predict.js loaded");

// Live fragility display
const fragilitySlider = document.getElementById("fragility");
const fragilityValue = document.getElementById("fragilityValue");
const fragilityLabel = document.getElementById("fragilityLabel");

const fragilityText = {
  1: "Very Low",
  2: "Low",
  3: "Medium",
  4: "High",
  5: "Very High"
};

fragilitySlider.addEventListener("input", () => {
  fragilityValue.innerText = fragilitySlider.value;
  fragilityLabel.innerText = `(${fragilityText[fragilitySlider.value]})`;
});

// Form submit
document.getElementById("productForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    product_name: document.getElementById("productName").value.trim(),
    product_category: document.getElementById("category").value,
    shipping_method: document.getElementById("shipping").value,
    weight: parseFloat(document.getElementById("weight").value),
    fragility_index: parseInt(document.getElementById("fragility").value)
  };

  const errorBox = document.getElementById("errorBox");
  errorBox.innerText = "";

  if (!payload.product_name || !payload.product_category || !payload.shipping_method) {
    errorBox.innerText = "All fields are required.";
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "ecopack-secret-key"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Prediction failed");

    localStorage.setItem("prediction", JSON.stringify(data));
    window.location.href = "result.html";

  } catch (err) {
    errorBox.innerText = err.message;
  }
});
