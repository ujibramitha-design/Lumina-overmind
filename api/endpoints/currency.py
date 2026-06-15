"""
Currency API
Endpoints for multi-currency support for Asia markets
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

router = APIRouter(prefix="/currency", tags=["Currency"])


class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str


class FormatRequest(BaseModel):
    amount: float
    currency: str
    locale: Optional[str] = None


class ExchangeRateUpdate(BaseModel):
    rates: Dict[str, float]


@router.get("/supported")
async def get_supported_currencies():
    """
    Get all supported currencies
    """
    from core_modules.currency import CurrencyConverter
    
    currencies = CurrencyConverter.get_supported_currencies()
    
    return {
        "currencies": currencies,
        "count": len(currencies)
    }


@router.get("/exchange-rates")
async def get_exchange_rates():
    """
    Get current exchange rates (base: USD)
    """
    from core_modules.currency import CurrencyConverter
    
    rates = CurrencyConverter.get_exchange_rates()
    
    return {
        "base_currency": "USD",
        "rates": rates,
        "last_updated": CurrencyConverter.LAST_UPDATE.isoformat() if CurrencyConverter.LAST_UPDATE else None
    }


@router.post("/convert")
async def convert_currency(request: ConvertRequest):
    """
    Convert amount from one currency to another
    """
    from core_modules.currency import CurrencyConverter
    
    try:
        converted_amount = CurrencyConverter.convert(
            request.amount,
            request.from_currency,
            request.to_currency
        )
        
        exchange_rate = CurrencyConverter.get_rate(request.from_currency, request.to_currency)
        
        return {
            "original_amount": request.amount,
            "original_currency": request.from_currency,
            "converted_amount": converted_amount,
            "target_currency": request.to_currency,
            "exchange_rate": exchange_rate
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/format")
async def format_currency(request: FormatRequest):
    """
    Format amount with currency symbol
    """
    from core_modules.currency import CurrencyFormatter
    
    try:
        formatted = CurrencyFormatter.format_for_display(
            request.amount,
            request.currency,
            request.locale
        )
        
        return {
            "amount": request.amount,
            "currency": request.currency,
            "formatted": formatted
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/format-range")
async def format_currency_range(min_amount: float, max_amount: float, currency: str):
    """
    Format a price range
    """
    from core_modules.currency import CurrencyFormatter
    
    try:
        formatted = CurrencyFormatter.format_range(min_amount, max_amount, currency)
        
        return {
            "min_amount": min_amount,
            "max_amount": max_amount,
            "currency": currency,
            "formatted": formatted
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/format-compact")
async def format_compact_currency(amount: float, currency: str):
    """
    Format amount in compact form (e.g., 1.5M, 2.5K)
    """
    from core_modules.currency import CurrencyFormatter
    
    try:
        formatted = CurrencyFormatter.format_compact(amount, currency)
        
        return {
            "amount": amount,
            "currency": currency,
            "formatted": formatted
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rate/{from_currency}/{to_currency}")
async def get_exchange_rate(from_currency: str, to_currency: str):
    """
    Get exchange rate between two currencies
    """
    from core_modules.currency import CurrencyConverter
    
    try:
        rate = CurrencyConverter.get_rate(from_currency, to_currency)
        
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": rate
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-rates")
async def update_exchange_rates(request: ExchangeRateUpdate):
    """
    Update exchange rates (admin only)
    """
    from core_modules.currency import CurrencyConverter
    
    try:
        CurrencyConverter.update_exchange_rates(request.rates)
        
        return {
            "status": "success",
            "message": "Exchange rates updated",
            "last_updated": CurrencyConverter.LAST_UPDATE.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare")
async def compare_currencies(amount: float, currencies: List[str]):
    """
    Compare amount across multiple currencies
    """
    from core_modules.currency import CurrencyConverter, CurrencyFormatter
    
    results = []
    
    for currency in currencies:
        try:
            converted = CurrencyConverter.convert(amount, "USD", currency)
            formatted = CurrencyFormatter.format_for_display(converted, currency)
            
            results.append({
                "currency": currency,
                "amount": converted,
                "formatted": formatted
            })
        except ValueError:
            continue
    
    return {
        "base_amount": amount,
        "base_currency": "USD",
        "comparisons": results
    }
