/**
 * EcoPackAI - Analytics Dashboard
 * Interactive charts and data visualization for sustainability insights
 */

class AnalyticsDashboard {
    constructor() {
        this.data = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.loadData();
        this.setupEventListeners();
    }

    loadData() {
        // Retrieve recommendation data from localStorage
        const storedData = localStorage.getItem("recommendationData");
        
        if (!storedData) {
            this.showNoDataMessage();
            return;
        }

        try {
            this.data = JSON.parse(storedData);
            this.renderDashboard();
        } catch (error) {
            console.error("Error parsing stored data:", error);
            this.showErrorMessage();
        }
    }

    showNoDataMessage() {
        const container = document.getElementById("chartsContainer");
        container.innerHTML = `
            <div class="no-data-message">
                <h3>No Data Available</h3>
                <p>Please generate a recommendation first to view analytics.</p>
                <a href="product.html" class="btn-primary">Go to Product Input</a>
            </div>
        `;
    }

    showErrorMessage() {
        const container = document.getElementById("chartsContainer");
        container.innerHTML = `
            <div class="error-message">
                <h3>Error Loading Data</h3>
                <p>There was a problem loading your analytics data.</p>
            </div>
        `;
    }

    renderDashboard() {
        if (!this.data || !this.data.predictions) {
            this.showNoDataMessage();
            return;
        }

        this.renderSummaryCards();
        this.renderCharts();
        this.renderDataTable();
        this.enableExportButtons();
    }

    renderSummaryCards() {
        const predictions = this.data.predictions;
        const bestMaterial = predictions[0];
        
        // Calculate statistics
        const avgCost = (predictions.reduce((sum, p) => sum + parseFloat(p.predicted_cost), 0) / predictions.length).toFixed(2);
        const avgCO2 = (predictions.reduce((sum, p) => sum + parseFloat(p.co2), 0) / predictions.length).toFixed(2);
        const avgSustainability = (predictions.reduce((sum, p) => sum + parseFloat(p.sustainability_score), 0) / predictions.length).toFixed(2);

        const summaryHTML = `
            <div class="summary-cards">
                <div class="summary-card card-best">
                    <h3>Best Recommendation</h3>
                    <p class="card-value">${bestMaterial.material}</p>
                    <p class="card-label">Sustainability: ${bestMaterial.sustainability_score}</p>
                </div>
                <div class="summary-card card-cost">
                    <h3>Average Cost</h3>
                    <p class="card-value">Rs.${avgCost}</p>
                    <p class="card-label">Across ${predictions.length} materials</p>
                </div>
                <div class="summary-card card-co2">
                    <h3>Average CO2 Impact</h3>
                    <p class="card-value">${avgCO2}</p>
                    <p class="card-label">kg CO2 equivalent</p>
                </div>
                <div class="summary-card card-sustainability">
                    <h3>Avg Sustainability</h3>
                    <p class="card-value">${avgSustainability}</p>
                    <p class="card-label">Out of 100</p>
                </div>
            </div>
        `;

        document.getElementById("summaryCards").innerHTML = summaryHTML;
    }

    renderCharts() {
        this.renderCostComparisonChart();
        this.renderCO2ComparisonChart();
        this.renderSustainabilityRankingChart();
        this.renderCombinedMetricsChart();
    }

