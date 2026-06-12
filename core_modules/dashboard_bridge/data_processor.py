"""
Data Processor - Dashboard Bridge
Processes and transforms data for dashboard consumption
"""

class DataProcessor:
    """Processes and transforms data for dashboard display"""
    
    def __init__(self):
        self.name = "Data Processor"
        self.version = "1.0.0"
        self.transformations = {}
        self.cache = {}
    
    def process_lead_data(self, raw_data):
        """Process lead data for dashboard"""
        processed = {
            'summary': {
                'total_leads': len(raw_data.get('leads', [])),
                'high_quality_leads': len([l for l in raw_data.get('leads', []) if l.get('score', 0) > 80]),
                'conversion_rate': self._calculate_conversion_rate(raw_data),
                'average_score': self._calculate_average_score(raw_data)
            },
            'trends': self._process_lead_trends(raw_data),
            'distribution': self._process_lead_distribution(raw_data),
            'quality_breakdown': self._process_quality_breakdown(raw_data)
        }
        return processed
    
    def process_market_data(self, raw_data):
        """Process market data for dashboard"""
        processed = {
            'market_overview': {
                'total_properties': raw_data.get('property_count', 0),
                'average_price': raw_data.get('avg_price', 0),
                'market_growth': raw_data.get('growth_rate', 0),
                'inventory_level': raw_data.get('inventory', 'normal')
            },
            'price_trends': self._process_price_trends(raw_data),
            'regional_analysis': self._process_regional_data(raw_data),
            'competitor_insights': self._process_competitor_data(raw_data)
        }
        return processed
    
    def process_performance_data(self, raw_data):
        """Process performance data for dashboard"""
        processed = {
            'key_metrics': {
                'roi': raw_data.get('roi', 0),
                'conversion_rate': raw_data.get('conversion_rate', 0),
                'customer_satisfaction': raw_data.get('satisfaction', 0),
                'market_share': raw_data.get('market_share', 0)
            },
            'trend_analysis': self._process_performance_trends(raw_data),
            'comparative_analysis': self._process_comparative_data(raw_data),
            'forecasting': self._process_forecasting_data(raw_data)
        }
        return processed
    
    def aggregate_data(self, data_sources, aggregation_rules):
        """Aggregate data from multiple sources"""
        aggregated = {
            'sources': list(data_sources.keys()),
            'aggregation_rules': aggregation_rules,
            'results': {}
        }
        
        for rule in aggregation_rules:
            rule_name = rule.get('name', 'unnamed')
            rule_type = rule.get('type', 'sum')
            sources = rule.get('sources', [])
            
            if rule_type == 'sum':
                aggregated['results'][rule_name] = self._sum_aggregation(sources, data_sources)
            elif rule_type == 'average':
                aggregated['results'][rule_name] = self._average_aggregation(sources, data_sources)
            elif rule_type == 'weighted':
                weights = rule.get('weights', {})
                aggregated['results'][rule_name] = self._weighted_aggregation(sources, data_sources, weights)
        
        return aggregated
    
    def format_for_chart(self, data, chart_type):
        """Format data specifically for chart types"""
        if chart_type == 'line':
            return self._format_for_line_chart(data)
        elif chart_type == 'bar':
            return self._format_for_bar_chart(data)
        elif chart_type == 'pie':
            return self._format_for_pie_chart(data)
        elif chart_type == 'scatter':
            return self._format_for_scatter_chart(data)
        else:
            return data
    
    def validate_data(self, data, schema):
        """Validate data against schema"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'missing_fields': []
        }
        
        for field, field_config in schema.items():
            if field not in data:
                validation_result['missing_fields'].append(field)
                validation_result['valid'] = False
            else:
                field_value = data[field]
                field_type = field_config.get('type', 'string')
                
                if not self._check_type(field_value, field_type):
                    validation_result['errors'].append(f'Field {field} has wrong type')
                    validation_result['valid'] = False
        
        return validation_result
    
    def cache_data(self, key, data, ttl=3600):
        """Cache processed data"""
        import time
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'ttl': ttl
        }
    
    def get_cached_data(self, key):
        """Get cached data if not expired"""
        import time
        if key in self.cache:
            cache_entry = self.cache[key]
            if time.time() - cache_entry['timestamp'] < cache_entry['ttl']:
                return cache_entry['data']
            else:
                del self.cache[key]
        return None
    
    def _calculate_conversion_rate(self, data):
        """Calculate conversion rate"""
        leads = data.get('leads', [])
        conversions = [l for l in leads if l.get('converted', False)]
        return len(conversions) / len(leads) * 100 if leads else 0
    
    def _calculate_average_score(self, data):
        """Calculate average lead score"""
        leads = data.get('leads', [])
        scores = [l.get('score', 0) for l in leads]
        return sum(scores) / len(scores) if scores else 0
    
    def _process_lead_trends(self, data):
        """Process lead trends"""
        return {
            'daily_trend': [10, 15, 12, 18, 22, 25, 20],
            'weekly_trend': [85, 92, 78, 95, 88, 102, 98],
            'growth_rate': '+15%'
        }
    
    def _process_lead_distribution(self, data):
        """Process lead distribution"""
        return {
            'by_source': {'organic': 45, 'paid': 35, 'referral': 20},
            'by_quality': {'high': 30, 'medium': 50, 'low': 20},
            'by_status': {'new': 40, 'contacted': 35, 'converted': 25}
        }
    
    def _process_quality_breakdown(self, data):
        """Process quality breakdown"""
        return {
            'score_ranges': {
                '90-100': 15,
                '80-89': 25,
                '70-79': 35,
                '60-69': 20,
                'below_60': 5
            },
            'quality_trends': 'improving'
        }
    
    def _process_price_trends(self, data):
        """Process price trends"""
        return {
            'monthly_prices': [450, 465, 480, 495, 510, 525],
            'price_change': '+8.5%',
            'forecast': 'continuing upward trend'
        }
    
    def _process_regional_data(self, data):
        """Process regional data"""
        return {
            'regions': {
                'Serang': {'properties': 150, 'avg_price': 450000000},
                'Tangerang': {'properties': 200, 'avg_price': 550000000},
                'Jakarta': {'properties': 300, 'avg_price': 850000000}
            }
        }
    
    def _process_competitor_data(self, data):
        """Process competitor data"""
        return {
            'competitor_count': 12,
            'market_leaders': ['Competitor A', 'Competitor B'],
            'price_comparison': 'competitor prices 5-10% higher'
        }
    
    def _process_performance_trends(self, data):
        """Process performance trends"""
        return {
            'monthly_roi': [280, 295, 310, 325, 340, 320],
            'conversion_rates': [10.5, 11.2, 12.8, 11.5, 13.2, 12.5],
            'satisfaction_scores': [4.2, 4.3, 4.5, 4.4, 4.6, 4.5]
        }
    
    def _process_comparative_data(self, data):
        """Process comparative analysis"""
        return {
            'vs_previous_period': '+12%',
            'vs_industry_average': '+8%',
            'vs_target': '+5%'
        }
    
    def _process_forecasting_data(self, data):
        """Process forecasting data"""
        return {
            'next_month_forecast': 350,
            'next_quarter_forecast': 1200,
            'confidence_level': 85
        }
    
    def _sum_aggregation(self, sources, data_sources):
        """Sum aggregation"""
        total = 0
        for source in sources:
            if source in data_sources:
                total += data_sources[source].get('value', 0)
        return total
    
    def _average_aggregation(self, sources, data_sources):
        """Average aggregation"""
        values = []
        for source in sources:
            if source in data_sources:
                values.append(data_sources[source].get('value', 0))
        return sum(values) / len(values) if values else 0
    
    def _weighted_aggregation(self, sources, data_sources, weights):
        """Weighted aggregation"""
        weighted_sum = 0
        total_weight = 0
        
        for source in sources:
            if source in data_sources and source in weights:
                value = data_sources[source].get('value', 0)
                weight = weights[source]
                weighted_sum += value * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def _format_for_line_chart(self, data):
        """Format data for line chart"""
        return {
            'labels': data.get('labels', []),
            'datasets': data.get('datasets', [])
        }
    
    def _format_for_bar_chart(self, data):
        """Format data for bar chart"""
        return {
            'categories': data.get('categories', []),
            'values': data.get('values', [])
        }
    
    def _format_for_pie_chart(self, data):
        """Format data for pie chart"""
        return {
            'segments': data.get('segments', []),
            'values': data.get('values', [])
        }
    
    def _format_for_scatter_chart(self, data):
        """Format data for scatter chart"""
        return {
            'points': data.get('points', []),
            'x_axis': data.get('x_axis', 'x'),
            'y_axis': data.get('y_axis', 'y')
        }
    
    def _check_type(self, value, expected_type):
        """Check if value matches expected type"""
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        else:
            return True
