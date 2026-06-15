"""
Timezone Module
Multi-timezone support for Asia markets
"""

from typing import Dict, Optional, List
from datetime import datetime, timezone, timedelta
import pytz


class TimezoneManager:
    """Timezone management utilities for Asia markets"""
    
    # Supported timezones for Asia expansion
    SUPPORTED_TIMEZONES = {
        "Asia/Jakarta": {
            "name": "Indonesia Western Time (WIB)",
            "country": "Indonesia",
            "offset": "+07:00",
            "utc_offset_hours": 7
        },
        "Asia/Makassar": {
            "name": "Indonesia Central Time (WITA)",
            "country": "Indonesia",
            "offset": "+08:00",
            "utc_offset_hours": 8
        },
        "Asia/Jayapura": {
            "name": "Indonesia Eastern Time (WIT)",
            "country": "Indonesia",
            "offset": "+09:00",
            "utc_offset_hours": 9
        },
        "Asia/Singapore": {
            "name": "Singapore Time",
            "country": "Singapore",
            "offset": "+08:00",
            "utc_offset_hours": 8
        },
        "Asia/Kuala_Lumpur": {
            "name": "Malaysia Time",
            "country": "Malaysia",
            "offset": "+08:00",
            "utc_offset_hours": 8
        },
        "Asia/Bangkok": {
            "name": "Indochina Time",
            "country": "Thailand",
            "offset": "+07:00",
            "utc_offset_hours": 7
        },
        "Asia/Ho_Chi_Minh": {
            "name": "Indochina Time",
            "country": "Vietnam",
            "offset": "+07:00",
            "utc_offset_hours": 7
        },
        "Asia/Manila": {
            "name": "Philippine Time",
            "country": "Philippines",
            "offset": "+08:00",
            "utc_offset_hours": 8
        },
        "UTC": {
            "name": "Coordinated Universal Time",
            "country": "Universal",
            "offset": "+00:00",
            "utc_offset_hours": 0
        },
    }
    
    @classmethod
    def convert_timezone(cls, dt: datetime, from_tz: str, to_tz: str) -> datetime:
        """
        Convert datetime from one timezone to another
        
        Args:
            dt: Datetime to convert
            from_tz: Source timezone (e.g., "Asia/Jakarta")
            to_tz: Target timezone (e.g., "Asia/Singapore")
            
        Returns:
            Converted datetime
        """
        if from_tz not in cls.SUPPORTED_TIMEZONES:
            raise ValueError(f"Unsupported timezone: {from_tz}")
        
        if to_tz not in cls.SUPPORTED_TIMEZONES:
            raise ValueError(f"Unsupported timezone: {to_tz}")
        
        # If datetime is naive, assume it's in the source timezone
        if dt.tzinfo is None:
            source_tz = pytz.timezone(from_tz)
            dt = source_tz.localize(dt)
        
        # Convert to target timezone
        target_tz = pytz.timezone(to_tz)
        converted_dt = dt.astimezone(target_tz)
        
        return converted_dt
    
    @classmethod
    def get_current_time(cls, tz: str) -> datetime:
        """
        Get current time in specific timezone
        
        Args:
            tz: Timezone identifier
            
        Returns:
            Current datetime in specified timezone
        """
        if tz not in cls.SUPPORTED_TIMEZONES:
            raise ValueError(f"Unsupported timezone: {tz}")
        
        target_tz = pytz.timezone(tz)
        return datetime.now(target_tz)
    
    @classmethod
    def get_offset(cls, tz: str) -> str:
        """
        Get UTC offset for timezone
        
        Args:
            tz: Timezone identifier
            
        Returns:
            UTC offset string (e.g., "+07:00")
        """
        if tz not in cls.SUPPORTED_TIMEZONES:
            raise ValueError(f"Unsupported timezone: {tz}")
        
        return cls.SUPPORTED_TIMEZONES[tz]["offset"]
    
    @classmethod
    def get_supported_timezones(cls) -> Dict[str, Dict]:
        """
        Get all supported timezones with metadata
        
        Returns:
            Dictionary of timezone information
        """
        return cls.SUPPORTED_TIMEZONES
    
    @classmethod
    def get_timezones_by_country(cls, country: str) -> List[str]:
        """
        Get timezones for a specific country
        
        Args:
            country: Country name
            
        Returns:
            List of timezone identifiers
        """
        return [
            tz for tz, info in cls.SUPPORTED_TIMEZONES.items()
            if info["country"].lower() == country.lower()
        ]
    
    @classmethod
    def format_datetime(cls, dt: datetime, tz: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime in specific timezone
        
        Args:
            dt: Datetime to format
            tz: Target timezone
            format: Format string
            
        Returns:
            Formatted datetime string
        """
        if dt.tzinfo is None:
            # Assume UTC if naive
            dt = pytz.UTC.localize(dt)
        
        target_tz = pytz.timezone(tz)
        localized_dt = dt.astimezone(target_tz)
        
        return localized_dt.strftime(format)
    
    @classmethod
    def is_business_hours(cls, dt: datetime, tz: str) -> bool:
        """
        Check if datetime is within business hours (9 AM - 6 PM)
        
        Args:
            dt: Datetime to check
            tz: Timezone to check in
            
        Returns:
            True if within business hours
        """
        if dt.tzinfo is None:
            target_tz = pytz.timezone(tz)
            dt = target_tz.localize(dt)
        else:
            dt = dt.astimezone(pytz.timezone(tz))
        
        # Business hours: 9 AM to 6 PM, Monday to Friday
        hour = dt.hour
        weekday = dt.weekday()  # 0 = Monday, 6 = Sunday
        
        return 9 <= hour < 18 and weekday < 5


class TimezoneFormatter:
    """Timezone formatting utilities"""
    
    @staticmethod
    def format_relative(dt: datetime, tz: str) -> str:
        """
        Format datetime as relative time (e.g., "2 hours ago")
        
        Args:
            dt: Datetime to format
            tz: Timezone for comparison
            
        Returns:
            Relative time string
        """
        from core_modules.timezone import TimezoneManager
        
        now = TimezoneManager.get_current_time(tz)
        
        if dt.tzinfo is None:
            target_tz = pytz.timezone(tz)
            dt = target_tz.localize(dt)
        else:
            dt = dt.astimezone(pytz.timezone(tz))
        
        diff = now - dt
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
    
    @staticmethod
    def format_with_timezone(dt: datetime, tz: str, format: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
        """
        Format datetime with timezone abbreviation
        
        Args:
            dt: Datetime to format
            tz: Target timezone
            format: Format string
            
        Returns:
            Formatted datetime with timezone
        """
        from core_modules.timezone import TimezoneManager
        
        return TimezoneManager.format_datetime(dt, tz, format)


# Singleton instance
_timezone_manager_instance: Optional[TimezoneManager] = None


def get_timezone_manager() -> TimezoneManager:
    """Get or create timezone manager instance"""
    global _timezone_manager_instance
    
    if _timezone_manager_instance is None:
        _timezone_manager_instance = TimezoneManager()
    
    return _timezone_manager_instance
