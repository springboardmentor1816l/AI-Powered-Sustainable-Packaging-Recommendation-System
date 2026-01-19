"""
Export Routes
=============

API endpoints for exporting prediction results to CSV and PDF formats.

Author: EcoPackAI Team
Date: 2026-01-12
"""

from flask import Blueprint, jsonify, request, send_file, make_response
from datetime import datetime
import pandas as pd
import io
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Create blueprint
export_bp = Blueprint('export', __name__, url_prefix='/api/v1/export')


def generate_csv_from_prediction(prediction_data: Dict) -> str:
    """
    Generate CSV content from prediction data
    
    Args:
        prediction_data: Prediction result dictionary
        
    Returns:
        CSV string content
    """
    rows = []
    
    # Add metadata
    rows.append(['Parameter', 'Value'])
    rows.append(['Timestamp', prediction_data.get('timestamp', datetime.now().isoformat())])
    rows.append(['Prediction Type', prediction_data.get('prediction_type', 'all')])
    rows.append(['', ''])  # Empty row
    
    # Add results
    if 'results' in prediction_data:
        rows.append(['RESULTS', ''])
        for key, value in prediction_data['results'].items():
            param_name = key.replace('_', ' ').title()
            formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
            rows.append([param_name, formatted_value])
        rows.append(['', ''])
    
    # Add metadata
    if 'metadata' in prediction_data:
        rows.append(['METADATA', ''])
        for key, value in prediction_data['metadata'].items():
            param_name = key.replace('_', ' ').title()
            rows.append([param_name, str(value)])
    
    # Convert to CSV
    df = pd.DataFrame(rows)
    csv_content = df.to_csv(index=False, header=False)
    
    return csv_content


def generate_materials_comparison_csv(materials: list) -> str:
    """
    Generate CSV for materials comparison
    
    Args:
        materials: List of material dictionaries
        
    Returns:
        CSV string content
    """
    export_data = []
    
    for idx, material in enumerate(materials):
        row = {
            'Material ID': material.get('id') or material.get('name') or f'Material {idx + 1}',
            'Predicted Cost ($)': f"{material.get('predicted_cost', 0):.2f}",
            'Predicted CO₂ (kg)': f"{material.get('predicted_co2', 0):.4f}",
            'Cost Confidence': f"{material.get('cost_confidence', 0):.4f}",
            'Recyclability (%)': material.get('recyclability_percent', 'N/A'),
            'Recycled Content (%)': material.get('recycled_content_percent', 'N/A'),
            'Sustainability Score': f"{material.get('overall_sustainability_score', 0):.4f}",
            'Material Suitability': material.get('material_suitability_score', 'N/A')
        }
        export_data.append(row)
    
    df = pd.DataFrame(export_data)
    csv_content = df.to_csv(index=False)
    
    return csv_content


@export_bp.route('/csv', methods=['POST'])
def export_csv():
    """
    Export prediction results to CSV
    
    Request Body:
        {
            "prediction_data": {...},
            "export_type": "single" | "comparison",
            "materials": [...] (for comparison export)
        }
    
    Response:
        200: CSV file download
        400: Invalid input
        500: Export error
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "No data provided"
            }), 400
        
        export_type = data.get('export_type', 'single')
        
        if export_type == 'single':
            # Export single prediction
            prediction_data = data.get('prediction_data')
            if not prediction_data:
                return jsonify({
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "Missing prediction_data"
                }), 400
            
            csv_content = generate_csv_from_prediction(prediction_data)
            filename = f"ecopack_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        elif export_type == 'comparison':
            # Export materials comparison
            materials = data.get('materials')
            if not materials or not isinstance(materials, list):
                return jsonify({
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "Missing or invalid materials array"
                }), 400
            
            csv_content = generate_materials_comparison_csv(materials)
            filename = f"materials_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        else:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": f"Unknown export_type: {export_type}"
            }), 400
        
        # Create response with CSV file
        output = io.StringIO()
        output.write(csv_content)
        output.seek(0)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        logger.info(f"CSV export successful: {filename}")
        return response
        
    except Exception as e:
        logger.error(f"CSV export error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Export Error",
            "message": str(e)
        }), 500


@export_bp.route('/pdf', methods=['POST'])
def export_pdf():
    """
    Export prediction results to PDF
    
    Note: This is a placeholder endpoint. PDF generation requires
    additional libraries like ReportLab or WeasyPrint.
    
    Request Body:
        {
            "prediction_data": {...},
            "include_charts": true|false
        }
    
    Response:
        200: PDF file download
        400: Invalid input
        501: Not implemented (if PDF library not available)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "No data provided"
            }), 400
        
        # Check if PDF libraries are available
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.units import inch
        except ImportError:
            logger.warning("ReportLab not installed, PDF export unavailable")
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "PDF Export Not Available",
                "message": "PDF generation library not installed. Please use client-side PDF export."
            }), 501
        
        prediction_data = data.get('prediction_data')
        if not prediction_data:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Missing prediction_data"
            }), 400
        
        # Generate PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#10B981'),
            spaceAfter=30
        )
        title = Paragraph("EcoPackAI Sustainability Report", title_style)
        elements.append(title)
        
        # Subtitle
        subtitle = Paragraph(
            "AI-Powered Packaging Analysis",
            styles['Heading2']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Metadata
        metadata_data = [
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Prediction Time:', prediction_data.get('timestamp', 'N/A')]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Results
        if 'results' in prediction_data:
            results_title = Paragraph("Prediction Results", styles['Heading2'])
            elements.append(results_title)
            elements.append(Spacer(1, 0.2*inch))
            
            results = prediction_data['results']
            results_data = []
            
            for key, value in results.items():
                param_name = key.replace('_', ' ').title()
                formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
                results_data.append([param_name, formatted_value])
            
            results_table = Table(results_data, colWidths=[3*inch, 3*inch])
            results_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ]))
            elements.append(results_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Model Information
        if 'metadata' in prediction_data:
            model_title = Paragraph("Model Information", styles['Heading2'])
            elements.append(model_title)
            elements.append(Spacer(1, 0.2*inch))
            
            metadata = prediction_data['metadata']
            model_data = []
            
            for key, value in metadata.items():
                param_name = key.replace('_', ' ').title()
                model_data.append([param_name, str(value)])
            
            model_table = Table(model_data, colWidths=[3*inch, 3*inch])
            model_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ]))
            elements.append(model_table)
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        filename = f"ecopack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"PDF export error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Export Error",
            "message": str(e)
        }), 500


@export_bp.route('/formats', methods=['GET'])
def get_export_formats():
    """
    Get available export formats
    
    Response:
        200: List of available formats
    """
    formats = {
        "csv": {
            "name": "CSV (Comma-Separated Values)",
            "extension": ".csv",
            "mime_type": "text/csv",
            "available": True,
            "description": "Export data in CSV format for Excel and data analysis tools"
        },
        "pdf": {
            "name": "PDF (Portable Document Format)",
            "extension": ".pdf",
            "mime_type": "application/pdf",
            "available": False,  # Will be set based on library availability
            "description": "Export formatted report as PDF document"
        }
    }
    
    # Check PDF availability
    try:
        import reportlab
        formats["pdf"]["available"] = True
    except ImportError:
        pass
    
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "formats": formats
    }), 200
