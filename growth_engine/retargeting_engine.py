"""
Retargeting Engine - Growth Engine
Manages retargeting campaigns and visitor tracking
"""

import json
import random
from datetime import datetime, timedelta

class RetargetingEngine:
    """Manager for retargeting campaigns and visitor tracking"""
    
    def __init__(self):
        self.name = "Retargeting Engine"
        self.version = "1.0.0"
        self.visitors = {}
        self.campaigns = {}
        self.audiences = {}
        self.tracking_pixels = {}
        self.conversion_paths = {}
    
    def create_visitor_profile(self, visitor_data):
        """Create visitor profile from tracking data"""
        visitor = {
            'visitor_id': f"VISITOR_{len(self.visitors) + 1:03d}",
            'first_visit': visitor_data.get('first_visit', datetime.now().isoformat()),
            'last_visit': visitor_data.get('last_visit', datetime.now().isoformat()),
            'visit_count': visitor_data.get('visit_count', 1),
            'pages_viewed': visitor_data.get('pages_viewed', []),
            'time_on_site': visitor_data.get('time_on_site', 0),
            'device': visitor_data.get('device', 'unknown'),
            'browser': visitor_data.get('browser', 'unknown'),
            'location': visitor_data.get('location', 'unknown'),
            'source': visitor_data.get('source', 'direct'),
            'medium': visitor_data.get('medium', 'none'),
            'campaign': visitor_data.get('campaign', 'none'),
            'keywords': visitor_data.get('keywords', []),
            'engagement_score': self._calculate_engagement_score(visitor_data),
            'conversion_probability': self._calculate_conversion_probability(visitor_data),
            'retargeting_eligible': visitor_data.get('visit_count', 1) >= 2,
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.visitors[visitor['visitor_id']] = visitor
        return visitor
    
    def _calculate_engagement_score(self, visitor_data):
        """Calculate visitor engagement score"""
        score = 0
        
        # Visit frequency
        visit_count = visitor_data.get('visit_count', 1)
        if visit_count >= 5:
            score += 20
        elif visit_count >= 3:
            score += 15
        elif visit_count >= 2:
            score += 10
        else:
            score += 5
        
        # Time on site
        time_on_site = visitor_data.get('time_on_site', 0)
        if time_on_site >= 300:  # 5 minutes
            score += 15
        elif time_on_site >= 180:  # 3 minutes
            score += 10
        elif time_on_site >= 60:  # 1 minute
            score += 5
        
        # Pages viewed
        pages_viewed = len(visitor_data.get('pages_viewed', []))
        if pages_viewed >= 5:
            score += 15
        elif pages_viewed >= 3:
            score += 10
        elif pages_viewed >= 2:
            score += 5
        
        # Source quality
        source = visitor_data.get('source', 'direct')
        if source in ['google', 'facebook', 'instagram', 'youtube']:
            score += 10
        elif source in ['direct', 'referral']:
            score += 5
        
        # Keywords
        keywords = visitor_data.get('keywords', [])
        if keywords:
            high_intent_keywords = ['property', 'real estate', 'buy', 'sell', 'investment', 'mortgage', 'loan']
            if any(keyword in ' '.join(keywords).lower() for keyword in high_intent_keywords):
                score += 10
        
        return min(100, score)
    
    def _calculate_conversion_probability(self, visitor_data):
        """Calculate visitor conversion probability"""
        probability = 0
        
        # Base probability
        probability += 0.1  # 10% base
        
        # Engagement score influence
        engagement_score = self._calculate_engagement_score(visitor_data)
        probability += (engagement_score / 100) * 0.3  # Up to 30% based on engagement
        
        # Visit frequency influence
        visit_count = visitor_data.get('visit_count', 1)
        if visit_count >= 5:
            probability += 0.2
        elif visit_count >= 3:
            probability += 0.15
        elif visit_count >= 2:
            probability += 0.1
        
        # Time on site influence
        time_on_site = visitor_data.get('time_on_site', 0)
        if time_on_site >= 300:
            probability += 0.1
        elif time_on_site >= 180:
            probability += 0.05
        
        # Pages viewed influence
        pages_viewed = len(visitor_data.get('pages_viewed', []))
        if pages_viewed >= 5:
            probability += 0.1
        elif pages_viewed >= 3:
            probability += 0.05
        
        return min(0.8, probability)  # Cap at 80%
    
    def create_retargeting_audience(self, audience_config):
        """Create retargeting audience"""
        audience = {
            'audience_id': f"RT_AUDIENCE_{len(self.audiences) + 1:03d}",
            'name': audience_config.get('name', 'Retargeting Audience'),
            'type': audience_config.get('type', 'website_visitors'),
            'criteria': audience_config.get('criteria', {}),
            'exclusions': audience_config.get('exclusions', {}),
            'membership_duration': audience_config.get('membership_duration', 30),  # In days
            'size': 0,
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        # Calculate audience size based on criteria
        audience['size'] = self._calculate_audience_size(audience['criteria'])
        
        self.audiences[audience['audience_id']] = audience
        return audience
    
    def _calculate_audience_size(self, criteria):
        """Calculate audience size based on criteria"""
        # Simulate audience size calculation
        base_size = len(self.visitors)
        filtered_size = base_size
        
        # Apply filters
        if criteria.get('min_visits'):
            filtered_size = len([v for v in self.visitors.values() if v.get('visit_count', 0) >= criteria['min_visits']])
        
        if criteria.get('min_engagement_score'):
            filtered_size = len([v for v in self.visitors.values() if v.get('engagement_score', 0) >= criteria['min_engagement_score']])
        
        if criteria.get('visited_pages'):
            filtered_size = len([v for v in self.visitors.values() if any(page in v.get('pages_viewed', []) for page in criteria['visited_pages'])])
        
        if criteria.get('time_range'):
            # Filter by time range
            time_range = criteria['time_range']
            cutoff_date = datetime.now() - timedelta(days=time_range)
            filtered_size = len([v for v in self.visitors.values() if datetime.fromisoformat(v['last_visit']) >= cutoff_date])
        
        return filtered_size
    
    def create_retargeting_campaign(self, campaign_config):
        """Create retargeting campaign"""
        campaign = {
            'campaign_id': f"RT_CAMPAIGN_{len(self.campaigns) + 1:03d}",
            'name': campaign_config.get('name', 'Retargeting Campaign'),
            'objective': campaign_config.get('objective', 'CONVERSIONS'),
            'budget': campaign_config.get('budget', 500000),  # In IDR
            'budget_type': campaign_config.get('budget_type', 'daily'),
            'target_audience_id': campaign_config.get('target_audience_id'),
            'placements': campaign_config.get('placements', ['facebook', 'instagram', 'google_display']),
            'frequency_capping': campaign_config.get('frequency_capping', 3),  # Impressions per day
            'status': 'active',
            'start_date': campaign_config.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            'end_date': campaign_config.get('end_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'created_at': datetime.now().isoformat()
        }
        
        self.campaigns[campaign['campaign_id']] = campaign
        return campaign
    
    def track_conversion_path(self, visitor_id, conversion_data):
        """Track conversion path for visitor"""
        visitor = self.visitors.get(visitor_id)
        if not visitor:
            return None
        
        path = {
            'conversion_id': f"CONVERSION_{len(self.conversion_paths) + 1:03d}",
            'visitor_id': visitor_id,
            'conversion_type': conversion_data.get('type', 'lead'),
            'conversion_value': conversion_data.get('value', 0),
            'conversion_date': conversion_data.get('date', datetime.now().isoformat()),
            'touchpoints': self._get_visitor_touchpoints(visitor_id),
            'attribution_model': conversion_data.get('attribution_model', 'last_click'),
            'attribution': {},
            'path_length': 0,
            'time_to_conversion': self._calculate_time_to_conversion(visitor_id, conversion_data.get('date')),
            'created_at': datetime.now().isoformat()
        }
        
        # Calculate attribution
        path['attribution'] = self._calculate_attribution(path['touchpoints'], path['attribution_model'])
        path['path_length'] = len(path['touchpoints'])
        
        self.conversion_paths[path['conversion_id']] = path
        return path
    
    def _get_visitor_touchpoints(self, visitor_id):
        """Get all touchpoints for visitor"""
        visitor = self.visitors.get(visitor_id)
        if not visitor:
            return []
        
        touchpoints = []
        
        # Add source touchpoint
        if visitor.get('source') != 'direct':
            touchpoints.append({
                'channel': visitor.get('source'),
                'medium': visitor.get('medium'),
                'campaign': visitor.get('campaign'),
                'timestamp': visitor.get('first_visit'),
                'type': 'first_touch'
            })
        
        # Add page view touchpoints
        for page in visitor.get('pages_viewed', []):
            touchpoints.append({
                'channel': 'website',
                'medium': 'page_view',
                'campaign': page,
                'timestamp': visitor.get('last_visit'),
                'type': 'engagement'
            })
        
        return touchpoints
    
    def _calculate_attribution(self, touchpoints, model):
        """Calculate attribution based on model"""
        attribution = {}
        
        if not touchpoints:
            return attribution
        
        if model == 'last_click':
            # Last click gets 100% attribution
            last_touchpoint = touchpoints[-1]
            attribution[last_touchpoint['channel']] = 1.0
        
        elif model == 'first_click':
            # First click gets 100% attribution
            first_touchpoint = touchpoints[0]
            attribution[first_touchpoint['channel']] = 1.0
        
        elif model == 'linear':
            # Equal attribution to all touchpoints
            equal_share = 1.0 / len(touchpoints)
            for touchpoint in touchpoints:
                channel = touchpoint['channel']
                attribution[channel] = attribution.get(channel, 0) + equal_share
        
        elif model == 'time_decay':
            # More recent touchpoints get more attribution
            total_weight = sum(range(1, len(touchpoints) + 1))
            for i, touchpoint in enumerate(touchpoints):
                channel = touchpoint['channel']
                weight = (i + 1) / total_weight
                attribution[channel] = attribution.get(channel, 0) + weight
        
        elif model == 'position_based':
            # First and last get 40% each, middle gets 20%
            if len(touchpoints) == 1:
                attribution[touchpoints[0]['channel']] = 1.0
            else:
                first_channel = touchpoints[0]['channel']
                last_channel = touchpoints[-1]['channel']
                attribution[first_channel] = 0.4
                attribution[last_channel] = 0.4
                
                # Middle touchpoints share 20%
                middle_share = 0.2 / (len(touchpoints) - 2)
                for touchpoint in touchpoints[1:-1]:
                    channel = touchpoint['channel']
                    attribution[channel] = attribution.get(channel, 0) + middle_share
        
        return attribution
    
    def _calculate_time_to_conversion(self, visitor_id, conversion_date):
        """Calculate time from first visit to conversion"""
        visitor = self.visitors.get(visitor_id)
        if not visitor:
            return 0
        
        first_visit = datetime.fromisoformat(visitor['first_visit'])
        conversion_dt = datetime.fromisoformat(conversion_date)
        
        return (conversion_dt - first_visit).days
    
    def optimize_retargeting_campaign(self, campaign_id, optimization_config):
        """Optimize retargeting campaign performance"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        optimization = {
            'campaign_id': campaign_id,
            'optimization_type': optimization_config.get('type', 'frequency'),
            'current_performance': self.get_campaign_performance(campaign_id),
            'recommendations': [],
            'applied_changes': []
        }
        
        # Frequency capping optimization
        if optimization_config.get('type') == 'frequency':
            frequency_recommendations = self._optimize_frequency_capping(campaign, optimization_config)
            optimization['recommendations'].extend(frequency_recommendations)
        
        # Audience optimization
        elif optimization_config.get('type') == 'audience':
            audience_recommendations = self._optimize_retargeting_audience(campaign, optimization_config)
            optimization['recommendations'].extend(audience_recommendations)
        
        # Budget optimization
        elif optimization_config.get('type') == 'budget':
            budget_recommendations = self._optimize_retargeting_budget(campaign, optimization_config)
            optimization['recommendations'].extend(budget_recommendations)
        
        # Creative optimization
        elif optimization_config.get('type') == 'creative':
            creative_recommendations = self._optimize_retargeting_creative(campaign, optimization_config)
            optimization['recommendations'].extend(creative_recommendations)
        
        return optimization
    
    def _optimize_frequency_capping(self, campaign, config):
        """Optimize frequency capping"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_capping = campaign.get('frequency_capping', 3)
        
        # Check for ad fatigue
        if performance.get('click_through_rate', 0) < 1.0 and current_capping > 1:
            recommended_capping = max(1, current_capping - 1)
            recommendations.append({
                'type': 'frequency_adjustment',
                'current_capping': current_capping,
                'recommended_capping': recommended_capping,
                'reason': 'Low CTR suggests ad fatigue, reduce frequency capping'
            })
        
        # Check for underexposure
        elif performance.get('impression_share', 0) < 30 and current_capping < 5:
            recommended_capping = min(5, current_capping + 1)
            recommendations.append({
                'type': 'frequency_adjustment',
                'current_capping': current_capping,
                'recommended_capping': recommended_capping,
                'reason': 'Low impression share suggests underexposure, increase frequency capping'
            })
        
        return recommendations
    
    def _optimize_retargeting_audience(self, campaign, config):
        """Optimize retargeting audience"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_audience_id = campaign.get('target_audience_id')
        if not current_audience_id:
            recommendations.append({
                'type': 'audience_setup',
                'recommendation': 'Create retargeting audience for better performance',
                'reason': 'No target audience configured'
            })
            return recommendations
        
        current_audience = self.audiences.get(current_audience_id)
        if not current_audience:
            return recommendations
        
        # Check audience size
        current_size = current_audience.get('size', 0)
        if current_size < 1000:
            recommendations.append({
                'type': 'audience_expansion',
                'current_size': current_size,
                'recommended_size': 'Expand audience criteria',
                'reason': 'Small audience size may limit reach'
            })
        
        # Check audience freshness
        if current_audience.get('membership_duration', 30) > 90:
            recommendations.append({
                'type': 'audience_refresh',
                'current_duration': current_audience.get('membership_duration', 30),
                'recommended_duration': 30,
                'reason': 'Long membership duration may include stale visitors'
            })
        
        return recommendations
    
    def _optimize_retargeting_budget(self, campaign, config):
        """Optimize retargeting budget"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_budget = campaign.get('budget', 500000)
        current_cpa = performance.get('cost_per_conversion', 0)
        current_roas = performance.get('return_on_ad_spend', 0)
        
        # Budget increase for high-performing campaigns
        if current_cpa < config.get('target_cpa', 30000) and current_roas > config.get('target_roas', 4.0):
            recommended_increase = int(current_budget * 0.25)  # 25% increase
            recommendations.append({
                'type': 'budget_increase',
                'current_budget': current_budget,
                'recommended_budget': current_budget + recommended_increase,
                'reason': 'Low CPA and high ROAS indicate room for budget increase'
            })
        
        # Budget decrease for poor performance
        elif current_cpa > config.get('target_cpa', 30000) * 1.5:
            recommended_decrease = int(current_budget * 0.3)  # 30% decrease
            recommendations.append({
                'type': 'budget_decrease',
                'current_budget': current_budget,
                'recommended_budget': current_budget - recommended_decrease,
                'reason': 'High CPA indicates need for budget reduction'
            })
        
        return recommendations
    
    def _optimize_retargeting_creative(self, campaign, config):
        """Optimize retargeting creative"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Check for creative fatigue
        if performance.get('click_through_rate', 0) < 1.5:
            recommendations.append({
                'type': 'creative_refresh',
                'recommendation': 'Refresh ad creative to combat fatigue',
                'reason': f'Low CTR ({performance.get("click_through_rate", 0):.2f}%) suggests creative fatigue'
            })
        
        # Dynamic content recommendations
        if performance.get('conversion_rate', 0) < 2.0:
            recommendations.append({
                'type': 'dynamic_content',
                'recommendation': 'Use dynamic content to show personalized ads',
                'reason': f'Low conversion rate ({performance.get("conversion_rate", 0):.2f}%) suggests need for personalization'
            })
        
        return recommendations
    
    def get_campaign_performance(self, campaign_id):
        """Get campaign performance metrics"""
        # Simulate performance data
        performance = {
            'campaign_id': campaign_id,
            'impressions': random.randint(50000, 200000),
            'clicks': random.randint(2500, 10000),
            'conversions': random.randint(50, 500),
            'cost': random.randint(5000000, 20000000),
            'click_through_rate': random.uniform(3.0, 8.0),
            'conversion_rate': random.uniform(2.0, 5.0),
            'cost_per_click': random.uniform(1000, 3000),
            'cost_per_conversion': random.uniform(20000, 80000),
            'return_on_ad_spend': random.uniform(3.0, 10.0),
            'impression_share': random.uniform(20, 80),
            'frequency': random.uniform(2.0, 5.0),
            'reach': random.randint(25000, 100000),
            'frequency_capped_impressions': random.randint(10000, 50000)
        }
        
        return performance
    
    def generate_retargeting_report(self, campaign_id, date_range='30d'):
        """Generate comprehensive retargeting report"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        performance = self.get_campaign_performance(campaign_id)
        
        report = {
            'campaign_info': campaign,
            'performance_metrics': performance,
            'audience_analysis': self._analyze_audience_performance(campaign['target_audience_id']),
            'conversion_analysis': self._analyze_conversion_paths(campaign_id),
            'attribution_analysis': self._analyze_attribution_models(campaign_id),
            'visitor_behavior': self._analyze_visitor_behavior(campaign_id),
            'optimization_recommendations': self._generate_retargeting_recommendations(campaign_id),
            'roi_analysis': self._analyze_retargeting_roi(campaign_id),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _analyze_audience_performance(self, audience_id):
        """Analyze audience performance"""
        audience = self.audiences.get(audience_id)
        if not audience:
            return {'error': 'Audience not found'}
        
        # Get audience members
        audience_size = audience.get('size', 0)
        
        analysis = {
            'audience_id': audience_id,
            'audience_name': audience.get('name', ''),
            'audience_size': audience_size,
            'engagement_distribution': self._generate_engagement_distribution(audience_id),
            'conversion_distribution': self._generate_conversion_distribution(audience_id),
            'time_distribution': self._generate_time_distribution(audience_id),
            'device_distribution': self._generate_device_distribution(audience_id),
            'freshness_analysis': self._analyze_audience_freshness(audience_id),
            'recommendations': []
        }
        
        # Add recommendations
        if audience_size < 1000:
            analysis['recommendations'].append({
                'type': 'audience_expansion',
                'recommendation': 'Expand audience criteria to increase size',
                'priority': 'medium'
            })
        
        return analysis
    
    def _generate_engagement_distribution(self, audience_id):
        """Generate engagement distribution for audience"""
        # Simulate engagement distribution
        return {
            'high_engagement': random.randint(10, 30),  # 70-100 score
            'medium_engagement': random.randint(30, 50),  # 40-70 score
            'low_engagement': random.randint(20, 40)   # 0-40 score
        }
    
    def _generate_conversion_distribution(self, audience_id):
        """Generate conversion distribution for audience"""
        # Simulate conversion distribution
        return {
            'converted': random.randint(5, 15),
            'high_probability': random.randint(15, 25),
            'medium_probability': random.randint(25, 35),
            'low_probability': random.randint(25, 55)
        }
    
    def _generate_time_distribution(self, audience_id):
        """Generate time distribution for audience"""
        # Simulate time distribution
        return {
            'last_7_days': random.randint(20, 40),
            'last_14_days': random.randint(20, 30),
            'last_30_days': random.randint(15, 25),
            'last_60_days': random.randint(10, 20),
            'older': random.randint(5, 15)
        }
    
    def _generate_device_distribution(self, audience_id):
        """Generate device distribution for audience"""
        # Simulate device distribution
        return {
            'mobile': random.randint(60, 80),
            'desktop': random.randint(15, 25),
            'tablet': random.randint(5, 15)
        }
    
    def _analyze_audience_freshness(self, audience_id):
        """Analyze audience freshness"""
        audience = self.audiences.get(audience_id)
        if not audience:
            return {'error': 'Audience not found'}
        
        membership_duration = audience.get('membership_duration', 30)
        
        freshness_analysis = {
            'membership_duration': membership_duration,
            'freshness_score': max(0, 100 - (membership_duration / 30) * 20),  # Decreases over time
            'stale_percentage': max(0, (membership_duration - 30) / membership_duration * 100),
            'recommendation': ''
        }
        
        if membership_duration > 90:
            freshness_analysis['recommendation'] = 'Consider refreshing audience to remove stale visitors'
        elif membership_duration > 60:
            freshness_analysis['recommendation'] = 'Monitor audience performance for potential refresh'
        else:
            freshness_analysis['recommendation'] = 'Audience freshness is optimal'
        
        return freshness_analysis
    
    def _analyze_conversion_paths(self, campaign_id):
        """Analyze conversion paths for campaign"""
        # Get conversions for campaign
        campaign_conversions = [path for path in self.conversion_paths.values() if path.get('campaign_id') == campaign_id]
        
        if not campaign_conversions:
            return {'total_conversions': 0, 'analysis': 'No conversions found'}
        
        analysis = {
            'total_conversions': len(campaign_conversions),
            'average_path_length': sum(path['path_length'] for path in campaign_conversions) / len(campaign_conversions),
            'average_time_to_conversion': sum(path['time_to_conversion'] for path in campaign_conversions) / len(campaign_conversions),
            'path_distribution': self._generate_path_distribution(campaign_conversions),
            'touchpoint_analysis': self._analyze_touchpoints(campaign_conversions),
            'conversion_funnel': self._generate_conversion_funnel(campaign_conversions)
        }
        
        return analysis
    
    def _generate_path_distribution(self, conversions):
        """Generate path length distribution"""
        distribution = {
            '1_touchpoint': 0,
            '2_touchpoints': 0,
            '3_touchpoints': 0,
            '4_touchpoints': 0,
            '5_plus_touchpoints': 0
        }
        
        for conversion in conversions:
            path_length = conversion['path_length']
            if path_length == 1:
                distribution['1_touchpoint'] += 1
            elif path_length == 2:
                distribution['2_touchpoints'] += 1
            elif path_length == 3:
                distribution['3_touchpoints'] += 1
            elif path_length == 4:
                distribution['4_touchpoints'] += 1
            else:
                distribution['5_plus_touchpoints'] += 1
        
        return distribution
    
    def _analyze_touchpoints(self, conversions):
        """Analyze touchpoint effectiveness"""
        touchpoint_analysis = {}
        
        for conversion in conversions:
            for touchpoint in conversion['touchpoints']:
                channel = touchpoint['channel']
                if channel not in touchpoint_analysis:
                    touchpoint_analysis[channel] = {
                        'appearances': 0,
                        'conversions': 0,
                        'conversion_rate': 0
                    }
                
                touchpoint_analysis[channel]['appearances'] += 1
        
        # Calculate conversion rates
        for conversion in conversions:
            attribution = conversion.get('attribution', {})
            for channel, attribution_value in attribution.items():
                if channel in touchpoint_analysis:
                    touchpoint_analysis[channel]['conversions'] += attribution_value
        
        # Calculate conversion rates
        for channel in touchpoint_analysis:
            if touchpoint_analysis[channel]['appearances'] > 0:
                touchpoint_analysis[channel]['conversion_rate'] = (
                    touchpoint_analysis[channel]['conversions'] / 
                    touchpoint_analysis[channel]['appearances']
                )
        
        return touchpoint_analysis
    
    def _generate_conversion_funnel(self, conversions):
        """Generate conversion funnel analysis"""
        funnel = {
            'total_visitors': len(self.visitors),
            'retargeted_visitors': len([v for v in self.visitors.values() if v.get('retargeting_eligible', False)]),
            'total_conversions': len(conversions),
            'conversion_rate': 0,
            'retargeting_conversion_rate': 0
        }
        
        if funnel['total_visitors'] > 0:
            funnel['conversion_rate'] = (funnel['total_conversions'] / funnel['total_visitors']) * 100
        
        if funnel['retargeted_visitors'] > 0:
            funnel['retargeting_conversion_rate'] = (funnel['total_conversions'] / funnel['retargeted_visitors']) * 100
        
        return funnel
    
    def _analyze_attribution_models(self, campaign_id):
        """Analyze different attribution models"""
        campaign_conversions = [path for path in self.conversion_paths.values() if path.get('campaign_id') == campaign_id]
        
        if not campaign_conversions:
            return {'error': 'No conversions found'}
        
        models = ['last_click', 'first_click', 'linear', 'time_decay', 'position_based']
        model_analysis = {}
        
        for model in models:
            model_attribution = {}
            total_value = 0
            
            for conversion in campaign_conversions:
                attribution = self._calculate_attribution(conversion['touchpoints'], model)
                value = conversion.get('conversion_value', 1)
                total_value += value
                
                for channel, attribution_value in attribution.items():
                    if channel not in model_attribution:
                        model_attribution[channel] = 0
                    model_attribution[channel] += attribution_value * value
            
            model_analysis[model] = {
                'attribution': model_attribution,
                'total_value': total_value,
                'top_channel': max(model_attribution.items(), key=lambda x: x[1]) if model_attribution else None
            }
        
        return model_analysis
    
    def _analyze_visitor_behavior(self, campaign_id):
        """Analyze visitor behavior patterns"""
        # Get visitors who saw campaign ads
        campaign_visitors = [v for v in self.visitors.values() if v.get('retargeting_eligible', False)]
        
        if not campaign_visitors:
            return {'error': 'No visitors found'}
        
        analysis = {
            'total_visitors': len(campaign_visitors),
            'engagement_score_distribution': self._generate_engagement_score_distribution(campaign_visitors),
            'visit_frequency_distribution': self._generate_visit_frequency_distribution(campaign_visitors),
            'time_on_site_distribution': self._generate_time_on_site_distribution(campaign_visitors),
            'page_view_distribution': self._generate_page_view_distribution(campaign_visitors),
            'device_distribution': self._generate_visitor_device_distribution(campaign_visitors),
            'source_distribution': self._generate_visitor_source_distribution(campaign_visitors)
        }
        
        return analysis
    
    def _generate_engagement_score_distribution(self, visitors):
        """Generate engagement score distribution"""
        distribution = {
            '0-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0,
            '81-100': 0
        }
        
        for visitor in visitors:
            score = visitor.get('engagement_score', 0)
            if score <= 20:
                distribution['0-20'] += 1
            elif score <= 40:
                distribution['21-40'] += 1
            elif score <= 60:
                distribution['41-60'] += 1
            elif score <= 80:
                distribution['61-80'] += 1
            else:
                distribution['81-100'] += 1
        
        return distribution
    
    def _generate_visit_frequency_distribution(self, visitors):
        """Generate visit frequency distribution"""
        distribution = {
            '1_visit': 0,
            '2-3_visits': 0,
            '4-5_visits': 0,
            '6-10_visits': 0,
            '11_plus_visits': 0
        }
        
        for visitor in visitors:
            visits = visitor.get('visit_count', 1)
            if visits == 1:
                distribution['1_visit'] += 1
            elif visits <= 3:
                distribution['2-3_visits'] += 1
            elif visits <= 5:
                distribution['4-5_visits'] += 1
            elif visits <= 10:
                distribution['6-10_visits'] += 1
            else:
                distribution['11_plus_visits'] += 1
        
        return distribution
    
    def _generate_time_on_site_distribution(self, visitors):
        """Generate time on site distribution"""
        distribution = {
            '0-30_seconds': 0,
            '31-60_seconds': 0,
            '1-3_minutes': 0,
            '3-5_minutes': 0,
            '5-10_minutes': 0,
            '10_plus_minutes': 0
        }
        
        for visitor in visitors:
            time_on_site = visitor.get('time_on_site', 0)
            if time_on_site <= 30:
                distribution['0-30_seconds'] += 1
            elif time_on_site <= 60:
                distribution['31-60_seconds'] += 1
            elif time_on_site <= 180:
                distribution['1-3_minutes'] += 1
            elif time_on_site <= 300:
                distribution['3-5_minutes'] += 1
            elif time_on_site <= 600:
                distribution['5-10_minutes'] += 1
            else:
                distribution['10_plus_minutes'] += 1
        
        return distribution
    
    def _generate_page_view_distribution(self, visitors):
        """Generate page view distribution"""
        distribution = {
            '1_page': 0,
            '2-3_pages': 0,
            '4-5_pages': 0,
            '6-10_pages': 0,
            '11_plus_pages': 0
        }
        
        for visitor in visitors:
            pages = len(visitor.get('pages_viewed', []))
            if pages == 1:
                distribution['1_page'] += 1
            elif pages <= 3:
                distribution['2-3_pages'] += 1
            elif pages <= 5:
                distribution['4-5_pages'] += 1
            elif pages <= 10:
                distribution['6-10_pages'] += 1
            else:
                distribution['11_plus_pages'] += 1
        
        return distribution
    
    def _generate_visitor_device_distribution(self, visitors):
        """Generate visitor device distribution"""
        distribution = {'mobile': 0, 'desktop': 0, 'tablet': 0}
        
        for visitor in visitors:
            device = visitor.get('device', 'unknown')
            if device in distribution:
                distribution[device] += 1
        
        return distribution
    
    def _generate_visitor_source_distribution(self, visitors):
        """Generate visitor source distribution"""
        distribution = {}
        
        for visitor in visitors:
            source = visitor.get('source', 'direct')
            if source not in distribution:
                distribution[source] = 0
            distribution[source] += 1
        
        return distribution
    
    def _generate_retargeting_recommendations(self, campaign_id):
        """Generate retargeting campaign recommendations"""
        performance = self.get_campaign_performance(campaign_id)
        recommendations = []
        
        # Frequency recommendations
        if performance.get('frequency', 0) > 5:
            recommendations.append({
                'type': 'frequency',
                'priority': 'high',
                'recommendation': 'Reduce frequency capping to avoid ad fatigue',
                'reason': f'High frequency: {performance.get("frequency", 0):.1f}'
            })
        
        # CPA recommendations
        if performance.get('cost_per_conversion', 0) > 50000:
            recommendations.append({
                'type': 'budget',
                'priority': 'high',
                'recommendation': 'Optimize audience or creative to reduce CPA',
                'reason': f'High CPA: {performance.get("cost_per_conversion", 0):,.0f}'
            })
        
        # Reach recommendations
        if performance.get('reach', 0) < 20000:
            recommendations.append({
                'type': 'audience',
                'priority': 'medium',
                'recommendation': 'Expand audience criteria to increase reach',
                'reason': f'Low reach: {performance.get("reach", 0):,.0f}'
            })
        
        return recommendations
    
    def _analyze_retargeting_roi(self, campaign_id):
        """Analyze retargeting campaign ROI"""
        performance = self.get_campaign_performance(campaign_id)
        
        roi_analysis = {
            'total_cost': performance.get('cost', 0),
            'total_conversions': performance.get('conversions', 0),
            'cost_per_conversion': performance.get('cost_per_conversion', 0),
            'average_lead_value': 60000,  # Average lead value in IDR
            'total_revenue': performance.get('conversions', 0) * 60000,
            'roi': (performance.get('conversions', 0) * 60000 - performance.get('cost', 0)) / performance.get('cost', 0) * 100,
            'break_even_point': performance.get('cost', 0) / 60000,
            'profit_margin': ((performance.get('conversions', 0) * 60000 - performance.get('cost', 0)) / (performance.get('conversions', 0) * 60000)) * 100 if performance.get('conversions', 0) > 0 else 0
        }
        
        return roi_analysis
    
    def export_retargeting_data(self, campaign_id, format='json'):
        """Export retargeting data in specified format"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        data = {
            'campaign': campaign,
            'performance': self.get_campaign_performance(campaign_id),
            'audience': self.audiences.get(campaign.get('target_audience_id'), {}),
            'conversions': {path_id: path for path_id, path in self.conversion_paths.items() if path.get('campaign_id') == campaign_id}
        }
        
        if format == 'json':
            return data
        elif format == 'csv':
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(['campaign_id', 'campaign_name', 'impressions', 'clicks', 'conversions', 'cost', 'ctr', 'conversion_rate', 'cpa', 'roas', 'frequency'])
            
            # Write campaign data
            performance = data['performance']
            writer.writerow([
                campaign_id,
                campaign['name'],
                performance['impressions'],
                performance['clicks'],
                performance['conversions'],
                performance['cost'],
                performance['click_through_rate'],
                performance['conversion_rate'],
                performance['cost_per_conversion'],
                performance['return_on_ad_spend'],
                performance['frequency']
            ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def create_tracking_pixel(self, pixel_config):
        """Create tracking pixel for retargeting"""
        pixel = {
            'pixel_id': f"PIXEL_{len(self.tracking_pixels) + 1:03d}",
            'name': pixel_config.get('name', 'Retargeting Pixel'),
            'type': pixel_config.get('type', 'website'),
            'pixel_code': f"<script>\n  fbq('init', '{pixel_config.get('pixel_id', '')}');\n  fbq('track', 'PageView');\n</script>",
            'events': pixel_config.get('events', ['PageView', 'Lead', 'Purchase']),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.tracking_pixels[pixel['pixel_id']] = pixel
        return pixel
    
    def get_pixel_performance(self, pixel_id):
        """Get tracking pixel performance"""
        pixel = self.tracking_pixels.get(pixel_id)
        if not pixel:
            raise ValueError(f"Pixel {pixel_id} not found")
        
        # Simulate pixel performance
        performance = {
            'pixel_id': pixel_id,
            'pixel_name': pixel['name'],
            'total_events': random.randint(10000, 50000),
            'page_views': random.randint(5000, 25000),
            'leads': random.randint(50, 500),
            'purchases': random.randint(5, 50),
            'cost_per_lead': random.uniform(20000, 80000),
            'cost_per_purchase': random.uniform(100000, 500000),
            'event_breakdown': self._generate_event_breakdown(pixel['events']),
            'generated_at': datetime.now().isoformat()
        }
        
        return performance
    
    def _generate_event_breakdown(self, events):
        """Generate event breakdown for pixel"""
        breakdown = {}
        
        for event in events:
            breakdown[event] = random.randint(100, 5000)
        
        return breakdown
