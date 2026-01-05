document
  .getElementById("predictionForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    let ok = true;
    const inputs = document.querySelectorAll("input, select");

    inputs.forEach((i) => {
      i.classList.remove("is-invalid");
      if (!i.checkValidity()) {
        ok = false;
        i.classList.add("is-invalid");
      }
    });

    const weight = parseFloat(document.getElementById("product_weight").value);
    const frag = parseFloat(document.getElementById("fragility_index").value);

    if (weight <= 0) {
      ok = false;
      product_weight.classList.add("is-invalid");
    }

    if (frag < 0 || frag > 1) {
      ok = false;
      fragility_index.classList.add("is-invalid");
    }

    if (!ok) return;

    const box = document.getElementById("result-container");
    const txt = document.getElementById("prediction-text");

    box.style.display = "block";

    // --- DEMO CALCULATIONS (Day-20 compliant) ---
    const cost = (weight * 120).toFixed(2);
    const co2 = (weight * 0.75).toFixed(2);

    let material = "Recycled Paper";
    if (frag >= 0.7) {
      material = "Molded Pulp";
    } else if (weight > 1) {
      material = "Corrugated Cardboard";
    }

    txt.innerHTML = `
    <strong>Predicted Cost:</strong> Rs. ${cost}<br>
<strong>CO2 Impact:</strong> ${co2} kg<br>

    <strong>Recommended Material:</strong> ${material}
  `;
  });
