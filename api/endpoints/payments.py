"""
LUMINA OS - PROJECT VAULT
====================================

Instant Checkout Integration System
Payment Gateway Integration for Lumina OS

Features:
- Midtrans/Xendit Payment Gateway Integration
- QRIS Generation for Booking Fees
- Webhook Payment Status Handling
- Automatic Lead Status Updates
- Unit Locking System
- Transaction History Tracking
"""

import os
import sys
import json
import hashlib
import time
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from decimal import Decimal

# FastAPI imports
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import httpx

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import required modules
try:
    from core_modules.db_manager_supabase import get_supabase_manager
    from core_modules.notifications.telegram_sender import get_telegram_sender
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

# Create router
router = APIRouter(prefix="/api/payments", tags=["payments"])

# Pydantic models
class QRISRequest(BaseModel):
    lead_id: str = Field(..., description="Lead ID for booking")
    nominal: int = Field(default=1000000, description="Booking fee amount in Rupiah")
    customer_name: Optional[str] = Field(None, description="Customer name")
    customer_email: Optional[str] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone")

class QRISResponse(BaseModel):
    success: bool
    transaction_id: str
    qris_url: str
    expiry_time: datetime
    amount: int
    payment_status: str

class WebhookPayload(BaseModel):
    order_id: str
    status_code: str
    gross_amount: str
    payment_type: str
    transaction_time: str
    fraud_status: str

@dataclass
class PaymentTransaction:
    """Payment transaction data structure"""
    transaction_id: str
    lead_id: str
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    amount: int
    payment_type: str
    status: str
    qris_url: Optional[str]
    expiry_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    webhook_data: Optional[Dict[str, Any]] = None

