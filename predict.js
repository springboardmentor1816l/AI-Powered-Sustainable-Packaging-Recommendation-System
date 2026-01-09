document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("productForm");
  const errorMsg = document.getElementById("errorMsg");
  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("productName").value.trim();
    const category = document.getElementById("categorySelect").value;
    const shipping = document.getElementById("shippingSelect").value;
    const weight = parseFloat(document.getElementById("weightInput").value);
    const fragility = parseFloat(document.getElementById("fragilityInput").value);

    errorMsg.innerText = "";

    // VALIDATION
    if (!name || !category || !shipping) {
      errorMsg.innerText = "All fields are required.";
      return;
    }

    if (isNaN(weight) || weight <= 0) {
      errorMsg.innerText = "Weight must be a positive number in kg.";
      return;
    }

    if (isNaN(fragility) || fragility < 0 || fragility > 1) {
      errorMsg.innerText = "Fragility must be between 0 and 1.";
      return;
    }

    // RECOMMENDATION LOGIC
    let material, protection, boxType;

    if (fragility > 0.7) {
      protection = "High cushioning with molded pulp inserts";
    } else if (fragility > 0.3) {
      protection = "Medium cushioning with paper padding";
    } else {
      protection = "Basic protection";
    }

    boxType = weight > 5
      ? "Double-wall corrugated box"
      : "Single-wall corrugated box";

    if (category === "Electronics") {
      material = "Recyclable corrugated board";
    } else if (category === "Food") {
      material = "Biodegradable kraft packaging";
    } else {
      material = "Recycled paper packaging";
    }

    // UPDATE RESULT ON SAME PAGE
    resultText.innerHTML = `
      <li><strong>Packaging Material:</strong> ${material}</li>
      <li><strong>Box Type:</strong> ${boxType}</li>
      <li><strong>Protection Level:</strong> ${protection}</li>
      <li><strong>Sustainability:</strong> Eco-friendly & recyclable materials</li>
    `;

    resultBox.classList.remove("d-none");
  });
});
