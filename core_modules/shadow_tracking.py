"""
LUMINA OS - Shadow Tracking & Pixel Management
Enterprise-grade visitor tracking and retargeting infrastructure
"""

import os
import logging
import asyncio
import json
import hashlib
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrackingType(Enum):
    """Types of tracking"""
    PIXEL = "pixel"
    COOKIE = "cookie"
    FINGERPRINT = "fingerprint"
    SESSION = "session"
    CUSTOM = "custom"

class PixelProvider(Enum):
    """Pixel providers"""
    META = "meta"  # Facebook Pixel
    GOOGLE = "google"  # Google Tag Manager
    TIKTOK = "tiktok"  # TikTok Pixel
    LINKEDIN = "linkedin"  # LinkedIn Insight Tag
    CUSTOM = "custom"  # Custom tracking

class EventType(Enum):
    """Pixel event types"""
    PAGE_VIEW = "page_view"
    LEAD_FORM_VIEW = "lead_form_view"
    LEAD_FORM_START = "lead_form_start"
    LEAD_FORM_COMPLETE = "lead_form_complete"
    CONTENT_VIEW = "content_view"
    SEARCH = "search"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"
    CUSTOM = "custom"

@dataclass
class TrackingPixel:
    """Tracking pixel configuration"""
    id: str
    name: str
    provider: PixelProvider
    pixel_id: str
    is_active: bool
    events: List[EventType]
    created_at: datetime
    last_updated: datetime
    configuration: Dict[str, Any]

@dataclass
class VisitorSession:
    """Visitor session tracking"""
    session_id: str
    visitor_id: str
    first_visit: datetime
    last_activity: datetime
    page_views: int
    time_on_site: float
    bounce_rate: float
    conversion_events: List[Dict[str, Any]]
    utm_parameters: Dict[str, str]
    device_info: Dict[str, str]
    referrer: Optional[str]
    landing_page: Optional[str]
    exit_page: Optional[str]

@dataclass
class TrackingEvent:
    """Tracking event record"""
    id: str
    session_id: str
    visitor_id: str
    event_type: EventType
    event_name: str
    event_data: Dict[str, Any]
    timestamp: datetime
    pixel_used: Optional[str]
    conversion_value: Optional[float]
    custom_parameters: Dict[str, str]

@dataclass
class RetargetingAudience:
    """Retargeting audience configuration"""
    id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    pixel_provider: PixelProvider
    audience_size: int
    is_active: bool
    created_at: datetime
    last_updated: datetime

