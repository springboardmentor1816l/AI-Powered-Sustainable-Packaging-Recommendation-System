const API_URL = "http://localhost:5000/api/predict";
const API_KEY = "ecopackai-secret-key"; // replace at build or manually

const form = document.getElementById("productForm");
const submitBtn = document.getElementById("submitBtn");
const loadingBox = document.getElementById("loadingBox");
const alertBox = document.getElementById("alert-box");

const fragilitySlider = document.getElementById("fragility_index");
const fragilityValue = document.getElementById("fragility_value");

fragilityValue.innerText = fragilitySlider.value;
fragilitySlider.oninput = () => {
  fragilityValue.innerText = fragilitySlider.value;
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  alertBox.innerHTML = "";

  const payload = [{
    product_name: document.getElementById("product_name").value.trim(),
    category: document.getElementById("category").value,
    product_weight: parseFloat(document.getElementById("product_weight").value),
    fragility_index: parseInt(fragilitySlider.value),
    shipping_type: document.getElementById("shipping_type").value
  }];

  // UI state
  submitBtn.disabled = true;
  loadingBox.classList.remove("d-none");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Prediction failed");
    }

    sessionStorage.setItem(
      "prediction_result",
      JSON.stringify(data.recommendations)
    );

    window.location.href = "results.html";

  } catch (err) {
    alertBox.innerHTML =
      `<div class="alert alert-danger">${err.message}</div>`;
  } finally {
    submitBtn.disabled = false;
    loadingBox.classList.add("d-none");
  }
});
