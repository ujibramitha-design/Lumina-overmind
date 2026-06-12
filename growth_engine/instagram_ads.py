"""
Instagram Ads Manager - Growth Engine
Manages Instagram advertising campaigns and optimization
"""

import json
import random
from datetime import datetime, timedelta

class InstagramAdsManager:
    """Manager for Instagram advertising campaigns"""
    
    def __init__(self):
        self.name = "Instagram Ads Manager"
        self.version = "1.0.0"
        self.campaigns = {}
        self.ad_sets = {}
        self.ads = {}
        self.performance_metrics = {}
    
    def create_campaign(self, campaign_config):
        """Create Instagram advertising campaign"""
        campaign = {
            'campaign_id': f"IG_CAMPAIGN_{len(self.campaigns) + 1:03d}",
            'name': campaign_config.get('name', 'Instagram Campaign'),
            'objective': campaign_config.get('objective', 'LEAD_GENERATION'),
            'budget': campaign_config.get('budget', 800000),  # In IDR
            'budget_type': campaign_config.get('budget_type', 'daily'),
            'status': 'active',
            'start_date': campaign_config.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            'end_date': campaign_config.get('end_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'target_audience': campaign_config.get('target_audience', {}),
            'placements': campaign_config.get('placements', ['instagram_feed', 'instagram_stories']),
            'created_at': datetime.now().isoformat(),
            'optimization_goal': campaign_config.get('optimization_goal', 'leads')
        }
        
        self.campaigns[campaign['campaign_id']] = campaign
        return campaign
    
    def create_ad_set(self, campaign_id, ad_set_config):
        """Create ad set within campaign"""
        ad_set = {
            'ad_set_id': f"IG_ADSET_{len(self.ad_sets) + 1:03d}",
            'campaign_id': campaign_id,
            'name': ad_set_config.get('name', 'Instagram Ad Set'),
            'budget': ad_set_config.get('budget', 400000),  # In IDR
            'budget_type': ad_set_config.get('budget_type', 'daily'),
            'target_audience': self._build_instagram_target_audience(ad_set_config.get('target_audience', {})),
            'placements': ad_set_config.get('placements', ['instagram_feed', 'instagram_stories']),
            'optimization_goal': ad_set_config.get('optimization_goal', 'leads'),
            'bid_strategy': ad_set_config.get('bid_strategy', 'lowest_cost'),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ad_sets[ad_set['ad_set_id']] = ad_set
        return ad_set
    
    def create_ad(self, ad_set_id, ad_config):
        """Create Instagram ad within ad set"""
        ad = {
            'ad_id': f"IG_AD_{len(self.ads) + 1:03d}",
            'ad_set_id': ad_set_id,
            'name': ad_config.get('name', 'Instagram Ad'),
            'creative': {
                'title': ad_config.get('title', 'Amazing Property Deal!'),
                'description': ad_config.get('description', 'Check out our latest property offerings'),
                'image_url': ad_config.get('image_url', ''),
                'video_url': ad_config.get('video_url', ''),
                'call_to_action': ad_config.get('call_to_action', 'LEARN_MORE'),
                'landing_page_url': ad_config.get('landing_page_url', ''),
                'display_link': ad_config.get('display_link', ''),
                'carousel_items': ad_config.get('carousel_items', []),
                'story_format': ad_config.get('story_format', 'standard')
            },
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[ad['ad_id']] = ad
        return ad
    
    def _build_instagram_target_audience(self, audience_config):
        """Build Instagram-specific target audience"""
        audience = {
            'age_min': audience_config.get('age_min', 18),
            'age_max': audience_config.get('age_max', 45),
            'genders': audience_config.get('genders', ['men', 'women']),
            'locations': audience_config.get('locations', ['Serang', 'Banten', 'Jakarta']),
            'radius': audience_config.get('radius', 50),  # In kilometers
            'interests': audience_config.get('interests', ['real estate', 'property investment', 'home buying', 'interior design']),
            'behaviors': audience_config.get('behaviors', ['engaged_shoppers', 'frequent_travelers', 'mobile_device_users']),
            'education': audience_config.get('education', ['college', 'graduate_school']),
            'income_level': audience_config.get('income_level', 'medium'),
            'relationship_status': audience_config.get('relationship_status', ['single', 'in_relationship', 'married']),
            'custom_audiences': audience_config.get('custom_audiences', []),
            'excluded_audiences': audience_config.get('excluded_audiences', []),
            'instagram_specific': {
                'followers_of': audience_config.get('followers_of', []),
                'interests_in': audience_config.get('interests_in', ['luxury lifestyle', 'home decor', 'architecture']),
                'device_platform': audience_config.get('device_platform', ['mobile', 'desktop'])
            }
        }
        
        return audience
    
    def optimize_campaign(self, campaign_id, optimization_config):
        """Optimize Instagram campaign performance"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        optimization = {
            'campaign_id': campaign_id,
            'optimization_type': optimization_config.get('type', 'creative'),
            'current_performance': self.get_campaign_performance(campaign_id),
            'recommendations': [],
            'applied_changes': []
        }
        
        # Creative optimization
        if optimization_config.get('type') == 'creative':
            creative_recommendations = self._optimize_instagram_creative(campaign, optimization_config)
            optimization['recommendations'].extend(creative_recommendations)
        
        # Audience optimization
        elif optimization_config.get('type') == 'audience':
            audience_recommendations = self._optimize_instagram_audience(campaign, optimization_config)
            optimization['recommendations'].extend(audience_recommendations)
        
        # Placement optimization
        elif optimization_config.get('type') == 'placement':
            placement_recommendations = self._optimize_instagram_placements(campaign, optimization_config)
            optimization['recommendations'].extend(placement_recommendations)
        
        # Budget optimization
        elif optimization_config.get('type') == 'budget':
            budget_recommendations = self._optimize_instagram_budget(campaign, optimization_config)
            optimization['recommendations'].extend(budget_recommendations)
        
        return optimization
    
    def _optimize_instagram_creative(self, campaign, config):
        """Optimize Instagram creative content"""
        recommendations = []
        
        # Get campaign ads
        campaign_ads = [ad for ad in self.ads.values() if ad.get('campaign_id') == campaign['campaign_id']]
        
        for ad in campaign_ads:
            ad_performance = self.get_ad_performance(ad['ad_id'])
            
            # Image optimization
            if not ad['creative'].get('image_url') and not ad['creative'].get('video_url'):
                recommendations.append({
                    'type': 'creative_media',
                    'ad_id': ad['ad_id'],
                    'recommendation': 'Add high-quality images or videos for better engagement',
                    'reason': 'Visual content is crucial for Instagram performance'
                })
            
            # Title optimization
            title = ad['creative'].get('title', '')
            if len(title) < 10 or len(title) > 30:
                recommendations.append({
                    'type': 'title_optimization',
                    'ad_id': ad['ad_id'],
                    'current_title': title,
                    'recommended_title': f"🏠 {title[:25]} - Limited Time!",
                    'reason': 'Optimal title length for Instagram is 10-30 characters'
                })
            
            # Call-to-action optimization
            cta = ad['creative'].get('call_to_action', '')
            if cta == 'LEARN_MORE':
                recommendations.append({
                    'type': 'cta_optimization',
                    'ad_id': ad['ad_id'],
                    'current_cta': cta,
                    'recommended_cta': 'SIGN_UP',
                    'reason': 'SIGN_UP may generate more qualified leads for property business'
                })
            
            # Story format optimization
            if ad['creative'].get('story_format') == 'standard' and ad_performance.get('click_through_rate', 0) < 1.5:
                recommendations.append({
                    'type': 'story_format',
                    'ad_id': ad['ad_id'],
                    'current_format': 'standard',
                    'recommended_format': 'interactive',
                    'reason': 'Interactive stories can improve engagement rates'
                })
        
        return recommendations
    
    def _optimize_instagram_audience(self, campaign, config):
        """Optimize Instagram target audience"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Age optimization
        current_age_range = [campaign['target_audience'].get('age_min', 18), 
                           campaign['target_audience'].get('age_max', 45)]
        
        if performance.get('click_through_rate', 0) < 1.0:
            # Suggest adjusting age range for Instagram
            recommendations.append({
                'type': 'age_adjustment',
                'current_range': current_age_range,
                'recommended_range': [20, 35],
                'reason': 'Instagram users tend to be younger; adjust age range for better engagement'
            })
        
        # Interest optimization
        current_interests = campaign['target_audience'].get('interests', [])
        instagram_specific = campaign['target_audience'].get('instagram_specific', {}).get('interests_in', [])
        
        if len(instagram_specific) < 3:
            new_interests = ['luxury lifestyle', 'home decor', 'architecture', 'interior design', 'minimalist living']
            recommendations.append({
                'type': 'interest_expansion',
                'current_interests': current_interests + instagram_specific,
                'recommended_interests': new_interests,
                'reason': 'Add Instagram-specific interests for better targeting'
            })
        
        # Followers optimization
        followers_of = campaign['target_audience'].get('instagram_specific', {}).get('followers_of', [])
        if not followers_of:
            recommendations.append({
                'type': 'followers_targeting',
                'current_followers': followers_of,
                'recommended_followers': ['@propertyexperts', '@realestateindonesia', '@homedecorideas'],
                'reason': 'Target followers of relevant accounts for better reach'
            })
        
        return recommendations
    
    def _optimize_instagram_placements(self, campaign, config):
        """Optimize Instagram ad placements"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        # Placement performance analysis
        placement_performance = performance.get('placement_performance', {})
        
        if placement_performance:
            # Find best performing placement
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
            
            # Instagram Stories optimization
            if 'instagram_stories' in placement_performance:
                stories_perf = placement_performance['instagram_stories']
                if stories_perf.get('conversion_rate', 0) > 2.0:
                    recommendations.append({
                        'type': 'stories_optimization',
                        'placement': 'instagram_stories',
                        'performance': stories_perf,
                        'recommendation': 'Create more story-specific content',
                        'reason': 'Stories performing well with high conversion rate'
                    })
        
        return recommendations
    
    def _optimize_instagram_budget(self, campaign, config):
        """Optimize Instagram campaign budget"""
        recommendations = []
        performance = self.get_campaign_performance(campaign['campaign_id'])
        
        current_budget = campaign['budget']
        current_cpa = performance.get('cost_per_lead', 0)
        current_roas = performance.get('return_on_ad_spend', 0)
        
        # Budget increase for high-performing campaigns
        if current_cpa < config.get('target_cpa', 40000) and current_roas > config.get('target_roas', 3.0):
            recommended_increase = int(current_budget * 0.3)  # 30% increase
            recommendations.append({
                'type': 'budget_increase',
                'current_budget': current_budget,
                'recommended_budget': current_budget + recommended_increase,
                'reason': 'Low CPA and high ROAS indicate room for budget increase on Instagram'
            })
        
        # Budget reallocation for Instagram Stories
        placement_performance = performance.get('placement_performance', {})
        if 'instagram_stories' in placement_performance:
            stories_perf = placement_performance['instagram_stories']
            if stories_perf.get('conversion_rate', 0) > performance.get('conversion_rate', 0):
                recommendations.append({
                    'type': 'budget_reallocation',
                    'placement': 'instagram_stories',
                    'recommendation': 'Allocate more budget to Instagram Stories',
                    'reason': 'Stories outperforming feed ads'
                })
        
        return recommendations
    
    def get_campaign_performance(self, campaign_id):
        """Get campaign performance metrics"""
        # Simulate performance data
        performance = {
            'campaign_id': campaign_id,
            'impressions': random.randint(20000, 100000),
            'clicks': random.randint(1000, 5000),
            'conversions': random.randint(20, 200),
            'cost': random.randint(1500000, 8000000),
            'click_through_rate': random.uniform(2.0, 5.0),
            'conversion_rate': random.uniform(1.0, 3.0),
            'cost_per_click': random.uniform(500, 2000),
            'cost_per_lead': random.uniform(20000, 80000),
            'return_on_ad_spend': random.uniform(2.0, 8.0),
            'placement_performance': self._generate_instagram_placement_performance(),
            'age_performance': self._generate_instagram_age_performance(),
            'gender_performance': self._generate_instagram_gender_performance(),
            'engagement_rate': random.uniform(3.0, 8.0),
            'reach': random.randint(15000, 75000),
            'frequency': random.uniform(1.5, 3.0)
        }
        
        return performance
    
    def get_ad_performance(self, ad_id):
        """Get ad performance metrics"""
        performance = {
            'ad_id': ad_id,
            'impressions': random.randint(10000, 50000),
            'clicks': random.randint(500, 2500),
            'conversions': random.randint(10, 100),
            'cost': random.randint(750000, 4000000),
            'click_through_rate': random.uniform(2.0, 5.0),
            'conversion_rate': random.uniform(1.0, 3.0),
            'cost_per_click': random.uniform(500, 2000),
            'cost_per_lead': random.uniform(20000, 80000),
            'return_on_ad_spend': random.uniform(2.0, 8.0),
            'engagement_rate': random.uniform(3.0, 8.0),
            'reach': random.randint(7500, 37500),
            'frequency': random.uniform(1.5, 3.0)
        }
        
        return performance
    
    def _generate_instagram_placement_performance(self):
        """Generate Instagram placement performance data"""
        placements = ['instagram_feed', 'instagram_stories', 'instagram_explore', 'instagram_reels']
        performance = {}
        
        for placement in placements:
            performance[placement] = {
                'impressions': random.randint(5000, 25000),
                'clicks': random.randint(250, 1250),
                'conversions': random.randint(5, 50),
                'conversion_rate': random.uniform(1.0, 3.0),
                'engagement_rate': random.uniform(3.0, 8.0)
            }
        
        return performance
    
    def _generate_instagram_age_performance(self):
        """Generate Instagram age performance data"""
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64']
        performance = {}
        
        for age_group in age_groups:
            performance[age_group] = {
                'impressions': random.randint(2000, 10000),
                'clicks': random.randint(100, 500),
                'conversions': random.randint(2, 20),
                'conversion_rate': random.uniform(1.0, 3.0),
                'engagement_rate': random.uniform(3.0, 8.0)
            }
        
        return performance
    
    def _generate_instagram_gender_performance(self):
        """Generate Instagram gender performance data"""
        genders = ['men', 'women']
        performance = {}
        
        for gender in genders:
            performance[gender] = {
                'impressions': random.randint(10000, 50000),
                'clicks': random.randint(500, 2500),
                'conversions': random.randint(10, 100),
                'conversion_rate': random.uniform(1.0, 3.0),
                'engagement_rate': random.uniform(3.0, 8.0)
            }
        
        return performance
    
    def create_story_ad(self, ad_set_id, story_config):
        """Create Instagram Story ad"""
        story_ad = {
            'ad_id': f"IG_STORY_{len(self.ads) + 1:03d}",
            'ad_set_id': ad_set_id,
            'name': story_config.get('name', 'Instagram Story Ad'),
            'creative': {
                'title': story_config.get('title', 'Property Deal!'),
                'description': story_config.get('description', 'Limited time offer'),
                'image_url': story_config.get('image_url', ''),
                'video_url': story_config.get('video_url', ''),
                'call_to_action': story_config.get('call_to_action', 'SWIPE_UP'),
                'landing_page_url': story_config.get('landing_page_url', ''),
                'story_format': story_config.get('story_format', 'standard'),
                'duration': story_config.get('duration', 15),  # In seconds
                'interactive_elements': story_config.get('interactive_elements', [])
            },
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[story_ad['ad_id']] = story_ad
        return story_ad
    
    def create_reels_ad(self, ad_set_id, reels_config):
        """Create Instagram Reels ad"""
        reels_ad = {
            'ad_id': f"IG_REELS_{len(self.ads) + 1:03d}",
            'ad_set_id': ad_set_id,
            'name': reels_config.get('name', 'Instagram Reels Ad'),
            'creative': {
                'title': reels_config.get('title', 'Property Tour'),
                'description': reels_config.get('description', 'Virtual property tour'),
                'video_url': reels_config.get('video_url', ''),
                'thumbnail_url': reels_config.get('thumbnail_url', ''),
                'call_to_action': reels_config.get('call_to_action', 'WATCH_MORE'),
                'landing_page_url': reels_config.get('landing_page_url', ''),
                'video_duration': reels_config.get('video_duration', 30),  # In seconds
                'music_track': reels_config.get('music_track', ''),
                'hashtags': reels_config.get('hashtags', [])
            },
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[reels_ad['ad_id']] = reels_ad
        return reels_ad
    
    def create_carousel_ad(self, ad_set_id, carousel_config):
        """Create Instagram Carousel ad"""
        carousel_ad = {
            'ad_id': f"IG_CAROUSEL_{len(self.ads) + 1:03d}",
            'ad_set_id': ad_set_id,
            'name': carousel_config.get('name', 'Instagram Carousel Ad'),
            'creative': {
                'title': carousel_config.get('title', 'Property Gallery'),
                'description': carousel_config.get('description', 'Explore our properties'),
                'carousel_items': carousel_config.get('carousel_items', []),
                'call_to_action': carousel_config.get('call_to_action', 'SWIPE_LEFT'),
                'landing_page_url': carousel_config.get('landing_page_url', ''),
                'autoplay': carousel_config.get('autoplay', True),
                'link_headline': carousel_config.get('link_headline', 'View Properties')
            },
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        self.ads[carousel_ad['ad_id']] = carousel_ad
        return carousel_ad
    
    def create_a_b_test(self, campaign_id, test_config):
        """Create A/B test for Instagram campaign"""
        test = {
            'test_id': f"IG_AB_TEST_{len(self.campaigns) + 1:03d}",
            'campaign_id': campaign_id,
            'name': test_config.get('name', 'Instagram A/B Test'),
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
        """Analyze Instagram A/B test results"""
        # Simulate test results
        results = {
            'test_id': test_id,
            'variant_results': {
                'variant_a': {
                    'impressions': random.randint(10000, 50000),
                    'clicks': random.randint(500, 2500),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(1.0, 3.0),
                    'cost_per_conversion': random.uniform(20000, 80000),
                    'engagement_rate': random.uniform(3.0, 8.0)
                },
                'variant_b': {
                    'impressions': random.randint(10000, 50000),
                    'clicks': random.randint(500, 2500),
                    'conversions': random.randint(10, 100),
                    'conversion_rate': random.uniform(1.0, 3.0),
                    'cost_per_conversion': random.uniform(20000, 80000),
                    'engagement_rate': random.uniform(3.0, 8.0)
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
            results['confidence_level'] = min(95, (variant_a_rate - variant_b_rate) * 40)
            results['recommendation'] = 'Implement variant A as the winning creative'
        elif variant_b_rate > variant_a_rate:
            results['winner'] = 'variant_b'
            results['confidence_level'] = min(95, (variant_b_rate - variant_a_rate) * 40)
            results['recommendation'] = 'Implement variant B as the winning creative'
        else:
            results['winner'] = 'inconclusive'
            results['confidence_level'] = 0
            results['recommendation'] = 'Test results are inconclusive, consider running a different test'
        
        return results
    
    def generate_campaign_report(self, campaign_id, date_range='7d'):
        """Generate comprehensive Instagram campaign report"""
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
            'engagement_analysis': self._analyze_engagement_metrics(campaign_id),
            'content_performance': self._analyze_content_performance(campaign_id),
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
                'impressions': random.randint(2000, 10000),
                'clicks': random.randint(100, 500),
                'conversions': random.randint(2, 20),
                'cost': random.randint(100000, 500000),
                'engagement_rate': random.uniform(3.0, 8.0)
            })
        
        return trends
    
    def _generate_campaign_recommendations(self, campaign_id):
        """Generate campaign optimization recommendations"""
        performance = self.get_campaign_performance(campaign_id)
        recommendations = []
        
        # Budget recommendations
        if performance.get('cost_per_lead', 0) > 60000:
            recommendations.append({
                'type': 'budget',
                'priority': 'high',
                'recommendation': 'Consider reducing budget or optimizing creative',
                'reason': f'High CPA: {performance.get("cost_per_lead", 0):,.0f}'
            })
        
        # Engagement recommendations
        if performance.get('engagement_rate', 0) < 4.0:
            recommendations.append({
                'type': 'engagement',
                'priority': 'medium',
                'recommendation': 'Test more interactive content like polls and questions',
                'reason': f'Low engagement rate: {performance.get("engagement_rate", 0):.2f}%'
            })
        
        # Creative recommendations
        if performance.get('click_through_rate', 0) < 3.0:
            recommendations.append({
                'type': 'creative',
                'priority': 'medium',
                'recommendation': 'Test new visuals and ad copy to improve CTR',
                'reason': f'Low CTR: {performance.get("click_through_rate", 0):.2f}%'
            })
        
        # Placement recommendations
        placement_performance = performance.get('placement_performance', {})
        if 'instagram_stories' in placement_performance:
            stories_perf = placement_performance['instagram_stories']
            if stories_perf.get('conversion_rate', 0) > performance.get('conversion_rate', 0):
                recommendations.append({
                    'type': 'placement',
                    'priority': 'low',
                    'recommendation': 'Increase budget for Instagram Stories',
                    'reason': 'Stories performing better than feed ads'
                })
        
        return recommendations
    
    def _analyze_campaign_roi(self, campaign_id):
        """Analyze campaign return on investment"""
        performance = self.get_campaign_performance(campaign_id)
        
        roi_analysis = {
            'total_cost': performance.get('cost', 0),
            'total_conversions': performance.get('conversions', 0),
            'cost_per_conversion': performance.get('cost_per_lead', 0),
            'average_lead_value': 400000,  # Average lead value in IDR
            'total_revenue': performance.get('conversions', 0) * 400000,
            'roi': (performance.get('conversions', 0) * 400000 - performance.get('cost', 0)) / performance.get('cost', 0) * 100,
            'break_even_point': performance.get('cost', 0) / 400000,
            'profit_margin': ((performance.get('conversions', 0) * 400000 - performance.get('cost', 0)) / (performance.get('conversions', 0) * 400000)) * 100 if performance.get('conversions', 0) > 0 else 0
        }
        
        return roi_analysis
    
    def _analyze_engagement_metrics(self, campaign_id):
        """Analyze engagement metrics"""
        performance = self.get_campaign_performance(campaign_id)
        
        engagement_analysis = {
            'overall_engagement_rate': performance.get('engagement_rate', 0),
            'reach': performance.get('reach', 0),
            'frequency': performance.get('frequency', 0),
            'placement_engagement': performance.get('placement_performance', {}),
            'age_engagement': performance.get('age_performance', {}),
            'gender_engagement': performance.get('gender_performance', {}),
            'engagement_trends': self._generate_engagement_trends(),
            'recommendations': []
        }
        
        # Engagement recommendations
        if engagement_analysis['overall_engagement_rate'] < 4.0:
            engagement_analysis['recommendations'].append({
                'type': 'engagement_improvement',
                'recommendation': 'Add interactive elements like polls and questions',
                'reason': 'Low engagement rate indicates need for more interactive content'
            })
        
        return engagement_analysis
    
    def _analyze_content_performance(self, campaign_id):
        """Analyze content performance by type"""
        campaign_ads = [ad for ad in self.ads.values() if ad.get('campaign_id') == campaign_id]
        
        content_performance = {
            'image_ads': {'count': 0, 'avg_engagement': 0, 'avg_ctr': 0},
            'video_ads': {'count': 0, 'avg_engagement': 0, 'avg_ctr': 0},
            'carousel_ads': {'count': 0, 'avg_engagement': 0, 'avg_ctr': 0},
            'story_ads': {'count': 0, 'avg_engagement': 0, 'avg_ctr': 0},
            'reels_ads': {'count': 0, 'avg_engagement': 0, 'avg_ctr': 0}
        }
        
        for ad in campaign_ads:
            ad_performance = self.get_ad_performance(ad['ad_id'])
            creative = ad.get('creative', {})
            
            # Determine content type
            if creative.get('video_url'):
                content_type = 'video_ads'
            elif len(creative.get('carousel_items', [])) > 1:
                content_type = 'carousel_ads'
            elif creative.get('story_format') != 'standard':
                content_type = 'story_ads'
            elif 'reels' in ad.get('name', '').lower():
                content_type = 'reels_ads'
            else:
                content_type = 'image_ads'
            
            # Update performance metrics
            if content_type in content_performance:
                content_performance[content_type]['count'] += 1
                content_performance[content_type]['avg_engagement'] += ad_performance.get('engagement_rate', 0)
                content_performance[content_type]['avg_ctr'] += ad_performance.get('click_through_rate', 0)
        
        # Calculate averages
        for content_type in content_performance:
            if content_performance[content_type]['count'] > 0:
                count = content_performance[content_type]['count']
                content_performance[content_type]['avg_engagement'] /= count
                content_performance[content_type]['avg_ctr'] /= count
        
        return content_performance
    
    def _generate_engagement_trends(self):
        """Generate engagement trend data"""
        trends = []
        
        for i in range(7):  # Last 7 days
            date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
            trends.append({
                'date': date,
                'engagement_rate': random.uniform(3.0, 8.0),
                'reach': random.randint(10000, 50000),
                'impressions': random.randint(20000, 100000)
            })
        
        return trends
    
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
            writer.writerow(['campaign_id', 'campaign_name', 'impressions', 'clicks', 'conversions', 'cost', 'ctr', 'conversion_rate', 'cpa', 'roas', 'engagement_rate'])
            
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
                performance['return_on_ad_spend'],
                performance['engagement_rate']
            ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def create_lookalike_audience(self, source_audience, audience_size):
        """Create Instagram lookalike audience"""
        lookalike = {
            'audience_id': f"IG_LOOKALIKE_{len(self.campaigns) + 1:03d}",
            'source_audience': source_audience,
            'audience_size': audience_size,  # 1%, 2%, 5%, 10%
            'country': 'ID',
            'creation_date': datetime.now().isoformat(),
            'status': 'active',
            'estimated_size': self._estimate_instagram_lookalike_size(audience_size)
        }
        
        return lookalike
    
    def _estimate_instagram_lookalike_size(self, percentage):
        """Estimate Instagram lookalike audience size"""
        base_size = 800000  # Base Instagram user count in Indonesia
        return int(base_size * (percentage / 100))
    
    def get_audience_insights(self, audience_id):
        """Get insights for Instagram audience"""
        insights = {
            'audience_id': audience_id,
            'size': random.randint(50000, 500000),
            'age_distribution': self._generate_instagram_age_distribution(),
            'gender_distribution': self._generate_instagram_gender_distribution(),
            'location_distribution': self._generate_instagram_location_distribution(),
            'interest_distribution': self._generate_instagram_interest_distribution(),
            'device_distribution': self._generate_instagram_device_distribution(),
            'behavior_distribution': self._generate_instagram_behavior_distribution(),
            'generated_at': datetime.now().isoformat()
        }
        
        return insights
    
    def _generate_instagram_age_distribution(self):
        """Generate Instagram age distribution data"""
        return {
            '18-24': random.randint(25, 35),
            '25-34': random.randint(30, 40),
            '35-44': random.randint(15, 25),
            '45-54': random.randint(5, 15),
            '55-64': random.randint(2, 8),
            '65+': random.randint(1, 5)
        }
    
    def _generate_instagram_gender_distribution(self):
        """Generate Instagram gender distribution data"""
        return {
            'men': random.randint(45, 55),
            'women': random.randint(45, 55)
        }
    
    def _generate_instagram_location_distribution(self):
        """Generate Instagram location distribution data"""
        locations = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Palembang', 'Makassar', 'South Tangerang', 'Depok', 'Batam']
        distribution = {}
        
        for location in locations:
            distribution[location] = random.randint(2, 15)
        
        return distribution
    
    def _generate_instagram_interest_distribution(self):
        """Generate Instagram interest distribution data"""
        interests = ['real estate', 'property investment', 'home buying', 'interior design', 'luxury lifestyle', 'architecture', 'home decor', 'minimalist living']
        distribution = {}
        
        for interest in interests:
            distribution[interest] = random.randint(5, 25)
        
        return distribution
    
    def _generate_instagram_device_distribution(self):
        """Generate Instagram device distribution data"""
        return {
            'mobile': random.randint(85, 95),
            'desktop': random.randint(3, 10),
            'tablet': random.randint(2, 5)
        }
    
    def _generate_instagram_behavior_distribution(self):
        """Generate Instagram behavior distribution data"""
        return {
            'engaged_shoppers': random.randint(15, 25),
            'frequent_travelers': random.randint(10, 20),
            'mobile_device_users': random.randint(70, 90),
            'social_media_enthusiasts': random.randint(20, 35),
            'luxury_shoppers': random.randint(5, 15)
        }
