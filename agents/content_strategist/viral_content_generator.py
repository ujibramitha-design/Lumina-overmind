"""
Viral Content Generator - Content Strategist Agent
Generates viral content ideas and predicts viral potential
"""

class ViralContentGenerator:
    """Generator for viral content ideas and analysis"""
    
    def __init__(self):
        self.name = "Viral Content Generator"
        self.version = "1.0.0"
        self.viral_patterns = []
        self.trending_topics = []
        self.engagement_metrics = {}
    
    def analyze_viral_potential(self, content_idea):
        """Analyze viral potential of content idea"""
        analysis = {
            'content_title': content_idea.get('title', ''),
            'viral_score': 0,
            'viral_factors': [],
            'engagement_prediction': 0,
            'shareability_score': 0,
            'trend_alignment': 0,
            'recommendations': [],
            'risk_assessment': 'low'
        }
        
        # Analyze viral factors
        viral_factors = self._analyze_viral_factors(content_idea)
        analysis['viral_factors'] = viral_factors
        
        # Calculate viral score
        analysis['viral_score'] = self._calculate_viral_score(viral_factors)
        
        # Predict engagement
        analysis['engagement_prediction'] = self._predict_engagement(content_idea, viral_factors)
        
        # Calculate shareability
        analysis['shareability_score'] = self._calculate_shareability(content_idea)
        
        # Check trend alignment
        analysis['trend_alignment'] = self._check_trend_alignment(content_idea)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_viral_recommendations(analysis)
        
        # Assess risk
        analysis['risk_assessment'] = self._assess_content_risk(analysis)
        
        return analysis
    
    def _analyze_viral_factors(self, content_idea):
        """Analyze viral factors in content"""
        factors = []
        
        title = content_idea.get('title', '').lower()
        description = content_idea.get('description', '').lower()
        keywords = content_idea.get('keywords', [])
        
        # Emotional triggers
        emotional_words = ['amazing', 'shocking', 'incredible', 'unbelievable', 'mind-blowing', 'life-changing', 'game-changing']
        for word in emotional_words:
            if word in title or word in description:
                factors.append({
                    'factor': 'emotional_trigger',
                    'word': word,
                    'impact': 'high',
                    'score': 8
                })
        
        # Urgency/scarcity
        urgency_words = ['limited time', 'only', 'exclusive', 'don\'t miss', 'last chance', 'ending soon']
        for word in urgency_words:
            if word in title or word in description:
                factors.append({
                    'factor': 'urgency',
                    'word': word,
                    'impact': 'high',
                    'score': 9
                })
        
        # Social proof elements
        social_proof = ['testimonials', 'reviews', 'success stories', 'case studies', 'customer stories']
        for proof in social_proof:
            if proof in description:
                factors.append({
                    'factor': 'social_proof',
                    'element': proof,
                    'impact': 'medium',
                    'score': 6
                })
        
        # Surprise/novelty
        surprise_words = ['secret', 'revealed', 'uncovered', 'hidden', 'never before seen', 'first time']
        for word in surprise_words:
            if word in title or word in description:
                factors.append({
                    'factor': 'surprise',
                    'word': word,
                    'impact': 'medium',
                    'score': 7
                })
        
        # List/breakdown content
        list_words = ['top 10', '5 ways', '3 secrets', '7 tips', 'ultimate guide', 'complete list']
        for word in list_words:
            if word in title:
                factors.append({
                    'factor': 'listicle_format',
                    'word': word,
                    'impact': 'medium',
                    'score': 5
                })
        
        # Question/curiosity gap
        question_words = ['why', 'how', 'what if', 'did you know', 'can you believe']
        for word in question_words:
            if word in title:
                factors.append({
                    'factor': 'curiosity_gap',
                    'word': word,
                    'impact': 'medium',
                    'score': 6
                })
        
        return factors
    
    def _calculate_viral_score(self, viral_factors):
        """Calculate overall viral score"""
        if not viral_factors:
            return 0
        
        # Weight different factors
        factor_weights = {
            'emotional_trigger': 0.3,
            'urgency': 0.35,
            'social_proof': 0.15,
            'surprise': 0.1,
            'listicle_format': 0.05,
            'curiosity_gap': 0.05
        }
        
        total_score = 0
        factor_scores = []
        
        for factor in viral_factors:
            weight = factor_weights.get(factor['factor'], 0.1)
            score = factor['score'] * weight
            total_score += score
            factor_scores.append({
                'factor': factor['factor'],
                'word': factor['word'],
                'score': score
            })
        
        return min(10, total_score)
    
    def _predict_engagement(self, content_idea, viral_factors):
        """Predict engagement metrics"""
        base_engagement = 100  # Base engagement
        
        # Boost based on viral factors
        engagement_boost = 0
        for factor in viral_factors:
            if factor['impact'] == 'high':
                engagement_boost += factor['score'] * 50
            elif factor['impact'] == 'medium':
                engagement_boost += factor['score'] * 25
        
        # Content type adjustments
        content_type = content_idea.get('content_type', 'blog')
        type_multipliers = {
            'video': 2.0,
            'infographic': 1.8,
            'social': 1.5,
            'blog': 1.0,
            'email': 0.8
        }
        
        multiplier = type_multipliers.get(content_type, 1.0)
        predicted_engagement = int(base_engagement * (1 + engagement_boost / 100) * multiplier)
        
        return min(10000, predicted_engagement)  # Cap at 10k
    
    def _calculate_shareability(self, content_idea):
        """Calculate shareability score"""
        shareability_score = 5.0  # Base score
        
        # Boost for visual content
        if content_idea.get('content_type') in ['video', 'infographic']:
            shareability_score += 2.0
        
        # Boost for emotional content
        if any(word in content_idea.get('title', '').lower() 
               for word in ['amazing', 'incredible', 'shocking']):
            shareability_score += 1.5
        
        # Boost for listicle content
        if any(word in content_idea.get('title', '').lower() 
               for word in ['top 10', '5 ways', 'ultimate guide']):
            shareability_score += 1.0
        
        # Boost for social proof
        if any(word in content_idea.get('description', '').lower() 
               for word in ['testimonials', 'success stories', 'case studies']):
            shareability_score += 0.5
        
        return min(10, shareability_score)
    
    def _check_trend_alignment(self, content_idea):
        """Check alignment with current trends"""
        trend_score = 5.0  # Base score
        
        # Check trending keywords
        trending_keywords = self.get_trending_keywords()
        content_keywords = content_idea.get('keywords', [])
        
        for keyword in content_keywords:
            if keyword.lower() in [trend.lower() for trend in trending_keywords]:
                trend_score += 0.5
        
        # Check trending topics
        trending_topics = self.get_trending_topics()
        content_text = f"{content_idea.get('title', '')} {content_idea.get('description', '')}"
        
        for topic in trending_topics:
            if topic.lower() in content_text.lower():
                trend_score += 0.3
        
        return min(10, trend_score)
    
    def _generate_viral_recommendations(self, analysis):
        """Generate recommendations for viral content"""
        recommendations = []
        
        viral_score = analysis['viral_score']
        
        if viral_score < 3:
            recommendations.append({
                'type': 'improvement',
                'recommendation': 'Add emotional triggers or urgency elements to increase viral potential',
                'priority': 'high'
            })
        
        if analysis['shareability_score'] < 5:
            recommendations.append({
                'type': 'format_change',
                'recommendation': 'Consider converting to video or infographic format for better shareability',
                'priority': 'medium'
            })
        
        if analysis['trend_alignment'] < 6:
            recommendations.append({
                'type': 'trending_content',
                'recommendation': 'Incorporate current trending topics to increase relevance',
                'priority': 'medium'
            })
        
        if len(analysis['viral_factors']) < 3:
            recommendations.append({
                'type': 'content_enhancement',
                'recommendation': 'Add more viral elements like emotional triggers, social proof, or surprise factors',
                'priority': 'high'
            })
        
        return recommendations
    
    def _assess_content_risk(self, analysis):
        """Assess content risk level"""
        viral_score = analysis['viral_score']
        
        if viral_score >= 8:
            return 'low'
        elif viral_score >= 5:
            return 'medium'
        else:
            return 'high'
    
    def generate_viral_ideas(self, topic, content_type='social', platform='instagram', count=5):
        """Generate viral content ideas"""
        ideas = []
        
        viral_patterns = [
            {
                'pattern': 'emotional_storytelling',
                'template': "The {emotional_adjective} story of how {subject} {action} {result}",
                'examples': ['inspiring', 'heartwarming', 'shocking', 'incredible']
            },
            {
                'pattern': 'urgency_with_social_proof',
                'template': "{urgency_phrase}: {subject} {action} - {social_proof}",
                'examples': ['Limited time only', 'Last chance', 'Don\'t miss out', 'Exclusive offer']
            },
            {
                'pattern': 'surprise_revelation',
                'template': "{surprise_word}: We discovered {surprise_element} about {topic}",
                'examples': ['Shocking discovery', 'Hidden secret', 'Never before seen']
            },
            {
                'pattern': 'listicle_with_numbers',
                'template': "{number} {adjective} ways to {action} {topic} {result}",
                'examples': ['10 powerful', '7 proven', '5 effective']
            },
            {
                'pattern': 'curiosity_gap',
                'template': "Did you know {surprising_fact} about {topic}?",
                'examples': ['Did you know', 'Can you believe', 'Have you heard']
            }
        ]
        
        # Generate ideas based on patterns
        for i in range(count):
            pattern = random.choice(viral_patterns)
            
            if pattern['pattern'] == 'emotional_storytelling':
                emotional = random.choice(pattern['examples'])
                ideas.append({
                    'title': f"The {emotional} story of how {topic} transformed lives",
                    'description': f"An inspiring tale about {topic} that will {action} and {result}",
                    'content_type': content_type,
                    'platform': platform,
                    'viral_potential': 'high'
                })
            
            elif pattern['pattern'] == 'urgency_with_social_proof':
                urgency = random.choice(pattern['examples'])
                ideas.append({
                    'title': f"{urgency}: {topic} {action} - Limited Time Only!",
                    'description': f"Don't miss this opportunity to {action} {topic}. {social_proof}",
                    'content_type': content_type,
                    'platform': platform,
                    'viral_potential': 'high'
                })
            
            elif pattern['pattern'] == 'surprise_revelation':
                surprise = random.choice(pattern['examples'])
                ideas.append({
                    'title': f"{surprise}: We discovered {topic} secret revealed!",
                    'description': f"Breaking news about {topic} that will change everything you thought you knew",
                    'content_type': content_type,
                    'platform': platform,
                    'viral_potential': 'high'
                })
            
            elif pattern['pattern'] == 'listicle_with_numbers':
                number = random.choice(pattern['examples'])
                adjective = random.choice(['powerful', 'proven', 'effective', 'amazing', 'incredible'])
                ideas.append({
                    'title': f"{number} {adjective} ways to {action} {topic}",
                    'description': f"Comprehensive guide on {topic} with {number} {adjective} methods",
                    'content_type': content_type,
                    'platform': platform,
                    'viral_potential': 'medium'
                })
            
            elif pattern['pattern'] == 'curiosity_gap':
                ideas.append({
                    'title': f"Did you know this surprising fact about {topic}?",
                    'description': f"Mind-blowing discovery about {topic} that most people don't know",
                    'content_type': content_type,
                    'platform': platform,
                    'viral_potential': 'medium'
                })
        
        return ideas
    
    def get_trending_keywords(self):
        """Get current trending keywords"""
        # In real implementation, this would fetch from trending APIs
        return [
            'property investment',
            'real estate tips',
            'home buying guide',
            'mortgage rates',
            'property market',
            'investment properties',
            'house hunting',
            'real estate trends',
            'property prices'
        ]
    
    def get_trending_topics(self):
        """Get current trending topics"""
        # In real implementation, this would fetch from trending APIs
        return [
            'sustainable housing',
            'smart homes',
            'remote work',
            'urban development',
            'property investment',
            'digital real estate',
            'affordable housing',
            'luxury properties',
            'green buildings',
            'co-living spaces'
        ]
    
    def predict_content_virality(self, content_idea):
        """Predict content virality with confidence score"""
        analysis = self.analyze_viral_potential(content_idea)
        
        # Calculate confidence based on multiple factors
        confidence_factors = {
            'viral_score_strength': min(1.0, analysis['viral_score'] / 8.0),
            'factor_diversity': min(1.0, len(analysis['viral_factors']) / 5.0),
            'trend_alignment': analysis['trend_alignment'] / 10.0,
            'shareability': analysis['shareability_score'] / 10.0
        }
        
        # Calculate overall confidence
        confidence = sum(confidence_factors.values()) / len(confidence_factors)
        
        return {
            'virality_prediction': {
                'is_viral': confidence >= 0.6,
                'confidence_score': round(confidence * 100, 2),
                'viral_score': analysis['viral_score'],
                'confidence_factors': confidence_factors
            },
            'recommendations': analysis['recommendations'],
            'risk_assessment': analysis['risk_assessment']
        }
    
    def optimize_content_for_virality(self, content_idea):
        """Optimize content idea for maximum virality"""
        optimization = {
            'original_idea': content_idea,
            'optimized_idea': content_idea.copy(),
            'optimizations': []
        }
        
        # Optimize title
        optimized_title = self._optimize_title(content_idea)
        if optimized_title != content_idea.get('title'):
            optimization['optimized_idea']['title'] = optimized_title
            optimization['optimizations'].append('Enhanced title for emotional impact')
        
        # Optimize description
        optimized_description = self._optimize_description(content_idea)
        if optimized_description != content_idea.get('description'):
            optimization['optimized_idea']['description'] = optimized_description
            optimization['optimizations'].append('Enhanced description for engagement')
        
        # Add viral elements
        viral_enhancements = self._add_viral_elements(content_idea)
        optimization['optimized_idea'].update(viral_enhancements)
        optimization['optimizations'].extend(viral_enhancements['added_elements'])
        
        # Re-analyze optimized content
        new_analysis = self.analyze_viral_potential(optimization['optimized_idea'])
        optimization['optimized_analysis'] = new_analysis
        optimization['improvement'] = new_analysis['viral_score'] - content_idea.get('viral_score', 0)
        
        return optimization
    
    def _optimize_title(self, content_idea):
        """Optimize title for virality"""
        title = content_idea.get('title', '')
        
        # Add emotional words if missing
        emotional_words = ['amazing', 'incredible', 'shocking', 'mind-blowing', 'life-changing']
        has_emotional = any(word in title.lower() for word in emotional_words)
        
        if not has_emotional:
            emotional_word = random.choice(emotional_words)
            title = f"The {emotional_word.title()} {title}"
        
        # Add urgency if missing
        urgency_words = ['limited time', 'only', 'exclusive', 'last chance']
        has_urgency = any(word in title.lower() for word in urgency_words)
        
        if not has_urgency and content_idea.get('content_type') == 'social':
            urgency_word = random.choice(urgency_words)
            title = f"{title} - {urgency_word.title()}!"
        
        # Add numbers for listicle content
        if content_idea.get('content_type') in ['blog', 'infographic']:
            number_words = ['10', '7', '5', '3']
            has_number = any(word in title for word in number_words)
            
            if not has_number:
                number = random.choice(number_words)
                title = f"{number} Ways to {title}"
        
        return title
    
    def _optimize_description(self, content_idea):
        """Optimize description for engagement"""
        description = content_idea.get('description', '')
        
        # Add emotional appeal
        if 'inspiring' not in description.lower():
            description = f"An inspiring {description}"
        
        # Add social proof if missing
        if 'testimonials' not in description.lower() and 'reviews' not in description.lower():
            description = f"{description}. See what our customers are saying!"
        
        # Add call-to-action
        if 'learn more' not in description.lower() and 'discover' not in description.lower():
            description = f"{description}. Learn more about this amazing opportunity!"
        
        return description
    
    def _add_viral_elements(self, content_idea):
        """Add viral elements to content"""
        enhancements = {
            'added_elements': {},
            'hashtags': [],
            'mentions': [],
            'call_to_actions': []
        }
        
        # Add trending hashtags
        trending_hashtags = ['#propertyinvestment', '#realestate', '#hometips', '#investment', '#propertytips']
        enhancements['hashtags'] = random.sample(trending_hashtags, 3)
        
        # Add call-to-actions
        ctas = ['Share this!', 'Tag a friend!', 'Learn more!', 'Don\'t miss out!']
        enhancements['call_to_actions'] = random.sample(ctas, 2)
        
        # Add urgency elements if appropriate
        if content_idea.get('content_type') == 'social' and 'limited' not in content_idea.get('description', '').lower():
            enhancements['urgency_badge'] = '⏰ Limited Time Offer!'
        
        return enhancements
