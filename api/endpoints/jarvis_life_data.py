"""
JARVIS Life Data API Endpoints
==============================

API endpoints to receive life data from Mobile APK:
- Calendar events
- Geolocation
- Local weather

This data is used for proactive assistance and conflict detection.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/jarvis-life", tags=["jarvis-life-data"])

# ============================================================================
# Data Models
# ============================================================================

class EventType(str, Enum):
    """Event types for calendar events"""
    MEETING = "meeting"
    APPOINTMENT = "appointment"
    REMINDER = "reminder"
    TRAVEL = "travel"
    WORK = "work"
    PERSONAL = "personal"
    OTHER = "other"

class CalendarEvent(BaseModel):
    """Calendar event model"""
    id: str
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    event_type: EventType = EventType.OTHER
    attendees: Optional[List[str]] = None
    is_all_day: bool = False
    reminder_minutes: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GeolocationData(BaseModel):
    """Geolocation data model"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy: Optional[float] = Field(None, ge=0)
    altitude: Optional[float] = None
    speed: Optional[float] = Field(None, ge=0)
    heading: Optional[float] = Field(None, ge=0, le=360)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class WeatherData(BaseModel):
    """Weather data model"""
    temperature: float  # Celsius
    humidity: Optional[float] = Field(None, ge=0, le=100)
    wind_speed: Optional[float] = Field(None, ge=0)
    wind_direction: Optional[float] = Field(None, ge=0, le=360)
    condition: str  # e.g., "sunny", "rainy", "cloudy"
    visibility: Optional[float] = Field(None, ge=0)
    pressure: Optional[float] = Field(None, ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None

class LifeDataPayload(BaseModel):
    """Complete life data payload from mobile app"""
    user_id: str
    device_id: str
    calendar_events: List[CalendarEvent] = []
    geolocation: Optional[GeolocationData] = None
    weather: Optional[WeatherData] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ConflictAlert(BaseModel):
    """Conflict alert model"""
    alert_type: str
    severity: str  # "low", "medium", "high", "critical"
    message: str
    suggested_actions: List[str]
    affected_events: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# In-Memory Storage (Replace with database in production)
# ============================================================================

# Store life data (user_id -> data)
life_data_store: Dict[str, Dict[str, Any]] = {}

# Store conflict alerts
conflict_alerts: List[ConflictAlert] = []

# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/sync")
async def sync_life_data(
    payload: LifeDataPayload,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Receive and sync life data from mobile app.
    
    This endpoint receives calendar events, geolocation, and weather data
    from the mobile app and stores it for proactive analysis.
    """
    try:
        # Verify service token (implement your verification logic)
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        # Store life data
        life_data_store[payload.user_id] = {
            'calendar_events': [event.dict() for event in payload.calendar_events],
            'geolocation': payload.geolocation.dict() if payload.geolocation else None,
            'weather': payload.weather.dict() if payload.weather else None,
            'timestamp': payload.timestamp.isoformat(),
            'device_id': payload.device_id,
        }
        
        # Run proactive analysis
        alerts = await analyze_life_data(payload)
        
        # Store alerts
        conflict_alerts.extend(alerts)
        
        logger.info(f"✅ Life data synced for user {payload.user_id}")
        
        return {
            'success': True,
            'message': 'Life data synced successfully',
            'alerts_generated': len(alerts),
            'alerts': alerts,
        }
    
    except Exception as e:
        logger.error(f"❌ Error syncing life data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{user_id}")
async def get_calendar_events(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Get calendar events for a user within a date range.
    """
    try:
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        if user_id not in life_data_store:
            return {'events': []}
        
        events = life_data_store[user_id]['calendar_events']
        
        # Filter by date range if provided
        if start_date or end_date:
            filtered_events = []
            for event in events:
                event_start = datetime.fromisoformat(event['start_time'])
                if start_date and event_start < start_date:
                    continue
                if end_date and event_start > end_date:
                    continue
                filtered_events.append(event)
            events = filtered_events
        
        return {'events': events}
    
    except Exception as e:
        logger.error(f"❌ Error getting calendar events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/location/{user_id}")
async def get_current_location(
    user_id: str,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Get current geolocation for a user.
    """
    try:
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        if user_id not in life_data_store:
            raise HTTPException(status_code=404, detail="User data not found")
        
        return life_data_store[user_id].get('geolocation', None)
    
    except Exception as e:
        logger.error(f"❌ Error getting location: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/{user_id}")
async def get_current_weather(
    user_id: str,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Get current weather for a user.
    """
    try:
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        if user_id not in life_data_store:
            raise HTTPException(status_code=404, detail="User data not found")
        
        return life_data_store[user_id].get('weather', None)
    
    except Exception as e:
        logger.error(f"❌ Error getting weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts/{user_id}")
async def get_conflict_alerts(
    user_id: str,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Get conflict alerts for a user.
    """
    try:
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        user_alerts = [alert for alert in conflict_alerts if alert.get('user_id') == user_id]
        
        return {'alerts': user_alerts}
    
    except Exception as e:
        logger.error(f"❌ Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/alerts/{alert_id}")
async def clear_alert(
    alert_id: str,
    x_service_token: str = Header(..., alias="X-Jarvis-Service-Token")
):
    """
    Clear a specific alert.
    """
    try:
        if not verify_service_token(x_service_token):
            raise HTTPException(status_code=403, detail="Invalid service token")
        
        global conflict_alerts
        conflict_alerts = [alert for alert in conflict_alerts if alert.get('id') != alert_id]
        
        return {'success': True, 'message': 'Alert cleared'}
    
    except Exception as e:
        logger.error(f"❌ Error clearing alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Analysis Functions
# ============================================================================

async def analyze_life_data(payload: LifeDataPayload) -> List[ConflictAlert]:
    """
    Analyze life data for conflicts and proactive alerts.
    """
    alerts = []
    
    # Analyze calendar conflicts
    calendar_alerts = await analyze_calendar_conflicts(payload)
    alerts.extend(calendar_alerts)
    
    # Analyze location-based conflicts
    location_alerts = await analyze_location_conflicts(payload)
    alerts.extend(location_alerts)
    
    # Analyze weather-based conflicts
    weather_alerts = await analyze_weather_conflicts(payload)
    alerts.extend(weather_alerts)
    
    # Send proactive notifications for high-severity alerts
    for alert in alerts:
        if alert.severity in ['high', 'critical']:
            await send_proactive_notification(payload.user_id, alert)
    
    return alerts

async def analyze_calendar_conflicts(payload: LifeDataPayload) -> List[ConflictAlert]:
    """
    Analyze calendar events for conflicts.
    """
    alerts = []
    events = payload.calendar_events
    
    # Check for overlapping events
    for i, event1 in enumerate(events):
        for event2 in events[i+1:]:
            if events_overlap(event1, event2):
                alert = ConflictAlert(
                    alert_type="calendar_conflict",
                    severity="high",
                    message=f"Calendar conflict: '{event1.title}' overlaps with '{event2.title}'",
                    suggested_actions=[
                        f"Reschedule '{event1.title}' to a different time",
                        f"Reschedule '{event2.title}' to a different time",
                        "Decline one of the events",
                    ],
                    affected_events=[event1.id, event2.id],
                )
                alerts.append(alert)
    
    # Check for back-to-back events with travel time
    for i, event1 in enumerate(events[:-1]):
        event2 = events[i+1]
        travel_time_needed = estimate_travel_time(event1.location, event2.location)
        time_between = (event2.start_time - event1.end_time).total_seconds() / 60
        
        if time_between < travel_time_needed:
            alert = ConflictAlert(
                alert_type="travel_time_conflict",
                severity="medium",
                message=f"Insufficient travel time between '{event1.title}' and '{event2.title}'",
                suggested_actions=[
                    f"Add {travel_time_needed - time_between} minutes buffer between events",
                    "Consider virtual attendance for one event",
                    "Reschedule to allow travel time",
                ],
                affected_events=[event1.id, event2.id],
            )
            alerts.append(alert)
    
    return alerts

async def analyze_location_conflicts(payload: LifeDataPayload) -> List[ConflictAlert]:
    """
    Analyze geolocation for location-based conflicts.
    """
    alerts = []
    
    if not payload.geolocation:
        return alerts
    
    current_location = payload.geolocation
    
    # Check if user can reach upcoming events on time
    for event in payload.calendar_events:
        if event.location and event.start_time > datetime.utcnow():
            travel_time = estimate_travel_time_from_coords(
                current_location.latitude,
                current_location.longitude,
                event.location
            )
            time_available = (event.start_time - datetime.utcnow()).total_seconds() / 60
            
            if time_available < travel_time:
                alert = ConflictAlert(
                    alert_type="location_conflict",
                    severity="high",
                    message=f"Cannot reach '{event.title}' on time from current location",
                    suggested_actions=[
                        "Leave immediately",
                        "Request to join virtually",
                        "Reschedule the event",
                        "Request a later start time",
                    ],
                    affected_events=[event.id],
                )
                alerts.append(alert)
    
    return alerts

async def analyze_weather_conflicts(payload: LifeDataPayload) -> List[ConflictAlert]:
    """
    Analyze weather for weather-based conflicts.
    """
    alerts = []
    
    if not payload.weather:
        return alerts
    
    weather = payload.weather
    
    # Check for weather conditions affecting outdoor events
    for event in payload.calendar_events:
        if event.location and is_outdoor_event(event):
            if weather.condition in ['rainy', 'stormy', 'snowy']:
                alert = ConflictAlert(
                    alert_type="weather_conflict",
                    severity="medium",
                    message=f"Weather alert for '{event.title}': {weather.condition} conditions expected",
                    suggested_actions=[
                        "Move event indoors",
                        "Reschedule for better weather",
                        "Prepare rain gear/umbrella",
                        "Request virtual attendance",
                    ],
                    affected_events=[event.id],
                )
                alerts.append(alert)
            
            # Check for extreme temperatures
            if weather.temperature > 35 or weather.temperature < 0:
                alert = ConflictAlert(
                    alert_type="extreme_temperature",
                    severity="medium",
                    message=f"Extreme temperature alert for '{event.title}': {weather.temperature}°C",
                    suggested_actions=[
                        "Stay hydrated if hot",
                        "Dress appropriately",
                        "Consider rescheduling if outdoor",
                    ],
                    affected_events=[event.id],
                )
                alerts.append(alert)
    
    return alerts

async def send_proactive_notification(user_id: str, alert: ConflictAlert):
    """
    Send proactive notification to user via WhatsApp.
    """
    try:
        # Import notification service
        import sys
        sys.path.append('./jarvis/channels')
        from hub import JarvisCommunicationHub
        
        hub = JarvisCommunicationHub()
        
        # Build notification message
        message = f"""
🚨 JARVIS Proactive Alert
========================

**Alert Type:** {alert.alert_type}
**Severity:** {alert.severity.upper()}

**Message:**
{alert.message}

**Suggested Actions:**
"""
        for i, action in enumerate(alert.suggested_actions, 1):
            message += f"{i}. {action}\n"
        
        message += f"""
**Affected Events:**
{', '.join(alert.affected_events)}

**Timestamp:** {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

This is an automated proactive alert from JARVIS.
"""
        
        # Get user's WhatsApp number from database (implement this)
        user_phone = get_user_phone_number(user_id)
        
        if user_phone:
            await hub.whatsapp.sendMessage(user_phone, message)
            logger.info(f"📢 Proactive notification sent to {user_id}")
        else:
            logger.warning(f"No phone number found for user {user_id}")
    
    except Exception as e:
        logger.error(f"Failed to send proactive notification: {e}")

# ============================================================================
# Helper Functions
# ============================================================================

def verify_service_token(token: str) -> bool:
    """
    Verify service token (implement your verification logic).
    """
    # For now, accept any token - implement proper verification
    return True

def events_overlap(event1: CalendarEvent, event2: CalendarEvent) -> bool:
    """
    Check if two events overlap in time.
    """
    return (
        event1.start_time < event2.end_time and
        event1.end_time > event2.start_time
    )

def estimate_travel_time(location1: Optional[str], location2: Optional[str]) -> int:
    """
    Estimate travel time between two locations (in minutes).
    This is a simplified version - use Google Maps API in production.
    """
    if not location1 or not location2:
        return 30  # Default 30 minutes
    
    # Simplified logic - in production, use Google Maps Distance Matrix API
    if location1 == location2:
        return 0
    
    # Random estimate between 15-60 minutes
    import random
    return random.randint(15, 60)

def estimate_travel_time_from_coords(lat1: float, lon1: float, location2: str) -> int:
    """
    Estimate travel time from coordinates to location.
    """
    # Simplified - use Google Maps API in production
    import random
    return random.randint(20, 90)

def is_outdoor_event(event: CalendarEvent) -> bool:
    """
    Determine if an event is likely outdoor.
    """
    outdoor_keywords = ['park', 'beach', 'hiking', 'outdoor', 'garden', 'stadium', 'field']
    
    if event.location:
        return any(keyword in event.location.lower() for keyword in outdoor_keywords)
    
    if event.description:
        return any(keyword in event.description.lower() for keyword in outdoor_keywords)
    
    return False

def get_user_phone_number(user_id: str) -> Optional[str]:
    """
    Get user's phone number from database.
    Implement this based on your user management system.
    """
    # Placeholder - implement proper lookup
    return None
