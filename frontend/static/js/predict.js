ddocument.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let name = document.getElementById("name").value;
    let category = document.getElementById("category").value;
    let weight = document.getElementById("weight").value;
    let fragility = document.getElementById("fragility").value;
    let shipping = document.getElementById("shipping").value;

    let errorDiv = document.getElementById("error");

    errorDiv.innerText = "";

    if (!name || !category || !weight || !fragility || !shipping) {
        errorDiv.innerText = "All fields are required";
        return;
    }

    if (weight <= 0) {
        errorDiv.innerText = "Weight must be greater than 0";
        return;
    }

    if (fragility < 1 || fragility > 5) {
        errorDiv.innerText = "Fragility must be between 1 and 5";
        return;
    }

    alert("Validation passed! Ready to predict 🚀");
});