class ShadowTracking:
    """
    Enterprise-grade shadow tracking system
    Manages pixels, cookies, and visitor tracking for retargeting
    """
    
    def __init__(self):
        """Initialize shadow tracking system"""
        self.logger = logging.getLogger(__name__)
        
        # Tracking pixels
        self.pixels: Dict[str, TrackingPixel] = {}
        
        # Visitor sessions
        self.visitor_sessions: Dict[str, VisitorSession] = {}
        
        # Tracking events
        self.tracking_events: List[TrackingEvent] = []
        
        # Retargeting audiences
        self.retargeting_audiences: Dict[str, RetargetingAudience] = {}
        
        # Configuration
        self.tracking_config = self._initialize_tracking_config()
        
        # Initialize default pixels
        self._initialize_default_pixels()
        
        self.logger.info("🔍 Shadow Tracking System initialized")
        self.logger.info(f"📊 Default pixels loaded: {len(self.pixels)}")
        self.logger.info(f"🎯 Retargeting audiences: {len(self.retargeting_audiences)}")
    
    def _initialize_tracking_config(self) -> Dict[str, Any]:
        """Initialize tracking configuration"""
        return {
            'cookie_duration_days': 30,
            'session_timeout_minutes': 30,
            'bounce_rate_threshold': 0.7,
            'conversion_value_currency': 'IDR',
            'pixel_firing_delay_ms': 500,
            'retention_days': 180,
            'gdpr_compliance': True,
            'cookie_consent_required': True,
            'anonymize_ip': True,
            'respect_do_not_track': True
        }
    
    def _initialize_default_pixels(self):
        """Initialize default tracking pixels"""
        default_pixels = [
            TrackingPixel(
                id="meta_pixel",
                name="Facebook Pixel",
                provider=PixelProvider.META,
                pixel_id=os.getenv("META_PIXEL_ID", ""),
                is_active=True,
                events=[EventType.PAGE_VIEW, EventType.LEAD_FORM_VIEW, EventType.LEAD_FORM_COMPLETE, EventType.CUSTOM],
                created_at=datetime.now(),
                last_updated=datetime.now(),
                configuration={
                    "auto_config": True,
                    "advanced_matching": True,
                    "delay_pixel_firing": True
                }
            ),
            TrackingPixel(
                id="google_tag_manager",
                name="Google Tag Manager",
                provider=PixelProvider.GOOGLE,
                pixel_id=os.getenv("GTM_ID", ""),
                is_active=True,
                events=[EventType.PAGE_VIEW, EventType.LEAD_FORM_VIEW, EventType.LEAD_FORM_START, EventType.LEAD_FORM_COMPLETE, EventType.CUSTOM],
                created_at=datetime.now(),
                last_updated=datetime.now(),
                configuration={
                    "data_layer": True,
                    "custom_events": True,
                    "ecommerce": True
                }
            ),
            TrackingPixel(
                id="tiktok_pixel",
                name="TikTok Pixel",
                provider=PixelProvider.TIKTOK,
                pixel_id=os.getenv("TIKTOK_PIXEL_ID", ""),
                is_active=False,  # Optional
                events=[EventType.PAGE_VIEW, EventType.LEAD_FORM_COMPLETE, EventType.CUSTOM],
                created_at=datetime.now(),
                last_updated=datetime.now(),
                configuration={
                    "advanced_matching": True,
                    "automatic_event_matching": True
                }
            )
        ]
        
        for pixel in default_pixels:
            self.pixels[pixel.id] = pixel
    
    def generate_pixel_script(self, pixel_id: str, page_url: str) -> str:
        """
        Generate pixel insertion script for frontend
        
        Args:
            pixel_id: ID of the pixel
            page_url: Current page URL
            
        Returns:
            str: HTML/JavaScript script for pixel insertion
        """
        try:
            pixel = self.pixels.get(pixel_id)
            if not pixel or not pixel.is_active:
                return ""
            
            if pixel.provider == PixelProvider.META:
                return self._generate_meta_pixel_script(pixel, page_url)
            elif pixel.provider == PixelProvider.GOOGLE:
                return self._generate_google_tag_manager_script(pixel, page_url)
            elif pixel.provider == PixelProvider.TIKTOK:
                return self._generate_tiktok_pixel_script(pixel, page_url)
            else:
                return ""
                
        except Exception as e:
            self.logger.error(f"❌ Failed to generate pixel script: {e}")
            return ""
    
    def _generate_meta_pixel_script(self, pixel: TrackingPixel, page_url: str) -> str:
        """Generate Facebook Pixel script"""
        if not pixel.pixel_id:
            return ""
        
        return f"""
<!-- Facebook Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');

fbq('init', '{pixel.pixel_id}');
fbq('track', 'PageView', {{
    page_url: '{page_url}',
    timestamp: new Date().getTime()
}});

// Lead form tracking
document.addEventListener('DOMContentLoaded', function() {{
    const leadForm = document.querySelector('form[data-lead-form="true"]');
    if (leadForm) {{
        // Form view
        fbq('trackCustom', 'LeadFormView', {{
            form_name: leadForm.getAttribute('data-form-name') || 'Unknown',
            page_url: '{page_url}'
        }});
        
        // Form start
        leadForm.addEventListener('focus', function() {{
            fbq('trackCustom', 'LeadFormStart', {{
                form_name: leadForm.getAttribute('data-form-name') || 'Unknown',
                page_url: '{page_url}'
            }});
        }}, {{ once: true }});
        
        // Form complete
        leadForm.addEventListener('submit', function(e) {{
            fbq('trackCustom', 'LeadFormComplete', {{
                form_name: leadForm.getAttribute('data-form-name') || 'Unknown',
                page_url: '{page_url}',
                conversion_value: leadForm.getAttribute('data-conversion-value') || 0
            }});
        }});
    }}
}});
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={pixel.pixel_id}&ev=PageView&noscript=1"
/></noscript>
<!-- End Facebook Pixel Code -->
        """.strip()
    
    def _generate_google_tag_manager_script(self, pixel: TrackingPixel, page_url: str) -> str:
        """Generate Google Tag Manager script"""
        if not pixel.pixel_id:
            return ""
        
        return f"""
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{pixel.pixel_id}');</script>

<!-- Page View Event -->
<script>
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({{
    'event': 'page_view',
    'page_url': '{page_url}',
    'page_title': document.title,
    'timestamp': new Date().getTime()
}});

// Lead Form Tracking
document.addEventListener('DOMContentLoaded', function() {{
    const leadForm = document.querySelector('form[data-lead-form="true"]');
    if (leadForm) {{
        // Form view
        window.dataLayer.push({{
            'event': 'lead_form_view',
            'form_name': leadForm.getAttribute('data-form-name') || 'Unknown',
            'page_url': '{page_url}'
        }});
        
        // Form start
        leadForm.addEventListener('focus', function() {{
            window.dataLayer.push({{
                'event': 'lead_form_start',
                'form_name': leadForm.getAttribute('data-form-name') || 'Unknown',
                'page_url': '{page_url}'
            }});
        }}, {{ once: true }});
        
        // Form complete
        leadForm.addEventListener('submit', function(e) {{
            window.dataLayer.push({{
                'event': 'lead_form_complete',
                'form_name': leadForm.getAttribute('data-form-name') || 'Unknown',
                'page_url': '{page_url}',
                'conversion_value': leadForm.getAttribute('data-conversion-value') || 0
            }});
        }});
    }}
}});
</script>
<!-- End Google Tag Manager -->
        """.strip()
    
    def _generate_tiktok_pixel_script(self, pixel: TrackingPixel, page_url: str) -> str:
        """Generate TikTok Pixel script"""
        if not pixel.pixel_id:
            return ""
        
        return f"""
<!-- TikTok Pixel -->
<script>
!function (w, d, t) {{
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify"],ttq.setAndDefer=function(t,e){{t[e]=function(){{ttq.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}};
  for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){{for(var e=ttq._i[t]||[],n=0;n<e.length;n++)ttq.setAndDefer(e,n,t)}};ttq.load=function(e,n){{var i="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{{}},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{{}},ttq._t[e]=!0,ttq._t[e]._c=i,ttq._t[e]._p=i;var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src=i+"?sdkid="+e;var o=document.getElementsByTagName("script")[0];o.parentNode.insertBefore(n,o)};ttq.load('{pixel.pixel_id}');ttq.page();
}}(window, document, 'ttq');

// Lead Form Tracking
document.addEventListener('DOMContentLoaded', function() {{
    const leadForm = document.querySelector('form[data-lead-form="true"]');
    if (leadForm) {{
        // Form view
        ttq.track('ViewContent', {{
            content_type: 'lead_form',
            content_name: leadForm.getAttribute('data-form-name') || 'Unknown',
            page_url: '{page_url}'
        }});
        
        // Form start
        leadForm.addEventListener('focus', function() {{
            ttq.track('SubmitForm', {{
                content_type: 'lead_form',
                content_name: leadForm.getAttribute('data-form-name') || 'Unknown',
                page_url: '{page_url}'
            }});
        }}, {{ once: true }});
        
        // Form complete
        leadForm.addEventListener('submit', function(e) {{
            ttq.track('CompletePayment', {{
                content_type: 'lead_form',
                content_name: leadForm.getAttribute('data-form-name') || 'Unknown',
                page_url: '{page_url}',
                value: leadForm.getAttribute('data-conversion-value') || 0,
                currency: 'IDR'
            }});
        }});
    }}
}});
</script>
<!-- End TikTok Pixel -->
        """.strip()
    
    def generate_visitor_tracking_script(self, session_id: str) -> str:
        """
        Generate visitor tracking script
        
        Args:
            session_id: Visitor session ID
            
        Returns:
            str: JavaScript script for visitor tracking
        """
        return f"""
<!-- Visitor Tracking Script -->
<script>
(function() {{
    const sessionId = '{session_id}';
    const trackingConfig = {{
        sessionTimeout: {self.tracking_config['session_timeout_minutes'] * 60000},
        bounceRateThreshold: {self.tracking_config['bounce_rate_threshold']},
        anonymizeIP: {str(self.tracking_config['anonymize_ip']).lower()}
    }};
    
    // Track page views
    function trackPageView(pageUrl, pageTitle) {{
        const eventData = {{
            session_id: sessionId,
            event_type: 'page_view',
            page_url: pageUrl,
            page_title: pageTitle,
            timestamp: new Date().toISOString(),
            referrer: document.referrer,
            user_agent: navigator.userAgent,
            screen_resolution: screen.width + 'x' + screen.height,
            viewport_size: window.innerWidth + 'x' + window.innerHeight
        }};
        
        // Send to tracking endpoint
        fetch('/api/tracking/track', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify(eventData)
        }}).catch(console.error);
    }}
    
    // Track form interactions
    function trackFormInteraction(formName, interactionType, formData) {{
        const eventData = {{
            session_id: sessionId,
            event_type: 'form_interaction',
            form_name: formName,
            interaction_type: interactionType,
            form_data: formData,
            timestamp: new Date().toISOString(),
            page_url: window.location.href
        }};
        
        // Send to tracking endpoint
        fetch('/api/tracking/track', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify(eventData)
        }}).catch(console.error);
    }}
    
    // Track scroll depth
    function trackScrollDepth() {{
        const maxScroll = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.offsetHeight,
            document.documentElement.scrollHeight
        );
        
        const scrollPercent = Math.round((window.scrollY / maxScroll) * 100);
        
        const eventData = {{
            session_id: sessionId,
            event_type: 'scroll_depth',
            scroll_percent: scrollPercent,
            timestamp: new Date().toISOString(),
            page_url: window.location.href
        }};
        
        // Send to tracking endpoint
        fetch('/api/tracking/track', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify(eventData)
        }}).catch(console.error);
    }}
    
    // Initialize tracking
    document.addEventListener('DOMContentLoaded', function() {{
        // Track initial page view
        trackPageView(window.location.href, document.title);
        
        // Track form interactions
        const forms = document.querySelectorAll('form[data-lead-form="true"]');
        forms.forEach(function(form) {{
            const formName = form.getAttribute('data-form-name') || 'Unknown';
            
            // Form view
            trackFormInteraction(formName, 'view', {{}});
            
            // Form focus (start)
            form.addEventListener('focus', function(e) {{
                trackFormInteraction(formName, 'start', {{}});
            }}, {{ once: true }});
            
            // Form submit (complete)
            form.addEventListener('submit', function(e) {{
                const formData = new FormData(form);
                const formDataObj = {{}};
                for (let [key, value] of formData.entries()) {{
                    formDataObj[key] = value;
                }}
                trackFormInteraction(formName, 'complete', formDataObj);
            }});
        }});
        
        // Track scroll depth
        let scrollTracked = false;
        window.addEventListener('scroll', function() {{
            if (!scrollTracked) {{
                setTimeout(trackScrollDepth, 1000);
                scrollTracked = true;
            }}
        }});
        
        // Track page unload
        window.addEventListener('beforeunload', function() {{
            const eventData = {{
                session_id: sessionId,
                event_type: 'page_unload',
                time_on_page: Date.now() - performance.timing.navigationStart,
                timestamp: new Date().toISOString(),
                page_url: window.location.href
            }};
            
            // Use sendBeacon for reliable delivery
            if (navigator.sendBeacon) {{
                navigator.sendBeacon('/api/tracking/track', JSON.stringify(eventData));
            }}
        }});
    }});
}})();
</script>
<!-- End Visitor Tracking Script -->
        """.strip()
    
    def create_retargeting_audience(self, name: str, description: str, 
                                  criteria: Dict[str, Any], 
                                  pixel_provider: PixelProvider) -> str:
        """
        Create retargeting audience
        
        Args:
            name: Audience name
            description: Audience description
            criteria: Audience criteria
            pixel_provider: Pixel provider for this audience
            
        Returns:
            str: Audience ID
        """
        try:
            audience_id = f"audience_{int(datetime.now().timestamp() * 1000000)}"
            
            audience = RetargetingAudience(
                id=audience_id,
                name=name,
                description=description,
                criteria=criteria,
                pixel_provider=pixel_provider,
                audience_size=0,  # Will be calculated
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
            
            self.retargeting_audiences[audience_id] = audience
            
            self.logger.info(f"🎯 Retargeting audience created: {audience_id}")
            self.logger.info(f"📝 Name: {name}, Provider: {pixel_provider.value}")
            
            return audience_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create retargeting audience: {e}")
            return ""
    
    def generate_audience_criteria(self, audience_type: str) -> Dict[str, Any]:
        """
        Generate audience criteria for common retargeting scenarios
        
        Args:
            audience_type: Type of audience
            
        Returns:
            Dict with audience criteria
        """
        criteria_templates = {
            "form_viewers": {
                "events": ["LeadFormView"],
                "time_range": "30d",
                "min_interactions": 1,
                "exclude_converted": True
            },
            "form_starters": {
                "events": ["LeadFormStart"],
                "time_range": "30d",
                "min_interactions": 1,
                "exclude_converted": True
            },
            "page_visitors": {
                "events": ["PageView"],
                "time_range": "7d",
                "min_page_views": 2,
                "exclude_converted": True
            },
            "high_intent": {
                "events": ["LeadFormView", "LeadFormStart"],
                "time_range": "14d",
                "min_interactions": 2,
                "exclude_converted": True
            },
            "bounce_visitors": {
                "events": ["PageView"],
                "time_range": "1d",
                "max_page_views": 1,
                "exclude_converted": True
            },
            "engaged_visitors": {
                "events": ["PageView"],
                "time_range": "7d",
                "min_page_views": 3,
                "min_time_on_site": 60,
                "exclude_converted": True
            }
        }
        
        return criteria_templates.get(audience_type, {})
    
    def get_tracking_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get tracking analytics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dict with tracking analytics
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Filter recent events
            recent_events = [e for e in self.tracking_events if e.timestamp >= cutoff_date]
            
            # Calculate metrics
            total_sessions = len(self.visitor_sessions)
            total_events = len(recent_events)
            unique_visitors = len(set(s.visitor_id for s in self.visitor_sessions.values()))
            
            # Event breakdown
            event_breakdown = {}
            for event in recent_events:
                event_type = event.event_type.value
                event_breakdown[event_type] = event_breakdown.get(event_type, 0) + 1
            
            # Conversion metrics
            conversion_events = [e for e in recent_events if e.event_type in [EventType.LEAD_FORM_COMPLETE]]
            conversion_rate = (len(conversion_events) / unique_visitors * 100) if unique_visitors > 0 else 0
            
            # Bounce rate
            bounce_sessions = [s for s in self.visitor_sessions.values() if s.page_views <= 1]
            bounce_rate = (len(bounce_sessions) / total_sessions * 100) if total_sessions > 0 else 0
            
            # Pixel performance
            pixel_performance = {}
            for pixel_id, pixel in self.pixels.items():
                pixel_events = [e for e in recent_events if e.pixel_used == pixel_id]
                pixel_performance[pixel_id] = {
                    'name': pixel.name,
                    'provider': pixel.provider.value,
                    'events': len(pixel_events),
                    'conversions': len([e for e in pixel_events if e.event_type == EventType.LEAD_FORM_COMPLETE])
                }
            
            return {
                'period_days': days,
                'total_sessions': total_sessions,
                'unique_visitors': unique_visitors,
                'total_events': total_events,
                'conversion_rate': conversion_rate,
                'bounce_rate': bounce_rate,
                'event_breakdown': event_breakdown,
                'pixel_performance': pixel_performance,
                'active_pixels': len([p for p in self.pixels.values() if p.is_active]),
                'retargeting_audiences': len(self.retargeting_audiences)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get tracking analytics: {e}")
            return {}
    
    def generate_pixel_config_for_frontend(self) -> Dict[str, Any]:
        """
        Generate pixel configuration for frontend consumption
        
        Returns:
            Dict with pixel configuration
        """
        try:
            config = {
                "tracking_enabled": True,
                "pixels": [],
                "tracking_config": self.tracking_config,
                "retargeting_audiences": []
            }
            
            # Add active pixels
            for pixel in self.pixels.values():
                if pixel.is_active:
                    config["pixels"].append({
                        "id": pixel.id,
                        "name": pixel.name,
                        "provider": pixel.provider.value,
                        "pixel_id": pixel.pixel_id,
                        "events": [e.value for e in pixel.events],
                        "configuration": pixel.configuration
                    })
            
            # Add retargeting audiences
            for audience in self.retargeting_audiences.values():
                if audience.is_active:
                    config["retargeting_audiences"].append({
                        "id": audience.id,
                        "name": audience.name,
                        "description": audience.description,
                        "criteria": audience.criteria,
                        "pixel_provider": audience.pixel_provider.value,
                        "audience_size": audience.audience_size
                    })
            
            return config
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate pixel config: {e}")
            return {}
    
    def add_pixel(self, pixel_id: str, name: str, provider: PixelProvider, 
                  pixel_code: str, events: List[EventType]) -> bool:
        """
        Add new tracking pixel
        
        Args:
            pixel_id: Internal pixel ID
            name: Pixel name
            provider: Pixel provider
            pixel_code: Provider-specific pixel ID/code
            events: Events to track
            
        Returns:
            bool: True if added successfully
        """
        try:
            pixel = TrackingPixel(
                id=pixel_id,
                name=name,
                provider=provider,
                pixel_id=pixel_code,
                is_active=True,
                events=events,
                created_at=datetime.now(),
                last_updated=datetime.now(),
                configuration={}
            )
            
            self.pixels[pixel_id] = pixel
            
            self.logger.info(f"📊 Pixel added: {pixel_id} - {name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add pixel: {e}")
            return False
    
    def update_pixel_status(self, pixel_id: str, is_active: bool) -> bool:
        """
        Update pixel active status
        
        Args:
            pixel_id: Pixel ID
            is_active: Active status
            
        Returns:
            bool: True if updated successfully
        """
        try:
            if pixel_id in self.pixels:
                self.pixels[pixel_id].is_active = is_active
                self.pixels[pixel_id].last_updated = datetime.now()
                
                self.logger.info(f"📊 Pixel status updated: {pixel_id} -> {'Active' if is_active else 'Inactive'}")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update pixel status: {e}")
            return False

# Global shadow tracking instance
shadow_tracking = ShadowTracking()
