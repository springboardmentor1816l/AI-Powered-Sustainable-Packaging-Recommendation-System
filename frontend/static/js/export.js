/**
 * EcoPackAI Export Functionality
 * ================================
 * 
 * Export prediction results to CSV and PDF formats
 * Supports both frontend download and backend generation
 * 
 * Author: EcoPackAI Team
 * Date: 2026-01-12
 */

class ExportManager {
    constructor() {
        this.apiBase = '/api/v1';
    }

    /**
     * Export data to CSV format
     * @param {Array} data - Array of prediction objects
     * @param {string} filename - Output filename
     */
    exportToCSV(data, filename = 'ecopack_predictions.csv') {
        if (!data || data.length === 0) {
            console.error('No data to export');
            alert('No data available for export');
            return;
        }

        try {
            // Extract headers from first object
            const headers = Object.keys(data[0]);

            // Create CSV content
            let csvContent = '';

            // Add headers
            csvContent += headers.map(h => this.escapeCSVValue(h)).join(',') + '\n';

            // Add data rows
            data.forEach(row => {
                const values = headers.map(header => {
                    const value = row[header];
                    return this.escapeCSVValue(value);
                });
                csvContent += values.join(',') + '\n';
            });

            // Create blob and download
            this.downloadFile(csvContent, filename, 'text/csv;charset=utf-8;');

            console.log(`Exported ${data.length} rows to ${filename}`);
            return true;
        } catch (error) {
            console.error('CSV export error:', error);
            alert('Failed to export CSV: ' + error.message);
            return false;
        }
    }

    /**
     * Escape CSV values to handle commas, quotes, and newlines
     * @param {*} value - Value to escape
     * @returns {string} Escaped value
     */
    escapeCSVValue(value) {
        if (value === null || value === undefined) {
            return '';
        }

        const stringValue = String(value);

        // If value contains comma, quote, or newline, wrap in quotes
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
            return `"${stringValue.replace(/"/g, '""')}"`;
        }

