document.addEventListener('DOMContentLoaded', async function() {
    console.log('Dashboard loaded');
    
    // Fetch summary stats
    try {
        const summaryResponse = await fetch('/api/analytics/summary');
        const summaryData = await summaryResponse.json();
        
        document.getElementById('totalPredictions').textContent = summaryData.total_predictions || 0;
        document.getElementById('avgCost').textContent = `₹${(summaryData.average_cost || 0).toFixed(2)}`;
        document.getElementById('avgCO2').textContent = `${(summaryData.average_co2 || 0).toFixed(2)} kg`;
    } catch (error) {
        console.error('Error fetching summary:', error);
    }
    
    // Fetch history for charts
    try {
        const historyResponse = await fetch('/api/analytics/history');
        const historyData = await historyResponse.json();
        const history = historyData.history || [];
        
        if (history.length === 0) {
            console.log('No prediction history available');
            return;
        }
        
        // Prepare data for charts
        const labels = history.map((p, i) => `#${i + 1}`);
        const costs = history.map(p => p.cost);
        const co2s = history.map(p => p.co2);
        
        // Cost Trend Chart
        const costCtx = document.getElementById('costChart').getContext('2d');
        new Chart(costCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Cost (₹)',
                    data: costs,
                    borderColor: '#00E676',
                    backgroundColor: 'rgba(0, 230, 118, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
        
        // CO2 Trend Chart
        const co2Ctx = document.getElementById('co2Chart').getContext('2d');
        new Chart(co2Ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'CO2 Emission (kg)',
                    data: co2s,
                    borderColor: '#2979FF',
                    backgroundColor: 'rgba(41, 121, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error fetching history:', error);
    }
});
