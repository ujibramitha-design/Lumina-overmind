"""
Dashboard Components - Visual Engine
Reusable dashboard components and widgets
"""

class DashboardComponents:
    """Collection of reusable dashboard components"""
    
    def __init__(self):
        self.name = "Dashboard Components"
        self.version = "1.0.0"
        self.component_library = self._initialize_components()
    
    def create_kpi_card(self, title, value, trend, icon='chart-line'):
        """Create KPI card component"""
        component = {
            'type': 'kpi_card',
            'title': title,
            'value': value,
            'trend': trend,
            'icon': icon,
            'styling': {
                'background_color': '#ffffff',
                'text_color': '#333333',
                'border_color': '#e0e0e0'
            },
            'size': {'width': '250px', 'height': '120px'}
        }
        return component
    
    def create_lead_funnel(self, funnel_data):
        """Create lead funnel visualization"""
        component = {
            'type': 'funnel_chart',
            'title': 'Lead Conversion Funnel',
            'data': funnel_data,
            'stages': ['Awareness', 'Interest', 'Consideration', 'Decision', 'Purchase'],
            'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83'],
            'interactive': True,
            'animations': True
        }
        return component
    
    def create_performance_gauge(self, metric_name, current_value, target_value, ranges):
        """Create performance gauge component"""
        component = {
            'type': 'gauge',
            'title': metric_name,
            'current_value': current_value,
            'target_value': target_value,
            'ranges': ranges,
            'colors': {
                'excellent': '#6BCF7F',
                'good': '#FFD93D',
                'warning': '#FF6B6B'
            },
            'size': {'width': '300px', 'height': '200px'}
        }
        return component
    
    def create_activity_timeline(self, activities):
        """Create activity timeline component"""
        component = {
            'type': 'timeline',
            'title': 'Recent Activities',
            'activities': activities,
            'grouping': 'daily',
            'filters': ['leads', 'conversions', 'meetings', 'calls'],
            'max_items': 20,
            'auto_refresh': True
        }
        return component
    
    def create_market_heatmap(self, market_data):
        """Create market heatmap component"""
        component = {
            'type': 'heatmap',
            'title': 'Market Activity Heatmap',
            'data': market_data,
            'color_scale': 'viridis',
            'interactive': True,
            'tooltip_format': 'detailed',
            'legend_position': 'right'
        }
        return component
    
    def create_leaderboard(self, leaderboard_data):
        """Create leaderboard component"""
        component = {
            'type': 'leaderboard',
            'title': 'Top Performers',
            'data': leaderboard_data,
            'columns': ['rank', 'name', 'score', 'trend'],
            'sorting': 'score',
            'max_items': 10,
            'animations': True
        }
        return component
    
    def create_alert_panel(self, alerts):
        """Create alert panel component"""
        component = {
            'type': 'alert_panel',
            'title': 'System Alerts',
            'alerts': alerts,
            'severity_levels': ['critical', 'warning', 'info'],
            'auto_dismiss': {'info': 5000, 'warning': 10000},
            'actions': ['dismiss', 'acknowledge', 'investigate']
        }
        return component
    
    def create_data_table(self, table_data, columns):
        """Create data table component"""
        component = {
            'type': 'data_table',
            'title': 'Data Table',
            'data': table_data,
            'columns': columns,
            'features': {
                'sorting': True,
                'filtering': True,
                'pagination': True,
                'export': True,
                'search': True
            },
            'page_size': 25
        }
        return component
    
    def create_chart_container(self, chart_config):
        """Create chart container component"""
        component = {
            'type': 'chart_container',
            'chart': chart_config,
            'controls': {
                'zoom': True,
                'pan': True,
                'fullscreen': True,
                'export': True
            },
            'responsive': True,
            'loading_indicator': True
        }
        return component
    
    def create_filter_panel(self, filter_options):
        """Create filter panel component"""
        component = {
            'type': 'filter_panel',
            'title': 'Filters',
            'filters': filter_options,
            'layout': 'vertical',
            'collapsible': True,
            'reset_button': True
        }
        return component
    
    def _initialize_components(self):
        """Initialize component library"""
        return {
            'kpi_card': self.create_kpi_card,
            'lead_funnel': self.create_lead_funnel,
            'performance_gauge': self.create_performance_gauge,
            'activity_timeline': self.create_activity_timeline,
            'market_heatmap': self.create_market_heatmap,
            'leaderboard': self.create_leaderboard,
            'alert_panel': self.create_alert_panel,
            'data_table': self.create_data_table,
            'chart_container': self.create_chart_container,
            'filter_panel': self.create_filter_panel
        }
