"""
Timezone API
Endpoints for multi-timezone support for Asia markets
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/timezone", tags=["Timezone"])


class ConvertTimezoneRequest(BaseModel):
    datetime: str  # ISO format datetime
    from_timezone: str
    to_timezone: str


class FormatTimezoneRequest(BaseModel):
    datetime: str  # ISO format datetime
    timezone: str
    format: Optional[str] = "%Y-%m-%d %H:%M:%S"


@router.get("/supported")
async def get_supported_timezones():
    """
    Get all supported timezones
    """
    from core_modules.timezone import TimezoneManager
    
    timezones = TimezoneManager.get_supported_timezones()
    
    return {
        "timezones": timezones,
        "count": len(timezones)
    }


@router.get("/current/{timezone}")
async def get_current_time(timezone: str):
    """
    Get current time in specific timezone
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        current_time = TimezoneManager.get_current_time(timezone)
        
        return {
            "timezone": timezone,
            "current_time": current_time.isoformat(),
            "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/convert")
async def convert_timezone(request: ConvertTimezoneRequest):
    """
    Convert datetime from one timezone to another
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        dt = datetime.fromisoformat(request.datetime)
        converted_dt = TimezoneManager.convert_timezone(
            dt,
            request.from_timezone,
            request.to_timezone
        )
        
        return {
            "original_datetime": request.datetime,
            "original_timezone": request.from_timezone,
            "converted_datetime": converted_dt.isoformat(),
            "target_timezone": request.to_timezone,
            "formatted": converted_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/format")
async def format_timezone(request: FormatTimezoneRequest):
    """
    Format datetime in specific timezone
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        dt = datetime.fromisoformat(request.datetime)
        formatted = TimezoneManager.format_datetime(
            dt,
            request.timezone,
            request.format
        )
        
        return {
            "datetime": request.datetime,
            "timezone": request.timezone,
            "formatted": formatted
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/offset/{timezone}")
async def get_timezone_offset(timezone: str):
    """
    Get UTC offset for timezone
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        offset = TimezoneManager.get_offset(timezone)
        
        return {
            "timezone": timezone,
            "utc_offset": offset
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/country/{country}")
async def get_timezones_by_country(country: str):
    """
    Get timezones for a specific country
    """
    from core_modules.timezone import TimezoneManager
    
    timezones = TimezoneManager.get_timezones_by_country(country)
    
    return {
        "country": country,
        "timezones": timezones
    }


@router.post("/business-hours")
async def check_business_hours(datetime: str, timezone: str):
    """
    Check if datetime is within business hours (9 AM - 6 PM)
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        dt = datetime.fromisoformat(datetime)
        is_business = TimezoneManager.is_business_hours(dt, timezone)
        
        return {
            "datetime": datetime,
            "timezone": timezone,
            "is_business_hours": is_business
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/relative")
async def format_relative_time(datetime: str, timezone: str):
    """
    Format datetime as relative time (e.g., "2 hours ago")
    """
    from core_modules.timezone import TimezoneFormatter
    
    try:
        dt = datetime.fromisoformat(datetime)
        relative = TimezoneFormatter.format_relative(dt, timezone)
        
        return {
            "datetime": datetime,
            "timezone": timezone,
            "relative": relative
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare")
async def compare_timezones(datetime: str, timezones: List[str]):
    """
    Compare datetime across multiple timezones
    """
    from core_modules.timezone import TimezoneManager
    
    try:
        dt = datetime.fromisoformat(datetime)
        results = []
        
        for tz in timezones:
            try:
                converted = TimezoneManager.convert_timezone("UTC", tz, dt)
                formatted = converted.strftime("%Y-%m-%d %H:%M:%S %Z")
                
                results.append({
                    "timezone": tz,
                    "datetime": converted.isoformat(),
                    "formatted": formatted
                })
            except ValueError:
                continue
        
        return {
            "base_datetime": datetime,
            "comparisons": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
