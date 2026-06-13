"""
Social Proof Manager - Closer Agent
Manages testimonials, case studies, and social proof content
"""

class SocialProofManager:
    """Manages social proof and customer testimonials"""
    
    def __init__(self):
        self.name = "Social Proof Manager"
        self.version = "1.0.0"
        self.testimonials = []
        self.case_studies = []
    
    def collect_testimonial(self, customer_data, testimonial_text):
        """Collect and store customer testimonials"""
        testimonial = {
            'customer_name': customer_data.get('name', 'Anonymous'),
            'property_purchased': customer_data.get('property', 'Unknown'),
            'testimonial': testimonial_text,
            'rating': customer_data.get('rating', 5),
            'date_collected': '2026-05-28',
            'verified': True
        }
        self.testimonials.append(testimonial)
        return testimonial
    
    def create_case_study(self, customer_journey):
        """Create detailed case study from customer journey"""
        case_study = {
            'title': f"Success Story: {customer_journey.get('customer_name', 'Customer')}",
            'background': customer_journey.get('background', 'Customer background'),
            'challenges': customer_journey.get('challenges', 'Challenges faced'),
            'solution': customer_journey.get('solution', 'Property solution'),
            'results': customer_journey.get('results', 'Positive outcomes'),
            'timeline': customer_journey.get('timeline', 'Process timeline'),
            'testimonials': customer_journey.get('testimonials', [])
        }
        self.case_studies.append(case_study)
        return case_study
    
    def get_social_proof_content(self, property_type=None):
        """Get relevant social proof content for marketing"""
        filtered_testimonials = self.testimonials
        if property_type:
            filtered_testimonials = [t for t in self.testimonials 
                                  if property_type.lower() in t.get('property_purchased', '').lower()]
        
        return {
            'testimonials': filtered_testimonials,
            'case_studies': self.case_studies,
            'total_customers': len(self.testimonials),
            'average_rating': sum(t.get('rating', 0) for t in self.testimonials) / len(self.testimonials) if self.testimonials else 0
        }
