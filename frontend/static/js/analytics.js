/**
 * EcoPackAI Analytics & Visualization
 * ====================================
 * 
 * Interactive charts for sustainability and cost insights
 * Uses Chart.js for beautiful, responsive visualizations
 * 
 * Author: EcoPackAI Team
 * Date: 2026-01-12
 */

// Chart.js configuration and utilities
const ChartConfig = {
    defaultColors: {
        primary: 'rgba(16, 185, 129, 0.8)',      // Green
        secondary: 'rgba(59, 130, 246, 0.8)',   // Blue
        warning: 'rgba(245, 158, 11, 0.8)',     // Amber
        danger: 'rgba(239, 68, 68, 0.8)',       // Red
        info: 'rgba(139, 92, 246, 0.8)',        // Purple
        success: 'rgba(34, 197, 94, 0.8)',      // Emerald
    },

    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        family: "'Inter', sans-serif",
                        size: 12
                    },
                    padding: 15,
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    family: "'Inter', sans-serif",
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    family: "'Inter', sans-serif",
                    size: 12
                },
                padding: 12,
                cornerRadius: 8,
                displayColors: true
            }
        },
        animation: {
            duration: 800,
            easing: 'easeInOutQuart'
        }
    }
};

// Analytics Manager Class
class AnalyticsManager {
    constructor() {
        this.charts = new Map();
        this.data = null;
        this.initialized = false;
    }

    /**
     * Initialize analytics with prediction data
     * @param {Object} predictionData - Results from API
     */
    init(predictionData) {
        this.data = predictionData;
        this.initialized = true;
        console.log('Analytics initialized with data:', predictionData);
    }

