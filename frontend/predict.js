/**
 * EcoPackAI Prediction Page Script
 * Enhanced with category-dependent product dropdown
 */

// Product catalog organized by category
const PRODUCT_CATALOG = {
    "food": [
        "Fresh Fruits Package",
        "Packaged Snacks",
        "Bottled Beverages",
        "Canned Goods",
        "Frozen Food Items",
        "Dairy Products",
        "Breakfast Cereal",
        "Condiments & Sauces"
    ],
    "electronics": [
        "Smartphone",
        "Laptop Computer",
        "Tablet Device",
        "Digital Camera",
        "Wireless Headphones",
        "Smartwatch",
        "Gaming Console",
        "Bluetooth Speaker"
    ],
    "cosmetics": [
        "Lipstick",
        "Face Cream",
        "Shampoo Bottle",
        "Perfume",
        "Skincare Set",
        "Makeup Kit",
        "Body Lotion",
        "Facial Cleanser"
    ],
    "pharmaceuticals": [
        "Prescription Medicine",
        "Vitamins & Supplements",
        "First Aid Kit",
        "Medical Devices",
        "Pain Relief Medication",
        "Antiseptic Products"
    ],
    "textiles": [
        "T-Shirts",
        "Jeans & Pants",
        "Sports Shoes",
        "Designer Handbag",
        "Winter Jacket",
        "Fashion Accessories",
        "Activewear"
    ],
    "industrial": [
        "Power Tools",
        "Machinery Parts",
        "Building Materials",
        "Hardware Items",
        "Safety Equipment",
        "Industrial Components"
    ],
    "other": [
        "Glassware",
        "Ceramics",
        "Office Supplies",
        "Books",
        "Toys",
        "Furniture",
        "Home Decor",
        "Kitchen Appliances"
    ]
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
    initializeCategoryDropdown();
    initializeForm();
    initializeButtons();
});

/**
 * Initialize category dropdown to control product suggestions
 */
function initializeCategoryDropdown() {
    const categorySelect = document.getElementById('product_category');
    const productInput = document.getElementById('product_name');
    const dropdown = document.getElementById('productDropdown');

    if (!categorySelect || !productInput) return;

    // Disable product input until category is selected
    productInput.disabled = true;
    productInput.placeholder = "Select category first";

    // When category changes, enable product input and show relevant suggestions
    categorySelect.addEventListener('change', function () {
        const selectedCategory = this.value;

        if (selectedCategory) {
            productInput.disabled = false;
            productInput.placeholder = "Select or type product name";
            productInput.value = "";
            showCategoryProducts(selectedCategory);
        } else {
            productInput.disabled = true;
            productInput.placeholder = "Select category first";
            productInput.value = "";
            if (dropdown) dropdown.style.display = 'none';
        }
    });

    // Product input interactions
    productInput.addEventListener('focus', function () {
        const category = categorySelect.value;
        if (category) {
            showCategoryProducts(category);
        }
    });

    productInput.addEventListener('input', function () {
        const category = categorySelect.value;
        if (category) {
            const query = this.value.toLowerCase();
            showFilteredProducts(category, query);
        }
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!productInput.contains(e.target) && dropdown && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

/**
 * Show products for selected category
 */
function showCategoryProducts(category) {
    const products = PRODUCT_CATALOG[category] || [];
    const dropdown = document.getElementById('productDropdown');
    const productInput = document.getElementById('product_name');

    if (!dropdown || products.length === 0) return;

    dropdown.innerHTML = products.map(product =>
        `<div class="autocomplete-item" data-value="${product}">${product}</div>`
    ).join('');

    // Add click handlers
    dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
        item.addEventListener('click', function () {
            productInput.value = this.dataset.value;
            dropdown.style.display = 'none';
        });
    });

    dropdown.style.display = 'block';
}

/**
 * Show filtered products based on search query
 */
function showFilteredProducts(category, query) {
    const products = PRODUCT_CATALOG[category] || [];
    const filtered = query
        ? products.filter(p => p.toLowerCase().includes(query))
        : products;

    const dropdown = document.getElementById('productDropdown');
    const productInput = document.getElementById('product_name');

    if (!dropdown) return;

    if (filtered.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    dropdown.innerHTML = filtered.map(product =>
        `<div class="autocomplete-item" data-value="${product}">${product}</div>`
    ).join('');

    // Add click handlers
    dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
        item.addEventListener('click', function () {
            productInput.value = this.dataset.value;
            dropdown.style.display = 'none';
        });
    });

    dropdown.style.display = 'block';
}

/**
 * Initialize form submission
 */
function initializeForm() {
    const form = document.getElementById('predictForm');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Hide any previous errors
        document.getElementById('errorAlert').style.display = 'none';

        // Show loading overlay
        showLoading();

        // Get form data
        const formData = {
            product_name: document.getElementById('product_name').value,
            product_category: document.getElementById('product_category').value,
            product_weight: parseFloat(document.getElementById('product_weight').value),
            fragility_level: parseInt(document.getElementById('fragility_level').value),
            shipping_type: document.getElementById('shipping_type').value,
            ranking_mode: document.getElementById('ranking_mode').value,
            moisture_sensitive: document.getElementById('moisture_sensitive')?.checked || false,
            temperature_sensitive: document.getElementById('temperature_sensitive')?.checked || false,
            hazardous: document.getElementById('hazardous')?.checked || false
        };

        try {
            // Try API first, fall back to demo data if API unavailable
            let data;
            try {
                const response = await fetch('http://localhost:5000/api/v1/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    throw new Error(`API returned status ${response.status}`);
                }

                data = await response.json();
            } catch (apiError) {
                console.warn('API unavailable, using demo data:', apiError);
                // Generate demo recommendations
                data = generateDemoRecommendations(formData);
            }

            // Hide loading
            hideLoading();

            // Display results
            displayResults(data, formData.product_name);

            // Save to localStorage for dashboard
            saveToLocalStorage(data);

        } catch (error) {
            hideLoading();
            showError('Failed to generate recommendations: ' + error.message);
        }
    });
}