        return stringValue;
    }

    /**
     * Export prediction results with detailed metadata
     * @param {Object} predictionResult - Complete prediction result object
     * @param {string} filename - Output filename
     */
    exportPredictionToCSV(predictionResult, filename = 'prediction_results.csv') {
        if (!predictionResult) {
            console.error('No prediction result to export');
            return;
        }

        try {
            const data = [];

            // Add metadata
            data.push({
                'Parameter': 'Timestamp',
                'Value': predictionResult.timestamp || new Date().toISOString()
            });

            data.push({
                'Parameter': 'Prediction Type',
                'Value': predictionResult.prediction_type || 'all'
            });

            data.push({ 'Parameter': '', 'Value': '' }); // Empty row

            // Add results
            if (predictionResult.results) {
                data.push({ 'Parameter': 'RESULTS', 'Value': '' });

                Object.entries(predictionResult.results).forEach(([key, value]) => {
                    data.push({
                        'Parameter': key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                        'Value': typeof value === 'number' ? value.toFixed(4) : value
                    });
                });
            }

            // Add metadata if present
            if (predictionResult.metadata) {
                data.push({ 'Parameter': '', 'Value': '' }); // Empty row
                data.push({ 'Parameter': 'METADATA', 'Value': '' });

                Object.entries(predictionResult.metadata).forEach(([key, value]) => {
                    data.push({
                        'Parameter': key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                        'Value': value
                    });
                });
            }

            this.exportToCSV(data, filename);
        } catch (error) {
            console.error('Prediction export error:', error);
            alert('Failed to export prediction: ' + error.message);
        }
    }

    /**
     * Export multiple materials comparison to CSV
     * @param {Array} materials - Array of material predictions
     * @param {string} filename - Output filename
     */
    exportMaterialsComparison(materials, filename = 'materials_comparison.csv') {
        if (!materials || materials.length === 0) {
            alert('No materials to export');
            return;
        }

        try {
            const exportData = materials.map((material, index) => ({
                'Material ID': material.id || material.name || `Material ${index + 1}`,
                'Predicted Cost ($)': material.predicted_cost?.toFixed(2) || 'N/A',
                'Predicted CO₂ (kg)': material.predicted_co2?.toFixed(4) || 'N/A',
                'Cost Confidence': material.cost_confidence?.toFixed(4) || 'N/A',
                'Recyclability (%)': material.recyclability_percent || 'N/A',
                'Recycled Content (%)': material.recycled_content_percent || 'N/A',
                'Sustainability Score': material.overall_sustainability_score?.toFixed(4) || 'N/A',
                'Material Suitability': material.material_suitability_score || 'N/A'
            }));

            this.exportToCSV(exportData, filename);
        } catch (error) {
            console.error('Materials comparison export error:', error);
            alert('Failed to export materials comparison: ' + error.message);
        }
    }

    /**
     * Generate PDF report (client-side using jsPDF)
     * @param {Object} predictionResult - Prediction result object
     * @param {string} filename - Output filename
     */
    async exportToPDF(predictionResult, filename = 'ecopack_report.pdf') {
        // Check if jsPDF is available
        if (typeof window.jsPDF === 'undefined' && typeof window.jspdf === 'undefined') {
            console.error('jsPDF library not loaded');
            alert('PDF export library not available. Please ensure jsPDF is included.');
            return;
        }

        try {
            // Support both window.jsPDF and window.jspdf for compatibility
            const jsPDF = window.jsPDF || window.jspdf?.jsPDF;
            if (!jsPDF) {
                throw new Error('jsPDF constructor not found');
            }
            const doc = new jsPDF();

            // Set up document
            let yPosition = 20;
            const lineHeight = 10;
            const pageWidth = doc.internal.pageSize.getWidth();
            const margin = 20;

            // Title
            doc.setFontSize(20);
            doc.setFont('helvetica', 'bold');
            doc.text('EcoPackAI Sustainability Report', margin, yPosition);

            yPosition += lineHeight * 1.5;

            // Subtitle
            doc.setFontSize(12);
            doc.setFont('helvetica', 'normal');
            doc.setTextColor(100);
            doc.text('AI-Powered Packaging Analysis', margin, yPosition);

            yPosition += lineHeight * 2;

            // Divider line
            doc.setDrawColor(200);
            doc.line(margin, yPosition, pageWidth - margin, yPosition);
            yPosition += lineHeight;

            // Metadata
            doc.setFontSize(10);
            doc.setTextColor(0);
            doc.setFont('helvetica', 'bold');
            doc.text('Report Date:', margin, yPosition);
            doc.setFont('helvetica', 'normal');
            doc.text(new Date().toLocaleString(), margin + 50, yPosition);
            yPosition += lineHeight;

            if (predictionResult.timestamp) {
                doc.setFont('helvetica', 'bold');
                doc.text('Prediction Time:', margin, yPosition);
                doc.setFont('helvetica', 'normal');
                doc.text(new Date(predictionResult.timestamp).toLocaleString(), margin + 50, yPosition);
                yPosition += lineHeight;
            }

            yPosition += lineHeight;

            // Results Section
            if (predictionResult.results) {
                doc.setFontSize(14);
                doc.setFont('helvetica', 'bold');
                doc.text('Prediction Results', margin, yPosition);
                yPosition += lineHeight * 1.5;

                doc.setFontSize(10);
                const results = predictionResult.results;

                // Cost
                if (results.predicted_cost !== undefined) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('Predicted Cost:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.setTextColor(16, 185, 129); // Green
                    doc.text(`$${results.predicted_cost.toFixed(2)}`, margin + 60, yPosition);
                    doc.setTextColor(0);
                    yPosition += lineHeight;
                }

                // Cost Confidence
                if (results.cost_confidence !== undefined) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('Cost Confidence:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.text(`${(results.cost_confidence * 100).toFixed(2)}%`, margin + 60, yPosition);
                    yPosition += lineHeight;
                }

                yPosition += 5;

                // CO2
                if (results.predicted_co2 !== undefined) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('Predicted CO₂:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.setTextColor(59, 130, 246); // Blue
                    doc.text(`${results.predicted_co2.toFixed(4)} kg`, margin + 60, yPosition);
                    doc.setTextColor(0);
                    yPosition += lineHeight;
                }

                yPosition += lineHeight;
            }

            // Model Information Section
            if (predictionResult.metadata) {
                doc.setFontSize(14);
                doc.setFont('helvetica', 'bold');
                doc.text('Model Information', margin, yPosition);
                yPosition += lineHeight * 1.5;

                doc.setFontSize(10);
                const metadata = predictionResult.metadata;

                if (metadata.cost_model) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('Cost Model:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.text(metadata.cost_model, margin + 50, yPosition);
                    yPosition += lineHeight;
                }

                if (metadata.co2_model) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('CO₂ Model:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.text(metadata.co2_model, margin + 50, yPosition);
                    yPosition += lineHeight;
                }

                if (metadata.cost_r2) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('Cost Model R²:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.text((metadata.cost_r2 * 100).toFixed(2) + '%', margin + 50, yPosition);
                    yPosition += lineHeight;
                }

                if (metadata.co2_r2) {
                    doc.setFont('helvetica', 'bold');
                    doc.text('CO₂ Model R²:', margin + 5, yPosition);
                    doc.setFont('helvetica', 'normal');
                    doc.text((metadata.co2_r2 * 100).toFixed(2) + '%', margin + 50, yPosition);
                    yPosition += lineHeight;
                }
            }

            // Footer
            const footerY = doc.internal.pageSize.getHeight() - 20;
            doc.setFontSize(8);
            doc.setTextColor(150);
            doc.text('Generated by EcoPackAI - AI-Powered Sustainable Packaging System', margin, footerY);
            doc.text('© 2026 EcoPackAI. All rights reserved.', margin, footerY + 5);

            // Save PDF
            doc.save(filename);

            console.log(`PDF exported: ${filename}`);
            return true;
        } catch (error) {
            console.error('PDF export error:', error);
            alert('Failed to export PDF: ' + error.message);
            return false;
        }
    }

    /**
     * Request server-side PDF generation
     * @param {Object} predictionData - Data to include in PDF
     * @param {string} filename - Desired filename
     */
    async requestServerPDF(predictionData, filename = 'ecopack_report.pdf') {
        try {
            const response = await fetch(`${this.apiBase}/export/pdf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(predictionData)
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            // Download the PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            console.log('Server-generated PDF downloaded');
            return true;
        } catch (error) {
            console.error('Server PDF export error:', error);
            // Fallback to client-side generation
            console.log('Falling back to client-side PDF generation');
            return this.exportToPDF(predictionData, filename);
        }
    }

    /**
     * Download file helper
     * @param {string} content - File content
     * @param {string} filename - Filename
     * @param {string} mimeType - MIME type
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    /**
     * Export current page data (for use in results pages)
     * @param {string} format - 'csv' or 'pdf'
     */
    exportCurrentData(format = 'csv') {
        // Try to get data from localStorage or sessionStorage
        const storedData = localStorage.getItem('latestPrediction') ||
            sessionStorage.getItem('latestPrediction');

        if (!storedData) {
            alert('No prediction data available to export');
            return;
        }

        try {
            const data = JSON.parse(storedData);

            if (format === 'csv') {
                this.exportPredictionToCSV(data);
            } else if (format === 'pdf') {
                this.exportToPDF(data);
            } else {
                console.error('Unsupported export format:', format);
            }
        } catch (error) {
            console.error('Export error:', error);
            alert('Failed to export data: ' + error.message);
        }
    }
}

// Export singleton instance
const exportManager = new ExportManager();

// Make available globally
window.ExportManager = exportManager;

// Add export buttons event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // CSV export button
    const csvButton = document.getElementById('exportCSV');
    if (csvButton) {
        csvButton.addEventListener('click', () => {
            exportManager.exportCurrentData('csv');
        });
    }

    // PDF export button
    const pdfButton = document.getElementById('exportPDF');
    if (pdfButton) {
        pdfButton.addEventListener('click', () => {
            exportManager.exportCurrentData('pdf');
        });
    }
});
