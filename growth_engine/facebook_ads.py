"""
Facebook Ads Manager - Growth Engine
Manages Facebook advertising campaigns and optimization
"""

import json
import random
from datetime import datetime, timedelta

class FacebookAdsManager:
    """Manager for Facebook advertising campaigns"""
    
    def __init__(self):
        self.name = "Facebook Ads Manager"
        self.version = "1.0.0"
        self.campaigns = {}
        self.ad_sets = {}
        self.ads = {}
        self.performance_metrics = {}
    
    def create_campaign(self, campaign_config):
        """Create Facebook advertising campaign"""
        campaign = {
            'campaign_id': f"FB_CAMPAIGN_{len(self.campaigns) + 1:03d}",
            'name': campaign_config.get('name', 'Facebook Campaign'),
            'objective': campaign_config.get('objective', 'lead_generation'),
            'budget': campaign_config.get('budget', 1000000),  # In IDR
            'budget_type': campaign_config.get('budget_type', 'daily'),
            'status': 'active',
            'start_date': campaign_config.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            'end_date': campaign_config.get('end_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'target_audience': campaign_config.get('target_audience', {}),
            'placements': campaign_config.get('placements', ['facebook_feed', 'instagram_feed']),
            'created_at': datetime.now().isoformat(),
            'optimization_goal': campaign_config.get('optimization_goal', 'leads')
        }
        
        self.campaigns[campaign['campaign_id']] = campaign
        return campaign
    
    def create_ad_set(self, campaign_id, ad_set_config):
        """Create ad set within campaign"""
        ad_set = {
            'ad_set_id': f"FB_ADSET_{len(self.ad_sets) + 1:03d}",
            'campaign_id': campaign_id,
            'name': ad_set_config.get('name', 'Ad Set'),
            'budget': ad_set_config.get('budget', 500000),  # In IDR
            'budget_type': ad_set_config.get('budget_type', 'daily'),
            'target_audience': self._build_target_audience(ad_set_config.get('target_audience', {})),
            'placements': ad_set_config.get('placements', ['facebook_feed', 'instagram_feed']),
            'optimization_goal': ad_set_config.get('optimization_goal', 'leads'),
            'bid_strategy': ad_set_config.get('bid_strategy', 'lowest_cost'),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ad_sets[ad_set['ad_set_id']] = ad_set
        return ad_set
    
    def create_ad(self, ad_set_id, ad_config):
        """Create ad within ad set"""
        ad = {
            'ad_id': f"FB_AD_{len(self.ads) + 1:03d}",
            'ad_set_id': ad_set_id,
            'name': ad_config.get('name', 'Facebook Ad'),
            'creative': {
                'title': ad_config.get('title', 'Amazing Property Deal!'),
                'description': ad_config.get('description', 'Check out our latest property offerings'),
                'image_url': ad_config.get('image_url', ''),
                'video_url': ad_config.get('video_url', ''),
                'call_to_action': ad_config.get('call_to_action', 'LEARN_MORE'),
                'landing_page_url': ad_config.get('landing_page_url', ''),
                'display_link': ad_config.get('display_link', '')
            },
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[ad['ad_id']] = ad
        return ad
    
    def _build_target_audience(self, audience_config):
        """Build comprehensive target audience"""
        audience = {
            'age_min': audience_config.get('age_min', 25),
            'age_max': audience_config.get('age_max', 55),
            'genders': audience_config.get('genders', ['men', 'women']),
            'locations': audience_config.get('locations', ['Serang', 'Banten']),
            'radius': audience_config.get('radius', 50),  # In kilometers
            'interests': audience_config.get('interests', ['real estate', 'property investment', 'home buying']),
            'behaviors': audience_config.get('behaviors', ['engaged_shoppers', 'frequent_travelers']),
            'education': audience_config.get('education', ['college', 'graduate_school']),
            'income_level': audience_config.get('income_level', 'medium'),
            'relationship_status': audience_config.get('relationship_status', ['married', 'in_relationship']),
            'custom_audiences': audience_config.get('custom_audiences', []),
            'excluded_audiences': audience_config.get('excluded_audiences', [])
        }
        
        return audience
    
    def optimize_campaign(self, campaign_id, optimization_config):
        """Optimize campaign performance"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        optimization = {
            'campaign_id': campaign_id,
            'optimization_type': optimization_config.get('type', 'budget'),
            'current_performance': self.get_campaign_performance(campaign_id),
            'recommendations': [],
            'applied_changes': []
        }
        
        # Budget optimization
        if optimization_config.get('type') == 'budget':
            budget_recommendations = self._optimize_budget(campaign, optimization_config)
            optimization['recommendations'].extend(budget_recommendations)
        
        # Audience optimization
        elif optimization_config.get('type') == 'audience':
            audience_recommendations = self._optimize_audience(campaign, optimization_config)
            optimization['recommendations'].extend(audience_recommendations)
        
        # Creative optimization
        elif optimization_config.get('type') == 'creative':
            creative_recommendations = self._optimize_creative(campaign, optimization_config)
            optimization['recommendations'].extend(creative_recommendations)
        
        # Placement optimization
        elif optimization_config.get('type') == 'placement':
            placement_recommendations = self._optimize_placements(campaign, optimization_config)
            optimization['recommendations'].extend(placement_recommendations)
        
        return optimization
    
    def _optimize_budget(self, campaign, config):
        """Optimize campaign budget"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_budget = campaign['budget']
        current_cpa = performance.get('cost_per_lead', 0)
        current_roas = performance.get('return_on_ad_spend', 0)
        
        # Budget increase recommendation
        if current_cpa < config.get('target_cpa', 50000) and current_roas > config.get('target_roas', 3.0):
            recommended_increase = int(current_budget * 0.2)  # 20% increase
            recommendations.append({
                'type': 'budget_increase',
                'current_budget': current_budget,
                'recommended_budget': current_budget + recommended_increase,
                'reason': 'Low CPA and high ROAS indicate room for budget increase'
            })
        
        # Budget decrease recommendation
        elif current_cpa > config.get('target_cpa', 50000) * 1.5:
            recommended_decrease = int(current_budget * 0.3)  # 30% decrease
            recommendations.append({
                'type': 'budget_decrease',
                'current_budget': current_budget,
                'recommended_budget': current_budget - recommended_decrease,
                'reason': 'High CPA indicates need for budget reduction'
            })
        
        return recommendations
    
    def _optimize_audience(self, campaign, config):
        """Optimize target audience"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Age optimization
        current_age_range = [campaign['target_audience'].get('age_min', 25), 
                           campaign['target_audience'].get('age_max', 55)]
        
        if performance.get('click_through_rate', 0) < 1.0:
            # Suggest expanding age range
            recommendations.append({
                'type': 'age_expansion',
                'current_range': current_age_range,
                'recommended_range': [20, 60],
                'reason': 'Low CTR suggests audience may be too narrow'
            })
        
        # Interest optimization
        current_interests = campaign['target_audience'].get('interests', [])
        if len(current_interests) < 5:
            new_interests = ['property investment', 'home buying', 'real estate', 'mortgage', 'housing market']
            recommendations.append({
                'type': 'interest_expansion',
                'current_interests': current_interests,
                'recommended_interests': new_interests,
                'reason': 'Expand interests to reach broader audience'
            })
        
        return recommendations
    
    def _optimize_creative(self, campaign, config):
        """Optimize ad creative"""
        recommendations = []
        
        # Get campaign ads
        campaign_ads = [ad for ad in self.ads.values() if ad.get('campaign_id') == campaign['campaign_id']]
        
        for ad in campaign_ads:
            ad_performance = self.get_ad_performance(ad['ad_id'])
            
            # Title optimization
            title = ad['creative'].get('title', '')
            if len(title) < 20:
                recommendations.append({
                    'type': 'title_optimization',
                    'ad_id': ad['ad_id'],
                    'current_title': title,
                    'recommended_title': f"🏠 {title} - Limited Time Offer!",
                    'reason': 'Short titles may not be compelling enough'
                })
            
            # Call-to-action optimization
            cta = ad['creative'].get('call_to_action', '')
            if cta == 'LEARN_MORE':
                recommendations.append({
                    'type': 'cta_optimization',
                    'ad_id': ad['ad_id'],
                    'current_cta': cta,
                    'recommended_cta': 'SIGN_UP',
                    'reason': 'SIGN_UP may generate more qualified leads'
                })
        
        return recommendations
    
    def _optimize_placements(self, campaign, config):
        """Optimize ad placements"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Placement performance analysis
        placement_performance = performance.get('placement_performance', {})
        
        # Find best performing placement
        if placement_performance:
            best_placement = max(placement_performance.items(), key=lambda x: x[1].get('conversion_rate', 0))
            worst_placement = min(placement_performance.items(), key=lambda x: x[1].get('conversion_rate', 0))
            
            # Recommend focusing on best placement
            recommendations.append({
                'type': 'placement_focus',
                'best_placement': best_placement[0],
                'best_performance': best_placement[1],
                'recommendation': f"Increase budget for {best_placement[0]}",
                'reason': f"Best performing placement with {best_placement[1].get('conversion_rate', 0):.2f}% conversion rate"
            })
            
            # Recommend removing worst placement
            recommendations.append({
                'type': 'placement_removal',
                'worst_placement': worst_placement[0],
                'worst_performance': worst_placement[1],
                'recommendation': f"Consider removing {worst_placement[0]}",
                'reason': f"Worst performing placement with {worst_placement[1].get('conversion_rate', 0):.2f}% conversion rate"
            })
        
        return recommendations
    
    def get_campaign_performance(self, campaign_id):
        """Get campaign performance metrics"""
        # Simulate performance data
        performance = {
            'campaign_id': campaign_id,
            'impressions': random.randint(10000, 50000),
            'clicks': random.randint(500, 2000),
            'conversions': random.randint(10, 100),
            'cost': random.randint(500000, 2000000),
            'click_through_rate': random.uniform(0.5, 3.0),
            'conversion_rate': random.uniform(0.5, 2.0),
            'cost_per_click': random.uniform(500, 2000),
            'cost_per_lead': random.uniform(20000, 80000),
            'return_on_ad_spend': random.uniform(2.0, 8.0),
            'placement_performance': self._generate_placement_performance(),
            'age_performance': self._generate_age_performance(),
            'gender_performance': self._generate_gender_performance()
        }
        
        return performance
    
    def get_ad_performance(self, ad_id):
        """Get ad performance metrics"""
        performance = {
            'ad_id': ad_id,
            'impressions': random.randint(5000, 25000),
            'clicks': random.randint(250, 1000),
            'conversions': random.randint(5, 50),
            'cost': random.randint(250000, 1000000),
            'click_through_rate': random.uniform(0.5, 3.0),
            'conversion_rate': random.uniform(0.5, 2.0),
            'cost_per_click': random.uniform(500, 2000),
            'cost_per_lead': random.uniform(20000, 80000),
            'return_on_ad_spend': random.uniform(2.0, 8.0)
        }
        
        return performance
    
    def _generate_placement_performance(self):
        """Generate placement performance data"""
        placements = ['facebook_feed', 'instagram_feed', 'facebook_stories', 'instagram_stories', 'facebook_marketplace']
        performance = {}
        
        for placement in placements:
            performance[placement] = {
                'impressions': random.randint(2000, 10000),
                'clicks': random.randint(100, 400),
                'conversions': random.randint(2, 20),
                'conversion_rate': random.uniform(0.5, 2.0)
            }
        
        return performance
    
    def _generate_age_performance(self):
        """Generate age group performance data"""
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        performance = {}
        
        for age_group in age_groups:
            performance[age_group] = {
                'impressions': random.randint(1000, 5000),
                'clicks': random.randint(50, 200),
                'conversions': random.randint(1, 10),
                'conversion_rate': random.uniform(0.5, 2.0)
            }
        
        return performance
    
    def _generate_gender_performance(self):
        """Generate gender performance data"""
        genders = ['men', 'women']
        performance = {}
        
        for gender in genders:
            performance[gender] = {
                'impressions': random.randint(5000, 25000),
                'clicks': random.randint(250, 1000),
                'conversions': random.randint(5, 50),
                'conversion_rate': random.uniform(0.5, 2.0)
            }
        
        return performance
    
    def create_a_b_test(self, campaign_id, test_config):
        """Create A/B test for campaign"""
        test = {
            'test_id': f"FB_AB_TEST_{len(self.campaigns) + 1:03d}",
            'campaign_id': campaign_id,
            'name': test_config.get('name', 'A/B Test'),
            'test_type': test_config.get('test_type', 'creative'),
            'variants': test_config.get('variants', []),
            'traffic_split': test_config.get('traffic_split', [50, 50]),
            'duration_days': test_config.get('duration_days', 7),
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'results': {}
        }
        
        return test
    
    def analyze_a_b_test_results(self, test_id):
        """Analyze A/B test results"""
        # Simulate test results
        results = {
            'test_id': test_id,
            'variant_results': {
                'variant_a': {
                    'impressions': random.randint(10000, 50000),
                    'clicks': random.randint(500, 2000),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(0.5, 2.0),
                    'cost_per_conversion': random.uniform(20000, 80000)
                },
                'variant_b': {
                    'impressions': random.randint(10000, 50000),
                    'clicks': random.randint(500, 2000),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(0.5, 2.0),
                    'cost_per_conversion': random.uniform(20000, 80000)
                }
            },
            'winner': None,
            'confidence_level': 0,
            'recommendation': ''
        }
        
        # Determine winner
        variant_a_rate = results['variant_results']['variant_a']['conversion_rate']
        variant_b_rate = results['variant_results']['variant_b']['conversion_rate']
        
        if variant_a_rate > variant_b_rate:
            results['winner'] = 'variant_a'
            results['confidence_level'] = min(95, (variant_a_rate - variant_b_rate) * 50)
            results['recommendation'] = 'Implement variant A as the winning creative'
        elif variant_b_rate > variant_a_rate:
            results['winner'] = 'variant_b'
            results['confidence_level'] = min(95, (variant_b_rate - variant_a_rate) * 50)
            results['recommendation'] = 'Implement variant B as the winning creative'
        else:
            results['winner'] = 'inconclusive'
            results['confidence_level'] = 0
            results['recommendation'] = 'Test results are inconclusive, consider running a different test'
        
        return results
    
    def generate_campaign_report(self, campaign_id, date_range='7d'):
        """Generate comprehensive campaign report"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        performance = self.get_campaign_performance(campaign_id)
        
        report = {
            'campaign_info': campaign,
            'performance_metrics': performance,
            'ad_performance': self._get_campaign_ads_performance(campaign_id),
            'trend_analysis': self._analyze_campaign_trends(campaign_id, date_range),
            'optimization_recommendations': self._generate_campaign_recommendations(campaign_id),
            'roi_analysis': self._analyze_campaign_roi(campaign_id),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _get_campaign_ads_performance(self, campaign_id):
        """Get performance of all ads in campaign"""
        campaign_ads = [ad for ad in self.ads.values() if ad.get('campaign_id') == campaign_id]
        ad_performance = {}
        
        for ad in campaign_ads:
            ad_performance[ad['ad_id']] = self.get_ad_performance(ad['ad_id'])
        
        return ad_performance
    
    def _analyze_campaign_trends(self, campaign_id, date_range):
        """Analyze campaign trends over time"""
        # Simulate trend data
        days = int(date_range.replace('d', ''))
        trends = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
            trends.append({
                'date': date,
                'impressions': random.randint(1000, 5000),
                'clicks': random.randint(50, 200),
                'conversions': random.randint(1, 10),
                'cost': random.randint(50000, 200000)
            })
        
        return trends
    
    def _generate_campaign_recommendations(self, campaign_id):
        """Generate campaign optimization recommendations"""
        performance = self.get_campaign_performance(campaign_id)
        recommendations = []
        
        # Budget recommendations
        if performance.get('cost_per_lead', 0) > 50000:
            recommendations.append({
                'type': 'budget',
                'priority': 'high',
                'recommendation': 'Consider reducing budget or optimizing targeting',
                'reason': f'High CPA: {performance.get("cost_per_lead", 0):,.0f}'
            })
        
        # Creative recommendations
        if performance.get('click_through_rate', 0) < 1.0:
            recommendations.append({
                'type': 'creative',
                'priority': 'medium',
                'recommendation': 'Test new ad creatives to improve CTR',
                'reason': f'Low CTR: {performance.get("click_through_rate", 0):.2f}%'
            })
        
        # Audience recommendations
        if performance.get('conversion_rate', 0) < 1.0:
            recommendations.append({
                'type': 'audience',
                'priority': 'medium',
                'recommendation': 'Refine target audience for better conversion',
                'reason': f'Low conversion rate: {performance.get("conversion_rate", 0):.2f}%'
            })
        
        return recommendations
    
    def _analyze_campaign_roi(self, campaign_id):
        """Analyze campaign return on investment"""
        performance = self.get_campaign_performance(campaign_id)
        
        roi_analysis = {
            'total_cost': performance.get('cost', 0),
            'total_conversions': performance.get('conversions', 0),
            'cost_per_conversion': performance.get('cost_per_lead', 0),
            'average_lead_value': 500000,  # Average lead value in IDR
            'total_revenue': performance.get('conversions', 0) * 500000,
            'roi': (performance.get('conversions', 0) * 500000 - performance.get('cost', 0)) / performance.get('cost', 0) * 100,
            'break_even_point': performance.get('cost', 0) / 500000,
            'profit_margin': ((performance.get('conversions', 0) * 500000 - performance.get('cost', 0)) / (performance.get('conversions', 0) * 500000)) * 100 if performance.get('conversions', 0) > 0 else 0
        }
        
        return roi_analysis
    
    def export_campaign_data(self, campaign_id, format='json'):
        """Export campaign data in specified format"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        data = {
            'campaign': campaign,
            'performance': self.get_campaign_performance(campaign_id),
            'ads': {ad_id: self.get_ad_performance(ad_id) for ad_id in self.ads if self.ads[ad_id].get('campaign_id') == campaign_id}
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
            writer.writerow(['campaign_id', 'campaign_name', 'impressions', 'clicks', 'conversions', 'cost', 'ctr', 'conversion_rate', 'cpa', 'roas'])
            
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
                performance['cost_per_lead'],
                performance['return_on_ad_spend']
            ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def create_lookalike_audience(self, source_audience, audience_size):
        """Create lookalike audience from source audience"""
        lookalike = {
            'audience_id': f"FB_LOOKALIKE_{len(self.campaigns) + 1:03d}",
            'source_audience': source_audience,
            'audience_size': audience_size,  # 1%, 2%, 5%, 10%
            'country': 'ID',
            'creation_date': datetime.now().isoformat(),
            'status': 'active',
            'estimated_size': self._estimate_lookalike_size(audience_size)
        }
        
        return lookalike
    
    def _estimate_lookalike_size(self, percentage):
        """Estimate lookalike audience size"""
        base_size = 1000000  # Base Facebook user count in Indonesia
        return int(base_size * (percentage / 100))
    
    def create_custom_audience(self, audience_config):
        """Create custom audience from various sources"""
        custom_audience = {
            'audience_id': f"FB_CUSTOM_{len(self.campaigns) + 1:03d}",
            'name': audience_config.get('name', 'Custom Audience'),
            'source_type': audience_config.get('source_type', 'customer_list'),
            'source_data': audience_config.get('source_data', {}),
            'retention_days': audience_config.get('retention_days', 180),
            'creation_date': datetime.now().isoformat(),
            'status': 'active',
            'estimated_size': random.randint(1000, 100000)
        }
        
        return custom_audience
    
    def get_audience_insights(self, audience_id):
        """Get insights for custom or lookalike audience"""
        insights = {
            'audience_id': audience_id,
            'size': random.randint(1000, 100000),
            'age_distribution': self._generate_age_distribution(),
            'gender_distribution': self._generate_gender_distribution(),
            'location_distribution': self._generate_location_distribution(),
            'interest_distribution': self._generate_interest_distribution(),
            'device_distribution': self._generate_device_distribution(),
            'generated_at': datetime.now().isoformat()
        }
        
        return insights
    
    def _generate_age_distribution(self):
        """Generate age distribution data"""
        return {
            '18-24': random.randint(5, 15),
            '25-34': random.randint(25, 35),
            '35-44': random.randint(20, 30),
            '45-54': random.randint(15, 25),
            '55-64': random.randint(5, 15),
            '65+': random.randint(2, 10)
        }
    
    def _generate_gender_distribution(self):
        """Generate gender distribution data"""
        return {
            'men': random.randint(45, 55),
            'women': random.randint(45, 55)
        }
    
    def _generate_location_distribution(self):
        """Generate location distribution data"""
        locations = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Palembang', 'Makassar', 'South Tangerang', 'Depok', 'Batam']
        distribution = {}
        
        for location in locations:
            distribution[location] = random.randint(1, 20)
        
        return distribution
    
    def _generate_interest_distribution(self):
        """Generate interest distribution data"""
        interests = ['real estate', 'property investment', 'home buying', 'mortgage', 'housing market', 'interior design', 'architecture', 'home improvement']
        distribution = {}
        
        for interest in interests:
            distribution[interest] = random.randint(5, 25)
        
        return distribution
    
    def _generate_device_distribution(self):
        """Generate device distribution data"""
        return {
            'mobile': random.randint(60, 80),
            'desktop': random.randint(15, 25),
            'tablet': random.randint(5, 15)
        }
