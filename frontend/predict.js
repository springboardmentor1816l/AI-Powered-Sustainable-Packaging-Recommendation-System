document.getElementById("productForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const payload = {
    product_name: productName.value,
    category: category.value,
    weight: parseFloat(weight.value),
    fragility: parseFloat(fragility.value),
    shipping: shipping.value
  };

  if (!payload.product_name || !payload.category || !payload.shipping) {
    errorMsg.innerText = "All fields are required.";
    return;
  }

  errorMsg.innerText = "";

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => renderTable(data.recommendations))
  .catch(() => {
    errorMsg.innerText = "Backend not responding.";
  });
});

function renderTable(list) {
  const table = document.getElementById("resultTable");
  const body = document.getElementById("tableBody");

  body.innerHTML = "";

  list.forEach(item => {
    body.innerHTML += `
      <tr>
        <td>${item.rank}</td>
        <td>${item.material}</td>
        <td>${item.cost}</td>
        <td>${item.co2}</td>
        <td>${item.score}</td>
      </tr>
    `;
  });

  table.classList.remove("d-none");
}
