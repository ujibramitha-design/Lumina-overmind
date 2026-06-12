"""
Google Ads Manager - Growth Engine
Manages Google advertising campaigns and optimization
"""

import json
import random
from datetime import datetime, timedelta

class GoogleAdsManager:
    """Manager for Google advertising campaigns"""
    
    def __init__(self):
        self.name = "Google Ads Manager"
        self.version = "1.0.0"
        self.campaigns = {}
        self.ad_groups = {}
        self.ads = {}
        self.keywords = {}
        self.performance_metrics = {}
    
    def create_campaign(self, campaign_config):
        """Create Google Ads campaign"""
        campaign = {
            'campaign_id': f"GA_CAMPAIGN_{len(self.campaigns) + 1:03d}",
            'name': campaign_config.get('name', 'Google Ads Campaign'),
            'advertising_channel_type': campaign_config.get('advertising_channel_type', 'SEARCH'),
            'campaign_goal': campaign_config.get('campaign_goal', 'LEAD_GENERATION'),
            'budget': campaign_config.get('budget', 1000000),  # In IDR
            'budget_type': campaign_config.get('budget_type', 'DAILY'),
            'start_date': campaign_config.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            'end_date': campaign_config.get('end_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'targeting': campaign_config.get('targeting', {}),
            'status': 'ENABLED',
            'created_at': datetime.now().isoformat(),
            'optimization_score': random.uniform(60, 95)
        }
        
        self.campaigns[campaign['campaign_id']] = campaign
        return campaign
    
    def create_ad_group(self, campaign_id, ad_group_config):
        """Create ad group within campaign"""
        ad_group = {
            'ad_group_id': f"GA_ADGROUP_{len(self.ad_groups) + 1:03d}",
            'campaign_id': campaign_id,
            'name': ad_group_config.get('name', 'Ad Group'),
            'cpc_bid': ad_group_config.get('cpc_bid', 5000),  # In IDR
            'targeting': self._build_ad_group_targeting(ad_group_config.get('targeting', {})),
            'status': 'ENABLED',
            'created_at': datetime.now().isoformat()
        }
        
        self.ad_groups[ad_group['ad_group_id']] = ad_group
        return ad_group
    
    def create_search_ad(self, ad_group_id, ad_config):
        """Create search ad within ad group"""
        ad = {
            'ad_id': f"GA_AD_{len(self.ads) + 1:03d}",
            'ad_group_id': ad_group_id,
            'ad_type': 'SEARCH_EXPANDED_TEXT_AD',
            'final_urls': ad_config.get('final_urls', ['https://example.com']),
            'headlines': ad_config.get('headlines', [
                'Amazing Property Deals',
                'Limited Time Offers',
                'Professional Real Estate'
            ]),
            'descriptions': ad_config.get('descriptions', [
                'Find your dream property with us',
                'Professional real estate services',
                'Best property deals available'
            ]),
            'path1': ad_config.get('path1', 'property'),
            'path2': ad_config.get('path2', 'deals'),
            'status': 'ENABLED',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[ad['ad_id']] = ad
        return ad
    
    def create_display_ad(self, ad_group_id, ad_config):
        """Create display ad within ad group"""
        ad = {
            'ad_id': f"GA_DISPLAY_AD_{len(self.ads) + 1:03d}",
            'ad_group_id': ad_group_id,
            'ad_type': 'RESPONSIVE_DISPLAY_AD',
            'final_urls': ad_config.get('final_urls', ['https://example.com']),
            'headlines': ad_config.get('headlines', [
                'Premium Properties',
                'Expert Real Estate',
                'Investment Opportunities'
            ]),
            'descriptions': ad_config.get('descriptions', [
                'Discover premium properties',
                'Expert real estate services',
                'Smart investment options'
            ]),
            'business_name': ad_config.get('business_name', 'Property Experts'),
            'images': ad_config.get('images', []),
            'status': 'ENABLED',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[ad['ad_id']] = ad
        return ad
    
    def _build_ad_group_targeting(self, targeting_config):
        """Build ad group targeting"""
        targeting = {
            'locations': targeting_config.get('locations', ['Indonesia']),
            'languages': targeting_config.get('languages', ['id']),
            'devices': targeting_config.get('devices', ['Mobile', 'Tablet', 'Desktop']),
            'audiences': targeting_config.get('audiences', []),
            'excluded_locations': targeting_config.get('excluded_locations', []),
            'excluded_audiences': targeting_config.get('excluded_audiences', [])
        }
        
        return targeting
    
    def add_keywords(self, ad_group_id, keywords_config):
        """Add keywords to ad group"""
        keywords = []
        
        for keyword_config in keywords_config:
            keyword = {
                'keyword_id': f"GA_KEYWORD_{len(self.keywords) + 1:03d}",
                'ad_group_id': ad_group_id,
                'text': keyword_config.get('text', ''),
                'match_type': keyword_config.get('match_type', 'BROAD'),
                'cpc_bid': keyword_config.get('cpc_bid', 5000),
                'status': 'ENABLED',
                'created_at': datetime.now().isoformat()
            }
            
            self.keywords[keyword['keyword_id']] = keyword
            keywords.append(keyword)
        
        return keywords
    
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
            budget_recommendations = self._optimize_google_budget(campaign, optimization_config)
            optimization['recommendations'].extend(budget_recommendations)
        
        # Keyword optimization
        elif optimization_config.get('type') == 'keywords':
            keyword_recommendations = self._optimize_keywords(campaign, optimization_config)
            optimization['recommendations'].extend(keyword_recommendations)
        
        # Ad optimization
        elif optimization_config.get('type') == 'ads':
            ad_recommendations = self._optimize_google_ads(campaign, optimization_config)
            optimization['recommendations'].extend(ad_recommendations)
        
        # Bidding optimization
        elif optimization_config.get('type') == 'bidding':
            bidding_recommendations = self._optimize_bidding(campaign, optimization_config)
            optimization['recommendations'].extend(bidding_recommendations)
        
        return optimization
    
    def _optimize_google_budget(self, campaign, config):
        """Optimize Google Ads budget"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_budget = campaign['budget']
        current_cpa = performance.get('cost_per_conversion', 0)
        current_roas = performance.get('return_on_ad_spend', 0)
        
        # Budget increase recommendation
        if current_cpa < config.get('target_cpa', 50000) and current_roas > config.get('target_roas', 3.0):
            recommended_increase = int(current_budget * 0.25)  # 25% increase
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
    
    def _optimize_keywords(self, campaign, config):
        """Optimize keywords"""
        recommendations = []
        
        # Get campaign keywords
        campaign_keywords = [kw for kw in self.keywords.values() if kw.get('ad_group_id') in self._get_campaign_ad_groups(campaign['campaign_id'])]
        
        for keyword in campaign_keywords:
            keyword_performance = self.get_keyword_performance(keyword['keyword_id'])
            
            # Low performing keywords
            if keyword_performance.get('conversion_rate', 0) < 0.5 and keyword_performance.get('impression_share', 0) < 20:
                recommendations.append({
                    'type': 'keyword_pause',
                    'keyword_id': keyword['keyword_id'],
                    'keyword_text': keyword['text'],
                    'reason': f"Low conversion rate ({keyword_performance.get('conversion_rate', 0):.2f}%) and low impression share"
                })
            
            # High performing keywords
            elif keyword_performance.get('conversion_rate', 0) > 2.0 and keyword_performance.get('impression_share', 0) > 80:
                recommendations.append({
                    'type': 'keyword_increase_bid',
                    'keyword_id': keyword['keyword_id'],
                    'keyword_text': keyword['text'],
                    'current_bid': keyword['cpc_bid'],
                    'recommended_bid': int(keyword['cpc_bid'] * 1.2),
                    'reason': f"High conversion rate ({keyword_performance.get('conversion_rate', 0):.2f}%) and high impression share"
                })
        
        return recommendations
    
    def _optimize_google_ads(self, campaign, config):
        """Optimize Google Ads"""
        recommendations = []
        
        # Get campaign ads
        campaign_ads = [ad for ad in self.ads.values() if ad.get('ad_group_id') in self._get_campaign_ad_groups(campaign['campaign_id'])]
        
        for ad in campaign_ads:
            ad_performance = self.get_ad_performance(ad['ad_id'])
            
            # Low CTR ads
            if ad_performance.get('click_through_rate', 0) < 1.0:
                recommendations.append({
                    'type': 'ad_optimization',
                    'ad_id': ad['ad_id'],
                    'current_ctr': ad_performance.get('click_through_rate', 0),
                    'recommendation': 'Test new headlines and descriptions to improve CTR',
                    'reason': f"Low CTR ({ad_performance.get('click_through_rate', 0):.2f}%)"
                })
            
            # High CPA ads
            elif ad_performance.get('cost_per_conversion', 0) > 50000:
                recommendations.append({
                    'type': 'ad_optimization',
                    'ad_id': ad['ad_id'],
                    'current_cpa': ad_performance.get('cost_per_conversion', 0),
                    'recommendation': 'Refine ad copy to improve conversion rate',
                    'reason': f"High CPA ({ad_performance.get('cost_per_conversion', 0):,.0f})"
                })
        
        return recommendations
    
    def _optimize_bidding(self, campaign, config):
        """Optimize bidding strategy"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Manual CPC recommendation
        if performance.get('conversion_rate', 0) > 2.0 and performance.get('impression_share', 0) < 50:
            recommendations.append({
                'type': 'bidding_strategy',
                'current_strategy': 'MANUAL_CPC',
                'recommended_strategy': 'TARGET_CPA',
                'target_cpa': config.get('target_cpa', 30000),
                'reason': 'High conversion rate suggests CPA bidding could work well'
            })
        
        # Target CPA recommendation
        elif performance.get('conversion_rate', 0) < 1.0 and performance.get('impression_share', 0) > 80:
            recommendations.append({
                'type': 'bidding_strategy',
                'current_strategy': 'TARGET_CPA',
                'recommended_strategy': 'MANUAL_CPC',
                'reason': 'Low conversion rate suggests manual CPC might work better'
            })
        
        return recommendations
    
    def _get_campaign_ad_groups(self, campaign_id):
        """Get ad groups for campaign"""
        return [ag['ad_group_id'] for ag in self.ad_groups.values() if ag.get('campaign_id') == campaign_id]
    
    def get_campaign_performance(self, campaign_id):
        """Get campaign performance metrics"""
        # Simulate performance data
        performance = {
            'campaign_id': campaign_id,
            'impressions': random.randint(50000, 200000),
            'clicks': random.randint(1000, 5000),
            'conversions': random.randint(20, 200),
            'cost': random.randint(2000000, 10000000),
            'click_through_rate': random.uniform(1.0, 3.0),
            'conversion_rate': random.uniform(1.0, 4.0),
            'cost_per_click': random.uniform(1000, 5000),
            'cost_per_conversion': random.uniform(20000, 100000),
            'return_on_ad_spend': random.uniform(2.0, 8.0),
            'impression_share': random.uniform(20, 80),
            'top_impression_share': random.uniform(30, 90),
            'absolute_top_impression_share': random.uniform(10, 50),
            'search_top_impression_share': random.uniform(25, 85),
            'search_absolute_top_impression_share': random.uniform(15, 55),
            'quality_score': random.uniform(5.0, 10.0)
        }
        
        return performance
    
    def get_ad_performance(self, ad_id):
        """Get ad performance metrics"""
        performance = {
            'ad_id': ad_id,
            'impressions': random.randint(25000, 100000),
            'clicks': random.randint(500, 2500),
            'conversions': random.randint(10, 100),
            'cost': random.randint(1000000, 5000000),
            'click_through_rate': random.uniform(1.0, 3.0),
            'conversion_rate': random.uniform(1.0, 4.0),
            'cost_per_click': random.uniform(1000, 5000),
            'cost_per_conversion': random.uniform(20000, 100000),
            'return_on_ad_spend': random.uniform(2.0, 8.0),
            'quality_score': random.uniform(5.0, 10.0)
        }
        
        return performance
    
    def get_keyword_performance(self, keyword_id):
        """Get keyword performance metrics"""
        performance = {
            'keyword_id': keyword_id,
            'impressions': random.randint(10000, 50000),
            'clicks': random.randint(200, 1000),
            'conversions': random.randint(5, 50),
            'cost': random.randint(500000, 2500000),
            'click_through_rate': random.uniform(1.0, 3.0),
            'conversion_rate': random.uniform(0.5, 2.0),
            'cost_per_click': random.uniform(1000, 5000),
            'cost_per_conversion': random.uniform(20000, 100000),
            'quality_score': random.uniform(5.0, 10.0),
            'impression_share': random.uniform(10, 90),
            'top_impression_rate': random.uniform(20, 80)
        }
        
        return performance
    
    def create_a_b_test(self, campaign_id, test_config):
        """Create A/B test for campaign"""
        test = {
            'test_id': f"GA_AB_TEST_{len(self.campaigns) + 1:03d}",
            'campaign_id': campaign_id,
            'name': test_config.get('name', 'A/B Test'),
            'test_type': test_config.get('test_type', 'ad_copy'),
            'variants': test_config.get('variants', []),
            'traffic_split': test_config.get('traffic_split', [50, 50]),
            'duration_days': test_config.get('duration_days', 14),
            'status': 'ENABLED',
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
                    'impressions': random.randint(25000, 100000),
                    'clicks': random.randint(500, 2500),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(1.0, 4.0),
                    'cost_per_conversion': random.uniform(20000, 100000)
                },
                'variant_b': {
                    'impressions': random.randint(25000, 100000),
                    'clicks': random.randint(500, 2500),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(1.0, 4.0),
                    'cost_per_conversion': random.uniform(20000, 100000)
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
            results['confidence_level'] = min(95, (variant_a_rate - variant_b_rate) * 30)
            results['recommendation'] = 'Implement variant A as the winning ad'
        elif variant_b_rate > variant_a_rate:
            results['winner'] = 'variant_b'
            results['confidence_level'] = min(95, (variant_b_rate - variant_a_rate) * 30)
            results['recommendation'] = 'Implement variant B as the winning ad'
        else:
            results['winner'] = 'inconclusive'
            results['confidence_level'] = 0
            results['recommendation'] = 'Test results are inconclusive, consider running a different test'
        
        return results
    
    def generate_campaign_report(self, campaign_id, date_range='14d'):
        """Generate comprehensive campaign report"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        performance = self.get_campaign_performance(campaign_id)
        
        report = {
            'campaign_info': campaign,
            'performance_metrics': performance,
            'ad_performance': self._get_campaign_ads_performance(campaign_id),
            'keyword_performance': self._get_campaign_keywords_performance(campaign_id),
            'trend_analysis': self._analyze_campaign_trends(campaign_id, date_range),
            'optimization_recommendations': self._generate_campaign_recommendations(campaign_id),
            'roi_analysis': self._analyze_campaign_roi(campaign_id),
            'quality_score_analysis': self._analyze_quality_scores(campaign_id),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _get_campaign_ads_performance(self, campaign_id):
        """Get performance of all ads in campaign"""
        campaign_ad_groups = self._get_campaign_ad_groups(campaign_id)
        campaign_ads = [ad for ad in self.ads.values() if ad.get('ad_group_id') in campaign_ad_groups]
        ad_performance = {}
        
        for ad in campaign_ads:
            ad_performance[ad['ad_id']] = self.get_ad_performance(ad['ad_id'])
        
        return ad_performance
    
    def _get_campaign_keywords_performance(self, campaign_id):
        """Get performance of all keywords in campaign"""
        campaign_ad_groups = self._get_campaign_ad_groups(campaign_id)
        campaign_keywords = [kw for kw in self.keywords.values() if kw.get('ad_group_id') in campaign_ad_groups]
        keyword_performance = {}
        
        for keyword in campaign_keywords:
            keyword_performance[keyword['keyword_id']] = self.get_keyword_performance(keyword['keyword_id'])
        
        return keyword_performance
    
    def _analyze_campaign_trends(self, campaign_id, date_range):
        """Analyze campaign trends over time"""
        # Simulate trend data
        days = int(date_range.replace('d', ''))
        trends = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
            trends.append({
                'date': date,
                'impressions': random.randint(2000, 10000),
                'clicks': random.randint(100, 500),
                'conversions': random.randint(2, 20),
                'cost': random.randint(100000, 500000),
                'quality_score': random.uniform(5.0, 10.0)
            })
        
        return trends
    
    def _generate_campaign_recommendations(self, campaign_id):
        """Generate campaign optimization recommendations"""
        performance = self.get_campaign_performance(campaign_id)
        recommendations = []
        
        # Budget recommendations
        if performance.get('cost_per_conversion', 0) > 50000:
            recommendations.append({
                'type': 'budget',
                'priority': 'high',
                'recommendation': 'Consider reducing budget or optimizing keywords',
                'reason': f'High CPA: {performance.get("cost_per_conversion", 0):,.0f}'
            })
        
        # CTR recommendations
        if performance.get('click_through_rate', 0) < 1.5:
            recommendations.append({
                'type': 'ad_copy',
                'priority': 'medium',
                'recommendation': 'Test new ad headlines and descriptions to improve CTR',
                'reason': f'Low CTR: {performance.get("click_through_rate", 0):.2f}%'
            })
        
        # Quality score recommendations
        if performance.get('quality_score', 0) < 7.0:
            recommendations.append({
                'type': 'quality_score',
                'priority': 'medium',
                'recommendation': 'Improve ad relevance and landing page experience',
                'reason': f'Low quality score: {performance.get("quality_score", 0):.1f}'
            })
        
        # Impression share recommendations
        if performance.get('impression_share', 0) < 30:
            recommendations.append({
                'type': 'budget',
                'priority': 'low',
                'recommendation': 'Consider increasing budget to improve impression share',
                'reason': f'Low impression share: {performance.get("impression_share", 0):.1f}%'
            })
        
        return recommendations
    
    def _analyze_campaign_roi(self, campaign_id):
        """Analyze campaign return on investment"""
        performance = self.get_campaign_performance(campaign_id)
        
        roi_analysis = {
            'total_cost': performance.get('cost', 0),
            'total_conversions': performance.get('conversions', 0),
            'cost_per_conversion': performance.get('cost_per_conversion', 0),
            'average_lead_value': 500000,  # Average lead value in IDR
            'total_revenue': performance.get('conversions', 0) * 500000,
            'roi': (performance.get('conversions', 0) * 500000 - performance.get('cost', 0)) / performance.get('cost', 0) * 100,
            'break_even_point': performance.get('cost', 0) / 500000,
            'profit_margin': ((performance.get('conversions', 0) * 500000 - performance.get('cost', 0)) / (performance.get('conversions', 0) * 500000)) * 100 if performance.get('conversions', 0) > 0 else 0
        }
        
        return roi_analysis
    
    def _analyze_quality_scores(self, campaign_id):
        """Analyze quality scores across campaign"""
        campaign_ad_groups = self._get_campaign_ad_groups(campaign_id)
        campaign_keywords = [kw for kw in self.keywords.values() if kw.get('ad_group_id') in campaign_ad_groups]
        
        quality_scores = []
        for keyword in campaign_keywords:
            performance = self.get_keyword_performance(keyword['keyword_id'])
            quality_scores.append(performance.get('quality_score', 0))
        
        if quality_scores:
            analysis = {
                'average_quality_score': sum(quality_scores) / len(quality_scores),
                'min_quality_score': min(quality_scores),
                'max_quality_score': max(quality_scores),
                'quality_score_distribution': self._generate_quality_score_distribution(quality_scores),
                'recommendations': self._generate_quality_score_recommendations(quality_scores)
            }
        else:
            analysis = {
                'average_quality_score': 0,
                'min_quality_score': 0,
                'max_quality_score': 0,
                'quality_score_distribution': {},
                'recommendations': []
            }
        
        return analysis
    
    def _generate_quality_score_distribution(self, scores):
        """Generate quality score distribution"""
        distribution = {
            '1-3': 0,
            '4-6': 0,
            '7-10': 0
        }
        
        for score in scores:
            if score <= 3:
                distribution['1-3'] += 1
            elif score <= 6:
                distribution['4-6'] += 1
            else:
                distribution['7-10'] += 1
        
        return distribution
    
    def _generate_quality_score_recommendations(self, scores):
        """Generate quality score recommendations"""
        recommendations = []
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        if avg_score < 5.0:
            recommendations.append({
                'type': 'quality_improvement',
                'priority': 'high',
                'recommendation': 'Significant improvements needed in ad relevance and landing page experience',
                'reason': f'Average quality score: {avg_score:.1f}'
            })
        elif avg_score < 7.0:
            recommendations.append({
                'type': 'quality_improvement',
                'priority': 'medium',
                'recommendation': 'Focus on improving ad relevance and landing page experience',
                'reason': f'Average quality score: {avg_score:.1f}'
            })
        else:
            recommendations.append({
                'type': 'quality_maintenance',
                'priority': 'low',
                'recommendation': 'Maintain current quality score levels',
                'reason': f'Good average quality score: {avg_score:.1f}'
            })
        
        return recommendations
    
    def export_campaign_data(self, campaign_id, format='json'):
        """Export campaign data in specified format"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        data = {
            'campaign': campaign,
            'performance': self.get_campaign_performance(campaign_id),
            'ads': {ad_id: self.get_ad_performance(ad_id) for ad_id in self.ads if self.ads[ad_id].get('ad_group_id') in self._get_campaign_ad_groups(campaign_id)},
            'keywords': {kw_id: self.get_keyword_performance(kw_id) for kw_id in self.keywords if self.keywords[kw_id].get('ad_group_id') in self._get_campaign_ad_groups(campaign_id)}
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
            writer.writerow(['campaign_id', 'campaign_name', 'impressions', 'clicks', 'conversions', 'cost', 'ctr', 'conversion_rate', 'cpa', 'roas', 'quality_score'])
            
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
                performance['quality_score']
            ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def create_remarketing_campaign(self, campaign_config):
        """Create remarketing campaign"""
        campaign = {
            'campaign_id': f"GA_REMARKETING_{len(self.campaigns) + 1:03d}",
            'name': campaign_config.get('name', 'Remarketing Campaign'),
            'advertising_channel_type': 'DISPLAY',
            'campaign_goal': 'CONVERSION',
            'budget': campaign_config.get('budget', 500000),
            'budget_type': 'DAILY',
            'targeting': {
                'remarketing_lists': campaign_config.get('remarketing_lists', []),
                'exclusions': campaign_config.get('exclusions', [])
            },
            'status': 'ENABLED',
            'created_at': datetime.now().isoformat()
        }
        
        self.campaigns[campaign['campaign_id']] = campaign
        return campaign
    
    def get_search_query_report(self, campaign_id):
        """Get search query performance report"""
        # Simulate search query data
        search_queries = []
        
        for i in range(20):  # Generate 20 search queries
            query = {
                'query': f"property {random.choice(['serang', 'banten', 'jakarta', 'tangerang'])} {random.choice(['for sale', 'investment', 'rent', 'buy'])}",
                'impressions': random.randint(100, 5000),
                'clicks': random.randint(5, 200),
                'conversions': random.randint(0, 10),
                'cost': random.randint(10000, 500000),
                'match_type': random.choice(['BROAD', 'PHRASE', 'EXACT'])
            }
            search_queries.append(query)
        
        return {
            'campaign_id': campaign_id,
            'search_queries': search_queries,
            'total_queries': len(search_queries),
            'generated_at': datetime.now().isoformat()
        }
    
    def get_geographic_performance(self, campaign_id):
        """Get geographic performance report"""
        # Simulate geographic data
        locations = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Palembang', 'Makassar', 'South Tangerang', 'Depok', 'Batam']
        geographic_data = []
        
        for location in locations:
            data = {
                'location': location,
                'impressions': random.randint(1000, 10000),
                'clicks': random.randint(50, 500),
                'conversions': random.randint(1, 20),
                'cost': random.randint(100000, 1000000),
                'conversion_rate': random.uniform(0.5, 3.0)
            }
            geographic_data.append(data)
        
        return {
            'campaign_id': campaign_id,
            'geographic_data': geographic_data,
            'total_locations': len(geographic_data),
            'generated_at': datetime.now().isoformat()
        }
    
    def get_device_performance(self, campaign_id):
        """Get device performance report"""
        devices = ['Mobile', 'Desktop', 'Tablet']
        device_data = []
        
        for device in devices:
            data = {
                'device': device,
                'impressions': random.randint(5000, 25000),
                'clicks': random.randint(250, 1250),
                'conversions': random.randint(5, 50),
                'cost': random.randint(500000, 2500000),
                'conversion_rate': random.uniform(0.5, 3.0),
                'click_through_rate': random.uniform(1.0, 3.0)
            }
            device_data.append(data)
        
        return {
            'campaign_id': campaign_id,
            'device_data': device_data,
            'total_devices': len(device_data),
            'generated_at': datetime.now().isoformat()
        }
