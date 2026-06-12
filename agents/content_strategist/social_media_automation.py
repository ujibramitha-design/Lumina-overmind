"""
Social Media Automation - Content Strategist Agent
Automates social media posting and engagement
"""

class SocialMediaAutomation:
    """Manager for social media automation and engagement"""
    
    def __init__(self):
        self.name = "Social Media Automation"
        self.version = "1.0.0"
        self.platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'tiktok', 'youtube']
        self.automation_rules = {}
        self.scheduled_posts = []
        self.engagement_metrics = {}
    
    def setup_automation_rules(self, platform_config):
        """Setup automation rules for social media platforms"""
        rules = {}
        
        for platform in platform_config:
            platform_rules = {
                'posting_schedule': self._create_posting_schedule(platform_config[platform]),
                'engagement_strategy': self._create_engagement_strategy(platform_config[platform]),
                'content_guidelines': self._create_content_guidelines(platform_config[platform]),
                'auto_reply': self._create_auto_reply_rules(platform_config[platform]),
                'hashtag_strategy': self._create_hashtag_strategy(platform_config[platform])
            }
            rules[platform] = platform_rules
        
        self.automation_rules = rules
        return rules
    
    def _create_posting_schedule(self, platform_config):
        """Create posting schedule for platform"""
        schedule = {
            'frequency': platform_config.get('frequency', 'daily'),
            'optimal_times': platform_config.get('optimal_times', ['09:00', '12:00', '15:00', '18:00', '21:00']),
            'days_of_week': platform_config.get('days_of_week', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']),
            'content_types': platform_config.get('content_types', ['image', 'video', 'text', 'story']),
            'max_posts_per_day': platform_config.get('max_posts_per_day', 3)
        }
        return schedule
    
    def _create_engagement_strategy(self, platform_config):
        """Create engagement strategy for platform"""
        strategy = {
            'auto_like': platform_config.get('auto_like', True),
            'auto_comment': platform_config.get('auto_comment', True),
            'auto_share': platform_config.get('auto_share', False),
            'comment_templates': platform_config.get('comment_templates', []),
            'like_delay_range': platform_config.get('like_delay_range', [30, 60]),
            'comment_delay_range': platform_config.get('comment_delay_range', [60, 120]),
            'share_threshold': platform_config.get('share_threshold', 10)
        }
        return strategy
    
    def _create_content_guidelines(self, platform_config):
        """Create content guidelines for platform"""
        guidelines = {
            'image_specs': platform_config.get('image_specs', {
                'resolution': '1080x1080',
                'format': 'jpg',
                'max_size': '5MB'
            }),
            'video_specs': platform_config.get('video_specs', {
                'resolution': '1080x1920',
                'duration': '15-60 seconds',
                'format': 'mp4'
            }),
            'text_length': platform_config.get('text_length', {
                'min': 50,
                'max': 280
            }),
            'hashtag_count': platform_config.get('hashtag_count', [3, 5]),
            'mention_limit': platform_config.get('mention_limit', 10)
        }
        return guidelines
    
    def _create_auto_reply_rules(self, platform_config):
        """Create auto-reply rules for platform"""
        rules = {
            'keywords': platform_config.get('auto_reply_keywords', []),
            'delay_range': platform_config.get('reply_delay_range', [5, 30]),
            'reply_templates': platform_config.get('reply_templates', []),
            'exclusion_keywords': platform_config.get('exclusion_keywords', ['spam', 'advertisement'])
        }
        return rules
    
    def _create_hashtag_strategy(self, platform_config):
        """Create hashtag strategy for platform"""
        strategy = {
            'primary_hashtags': platform_config.get('primary_hashtags', []),
            'secondary_hashtags': platform_config.get('secondary_hashtags', []),
            'trending_hashtags': platform_config.get('trending_hashtags', []),
            'location_hashtags': platform_config.get('location_hashtags', []),
            'hashtag_count': platform_config.get('hashtag_count', [3, 5])
        }
        return strategy
    
    def schedule_post(self, platform, content_data, scheduled_time):
        """Schedule post for specific platform"""
        post = {
            'post_id': f"POST_{len(self.scheduled_posts) + 1:03d}",
            'platform': platform,
            'content': content_data,
            'scheduled_time': scheduled_time,
            'status': 'scheduled',
            'created_at': '2026-05-28'
        }
        
        self.scheduled_posts.append(post)
        return post
    
    def generate_content_for_platform(self, platform, content_idea):
        """Generate platform-specific content"""
        guidelines = self.automation_rules.get(platform, {}).get('content_guidelines', {})
        
        content = {
            'platform': platform,
            'title': self._generate_platform_title(content_idea, platform),
            'caption': self._generate_platform_caption(content_idea, platform),
            'hashtags': self._generate_platform_hashtags(content_idea, platform),
            'media_type': self._select_media_type(content_idea, platform),
            'media_url': content_idea.get('media_url', ''),
            'call_to_action': content_idea.get('call_to_action', ''),
            'scheduled_time': content_idea.get('scheduled_time'),
            'status': 'generated'
        }
        
        # Validate content against guidelines
        validation_result = self._validate_content(content, guidelines)
        content['validation'] = validation_result
        
        return content
    
    def _generate_platform_title(self, content_idea, platform):
        """Generate platform-specific title"""
        title = content_idea.get('title', '')
        
        # Platform-specific title optimizations
        if platform == 'twitter':
            # Twitter has 280 character limit
            max_length = 280
            if len(title) > max_length:
                title = title[:max_length-3] + "..."
        elif platform == 'instagram':
            # Instagram titles work well with emojis and questions
            if '?' not in title and not title.endswith('?'):
                title += f"? #{random.choice(self._get_random_hashtag())}"
            elif len(title) < 50:
                title = f"🏠 {title}"
        elif platform == 'facebook':
            # Facebook titles work well with emojis and engagement questions
            if '?' not in title and not title.endswith('?'):
                title += f" 💭 {title}"
        elif platform == 'linkedin':
            # LinkedIn titles should be professional
            title = title.replace('🏠', '').replace('💭', '')
        elif platform == 'tiktok':
            # TikTok titles should be catchy and short
            if len(title) > 100:
                title = title[:100]
        
        return title
    
    def _generate_platform_caption(self, content_idea, platform):
        """Generate platform-specific caption"""
        caption = content_idea.get('description', '')
        
        # Platform-specific caption optimizations
        if platform == 'instagram':
            # Instagram captions work well with emojis and hashtags
            caption = f"{caption}\n\n{self._generate_platform_hashtags(content_idea, platform)}\n\n💬 DM for details!"
        elif platform == 'facebook':
            # Facebook captions can be longer and more detailed
            caption = f"{caption}\n\n{self._generate_platform_hashtags(content_idea, platform)}\n\n📞 Learn more: {content_idea.get('call_to_action', '')}"
        elif platform == 'twitter':
            # Twitter captions need to be concise
            max_length = 280 - len(self._generate_platform_hashtags(content_idea, platform)) - 10
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
        elif platform == 'linkedin':
            # LinkedIn captions should be professional
            caption = caption.replace('🏠', '').replace('💭', '')
        elif platform == 'tiktok':
            # TikTok captions should be engaging and short
            caption = f"{caption}\n\n{self._generate_platform_hashtags(content_idea, platform)}"
        
        return caption
    
    def _generate_platform_hashtags(self, content_idea, platform):
        """Generate platform-specific hashtags"""
        hashtags = []
        
        # Get strategy for platform
        strategy = self.automation_rules.get(platform, {}).get('hashtag_strategy', {})
        
        # Add primary hashtags
        primary_hashtags = strategy.get('primary_hashtags', [])
        hashtags.extend(primary_hashtags)
        
        # Add secondary hashtags
        secondary_hashtags = strategy.get('secondary_hashtags', [])
        hashtags.extend(secondary_hashtags)
        
        # Add trending hashtags
        trending_hashtags = strategy.get('trending_hashtags', [])
        hashtags.extend(trending_hashtags[:2])  # Limit to 2 trending hashtags
        
        # Add location hashtags
        location_hashtags = strategy.get('location_hashtags', [])
        hashtags.extend(location_hashtags)
        
        # Add content-specific hashtags
        content_hashtags = content_idea.get('hashtags', [])
        hashtags.extend(content_hashtags)
        
        # Remove duplicates and limit count
        unique_hashtags = list(set(hashtags))
        hashtag_count = strategy.get('hashtag_count', [3, 5])
        
        return unique_hashtags[:hashtag_count[0]]
    
    def _select_media_type(self, content_idea, platform):
        """Select appropriate media type for platform"""
        if content_idea.get('media_url'):
            # If media URL provided, determine type
            media_url = content_idea['media_url'].lower()
            if any(ext in media_url for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                return 'image'
            elif any(ext in media_url for ext in ['.mp4', '.mov', '.avi']):
                return 'video'
        
        # Default media type based on platform and content type
        platform_preferences = {
            'instagram': ['image', 'video', 'story'],
            'facebook': ['image', 'video', 'link'],
            'twitter': ['image', 'video'],
            'linkedin': ['image', 'article'],
            'tiktok': ['video'],
            'youtube': ['video']
        }
        
        content_type = content_idea.get('content_type', 'social')
        
        if content_type == 'video':
            return 'video'
        elif content_type == 'infographic':
            return 'image'
        else:
            return random.choice(platform_preferences.get(platform, ['image']))
    
    def _validate_content(self, content, guidelines):
        """Validate content against platform guidelines"""
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check image specs
        if content.get('media_type') == 'image':
            image_specs = guidelines.get('image_specs', {})
            # In real implementation, would check actual image properties
            validation['image_size_ok'] = True  # Placeholder
            validation['image_resolution_ok'] = True  # Placeholder
        
        # Check video specs
        elif content.get('media_type') == 'video':
            video_specs = guidelines.get('video_specs', {})
            # In real implementation, would check actual video properties
            validation['video_duration_ok'] = True  # Placeholder
            validation['video_resolution_ok'] = True  # Placeholder
        
        # Check text length
        if content.get('caption'):
            text_length = len(content['caption'])
            min_length = guidelines.get('text_length', {}).get('min', 0)
            max_length = guidelines.get('text_length', {}).get('max', 1000)
            
            if text_length < min_length:
                validation['errors'].append(f"Text too short (minimum {min_length} characters)")
                validation['is_valid'] = False
            elif text_length > max_length:
                validation['errors'].append(f"Text too long (maximum {max_length} characters)")
                validation['is_valid'] = False
        
        # Check hashtag count
        hashtags = content.get('hashtags', [])
        hashtag_count = len(hashtags)
        min_hashtags = guidelines.get('hashtag_count', [3, 5])[0]
        max_hashtags = guidelines.get('hashtag_count', [3, 5])[1]
        
        if hashtag_count < min_hashtags:
            validation['warnings'].append(f"Consider adding more hashtags (minimum {min_hashtags})")
        elif hashtag_count > max_hashtags:
            validation['warnings'].append(f"Too many hashtags (maximum {max_hashtags})")
        
        return validation
    
    def auto_engage_with_post(self, post_id, platform):
        """Automatically engage with posted content"""
        strategy = self.automation_rules.get(platform, {}).get('engagement_strategy', {})
        
        if not strategy.get('auto_like', False):
            return {'status': 'auto_engagement_disabled', 'actions': []}
        
        actions = []
        
        # Auto-like with delay
        if strategy.get('auto_like', False):
            like_delay = random.randint(strategy.get('like_delay_range', [30, 60]))
            actions.append({
                'action': 'like',
                'delay': like_delay,
                'post_id': post_id,
                'platform': platform
            })
        
        # Auto-comment with delay
        if strategy.get('auto_comment', False):
            comment_delay = random.randint(strategy.get('comment_delay_range', [60, 120]))
            comment_template = random.choice(strategy.get('comment_templates', ['Great post! 👍', 'Amazing content! 🎉', 'Love this! 💙', 'Interesting! 🤔']))
            actions.append({
                'action': 'comment',
                'delay': comment_delay,
                'post_id': post_id,
                'platform': platform,
                'template': comment_template
            })
        
        # Auto-share if threshold met
        if strategy.get('auto_share', False):
            share_threshold = strategy.get('share_threshold', 10)
            # In real implementation, would check actual engagement metrics
            current_engagement = random.randint(5, 20)  # Simulated engagement
            if current_engagement >= share_threshold:
                actions.append({
                    'action': 'share',
                    'delay': 300,  # 5 minutes delay
                    'post_id': post_id,
                    'platform': platform
                })
        
        return {
            'status': 'auto_engagement_enabled',
            'actions': actions
        }
    
    def monitor_engagement_metrics(self, post_id, platform, metrics_data):
        """Monitor engagement metrics for posted content"""
        metrics = {
            'post_id': post_id,
            'platform': platform,
            'views': metrics_data.get('views', 0),
            'likes': metrics_data.get('likes', 0),
            'comments': metrics_data.get('comments', 0),
            'shares': metrics_data.get('shares', 0),
            'clicks': metrics_data.get('clicks', 0),
            'saves': metrics_data.get('saves', 0),
            'engagement_rate': self._calculate_engagement_rate(metrics_data),
            'reach': metrics_data.get('reach', 0),
            'impressions': metrics_data.get('impressions', 0),
            'monitored_at': '2026-05-28'
        }
        
        # Store metrics for analysis
        self.engagement_metrics[post_id] = metrics
        
        return metrics
    
    def _calculate_engagement_rate(self, metrics_data):
        """Calculate engagement rate"""
        views = metrics_data.get('views', 1)
        total_engagement = metrics_data.get('likes', 0) + metrics_data.get('comments', 0) + metrics_data.get('shares', 0)
        
        return (total_engagement / views) * 100 if views > 0 else 0
    
    def generate_automation_report(self, platform, date_range='7d'):
        """Generate automation report for platform"""
        report = {
            'platform': platform,
            'date_range': date_range,
            'total_posts_scheduled': len(self.scheduled_posts),
            'total_posts_published': len([p for p in self.scheduled_posts if p.get('status') == 'published']),
            'total_engagement': sum(self.engagement_metrics.values()),
            'average_engagement_rate': self._calculate_average_engagement_rate(),
            'top_performing_posts': self._get_top_performing_posts(),
            'automation_efficiency': self._calculate_automation_efficiency(),
            'generated_at': '2026-05-28'
        }
        
        return report
    
    def _calculate_average_engagement_rate(self):
        """Calculate average engagement rate across all posts"""
        if not self.engagement_metrics:
            return 0
        
        total_engagement_rate = sum(
            metrics.get('engagement_rate', 0) 
            for metrics in self.engagement_metrics.values()
        )
        
        return total_engagement_rate / len(self.engagement_metrics)
    
    def _get_top_performing_posts(self):
        """Get top performing posts by engagement rate"""
        if not self.engagement_metrics:
            return []
        
        # Sort by engagement rate
        sorted_posts = sorted(
            self.engagement_metrics.items(),
            key=lambda x: x[1].get('engagement_rate', 0),
            reverse=True
        )
        
        return [
            {
                'post_id': post_id,
                'engagement_rate': metrics['engagement_rate'],
                'total_engagement': metrics['likes'] + metrics['comments'] + metrics['shares'],
                'platform': self.scheduled_posts.get(post_id, {}).get('platform', 'unknown')
            }
            for post_id, metrics in sorted_posts[:5]  # Top 5 posts
        ]
    
    def _calculate_automation_efficiency(self):
        """Calculate automation efficiency score"""
        total_scheduled = len(self.scheduled_posts)
        published_posts = len([p for p in self.scheduled_posts if p.get('status') == 'published'])
        
        if total_scheduled == 0:
            return 0
        
        return (published_posts / total_scheduled) * 100
    
    def optimize_automation_strategy(self, platform, performance_data):
        """Optimize automation strategy based on performance data"""
        current_strategy = self.automation_rules.get(platform, {})
        
        optimizations = {
            'posting_frequency': self._optimize_posting_frequency(platform, performance_data),
            'engagement_strategy': self._optimize_engagement_strategy(platform, performance_data),
            'content_guidelines': self._optimize_content_guidelines(platform, performance_data),
            'auto_reply_rules': self._optimize_auto_reply_rules(platform, performance_data)
        }
        
        return optimizations
    
    def _optimize_posting_frequency(self, platform, performance_data):
        """Optimize posting frequency based on performance"""
        current_frequency = current_strategy.get('posting_schedule', {}).get('frequency', 'daily')
        
        # Analyze performance by time of day
        time_performance = self._analyze_time_performance(platform, performance_data)
        
        # Find best performing time slots
        best_times = max(time_performance.items(), key=lambda x: x[1]) if time_performance else (0, 0))
        best_time = best_times[0] if best_times else '12:00'
        
        # Adjust frequency based on performance
        if performance_data.get('average_engagement_rate', 0) > 5.0:
            new_frequency = 'twice_daily'
        elif performance_data.get('average_engagement_rate', 0) < 1.0:
            new_frequency = 'weekly'
        else:
            new_frequency = current_frequency
        
        return {
            'current_frequency': current_frequency,
            'recommended_frequency': new_frequency,
            'optimal_time': best_time,
            'reasoning': self._get_frequency_recommendation(performance_data)
        }
    
    def _analyze_time_performance(self, platform, performance_data):
        """Analyze performance by time of day"""
        time_performance = {}
        
        # Group posts by time of day
        for metrics in performance_data.values():
            # Extract time from timestamp (simplified)
            hour = 12  # Placeholder - in real implementation would extract from actual timestamp
            
            if hour not in time_performance:
                time_performance[hour] = {
                    'engagement_rate': metrics.get('engagement_rate', 0),
                    'post_count': 1
                }
            else:
                time_performance[hour]['engagement_rate'] += metrics.get('engagement_rate', 0)
                time_performance[hour]['post_count'] += 1
        
        # Calculate average engagement rate by time
        for hour in time_performance:
            if time_performance[hour]['post_count'] > 0:
                time_performance[hour]['engagement_rate'] /= time_performance[hour]['post_count']
        
        return time_performance
    
    def _get_frequency_recommendation(self, performance_data):
        """Get recommendation for posting frequency"""
        avg_engagement = performance_data.get('average_engagement_rate', 0)
        
        if avg_engagement > 5.0:
            return "High engagement - consider increasing posting frequency"
        elif avg_engagement > 3.0:
            return "Good engagement - maintain current frequency"
        elif avg_engagement > 1.0:
            return "Moderate engagement - consider optimizing content"
        else:
            return "Low engagement - reduce frequency and improve content quality"
    
    def _optimize_engagement_strategy(self, platform, performance_data):
        """Optimize engagement strategy based on performance data"""
        current_strategy = self.automation_rules.get(platform, {}).get('engagement_strategy', {})
        
        optimized_strategy = current_strategy.copy()
        
        # Adjust auto-like based on engagement rates
        if performance_data.get('average_engagement_rate', 0) > 5.0:
            optimized_strategy['auto_like'] = True
            optimized_strategy['like_delay_range'] = [15, 30]  # Faster for high engagement
        elif performance_data.get('share_rate', 0) > 0.1:
            optimized_strategy['auto_share'] = True
            optimized_strategy['share_threshold'] = 5  # Lower threshold for high share rates
        
        return optimized_strategy
    
    def _optimize_content_guidelines(self, platform, performance_data):
        """Optimize content guidelines based on performance data"""
        current_guidelines = self.automation_rules.get(platform, {}).get('content_guidelines', {})
        
        optimized_guidelines = current_guidelines.copy()
        
        # Adjust based on content type performance
        content_performance = self._analyze_content_type_performance(platform, performance_data)
        
        best_performing_type = max(content_performance.items(), key=lambda x: x[1]) if content_performance else (None, 0))
        
        if best_performing_type:
            best_type = best_performing_type[0]
            optimized_guidelines['preferred_content_type'] = best_type
        
        return optimized_guidelines
    
    def _optimize_auto_reply_rules(self, platform, performance_data):
        """Optimize auto-reply rules based on performance data"""
        current_rules = self.automation_rules.get(platform, {}).get('auto_reply_rules', {})
        
        optimized_rules = current_rules.copy()
        
        # Adjust delays based on engagement rates
        if performance_data.get('average_engagement_rate', 0) > 5.0:
            optimized_rules['delay_range'] = [10, 30]  # Faster for high engagement
            optimized_rules['reply_templates'] = ['Amazing! 👍', 'Love this! 💙', 'Great! 🎉']
        elif performance_data.get('comment_rate', 0) > 0.1:
            optimized_rules['delay_range'] = [30, 60]  # Moderate for moderate engagement
            optimized_rules['reply_templates'] = ['Great post! 👍', 'Interesting! 🤔', 'Thanks for sharing!']
        
        return optimized_rules
    
    def _analyze_content_type_performance(self, platform, performance_data):
        """Analyze performance by content type"""
        content_performance = {}
        
        for metrics in performance_data.values():
            content_type = metrics.get('content_type', 'unknown')
            if content_type not in content_performance:
                content_performance[content_type] = {
                    'engagement_rate': metrics.get('engagement_rate', 0),
                    'post_count': 1
                }
            else:
                content_performance[content_type]['engagement_rate'] += metrics.get('engagement_rate', 0)
                content_performance[content_type]['post_count'] += 1
        
        # Calculate average engagement rate by content type
        for content_type in content_performance:
            if content_performance[content_type]['post_count'] > 0:
                content_performance[content_type]['engagement_rate'] /= content_performance[content_type]['post_count']
        
        return content_performance
    
    def create_automation_dashboard(self):
        """Create comprehensive automation dashboard"""
        dashboard = {
            'overview': {
                'total_platforms': len(self.platforms),
                'active_automations': len([p for p in self.automation_rules.keys()]),
                'total_scheduled_posts': len(self.scheduled_posts),
                'total_published_posts': len([p for p in self.scheduled_posts if p.get('status') == 'published']),
                'automation_efficiency': self._calculate_automation_efficiency()
            },
            'platform_performance': {},
            'recent_activity': []
        }
        
        # Add platform-specific performance
        for platform in self.platforms:
            platform_report = self.generate_automation_report(platform)
            dashboard['platform_performance'][platform] = platform_report
        
        # Add recent activity
        dashboard['recent_activity'] = self.scheduled_posts[-5:]  # Last 5 scheduled posts
        
        return dashboard
    
    def export_automation_data(self, format='json'):
        """Export automation data in specified format"""
        data = {
            'automation_rules': self.automation_rules,
            'scheduled_posts': self.scheduled_posts,
            'engagement_metrics': self.engagement_metrics,
            'platforms': self.platforms
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
            writer.writerow(['post_id', 'platform', 'title', 'status', 'scheduled_time', 'created_at'])
            
            # Write data
            for post in self.scheduled_posts:
                writer.writerow([
                    post['post_id'],
                    post['platform'],
                    post['content'].get('title', ''),
                    post['status'],
                    post.get('scheduled_time', ''),
                    post['created_at', '')
                ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def test_automation_functionality(self, platform):
        """Test automation functionality for specific platform"""
        test_results = {
            'platform': platform,
            'test_timestamp': '2026-05-28',
            'tests_passed': 0,
            'tests_failed': 0,
            'test_results': []
        }
        
        # Test content generation
        try:
            test_content = {
                'title': f"Test post for {platform}",
                'description': "This is a test post for automation testing",
                'content_type': 'social'
            }
            generated_content = self.generate_content_for_platform(platform, test_content)
            test_results['tests_passed'] += 1
            test_results['test_results'].append({
                'test': 'content_generation',
                'status': 'passed'
            })
        except Exception as e:
            test_results['tests_failed'] += 1
            test_results['test_results'].append({
                'test': 'content_generation',
                'status': 'failed',
                'error': str(e)
            })
        
        # Test content validation
        try:
            validation = self._validate_content(generated_content, 
                                         self.automation_rules.get(platform, {}).get('content_guidelines', {}))
            if validation['is_valid']:
                test_results['tests_passed'] += 1
                test_results['test_results'].append({
                    'test': 'content_validation',
                    'status': 'passed'
                })
            else:
                test_results['tests_failed'] += 1
                test_results['test_results'].append({
                    'test': 'content_validation',
                    'status': 'failed',
                    'errors': validation['errors']
                })
        except Exception as e:
            test_results['tests_failed'] += 1
            test_results['test_results'].append({
                'test': 'content_validation',
                'status': 'failed',
                'error': str(e)
            })
        
        # Test auto-engagement simulation
        try:
            engagement_simulation = self.auto_engage_with_post('test_post_123', platform)
            test_results['tests_passed'] += 1
            test_results['test_results'].append({
                'test': 'auto_engagement',
                'status': 'passed'
            })
        except Exception as e:
            test_results['tests_failed'] += 1
            test_results['test_results'].append({
                'test': 'auto_engagement',
                'status': 'failed',
                'error': str(e)
            })
        
        test_results['success_rate'] = (test_results['tests_passed'] / (test_results['tests_passed'] + test_results['tests_failed'])) * 100
        
        return test_results