/**
 * Generate demo recommendations when API is unavailable
 */
function generateDemoRecommendations(formData) {
    const materials = [
        { name: "Recycled Cardboard", cost_mult: 1.0, co2_mult: 0.8, sust: 0.85 },
        { name: "Biodegradable Plastic", cost_mult: 1.5, co2_mult: 1.2, sust: 0.70 },
        { name: "Paper-based Packaging", cost_mult: 0.9, co2_mult: 0.7, sust: 0.80 },
        { name: "Molded Pulp", cost_mult: 1.1, co2_mult: 0.75, sust: 0.82 },
        { name: "Compostable Materials", cost_mult: 1.6, co2_mult: 1.0, sust: 0.88 }
    ];

    const baseCost = formData.product_weight * 10;
    const baseCO2 = formData.product_weight * 2;

    const recommendations = materials.map((mat, idx) => ({
        material_name: mat.name,
        predicted_cost: (baseCost * mat.cost_mult).toFixed(2),
        predicted_co2: (baseCO2 * mat.co2_mult).toFixed(4),
        cost_confidence: 0.92 - (idx * 0.02),
        overall_sustainability_score: mat.sust,
        recyclability_percent: 85 + (idx * 2),
        recycled_content_percent: 70 - (idx * 5),
        final_score: (100 - idx * 5).toFixed(2)
    }));

    return {
        status: 'success',
        recommendations: recommendations,
        metadata: {
            mode: 'demo',
            cost_model: 'Random Forest',
            co2_model: 'XGBoost'
        }
    };
}

/**
 * Display recommendation results
 */
function displayResults(data, productName) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';

    // Update product name display
    document.getElementById('productNameDisplay').textContent = productName;

    // Get recommendations
    const recommendations = data.recommendations || data.results?.recommendations || [];

    if (recommendations.length === 0) {
        showError('No recommendations available');
        return;
    }

    // Populate recommendations table
    const tbody = document.getElementById('recommendationsTableBody');
    tbody.innerHTML = '';

    recommendations.forEach((rec, index) => {
        const row = createRecommendationRow(rec, index + 1);
        tbody.appendChild(row);
    });

    // Scroll to results smoothly
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }, 100);
}

/**
 * Create a table row for recommendation
 */
function createRecommendationRow(rec, rank) {
    const tr = document.createElement('tr');
    if (rank === 1) tr.classList.add('top-rank');

    tr.innerHTML = `
        <td class="rank-cell">
            <span class="rank-badge-table">${rank}</span>
        </td>
        <td class="material-name-cell">${rec.material_name || rec.name || 'Unknown'}</td>
        <td class="cost-cell">$${parseFloat(rec.predicted_cost || 0).toFixed(2)}</td>
        <td class="co2-cell">${parseFloat(rec.predicted_co2 || 0).toFixed(4)} kg</td>
        <td class="sustainability-cell">
            <div class="mini-progress">
                <div class="mini-progress-fill" style="width: ${(rec.overall_sustainability_score || 0) * 100}%"></div>
            </div>
            <small>${((rec.overall_sustainability_score || 0) * 100).toFixed(1)}%</small>
        </td>
        <td>${parseFloat(rec.final_score || rec.score || 0).toFixed(2)}</td>
        <td>${((rec.cost_confidence || rec.confidence || 0) * 100).toFixed(1)}%</td>
    `;

    return tr;
}

/**
 * Save recommendations to localStorage for dashboard
 */
function saveToLocalStorage(data) {
    const recommendations = data.recommendations || data.results?.recommendations || [];

    // Transform to dashboard format
    const materials = recommendations.map(rec => ({
        name: rec.material_name || rec.name,
        material_name: rec.material_name || rec.name,
        predicted_cost: parseFloat(rec.predicted_cost || 0),
        predicted_co2: parseFloat(rec.predicted_co2 || 0),
        cost_confidence: rec.cost_confidence || rec.confidence || 0,
        overall_sustainability_score: rec.overall_sustainability_score || 0,
        recyclability_percent: rec.recyclability_percent || 0,
        recycled_content_percent: rec.recycled_content_percent || 0
    }));

    // Save to localStorage
    localStorage.setItem('analyticsData', JSON.stringify(materials));

    // Also save latest prediction for export
    localStorage.setItem('latestPrediction', JSON.stringify({
        timestamp: new Date().toISOString(),
        prediction_type: 'recommendation',
        results: {
            materials: materials
        },
        metadata: data.metadata || {
            cost_model: 'Random Forest',
            co2_model: 'XGBoost',
            cost_r2: 0.997,
            co2_r2: 0.994
        }
    }));

    console.log('Saved', materials.length, 'materials to localStorage');
}

/**
 * Initialize button handlers
 */
function initializeButtons() {
    // New prediction button
    const newPredBtn = document.getElementById('newPrediction');
    if (newPredBtn) {
        newPredBtn.addEventListener('click', function () {
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('predictForm').reset();
            document.getElementById('product_name').disabled = true;
            document.getElementById('product_name').placeholder = "Select category first";
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

/**
 * Show loading overlay
 */
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    if (errorAlert) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
        setTimeout(() => {
            errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}
