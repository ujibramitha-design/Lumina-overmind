"""
Currency Module
Multi-currency support for Asia markets
"""

from typing import Dict, Optional
from datetime import datetime
import json


class CurrencyConverter:
    """Currency conversion utilities for Asia markets"""
    
    # Supported currencies for Asia expansion
    SUPPORTED_CURRENCIES = {
        "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp", "locale": "id-ID"},
        "SGD": {"name": "Singapore Dollar", "symbol": "S$", "locale": "en-SG"},
        "MYR": {"name": "Malaysian Ringgit", "symbol": "RM", "locale": "en-MY"},
        "THB": {"name": "Thai Baht", "symbol": "฿", "locale": "th-TH"},
        "VND": {"name": "Vietnamese Dong", "symbol": "₫", "locale": "vi-VN"},
        "PHP": {"name": "Philippine Peso", "symbol": "₱", "locale": "en-PH"},
        "USD": {"name": "US Dollar", "symbol": "$", "locale": "en-US"},
    }
    
    # Exchange rates (base: USD) - In production, fetch from API
    EXCHANGE_RATES = {
        "USD": 1.0,
        "IDR": 15800.0,
        "SGD": 1.35,
        "MYR": 4.75,
        "THB": 36.0,
        "VND": 24500.0,
        "PHP": 56.0,
    }
    
    # Last update timestamp
    LAST_UPDATE: Optional[datetime] = None
    
    @classmethod
    def convert(cls, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., "USD", "IDR")
            to_currency: Target currency code (e.g., "SGD", "MYR")
            
        Returns:
            Converted amount
        """
        if from_currency not in cls.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {from_currency}")
        
        if to_currency not in cls.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {to_currency}")
        
        # Convert to USD first (base currency)
        amount_in_usd = amount / cls.EXCHANGE_RATES[from_currency]
        
        # Convert from USD to target currency
        converted_amount = amount_in_usd * cls.EXCHANGE_RATES[to_currency]
        
        return round(converted_amount, 2)
    
    @classmethod
    def format(cls, amount: float, currency: str) -> str:
        """
        Format amount with currency symbol
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Formatted string with symbol
        """
        if currency not in cls.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")
        
        symbol = cls.SUPPORTED_CURRENCIES[currency]["symbol"]
        
        # Format based on currency
        if currency in ["IDR", "VND"]:
            # No decimal places for these currencies
            return f"{symbol}{int(amount):,}"
        else:
            # 2 decimal places for others
            return f"{symbol}{amount:,.2f}"
    
    @classmethod
    def get_supported_currencies(cls) -> Dict[str, Dict]:
        """
        Get all supported currencies with metadata
        
        Returns:
            Dictionary of currency information
        """
        return cls.SUPPORTED_CURRENCIES
    
    @classmethod
    def get_exchange_rates(cls) -> Dict[str, float]:
        """
        Get current exchange rates
        
        Returns:
            Dictionary of exchange rates (base: USD)
        """
        return cls.EXCHANGE_RATES
    
    @classmethod
    def update_exchange_rates(cls, new_rates: Dict[str, float]) -> None:
        """
        Update exchange rates (call from external API)
        
        Args:
            new_rates: New exchange rates dictionary
        """
        cls.EXCHANGE_RATES.update(new_rates)
        cls.LAST_UPDATE = datetime.utcnow()
    
    @classmethod
    def get_rate(cls, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate between two currencies
        
        Args:
            from_currency: Source currency
            to_currency: Target currency
            
        Returns:
            Exchange rate
        """
        if from_currency == to_currency:
            return 1.0
        
        return cls.EXCHANGE_RATES[to_currency] / cls.EXCHANGE_RATES[from_currency]


class CurrencyFormatter:
    """Currency formatting utilities"""
    
    @staticmethod
    def format_for_display(amount: float, currency: str, locale: Optional[str] = None) -> str:
        """
        Format amount for display in specific locale
        
        Args:
            amount: Amount to format
            currency: Currency code
            locale: Optional locale override
            
        Returns:
            Locale-formatted string
        """
        if locale is None:
            locale = CurrencyConverter.SUPPORTED_CURRENCIES.get(currency, {}).get("locale", "en-US")
        
        # Simple formatting - in production, use locale-aware formatting
        return CurrencyConverter.format(amount, currency)
    
    @staticmethod
    def format_range(min_amount: float, max_amount: float, currency: str) -> str:
        """
        Format a price range
        
        Args:
            min_amount: Minimum amount
            max_amount: Maximum amount
            currency: Currency code
            
        Returns:
            Formatted range string
        """
        min_formatted = CurrencyConverter.format(min_amount, currency)
        max_formatted = CurrencyConverter.format(max_amount, currency)
        
        return f"{min_formatted} - {max_formatted}"
    
    @staticmethod
    def format_compact(amount: float, currency: str) -> str:
        """
        Format amount in compact form (e.g., 1.5M, 2.5K)
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Compact formatted string
        """
        symbol = CurrencyConverter.SUPPORTED_CURRENCIES[currency]["symbol"]
        
        if amount >= 1_000_000_000:
            return f"{symbol}{amount / 1_000_000_000:.1f}B"
        elif amount >= 1_000_000:
            return f"{symbol}{amount / 1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"{symbol}{amount / 1_000:.1f}K"
        else:
            return CurrencyConverter.format(amount, currency)


# Singleton instance
_currency_converter_instance: Optional[CurrencyConverter] = None


def get_currency_converter() -> CurrencyConverter:
    """Get or create currency converter instance"""
    global _currency_converter_instance
    
    if _currency_converter_instance is None:
        _currency_converter_instance = CurrencyConverter()
    
    return _currency_converter_instance