    /**
     * Create CO₂ Comparison Bar Chart
     * @param {string} canvasId - Canvas element ID
     * @param {Array} materials - Array of material predictions
     */
    createCO2ComparisonChart(canvasId, materials) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element '${canvasId}' not found`);
            return null;
        }

        // Destroy existing chart if present
        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        // Prepare data
        const labels = materials.map((m, i) => m.name || `Material ${i + 1}`);
        const co2Values = materials.map(m => m.predicted_co2 || 0);

        // Create color gradient based on values
        const colors = co2Values.map(value => {
            const normalized = Math.min(value / Math.max(...co2Values), 1);
            if (normalized < 0.33) return ChartConfig.defaultColors.success;
            if (normalized < 0.67) return ChartConfig.defaultColors.warning;
            return ChartConfig.defaultColors.danger;
        });

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'CO₂ Emissions (kg)',
                    data: co2Values,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'CO₂ Emissions (kg)',
                            font: {
                                family: "'Inter', sans-serif",
                                size: 13,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                family: "'Inter', sans-serif",
                                size: 11
                            }
                        }
                    }
                },
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    tooltip: {
                        ...ChartConfig.defaultOptions.plugins.tooltip,
                        callbacks: {
                            label: function (context) {
                                return `CO₂: ${context.parsed.y.toFixed(3)} kg`;
                            }
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    /**
     * Create Cost Comparison Chart
     * @param {string} canvasId - Canvas element ID
     * @param {Array} materials - Array of material predictions
     */
    createCostComparisonChart(canvasId, materials) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element '${canvasId}' not found`);
            return null;
        }

        // Destroy existing chart
        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        const labels = materials.map((m, i) => m.name || `Material ${i + 1}`);
        const costValues = materials.map(m => m.predicted_cost || 0);

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Cost ($)',
                    data: costValues,
                    backgroundColor: ChartConfig.defaultColors.primary,
                    borderColor: ChartConfig.defaultColors.primary.replace('0.8', '1'),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cost ($)',
                            font: {
                                family: "'Inter', sans-serif",
                                size: 13,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    tooltip: {
                        ...ChartConfig.defaultOptions.plugins.tooltip,
                        callbacks: {
                            label: function (context) {
                                return `Cost: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    /**
     * Create Sustainability Score Radar Chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} materialData - Single material data with all metrics
     */
    createSustainabilityRadar(canvasId, materialData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element '${canvasId}' not found`);
            return null;
        }

        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        const chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: [
                    'Recyclability',
                    'Recycled Content',
                    'Reusability',
                    'Waste Reduction',
                    'Sustainability Progress',
                    'Supplier Compliance'
                ],
                datasets: [{
                    label: 'Sustainability Metrics',
                    data: [
                        materialData.recyclability_percent || 0,
                        materialData.recycled_content_percent || 0,
                        materialData.reusability_percent || 0,
                        materialData.waste_reduction_impact_percent || 0,
                        materialData.sustainability_target_progress_percent || 0,
                        materialData.supplier_sustainability_compliance_percent || 0
                    ],
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: ChartConfig.defaultColors.primary,
                    borderWidth: 2,
                    pointBackgroundColor: ChartConfig.defaultColors.primary,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: ChartConfig.defaultColors.primary,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20,
                            font: {
                                size: 10
                            }
                        },
                        pointLabels: {
                            font: {
                                family: "'Inter', sans-serif",
                                size: 11,
                                weight: '500'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    tooltip: {
                        ...ChartConfig.defaultOptions.plugins.tooltip,
                        callbacks: {
                            label: function (context) {
                                return `${context.label}: ${context.parsed.r.toFixed(1)}%`;
                            }
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    /**
     * Create Cost vs CO₂ Scatter Plot
     * @param {string} canvasId - Canvas element ID
     * @param {Array} materials - Array of material predictions
     */
    createCostVsCO2Scatter(canvasId, materials) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element '${canvasId}' not found`);
            return null;
        }

        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        const scatterData = materials.map((m, i) => ({
            x: m.predicted_co2 || 0,
            y: m.predicted_cost || 0,
            label: m.name || `Material ${i + 1}`
        }));

        const chart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Cost vs CO₂',
                    data: scatterData,
                    backgroundColor: ChartConfig.defaultColors.secondary,
                    borderColor: ChartConfig.defaultColors.secondary.replace('0.8', '1'),
                    borderWidth: 2,
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                ...ChartConfig.defaultOptions,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'CO₂ Emissions (kg)',
                            font: {
                                family: "'Inter', sans-serif",
                                size: 13,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Cost ($)',
                            font: {
                                family: "'Inter', sans-serif",
                                size: 13,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                },
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    tooltip: {
                        ...ChartConfig.defaultOptions.plugins.tooltip,
                        callbacks: {
                            label: function (context) {
                                const point = context.raw;
                                return [
                                    `${point.label}`,
                                    `Cost: $${point.y.toFixed(2)}`,
                                    `CO₂: ${point.x.toFixed(3)} kg`
                                ];
                            }
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    /**
     * Create Material Ranking Chart
     * @param {string} canvasId - Canvas element ID
     * @param {Array} materials - Array of material predictions with scores
     */
    createMaterialRankingChart(canvasId, materials) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element '${canvasId}' not found`);
            return null;
        }

        if (this.charts.has(canvasId)) {
            this.charts.get(canvasId).destroy();
        }

        // Sort by sustainability score
        const sorted = [...materials].sort((a, b) =>
            (b.overall_sustainability_score || 0) - (a.overall_sustainability_score || 0)
        );

        const labels = sorted.map((m, i) => m.name || `Material ${i + 1}`);
        const scores = sorted.map(m => (m.overall_sustainability_score || 0) * 100);

        const chart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sustainability Score',
                    data: scores,
                    backgroundColor: ChartConfig.defaultColors.success,
                    borderColor: ChartConfig.defaultColors.success.replace('0.8', '1'),
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                ...ChartConfig.defaultOptions,
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Sustainability Score (%)',
                            font: {
                                family: "'Inter', sans-serif",
                                size: 13,
                                weight: '600'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    ...ChartConfig.defaultOptions.plugins,
                    tooltip: {
                        ...ChartConfig.defaultOptions.plugins.tooltip,
                        callbacks: {
                            label: function (context) {
                                return `Score: ${context.parsed.x.toFixed(1)}%`;
                            }
                        }
                    }
                }
            }
        });

        this.charts.set(canvasId, chart);
        return chart;
    }

    /**
     * Update chart with new data
     * @param {string} canvasId - Chart to update
     * @param {Object} newData - New data for chart
     */
    updateChart(canvasId, newData) {
        const chart = this.charts.get(canvasId);
        if (!chart) {
            console.warn(`Chart '${canvasId}' not found`);
            return;
        }

        chart.data = newData;
        chart.update('active');
    }

    /**
     * Destroy a specific chart
     * @param {string} canvasId - Chart to destroy
     */
    destroyChart(canvasId) {
        const chart = this.charts.get(canvasId);
        if (chart) {
            chart.destroy();
            this.charts.delete(canvasId);
        }
    }

    /**
     * Destroy all charts
     */
    destroyAll() {
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
    }

    /**
     * Resize all charts (useful for responsive layouts)
     */
    resizeAll() {
        this.charts.forEach(chart => chart.resize());
    }
}

// Export singleton instance
const analyticsManager = new AnalyticsManager();

// Auto-resize charts on window resize
window.addEventListener('resize', () => {
    analyticsManager.resizeAll();
});

// Make available globally
window.AnalyticsManager = analyticsManager;