class PaymentVault:
    """
    Project Vault - Payment Gateway Integration System
    Instant checkout and payment processing for Lumina OS
    """
    
    def __init__(self):
        """Initialize Payment Vault"""
        self.logger = logging.getLogger(__name__)
        
        # Payment gateway configuration
        self.payment_gateway = os.getenv('PAYMENT_GATEWAY', 'midtrans')  # midtrans or xendit
        self.midtrans_server_key = os.getenv('MIDTRANS_SERVER_KEY', '')
        self.midtrans_client_key = os.getenv('MIDTRANS_CLIENT_KEY', '')
        self.xendit_secret_key = os.getenv('XENDIT_SECRET_KEY', '')
        
        # Initialize database
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Database connected for payment vault{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Database connection failed: {e}{END}")
        
        # Initialize Telegram sender
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Telegram sender initialized for payment notifications{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Telegram sender failed: {e}{END}")
        
        # Transaction storage (in production, use database)
        self.transactions: Dict[str, PaymentTransaction] = {}
        
        # Booking fee configuration
        self.booking_fee_amount = 1000000  # Rp 1,000,000
        self.qris_expiry_minutes = 30  # 30 minutes
        
        self.logger.info(f"{MAGENTA}🔐 PROJECT VAULT: Payment Gateway initialized{END}")
        self.logger.info(f"{CYAN}💳 Payment Gateway: {self.payment_gateway.upper()}{END}")
        self.logger.info(f"{GREEN}✅ Booking Fee: Rp {self.booking_fee_amount:,}{END}")
        self.logger.info(f"{GREEN}✅ QRIS Expiry: {self.qris_expiry_minutes} minutes{END}")
    
    def generate_transaction_id(self, lead_id: str) -> str:
        """
        Generate unique transaction ID
        
        Args:
            lead_id: Lead ID
            
        Returns:
            Unique transaction ID
        """
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"BOOK-{lead_id}-{timestamp}-{unique_id}"
    
    async def create_midtrans_transaction(self, transaction_data: PaymentTransaction) -> Dict[str, Any]:
        """
        Create transaction with Midtrans
        
        Args:
            transaction_data: Transaction data
            
        Returns:
            Midtrans response data
        """
        try:
            if not self.midtrans_server_key:
                raise HTTPException(status_code=500, detail="Midtrans server key not configured")
            
            # Midtrans API endpoint
            url = "https://api.sandbox.midtrans.com/v2/charge"
            
            # Prepare payload
            payload = {
                "payment_type": "qris",
                "transaction_details": {
                    "order_id": transaction_data.transaction_id,
                    "gross_amount": transaction_data.amount,
                    "currency": "IDR"
                },
                "customer_details": {
                    "first_name": transaction_data.customer_name or "Customer",
                    "email": transaction_data.customer_email or "customer@example.com",
                    "phone": transaction_data.customer_phone or "+62812345678"
                },
                "qris": {
                    "acquirer": "gopay"
                },
                "expiry": {
                    "start_time": datetime.now().isoformat(),
                    "unit": "minutes",
                    "duration": self.qris_expiry_minutes
                }
            }
            
            # Make request to Midtrans
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.midtrans_server_key}"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"{GREEN}✅ Midtrans transaction created: {transaction_data.transaction_id}{END}")
                    return result
                else:
                    error_text = response.text
                    self.logger.error(f"{RED}❌ Midtrans API error: {response.status_code} - {error_text}{END}")
                    raise HTTPException(status_code=response.status_code, detail=f"Midtrans API error: {error_text}")
                    
        except Exception as e:
            self.logger.error(f"{RED}❌ Create Midtrans transaction error: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"Payment gateway error: {str(e)}")
    
    async def create_xendit_transaction(self, transaction_data: PaymentTransaction) -> Dict[str, Any]:
        """
        Create transaction with Xendit
        
        Args:
            transaction_data: Transaction data
            
        Returns:
            Xendit response data
        """
        try:
            if not self.xendit_secret_key:
                raise HTTPException(status_code=500, detail="Xendit secret key not configured")
            
            # Xendit API endpoint
            url = "https://api.xendit.co/v2/invoices"
            
            # Prepare payload
            payload = {
                "external_id": transaction_data.transaction_id,
                "amount": transaction_data.amount,
                "description": f"Booking Fee for Lead {transaction_data.lead_id}",
                "invoice_duration": 3600,  # 1 hour in seconds
                "customer": {
                    "given_names": transaction_data.customer_name or "Customer",
                    "email": transaction_data.customer_email or "customer@example.com",
                    "mobile_number": transaction_data.customer_phone or "+62812345678"
                },
                "success_redirect_url": f"https://lumina-os.com/payment/success/{transaction_data.transaction_id}",
                "failure_redirect_url": f"https://lumina-os.com/payment/failed/{transaction_data.transaction_id}",
                "payment_methods": ["QRIS", "OVO", "DANA", "SHOPEEPAY"]
            }
            
            # Make request to Xendit
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=headers,
                    auth=(self.xendit_secret_key, ""),
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"{GREEN}✅ Xendit transaction created: {transaction_data.transaction_id}{END}")
                    return result
                else:
                    error_text = response.text
                    self.logger.error(f"{RED}❌ Xendit API error: {response.status_code} - {error_text}{END}")
                    raise HTTPException(status_code=response.status_code, detail=f"Xendit API error: {error_text}")
                    
        except Exception as e:
            self.logger.error(f"{RED}❌ Create Xendit transaction error: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"Payment gateway error: {str(e)}")
    
    async def generate_qris(self, request_data: QRISRequest) -> QRISResponse:
        """
        Generate QRIS for payment
        
        Args:
            request_data: QRIS request data
            
        Returns:
            QRIS response with payment details
        """
        try:
            self.logger.info(f"{CYAN}💳 Generating QRIS for lead {request_data.lead_id}{END}")
            
            # Validate lead exists
            if not self.supabase_manager:
                raise HTTPException(status_code=500, detail="Database not available")
            
            lead_result = self.supabase_manager.get_lead(request_data.lead_id)
            if not lead_result['success']:
                raise HTTPException(status_code=404, detail="Lead not found")
            
            lead_data = lead_result['data']
            
            # Create transaction data
            transaction_id = self.generate_transaction_id(request_data.lead_id)
            expiry_time = datetime.now() + timedelta(minutes=self.qris_expiry_minutes)
            
            transaction_data = PaymentTransaction(
                transaction_id=transaction_id,
                lead_id=request_data.lead_id,
                customer_name=request_data.customer_name or lead_data.get('business_name', 'Customer'),
                customer_email=request_data.customer_email,
                customer_phone=request_data.customer_phone,
                amount=request_data.nominal,
                payment_type="qris",
                status="pending",
                qris_url=None,
                expiry_time=expiry_time,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Create transaction with payment gateway
            if self.payment_gateway == 'midtrans':
                gateway_response = await self.create_midtrans_transaction(transaction_data)
                qris_url = gateway_response.get('actions', [{}])[0].get('qr_code_url', '')
            elif self.payment_gateway == 'xendit':
                gateway_response = await self.create_xendit_transaction(transaction_data)
                qris_url = gateway_response.get('invoice_url', '')
            else:
                raise HTTPException(status_code=500, detail="Payment gateway not configured")
            
            # Update transaction with QRIS URL
            transaction_data.qris_url = qris_url
            
            # Store transaction
            self.transactions[transaction_id] = transaction_data
            
            # Update lead status to 'Booking_Initiated'
            lead_update = {
                'status': 'Booking_Initiated',
                'updated_at': datetime.now().isoformat(),
                'booking_data': {
                    'transaction_id': transaction_id,
                    'amount': request_data.nominal,
                    'payment_gateway': self.payment_gateway,
                    'created_at': datetime.now().isoformat()
                }
            }
            
            self.supabase_manager.update_lead(request_data.lead_id, lead_update)
            
            # Send notification to Telegram
            if self.telegram_sender:
                notification_message = f"""
💳 **BOOKING INITIATED**

🏠 **Lead ID**: {request_data.lead_id}
👤 **Customer**: {transaction_data.customer_name}
💰 **Amount**: Rp {request_data.nominal:,}
🔗 **Transaction**: {transaction_id}
⏰ **Expiry**: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}

📱 **QRIS URL**: {qris_url}

⚡ **Status**: Waiting for payment...
                """.strip()
                
                self.telegram_sender.send_message(notification_message)
            
            self.logger.info(f"{GREEN}✅ QRIS generated successfully: {transaction_id}{END}")
            
            return QRISResponse(
                success=True,
                transaction_id=transaction_id,
                qris_url=qris_url,
                expiry_time=expiry_time,
                amount=request_data.nominal,
                payment_status="pending"
            )
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Generate QRIS error: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"QRIS generation error: {str(e)}")
    
    async def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment webhook from payment gateway
        
        Args:
            webhook_data: Webhook payload
            
        Returns:
            Webhook processing result
        """
        try:
            self.logger.info(f"{CYAN}🔔 Processing payment webhook...{END}")
            
            # Extract transaction info
            order_id = webhook_data.get('order_id')
            status_code = webhook_data.get('status_code')
            gross_amount = webhook_data.get('gross_amount')
            
            if not order_id:
                raise HTTPException(status_code=400, detail="Missing order_id")
            
            # Find transaction
            transaction = self.transactions.get(order_id)
            if not transaction:
                self.logger.warning(f"{YELLOW}⚠️ Transaction not found: {order_id}{END}")
                return {"status": "transaction_not_found"}
            
            # Update transaction status
            old_status = transaction.status
            transaction.status = status_code
            transaction.updated_at = datetime.now()
            transaction.webhook_data = webhook_data
            
            self.transactions[order_id] = transaction
            
            self.logger.info(f"{BLUE}📊 Transaction {order_id}: {old_status} → {status_code}{END}")
            
            # Handle successful payment
            if status_code in ['200', '201', 'SUCCESS'] and old_status != status_code:
                return await self._handle_successful_payment(transaction)
            elif status_code in ['202', 'PENDING']:
                return await self._handle_pending_payment(transaction)
            elif status_code in ['400', '401', '402', 'FAILED', 'CANCELLED']:
                return await self._handle_failed_payment(transaction)
            else:
                return {"status": "processed", "message": f"Status updated to {status_code}"}
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Handle webhook error: {str(e)}{END}")
            raise HTTPException(status_code=500, detail=f"Webhook processing error: {str(e)}")
    
    async def _handle_successful_payment(self, transaction: PaymentTransaction) -> Dict[str, Any]:
        """
        Handle successful payment
        
        Args:
            transaction: Payment transaction data
            
        Returns:
            Processing result
        """
        try:
            self.logger.info(f"{GREEN}✅ Processing successful payment: {transaction.transaction_id}{END}")
            
            # Update lead status to 'BOOKED'
            if self.supabase_manager:
                lead_update = {
                    'status': 'BOOKED',
                    'updated_at': datetime.now().isoformat(),
                    'booking_data': {
                        'transaction_id': transaction.transaction_id,
                        'amount': transaction.amount,
                        'payment_completed_at': datetime.now().isoformat(),
                        'payment_gateway': self.payment_gateway
                    }
                }
                
                # Lock the unit (if applicable)
                lead_result = self.supabase_manager.get_lead(transaction.lead_id)
                if lead_result['success']:
                    lead_data = lead_result['data']
                    unit_info = lead_data.get('unit_info', {})
                    if unit_info.get('unit_id'):
                        lead_update['unit_info'] = {
                            **unit_info,
                            'status': 'LOCKED',
                            'locked_at': datetime.now().isoformat(),
                            'locked_by': transaction.customer_name,
                            'booking_transaction_id': transaction.transaction_id
                        }
                
                self.supabase_manager.update_lead(transaction.lead_id, lead_update)
            
            # Send success notification to Telegram
            if self.telegram_sender:
                success_message = f"""
🎉 **PAYMENT SUCCESSFUL**

💳 **Transaction**: {transaction.transaction_id}
🏠 **Lead ID**: {transaction.lead_id}
👤 **Customer**: {transaction.customer_name}
💰 **Amount**: Rp {transaction.amount:,}
🏢 **Status**: BOOKED & LOCKED
⏰ **Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔒 **Unit has been locked for this customer**
                """.strip()
                
                self.telegram_sender.send_message(success_message)
            
            self.logger.info(f"{GREEN}✅ Payment processed and unit locked: {transaction.transaction_id}{END}")
            
            return {
                "status": "success",
                "transaction_id": transaction.transaction_id,
                "lead_id": transaction.lead_id,
                "message": "Payment successful - unit locked"
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Handle successful payment error: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _handle_pending_payment(self, transaction: PaymentTransaction) -> Dict[str, Any]:
        """Handle pending payment"""
        self.logger.info(f"{YELLOW}⏳ Payment pending: {transaction.transaction_id}{END}")
        
        if self.telegram_sender:
            pending_message = f"⏳ **PAYMENT PENDING**\nTransaction: {transaction.transaction_id}\nAmount: Rp {transaction.amount:,}"
            self.telegram_sender.send_message(pending_message)
        
        return {
            "status": "pending",
            "transaction_id": transaction.transaction_id,
            "message": "Payment is pending"
        }
    
    async def _handle_failed_payment(self, transaction: PaymentTransaction) -> Dict[str, Any]:
        """Handle failed payment"""
        self.logger.info(f"{RED}❌ Payment failed: {transaction.transaction_id}{END}")
        
        # Update lead status back to 'Available'
        if self.supabase_manager:
            lead_update = {
                'status': 'Available',
                'updated_at': datetime.now().isoformat(),
                'booking_data': {
                    'transaction_id': transaction.transaction_id,
                    'amount': transaction.amount,
                    'payment_failed_at': datetime.now().isoformat(),
                    'payment_gateway': self.payment_gateway
                }
            }
            
            # Unlock unit if it was locked
            lead_result = self.supabase_manager.get_lead(transaction.lead_id)
            if lead_result['success']:
                lead_data = lead_result['data']
                unit_info = lead_data.get('unit_info', {})
                if unit_info.get('status') == 'LOCKED':
                    lead_update['unit_info'] = {
                        **unit_info,
                        'status': 'AVAILABLE',
                        'unlocked_at': datetime.now().isoformat(),
                        'unlock_reason': 'Payment failed'
                    }
            
            self.supabase_manager.update_lead(transaction.lead_id, lead_update)
        
        # Send failure notification to Telegram
        if self.telegram_sender:
            failure_message = f"""
❌ **PAYMENT FAILED**

💳 **Transaction**: {transaction.transaction_id}
🏠 **Lead ID**: {transaction.lead_id}
👤 **Customer**: {transaction.customer_name}
💰 **Amount**: Rp {transaction.amount:,}
🏢 **Status**: Available (unit unlocked)
⏰ **Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 **Unit has been unlocked and is available again**
            """.strip()
            
            self.telegram_sender.send_message(failure_message)
        
        return {
            "status": "failed",
            "transaction_id": transaction.transaction_id,
            "lead_id": transaction.lead_id,
            "message": "Payment failed - unit unlocked"
        }
    
    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get transaction status
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Transaction status information
        """
        transaction = self.transactions.get(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {
            "transaction_id": transaction.transaction_id,
            "lead_id": transaction.lead_id,
            "customer_name": transaction.customer_name,
            "amount": transaction.amount,
            "status": transaction.status,
            "payment_type": transaction.payment_type,
            "qris_url": transaction.qris_url,
            "expiry_time": transaction.expiry_time,
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at
        }
    
    def get_payment_statistics(self) -> Dict[str, Any]:
        """Get payment statistics"""
        total_transactions = len(self.transactions)
        successful_payments = len([t for t in self.transactions.values() if t.status in ['200', '201', 'SUCCESS']])
        pending_payments = len([t for t in self.transactions.values() if t.status in ['202', 'PENDING']])
        failed_payments = len([t for t in self.transactions.values() if t.status in ['400', '401', '402', 'FAILED', 'CANCELLED']])
        
        total_amount = sum(t.amount for t in self.transactions.values() if t.status in ['200', '201', 'SUCCESS'])
        
        return {
            "total_transactions": total_transactions,
            "successful_payments": successful_payments,
            "pending_payments": pending_payments,
            "failed_payments": failed_payments,
            "success_rate": (successful_payments / max(total_transactions, 1)) * 100,
            "total_amount": total_amount,
            "average_amount": total_amount / max(successful_payments, 1),
            "payment_gateway": self.payment_gateway,
            "timestamp": datetime.now().isoformat()
        }

# Global payment vault instance
payment_vault = PaymentVault()

# API endpoints
@router.post("/generate-qris", response_model=QRISResponse)
async def generate_qris(request: QRISRequest):
    """Generate QRIS for booking fee payment"""
    return await payment_vault.generate_qris(request)

@router.post("/webhook")
async def payment_webhook(webhook_data: Dict[str, Any]):
    """Handle payment webhook from payment gateway"""
    return await payment_vault.handle_webhook(webhook_data)

@router.get("/status/{transaction_id}")
async def get_transaction_status(transaction_id: str):
    """Get transaction status"""
    return payment_vault.get_transaction_status(transaction_id)

@router.get("/statistics")
async def get_payment_statistics():
    """Get payment statistics"""
    return payment_vault.get_payment_statistics()

# Convenience functions
async def create_booking_qris(lead_id: str, customer_name: str = None, 
                             customer_email: str = None, customer_phone: str = None) -> Dict[str, Any]:
    """Convenience function to create booking QRIS"""
    request_data = QRISRequest(
        lead_id=lead_id,
        nominal=payment_vault.booking_fee_amount,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone
    )
    return await payment_vault.generate_qris(request_data)

def get_payment_stats() -> Dict[str, Any]:
    """Convenience function to get payment statistics"""
    return payment_vault.get_payment_statistics()

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - PROJECT VAULT{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    # Test QRIS generation
    print(f"{BLUE}💳 Testing QRIS generation...{END}")
    
    # This would be tested in the actual API
    print(f"{GREEN}✅ Payment Vault initialized{END}")
    print(f"{CYAN}💳 Payment Gateway: {payment_vault.payment_gateway.upper()}{END}")
    print(f"{GREEN}✅ Booking Fee: Rp {payment_vault.booking_fee_amount:,}{END}")
    
    # Show statistics
    stats = get_payment_stats()
    print(f"{CYAN}📊 Payment Statistics:{END}")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"{MAGENTA}{'='*80}{END}")
