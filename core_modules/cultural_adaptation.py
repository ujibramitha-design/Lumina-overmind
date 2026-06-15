"""
Cultural Adaptation Module
RTL support for Middle East, Cyrillic support for Russia, and cultural adaptations
"""

from typing import Dict, Optional, List
import re


class CulturalAdapter:
    """Cultural adaptation utilities for global markets"""
    
    # Supported writing directions
    DIRECTIONS = {
        "LTR": "Left-to-Right",
        "RTL": "Right-to-Left"
    }
    
    # Language metadata with direction and script
    LANGUAGES = {
        "en": {
            "name": "English",
            "direction": "LTR",
            "script": "Latin",
            "countries": ["US", "UK", "AU", "CA", "NZ"]
        },
        "id": {
            "name": "Indonesian",
            "direction": "LTR",
            "script": "Latin",
            "countries": ["ID"]
        },
        "ar": {
            "name": "Arabic",
            "direction": "RTL",
            "script": "Arabic",
            "countries": ["SA", "AE", "QA", "KW", "BH", "OM", "EG", "JO", "LB", "SY", "IQ", "YE"]
        },
        "he": {
            "name": "Hebrew",
            "direction": "RTL",
            "script": "Hebrew",
            "countries": ["IL"]
        },
        "ru": {
            "name": "Russian",
            "direction": "LTR",
            "script": "Cyrillic",
            "countries": ["RU", "UA", "BY", "KZ", "KG", "TJ", "UZ"]
        },
        "fa": {
            "name": "Persian (Farsi)",
            "direction": "RTL",
            "script": "Arabic",
            "countries": ["IR", "AF"]
        },
        "ur": {
            "name": "Urdu",
            "direction": "RTL",
            "script": "Arabic",
            "countries": ["PK", "IN"]
        },
        "th": {
            "name": "Thai",
            "direction": "LTR",
            "script": "Thai",
            "countries": ["TH"]
        },
        "zh": {
            "name": "Chinese",
            "direction": "LTR",
            "script": "CJK",
            "countries": ["CN", "TW", "HK", "SG"]
        },
        "ja": {
            "name": "Japanese",
            "direction": "LTR",
            "script": "CJK",
            "countries": ["JP"]
        },
        "ko": {
            "name": "Korean",
            "direction": "LTR",
            "script": "Hangul",
            "countries": ["KR"]
        }
    }
    
    # Number formatting by culture
    NUMBER_FORMATS = {
        "en": {"decimal": ".", "thousands": ","},
        "id": {"decimal": ",", "thousands": "."},
        "ar": {"decimal": ".", "thousands": ","},
        "he": {"decimal": ".", "thousands": ","},
        "ru": {"decimal": ",", "thousands": " "},
        "fa": {"decimal": ".", "thousands": ","},
        "th": {"decimal": ".", "thousands": ","},
        "zh": {"decimal": ".", "thousands": ","},
        "ja": {"decimal": ".", "thousands": ","},
        "ko": {"decimal": ".", "thousands": ","}
    }
    
    # Date formatting by culture
    DATE_FORMATS = {
        "en": "MM/DD/YYYY",
        "id": "DD/MM/YYYY",
        "ar": "DD/MM/YYYY",
        "he": "DD/MM/YYYY",
        "ru": "DD.MM.YYYY",
        "fa": "DD/MM/YYYY",
        "th": "DD/MM/YYYY",
        "zh": "YYYY-MM-DD",
        "ja": "YYYY/MM/DD",
        "ko": "YYYY-MM-DD"
    }
    
    @classmethod
    def get_direction(cls, language: str) -> str:
        """
        Get text direction for language
        
        Args:
            language: Language code (e.g., "ar", "en")
            
        Returns:
            "LTR" or "RTL"
        """
        lang_info = cls.LANGUAGES.get(language)
        if lang_info:
            return lang_info["direction"]
        return "LTR"  # Default to LTR
    
    @classmethod
    def is_rtl(cls, language: str) -> bool:
        """
        Check if language is RTL
        
        Args:
            language: Language code
            
        Returns:
            True if RTL
        """
        return cls.get_direction(language) == "RTL"
    
    @classmethod
    def get_script(cls, language: str) -> str:
        """
        Get script type for language
        
        Args:
            language: Language code
            
        Returns:
            Script name (e.g., "Arabic", "Cyrillic", "Latin")
        """
        lang_info = cls.LANGUAGES.get(language)
        if lang_info:
            return lang_info["script"]
        return "Latin"  # Default to Latin
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, Dict]:
        """
        Get all supported languages with metadata
        
        Returns:
            Dictionary of language information
        """
        return cls.LANGUAGES
    
    @classmethod
    def get_languages_by_direction(cls, direction: str) -> List[str]:
        """
        Get languages by text direction
        
        Args:
            direction: "LTR" or "RTL"
            
        Returns:
            List of language codes
        """
        return [
            lang for lang, info in cls.LANGUAGES.items()
            if info["direction"] == direction
        ]
    
    @classmethod
    def get_languages_by_script(cls, script: str) -> List[str]:
        """
        Get languages by script type
        
        Args:
            script: Script name (e.g., "Arabic", "Cyrillic")
            
        Returns:
            List of language codes
        """
        return [
            lang for lang, info in cls.LANGUAGES.items()
            if info["script"] == script
        ]
    
    @classmethod
    def format_number(cls, number: float, language: str) -> str:
        """
        Format number according to cultural conventions
        
        Args:
            number: Number to format
            language: Language code
            
        Returns:
            Formatted number string
        """
        formats = cls.NUMBER_FORMATS.get(language, cls.NUMBER_FORMATS["en"])
        decimal_sep = formats["decimal"]
        thousands_sep = formats["thousands"]
        
        # Split into integer and decimal parts
        if isinstance(number, int):
            integer_part = number
            decimal_part = None
        else:
            integer_part = int(number)
            decimal_part = round(number - integer_part, 2)
        
        # Format integer part with thousands separator
        integer_str = f"{integer_part:,}".replace(",", thousands_sep)
        
        # Add decimal part if exists
        if decimal_part is not None and decimal_part > 0:
            decimal_str = f"{decimal_part:.2f}".split(".")[1]
            return f"{integer_str}{decimal_sep}{decimal_str}"
        
        return integer_str
    
    @classmethod
    def get_date_format(cls, language: str) -> str:
        """
        Get date format for language
        
        Args:
            language: Language code
            
        Returns:
            Date format string
        """
        return cls.DATE_FORMATS.get(language, cls.DATE_FORMATS["en"])
    
    @classmethod
    def detect_script_from_text(cls, text: str) -> str:
        """
        Detect script from text content
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected script name
        """
        # Arabic script range
        if re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text):
            return "Arabic"
        
        # Cyrillic script range
        if re.search(r'[\u0400-\u04FF\u0500-\u052F]', text):
            return "Cyrillic"
        
        # CJK script range
        if re.search(r'[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\uF900-\uFAFF]', text):
            return "CJK"
        
        # Thai script range
        if re.search(r'[\u0E00-\u0E7F]', text):
            return "Thai"
        
        # Hangul script range
        if re.search(r'[\uAC00-\uD7AF\u1100-\u11FF]', text):
            return "Hangul"
        
        # Default to Latin
        return "Latin"
    
    @classmethod
    def get_rtl_languages(cls) -> List[str]:
        """
        Get all RTL languages
        
        Returns:
            List of RTL language codes
        """
        return cls.get_languages_by_direction("RTL")
    
    @classmethod
    def get_cyrillic_languages(cls) -> List[str]:
        """
        Get all Cyrillic languages
        
        Returns:
            List of Cyrillic language codes
        """
        return cls.get_languages_by_script("Cyrillic")