    renderCostComparisonChart() {
        const ctx = document.getElementById("costChart").getContext("2d");
        const predictions = this.data.predictions;

        const materials = predictions.map(p => p.material);
        const costs = predictions.map(p => parseFloat(p.predicted_cost));

        // Color gradient: green for lowest cost, red for highest
        const colors = this.generateColorGradient(costs, '#4CAF50', '#FF5722');

        this.charts.costChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: materials,
                datasets: [{
                    label: 'Predicted Cost (Rs.)',
                    data: costs,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.7', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Cost Comparison Across Materials',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `Cost: Rs.${context.parsed.y.toFixed(2)}`
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cost (Rs.)'
                        }
                    }
                }
            }
        });
    }

    renderCO2ComparisonChart() {
        const ctx = document.getElementById("co2Chart").getContext("2d");
        const predictions = this.data.predictions;

        const materials = predictions.map(p => p.material);
        const co2Values = predictions.map(p => parseFloat(p.co2));

        // Color gradient: green for lowest CO2, red for highest
        const colors = this.generateColorGradient(co2Values, '#81C784', '#EF5350');

        this.charts.co2Chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: materials,
                datasets: [{
                    label: 'CO2 Emissions (kg)',
                    data: co2Values,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.7', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'CO2 Impact Comparison',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `CO2: ${context.parsed.y.toFixed(2)} kg`
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'CO2 Emissions (kg)'
                        }
                    }
                }
            }
        });
    }

    renderSustainabilityRankingChart() {
        const ctx = document.getElementById("sustainabilityChart").getContext("2d");
        const predictions = this.data.predictions;

        const materials = predictions.map(p => p.material);
        const scores = predictions.map(p => parseFloat(p.sustainability_score));

        // Color gradient: red for lowest score, green for highest
        const colors = this.generateColorGradient(scores, '#FF6B6B', '#51CF66', true);

        this.charts.sustainabilityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: materials,
                datasets: [{
                    label: 'Sustainability Score',
                    data: scores,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.7', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Material Sustainability Ranking',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `Score: ${context.parsed.x.toFixed(2)}/100`
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Sustainability Score'
                        }
                    }
                }
            }
        });
    }

    renderCombinedMetricsChart() {
        const ctx = document.getElementById("combinedChart").getContext("2d");
        const predictions = this.data.predictions;

        const materials = predictions.map(p => p.material);
        
        // Normalize values to 0-100 scale for comparison
        const costs = predictions.map(p => parseFloat(p.predicted_cost));
        const co2Values = predictions.map(p => parseFloat(p.co2));
        const scores = predictions.map(p => parseFloat(p.sustainability_score));

        const maxCost = Math.max(...costs);
        const maxCO2 = Math.max(...co2Values);

        const normalizedCosts = costs.map(c => (c / maxCost) * 100);
        const normalizedCO2 = co2Values.map(c => (c / maxCO2) * 100);

        this.charts.combinedChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: materials,
                datasets: [
                    {
                        label: 'Cost (normalized)',
                        data: normalizedCosts,
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'CO2 Impact (normalized)',
                        data: normalizedCO2,
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Sustainability Score',
                        data: scores,
                        borderColor: '#4BC0C0',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Multi-Metric Comparison',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Normalized Score (0-100)'
                        }
                    }
                }
            }
        });
    }

    generateColorGradient(values, startColor, endColor, reverse = false) {
        const min = Math.min(...values);
        const max = Math.max(...values);
        const range = max - min;

        return values.map(value => {
            let ratio = range === 0 ? 0.5 : (value - min) / range;
            if (reverse) ratio = 1 - ratio;

            const r = Math.round(this.hexToRgb(startColor).r + ratio * (this.hexToRgb(endColor).r - this.hexToRgb(startColor).r));
            const g = Math.round(this.hexToRgb(startColor).g + ratio * (this.hexToRgb(endColor).g - this.hexToRgb(startColor).g));
            const b = Math.round(this.hexToRgb(startColor).b + ratio * (this.hexToRgb(endColor).b - this.hexToRgb(startColor).b));

            return `rgba(${r}, ${g}, ${b}, 0.7)`;
        });
    }

    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : { r: 0, g: 0, b: 0 };
    }

    setupEventListeners() {
        document.getElementById("exportCSV")?.addEventListener("click", () => this.exportToCSV());
        document.getElementById("exportPDF")?.addEventListener("click", () => this.exportToPDF());
    }

    enableExportButtons() {
        const exportCSV = document.getElementById("exportCSV");
        const exportPDF = document.getElementById("exportPDF");
        
        if (exportCSV) exportCSV.disabled = false;
        if (exportPDF) exportPDF.disabled = false;
    }

    renderDataTable() {
        const predictions = this.data.predictions;
        const tableBody = document.querySelector("#detailsTable tbody");

        if (!tableBody) return;

        tableBody.innerHTML = '';

        predictions.forEach(pred => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${pred.rank}</td>
                <td>${pred.material}</td>
                <td>Rs.${parseFloat(pred.predicted_cost).toFixed(2)}</td>
                <td>${parseFloat(pred.co2).toFixed(2)}</td>
                <td>${parseFloat(pred.sustainability_score).toFixed(2)}</td>
            `;

            // Highlight best recommendation
            if (pred.rank === 1) {
                row.style.backgroundColor = "#e6f4ea";
                row.style.fontWeight = "bold";
            }

            tableBody.appendChild(row);
        });
    }

    exportToCSV() {
        console.log('Export CSV clicked');
        
        if (!this.data || !this.data.predictions) {
            alert("No data available to export");
            return;
        }

        try {
            const predictions = this.data.predictions;
            const productInfo = this.data.product_info || {};

            // CSV Headers
            let csv = "EcoPackAI Sustainability Report\n\n";
        csv += "Product Information\n";
        csv += `Product Name,${productInfo.product_name || 'N/A'}\n`;
        csv += `Weight (kg),${productInfo.product_weight_kg || 'N/A'}\n`;
        csv += `Category,${productInfo.category || 'N/A'}\n`;
        csv += `Fragility Index,${productInfo.fragility_index || 'N/A'}\n`;
        csv += `Shipping Type,${productInfo.shipping_type || 'N/A'}\n`;
        csv += `\nGenerated,${new Date().toLocaleString()}\n\n`;

        csv += "Material Recommendations\n";
        csv += "Rank,Material,Predicted Cost (Rs.),CO2 Impact (kg),Sustainability Score\n";

        predictions.forEach(pred => {
            csv += `${pred.rank},"${pred.material}",${pred.predicted_cost},${pred.co2},${pred.sustainability_score}\n`;
        });

        // Statistics
        csv += "\nStatistics\n";
        const avgCost = (predictions.reduce((sum, p) => sum + parseFloat(p.predicted_cost), 0) / predictions.length).toFixed(2);
        const avgCO2 = (predictions.reduce((sum, p) => sum + parseFloat(p.co2), 0) / predictions.length).toFixed(2);
        const avgSustainability = (predictions.reduce((sum, p) => sum + parseFloat(p.sustainability_score), 0) / predictions.length).toFixed(2);

        csv += `Average Cost (Rs.),${avgCost}\n`;
        csv += `Average CO2 Impact (kg),${avgCO2}\n`;
        csv += `Average Sustainability Score,${avgSustainability}\n`;

        // Download
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        
        link.setAttribute("href", url);
        link.setAttribute("download", `EcoPackAI_Report_${Date.now()}.csv`);
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.showExportNotification("CSV exported successfully!");
        } catch (error) {
            console.error('CSV Export Error:', error);
            alert('Failed to export CSV: ' + error.message);
        }
    }

    exportToPDF() {
        console.log('Export PDF clicked');
        
        if (!this.data || !this.data.predictions) {
            alert("No data available to export");
            return;
        }

        try {
            // Check if jsPDF is loaded
            if (!window.jspdf) {
                alert("PDF library not loaded. Please refresh the page and try again.");
                console.error('jsPDF library not found');
                return;
            }

            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

        const predictions = this.data.predictions;
        const productInfo = this.data.product_info || {};

        // Title
        doc.setFontSize(20);
        doc.setTextColor(40, 167, 69);
        doc.text("EcoPackAI Sustainability Report", 20, 20);

        // Product Information
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text("Product Information", 20, 35);
        
        doc.setFontSize(10);
        let yPos = 45;
        doc.text(`Product Name: ${productInfo.product_name || 'N/A'}`, 20, yPos);
        yPos += 7;
        doc.text(`Weight: ${productInfo.product_weight_kg || 'N/A'} kg`, 20, yPos);
        yPos += 7;
        doc.text(`Category: ${productInfo.category || 'N/A'}`, 20, yPos);
        yPos += 7;
        doc.text(`Fragility Index: ${productInfo.fragility_index || 'N/A'}`, 20, yPos);
        yPos += 7;
        doc.text(`Shipping Type: ${productInfo.shipping_type || 'N/A'}`, 20, yPos);
        yPos += 10;

        // Recommendations Table
        doc.setFontSize(14);
        doc.text("Material Recommendations", 20, yPos);
        yPos += 10;

        doc.autoTable({
            startY: yPos,
            head: [['Rank', 'Material', 'Cost (Rs.)', 'CO2 (kg)', 'Score']],
            body: predictions.map(p => [
                p.rank,
                p.material,
                parseFloat(p.predicted_cost).toFixed(2),
                parseFloat(p.co2).toFixed(2),
                parseFloat(p.sustainability_score).toFixed(2)
            ]),
            theme: 'striped',
            headStyles: { fillColor: [40, 167, 69] },
            styles: { fontSize: 9 }
        });

        // Statistics
        yPos = doc.lastAutoTable.finalY + 15;
        doc.setFontSize(14);
        doc.text("Summary Statistics", 20, yPos);
        yPos += 10;

        const avgCost = (predictions.reduce((sum, p) => sum + parseFloat(p.predicted_cost), 0) / predictions.length).toFixed(2);
        const avgCO2 = (predictions.reduce((sum, p) => sum + parseFloat(p.co2), 0) / predictions.length).toFixed(2);
        const avgSustainability = (predictions.reduce((sum, p) => sum + parseFloat(p.sustainability_score), 0) / predictions.length).toFixed(2);

        doc.setFontSize(10);
        doc.text(`Average Cost: Rs.${avgCost}`, 20, yPos);
        yPos += 7;
        doc.text(`Average CO2 Impact: ${avgCO2} kg`, 20, yPos);
        yPos += 7;
        doc.text(`Average Sustainability Score: ${avgSustainability}/100`, 20, yPos);
        yPos += 10;

        // Best Recommendation Highlight
        const bestMaterial = predictions[0];
        doc.setFillColor(230, 244, 234);
        doc.rect(15, yPos, 180, 25, 'F');
        
        doc.setFontSize(12);
        doc.setTextColor(40, 167, 69);
        doc.text("Best Recommendation", 20, yPos + 8);
        
        doc.setFontSize(10);
        doc.setTextColor(0, 0, 0);
        doc.text(`${bestMaterial.material} - Sustainability Score: ${bestMaterial.sustainability_score}`, 20, yPos + 16);

        // Footer
        doc.setFontSize(8);
        doc.setTextColor(128, 128, 128);
        doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 280);
        doc.text("EcoPackAI © 2026 - Sustainable Packaging Intelligence", 20, 285);

        // Download
        doc.save(`EcoPackAI_Report_${Date.now()}.pdf`);

        this.showExportNotification("PDF exported successfully!");
        } catch (error) {
            console.error('PDF Export Error:', error);
            alert('Failed to export PDF: ' + error.message);
        }
    }

    showExportNotification(message) {
        const notification = document.createElement("div");
        notification.className = "export-notification";
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add("show");
        }, 100);

        setTimeout(() => {
            notification.classList.remove("show");
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    new AnalyticsDashboard();
});
