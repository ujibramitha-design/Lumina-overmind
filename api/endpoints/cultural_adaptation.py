"""
Cultural Adaptation API
Endpoints for RTL support, Cyrillic support, and cultural adaptations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix="/cultural", tags=["Cultural Adaptation"])


class FormatNumberRequest(BaseModel):
    number: float
    language: str


class DetectScriptRequest(BaseModel):
    text: str


@router.get("/languages")
async def get_supported_languages():
    """
    Get all supported languages with metadata
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    languages = CulturalAdapter.get_supported_languages()
    
    return {
        "languages": languages,
        "count": len(languages)
    }


@router.get("/languages/{language}")
async def get_language_info(language: str):
    """
    Get information for a specific language
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    languages = CulturalAdapter.get_supported_languages()
    
    if language not in languages:
        raise HTTPException(status_code=404, detail=f"Language not found: {language}")
    
    return {
        "language": language,
        "info": languages[language]
    }


@router.get("/direction/{language}")
async def get_text_direction(language: str):
    """
    Get text direction for language (LTR or RTL)
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    direction = CulturalAdapter.get_direction(language)
    is_rtl = CulturalAdapter.is_rtl(language)
    
    return {
        "language": language,
        "direction": direction,
        "is_rtl": is_rtl
    }


@router.get("/script/{language}")
async def get_script_type(language: str):
    """
    Get script type for language
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    script = CulturalAdapter.get_script(language)
    
    return {
        "language": language,
        "script": script
    }


@router.get("/languages/direction/{direction}")
async def get_languages_by_direction(direction: str):
    """
    Get languages by text direction
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    if direction not in ["LTR", "RTL"]:
        raise HTTPException(status_code=400, detail="Direction must be 'LTR' or 'RTL'")
    
    languages = CulturalAdapter.get_languages_by_direction(direction)
    
    return {
        "direction": direction,
        "languages": languages,
        "count": len(languages)
    }


@router.get("/languages/script/{script}")
async def get_languages_by_script(script: str):
    """
    Get languages by script type
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    languages = CulturalAdapter.get_languages_by_script(script)
    
    return {
        "script": script,
        "languages": languages,
        "count": len(languages)
    }


@router.post("/format-number")
async def format_number_cultural(request: FormatNumberRequest):
    """
    Format number according to cultural conventions
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    try:
        formatted = CulturalAdapter.format_number(request.number, request.language)
        
        return {
            "number": request.number,
            "language": request.language,
            "formatted": formatted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/date-format/{language}")
async def get_date_format(language: str):
    """
    Get date format for language
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    date_format = CulturalAdapter.get_date_format(language)
    
    return {
        "language": language,
        "date_format": date_format
    }


@router.post("/detect-script")
async def detect_script_from_text(request: DetectScriptRequest):
    """
    Detect script from text content
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    script = CulturalAdapter.detect_script_from_text(request.text)
    
    return {
        "text": request.text,
        "detected_script": script
    }


@router.get("/rtl-languages")
async def get_rtl_languages():
    """
    Get all RTL languages
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    languages = CulturalAdapter.get_rtl_languages()
    
    return {
        "rtl_languages": languages,
        "count": len(languages)
    }


@router.get("/cyrillic-languages")
async def get_cyrillic_languages():
    """
    Get all Cyrillic languages
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    languages = CulturalAdapter.get_cyrillic_languages()
    
    return {
        "cyrillic_languages": languages,
        "count": len(languages)
    }


@router.post("/wrap-rtl")
async def wrap_content_rtl(content: str, language: str):
    """
    Wrap content with RTL direction if needed
    """
    from core_modules.cultural_adaptation import RTLFormatter
    
    wrapped = RTLFormatter.wrap_rtl(content, language)
    
    return {
        "content": content,
        "language": language,
        "wrapped": wrapped
    }


@router.get("/mirror-layout/{language}")
async def get_mirror_layout_css(language: str):
    """
    Get CSS properties for mirroring layout
    """
    from core_modules.cultural_adaptation import RTLFormatter
    
    css_props = RTLFormatter.mirror_layout(language)
    
    return {
        "language": language,
        "css_properties": css_props
    }


@router.get("/number-formats")
async def get_all_number_formats():
    """
    Get all number formatting conventions
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    return {
        "number_formats": CulturalAdapter.NUMBER_FORMATS
    }


@router.get("/date-formats")
async def get_all_date_formats():
    """
    Get all date formatting conventions
    """
    from core_modules.cultural_adaptation import CulturalAdapter
    
    return {
        "date_formats": CulturalAdapter.DATE_FORMATS
    }
