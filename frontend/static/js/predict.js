// static/js/predict.js

document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button');

    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    // 1. Show Loading State
    const originalBtnText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Analyzing...';

    // 2. Collect Data
    const payload = {
        product_name: document.getElementById('product_name').value,
        category: document.getElementById('category').value,
        product_weight_kg: parseFloat(document.getElementById('product_weight_kg').value),
        fragility_index: parseFloat(document.getElementById('fragility_index').value),
        shipping_type: document.getElementById('shipping_type').value
    };

    try {
        // 3. Send AJAX Request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.status === 'success') {
            // 4. Store results in SessionStorage to pass to results page
            sessionStorage.setItem('lastResult', JSON.stringify(result));
            window.location.href = '/results';
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        console.error("Integration Error:", err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnText;
    }
});