class RTLFormatter:
    """RTL formatting utilities"""
    
    @staticmethod
    def wrap_rtl(content: str, language: str) -> str:
        """
        Wrap content with RTL direction if needed
        
        Args:
            content: Content to wrap
            language: Language code
            
        Returns:
            Wrapped content with dir attribute
        """
        if CulturalAdapter.is_rtl(language):
            return f'<div dir="rtl" lang="{language}">{content}</div>'
        return f'<div dir="ltr" lang="{language}">{content}</div>'
    
    @staticmethod
    def mirror_layout(language: str) -> Dict[str, str]:
        """
        Get CSS properties for mirroring layout
        
        Args:
            language: Language code
            
        Returns:
            Dictionary of CSS properties
        """
        if CulturalAdapter.is_rtl(language):
            return {
                "direction": "rtl",
                "text-align": "right",
                "margin-left": "auto",
                "margin-right": "0"
            }
        return {
            "direction": "ltr",
            "text-align": "left",
            "margin-left": "0",
            "margin-right": "auto"
        }


# Singleton instance
_cultural_adapter_instance: Optional[CulturalAdapter] = None


def get_cultural_adapter() -> CulturalAdapter:
    """Get or create cultural adapter instance"""
    global _cultural_adapter_instance
    
    if _cultural_adapter_instance is None:
        _cultural_adapter_instance = CulturalAdapter()
    
    return _cultural_adapter_instance
