"""
Chart Generator - Visual Engine
Generates various types of charts and visualizations
"""

class ChartGenerator:
    """Generator for charts and data visualizations"""
    
    def __init__(self):
        self.name = "Chart Generator"
        self.version = "1.0.0"
        self.chart_types = ['line', 'bar', 'pie', 'scatter', 'heatmap', 'gauge']
    
    def generate_lead_conversion_chart(self, data, chart_type='line'):
        """Generate lead conversion chart"""
        chart_config = {
            'type': chart_type,
            'title': 'Lead Conversion Trends',
            'data': data,
            'x_axis': 'date',
            'y_axis': 'conversion_rate',
            'colors': ['#2E86AB', '#A23B72', '#F18F01'],
            'responsive': True,
            'interactive': True
        }
        return chart_config
    
    def generate_market_performance_chart(self, performance_data):
        """Generate market performance visualization"""
        chart_config = {
            'type': 'combination',
            'title': 'Market Performance Dashboard',
            'charts': [
                {
                    'type': 'line',
                    'data': performance_data['price_trends'],
                    'title': 'Price Trends'
                },
                {
                    'type': 'bar',
                    'data': performance_data['volume_data'],
                    'title': 'Sales Volume'
                }
            ],
            'layout': 'grid',
            'responsive': True
        }
        return chart_config
    
    def generate_demographic_chart(self, demographic_data):
        """Generate demographic visualization"""
        chart_config = {
            'type': 'pie',
            'title': 'Customer Demographics',
            'data': demographic_data,
            'segments': ['age_groups', 'income_levels', 'locations'],
            'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            'legend_position': 'right'
        }
        return chart_config
    
    def generate_roi_chart(self, roi_data):
        """Generate ROI visualization"""
        chart_config = {
            'type': 'gauge',
            'title': 'ROI Performance',
            'data': roi_data,
            'ranges': [
                {'min': 0, 'max': 100, 'color': '#FF6B6B'},
                {'min': 100, 'max': 200, 'color': '#FFD93D'},
                {'min': 200, 'max': 500, 'color': '#6BCF7F'}
            ],
            'current_value': roi_data.get('current_roi', 150)
        }
        return chart_config
    
    def export_chart(self, chart_config, format='png', filename=None):
        """Export chart to specified format"""
        export_config = {
            'chart': chart_config,
            'format': format,
            'filename': filename or f"chart_{chart_config['type']}",
            'quality': 'high',
            'dimensions': {'width': 1200, 'height': 600}
        }
        return export_config
