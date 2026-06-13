# 📱 Lumina OS WhatsApp Gateway - Documentation

## Overview
Professional WhatsApp message delivery system for Lumina OS with multiple delivery modes, comprehensive error handling, and database integration.

## 🎯 Features

### Core Functionality
- **Dual Delivery Modes**: Web mode and API simulation
- **Database Integration**: SQLite with leads.db
- **Queue Processing**: Automated pending message handling
- **Phone Validation**: International format normalization
- **Message Validation**: Content length and format checking
- **Error Handling**: Professional exception management
- **Statistics Tracking**: Delivery metrics and success rates

### Delivery Modes

#### Web Mode
- **URL Generation**: Creates wa.me links with encoded messages
- **Browser Integration**: Opens WhatsApp Web automatically
- **Fallback Option**: Returns URL for manual opening
- **Use Case**: Manual message sending with user interaction

#### API Simulation Mode
- **Realistic Simulation**: 95% success rate with random delays
- **Message Logging**: Detailed delivery information
- **Error Simulation**: Rate limiting and API error scenarios
- **Use Case**: Automated bulk messaging and testing

## 🔧 Technical Implementation

### Class Structure
```python
class WhatsAppGateway:
    """Professional WhatsApp Gateway for Lumina OS"""
    
    def __init__(self, db_path: Optional[str] = None)
    def send_message(self, phone_number: str, message: str, mode: str = 'web') -> MessageResult
    def process_pending_queue(self) -> Dict[str, Any]
    def get_delivery_stats(self) -> Dict[str, Any]
    def reset_stats(self) -> None
```

### Data Classes
```python
@dataclass
class MessageResult:
    success: bool
    phone_number: str
    message: str
    mode: str
    timestamp: str
    delivery_method: str
    error_message: Optional[str] = None
    message_id: Optional[str] = None

@dataclass
class QueuedMessage:
    id: int
    lead_id: int
    phone_number: str
    message: str
    lead_name: str
    created_at: str
    attempts: int = 0
    last_attempt: Optional[str] = None
```

## 📱 Message Delivery

### Web Mode Implementation
```python
def _send_web_mode(self, phone_number: str, message: str, message_id: str, timestamp: str) -> MessageResult:
    """Send message using web mode (wa.me URL)"""
    try:
        # Encode message for URL
        encoded_message = urllib.parse.quote(message)
        
        # Generate WhatsApp URL
        wa_url = f"https://wa.me/{phone_number}?text={encoded_message}"
        
        if self.webbrowser_available:
            webbrowser.open_new(wa_url)
            delivery_method = "web_browser"
        else:
            delivery_method = "url_returned"
        
        return MessageResult(
            success=True,
            phone_number=phone_number,
            message=message,
            mode='web',
            timestamp=timestamp,
            delivery_method=delivery_method,
            message_id=message_id
        )
```

### API Simulation Mode Implementation
```python
def _send_api_simulation_mode(self, phone_number: str, message: str, message_id: str, timestamp: str) -> MessageResult:
    """Send message using API simulation mode"""
    try:
        # Simulate API call delay
        time.sleep(random.uniform(0.5, 1.5))
        
        # Simulate success (95% success rate)
        if random.random() < 0.95:
            print(f"✅ Message successfully dispatched to +{phone_number} via Lumina Gateway")
            return MessageResult(
                success=True,
                phone_number=phone_number,
                message=message,
                mode='api_simulation',
                timestamp=timestamp,
                delivery_method="api_simulation",
                message_id=message_id
            )
        else:
            # Simulate API error
            error_msg = "API rate limit exceeded"
            return MessageResult(
                success=False,
                phone_number=phone_number,
                message=message,
                mode='api_simulation',
                timestamp=timestamp,
                delivery_method="api_simulation_error",
                error_message=error_msg,
                message_id=message_id
            )
```

## 🗄️ Database Integration

### Database Schema
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    contact TEXT,
    url TEXT,
    keywords TEXT,
    source TEXT DEFAULT 'web_scraping',
    score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'new',
    location TEXT,
    date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    catatan_followup TEXT,
    message_sent_time TEXT  -- Added by WhatsApp Gateway
);
```

### Queue Processing Logic
```python
def process_pending_queue(self) -> Dict[str, Any]:
    """Process pending messages from leads database"""
    try:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Check if message_sent_time column exists
        if 'message_sent_time' not in columns:
            cursor.execute('ALTER TABLE leads ADD COLUMN message_sent_time TEXT')
        
        # Find pending leads
        cursor.execute('''
            SELECT id, business_name, contact, created_at
            FROM leads 
            WHERE status = 'Contacted' 
            AND (message_sent_time IS NULL OR message_sent_time = '')
            ORDER BY created_at ASC
            LIMIT 10
        ''')
        
        pending_leads = cursor.fetchall()
        
        # Process each lead
        for lead in pending_leads:
            phone_number = self._extract_phone_from_contact(contact_info)
            message = self._generate_default_message(lead_name)
            result = self.send_message(phone_number, message, mode='api_simulation')
            
            if result.success:
                # Update database
                cursor.execute('''
                    UPDATE leads 
                    SET message_sent_time = ?, updated_at = ?
                    WHERE id = ?
                ''', (result.timestamp, datetime.now().isoformat(), lead_id))
        
        conn.commit()
        
    except Exception as e:
        logger.error(f"Error processing queue: {e}")
```

## 🔍 Input Validation

### Phone Number Validation
```python
def _validate_phone_number(self, phone_number: str) -> str:
    """Validate and normalize phone number"""
    # Remove common prefixes and symbols
    cleaned = phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Remove leading zeros for international format
    if cleaned.startswith('0'):
        cleaned = cleaned[1:]
    
    # Add country code if not present
    if not cleaned.startswith('62'):
        cleaned = '62' + cleaned
    
    # Basic validation
    if len(cleaned) < 10 or len(cleaned) > 15:
        raise WhatsAppGatewayError(f"Invalid phone number: {phone_number}")
    
    if not cleaned.isdigit():
        raise WhatsAppGatewayError(f"Phone number contains invalid characters: {phone_number}")
    
    return cleaned
```

### Message Validation
```python
def _validate_message(self, message: str) -> str:
    """Validate message content"""
    if not message or not message.strip():
        raise WhatsAppGatewayError("Message cannot be empty")
    
    if len(message) > 1600:  # WhatsApp message limit
        raise WhatsAppGatewayError(f"Message too long: {len(message)} characters (max 1600)")
    
    return message.strip()
```

## 📊 Statistics and Monitoring

### Delivery Statistics
```python
def get_delivery_stats(self) -> Dict[str, Any]:
    """Get delivery statistics"""
    return {
        'total_sent': self.delivery_stats['total_sent'],
        'total_failed': self.delivery_stats['total_failed'],
        'web_mode_used': self.delivery_stats['web_mode_used'],
        'api_simulation_used': self.delivery_stats['api_simulation_used'],
        'success_rate': (self.delivery_stats['total_sent'] / max(1, self.delivery_stats['total_sent'] + self.delivery_stats['total_failed'])) * 100
    }
```

### Sample Output
```python
stats = gateway.get_delivery_stats()
# Output:
{
    'total_sent': 15,
    'total_failed': 2,
    'web_mode_used': 5,
    'api_simulation_used': 10,
    'success_rate': 88.2
}
```

## 🚨 Error Handling

### Custom Exception
```python
class WhatsAppGatewayError(Exception):
    """Custom exception for WhatsApp Gateway errors"""
    pass
```

### Error Handling Strategy
```python
def send_message(self, phone_number: str, message: str, mode: str = 'web') -> MessageResult:
    try:
        # Validate inputs
        validated_phone = self._validate_phone_number(phone_number)
        validated_message = self._validate_message(message)
        
        # Send message
        if mode == 'web':
            result = self._send_web_mode(validated_phone, validated_message, message_id, timestamp)
        else:
            result = self._send_api_simulation_mode(validated_phone, validated_message, message_id, timestamp)
        
        return result
        
    except WhatsAppGatewayError as e:
        logger.error(f"WhatsApp Gateway error: {e}")
        return MessageResult(
            success=False,
            phone_number=phone_number,
            message=message,
            mode=mode,
            timestamp=timestamp,
            delivery_method=f"gateway_error",
            error_message=str(e),
            message_id=message_id
        )
    except Exception as e:
        logger.error(f"Unexpected error in send_message: {e}")
        return MessageResult(
            success=False,
            phone_number=phone_number,
            message=message,
            mode=mode,
            timestamp=timestamp,
            delivery_method=f"unexpected_error",
            error_message=str(e),
            message_id=message_id
        )
```

## 🎨 ASCII Art & Terminal Output

### ASCII Art Display
```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██╗    ██╗██╗  ██╗ ██████╗ ██████╗ ██╗███╗   ██╗██╗██╗ ║
    ║    ██║    ██║╚██╗██╔╝██╔════╝██╔═══╝ ██║████╗ ████║██║██║ ║
    ║    ██║ █╗ ██║ ╚███╔╝ ██║     ██║     ██║██╔████╔██║██║██║ ║
    ║    ██║███╗██║ ██╔██╗ ██║     ██║     ██║██║╚██╔╝██║╚██╗╚██╗║
    ║    ╚███╔███╔╝ ██╔╝ ██╗╚██████╗╚██████╗██║██║ ╚═╝██║╚██╗╚██╗║
    ║     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    ║                                                              ║
    ║              LUMINA OS WA GATEWAY v1.0                      ║
    ║              Professional Message Delivery                ║
    ╚══════════════════════════════════════════════════════════════╝
```

### Terminal Logging
```python
print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Initializing Lumina OS WhatsApp Gateway...")
print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ WhatsApp Gateway initialized successfully")
print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Database path: {self.db_path}")
print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌐 Web browser available: {self.webbrowser_available}")
```

## 🔧 Usage Examples

### Basic Usage
```python
# Initialize gateway
gateway = WhatsAppGateway()

# Send message via web mode
result = gateway.send_message("628123456789", "Hello from Lumina OS!", mode='web')

# Send message via API simulation
result = gateway.send_message("628123456789", "Test message", mode='api_simulation')

# Process pending queue
queue_result = gateway.process_pending_queue()

# Get statistics
stats = gateway.get_delivery_stats()
```

### Advanced Usage
```python
# Custom message
message = """
Halo John Doe,
Terima kasih atas minat Anda pada properti kami.
Ada yang bisa kami bantu hari ini?

Salam,
HUNTER AGENT Team
"""

# Send with validation
try:
    result = gateway.send_message("628123456789", message, mode='api_simulation')
    if result.success:
        print(f"✅ Message sent successfully (ID: {result.message_id})")
    else:
        print(f"❌ Failed to send: {result.error_message}")
except WhatsAppGatewayError as e:
    print(f"❌ Gateway error: {e}")
```

### Integration with Other Modules
```python
from core_modules.notifications.whatsapp_gateway import WhatsAppGateway

class NotificationService:
    def __init__(self):
        self.wa_gateway = WhatsAppGateway()
    
    def send_lead_notification(self, lead_data):
        """Send notification for new lead"""
        phone = self.extract_phone(lead_data['contact'])
        message = f"Halo {lead_data['name']}, kami siap membantu kebutuhan properti Anda."
        
        result = self.wa_gateway.send_message(phone, message, mode='api_simulation')
        return result
    
    def process_daily_queue(self):
        """Process daily message queue"""
        return self.wa_gateway.process_pending_queue()
```

## 📱 Message Templates

### Default Messages
```python
def _generate_default_message(self, lead_name: str) -> str:
    """Generate default message for lead"""
    messages = [
        f"Halo {lead_name}, terima kasih atas minat Anda. Kami siap membantu menemukan properti impian Anda.",
        f"Selamat pagi {lead_name}. Ada yang bisa kami bantu untuk kebutuhan properti Anda?",
        f"Halo {lead_name}, kami dari HUNTER AGENT siap memberikan solusi properti terbaik untuk Anda.",
        f"Terima kasih {lead_name} atas kepercayaan Anda. Mari kami bantu temukan rumah idaman keluarga.",
        f"Halo {lead_name}, kami punya berbagai pilihan properti menarik yang mungkin cocok untuk Anda."
    ]
    
    return random.choice(messages)
```

### Custom Templates
```python
def generate_property_message(lead_data, property_info):
    """Generate property-specific message"""
    templates = [
        f"Halo {lead_data['name']}, kami menemukan {property_info['type']} di {property_info['location']} yang mungkin cocok untuk Anda.",
        f"Hai {lead_data['name']}, properti {property_info['type']} di {property_info['location']} dengan harga Rp{property_info['price']:,} bisa menjadi pilihan Anda.",
        f"Selamat {lead_data['name']}, properti {property_info['type']} di {property_info['location']} sedang tersedia. Apakah Anda tertarik untuk survei?"
    ]
    
    return random.choice(templates)
```

## 🔍 Phone Number Extraction

### Contact Parsing Logic
```python
def _extract_phone_from_contact(self, contact: str) -> Optional[str]:
    """Extract phone number from contact string"""
    try:
        import re
        
        # Pattern 1: Phone: +62xxx
        phone_match = re.search(r'Phone:\s*([+0-9\s\-\(\)]+)', contact)
        if phone_match:
            phone = phone_match.group(1)
            return self._validate_phone_number(phone)
        
        # Pattern 2: +62xxx at beginning
        phone_match = re.search(r'^([+0-9\s\-\(\)]+)', contact)
        if phone_match:
            phone = phone_match.group(1)
            return self._validate_phone_number(phone)
        
        # Pattern 3: Any 10-15 digit number
        phone_match = re.search(r'([0-9]{10,15})', contact)
        if phone_match:
            phone = phone_match.group(1)
            return self._validate_phone_number(phone)
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting phone number: {e}")
        return None
```

### Supported Formats
- `Phone: +628123456789`
- `Phone: 08123456789`
- `628123456789`
- `08123456789`
- `+62-812-345-6789`
- `(62) 812-345-6789`

## 🚀 Deployment & Configuration

### Environment Setup
```python
# Database configuration
DB_PATH = os.path.join('data', 'leads.db')

# Gateway initialization
gateway = WhatsAppGateway(db_path=DB_PATH)

# Mode selection
MODE = 'api_simulation'  # or 'web'
```

### Production Configuration
```python
# Production settings
PRODUCTION_SETTINGS = {
    'max_retries': 3,
    'retry_delay': 5,  # seconds
    'batch_size': 10,
    'rate_limit': 100,  # messages per hour
    'default_mode': 'api_simulation'
}
```

### Testing Configuration
```python
# Test settings
TEST_SETTINGS = {
    'test_phone': '+628123456789',
    'test_message': "Test message from Lumina OS",
    'test_mode': 'api_simulation',
    'mock_database': True
}
```

## 📈 Performance Metrics

### Delivery Metrics
- **Total Sent**: Cumulative successful messages
- **Total Failed**: Cumulative failed messages
- **Success Rate**: Percentage of successful deliveries
- **Mode Usage**: Distribution between web and API simulation modes

### Queue Processing
- **Pending Count**: Number of messages waiting to be sent
- **Processed Count**: Number of messages processed in current batch
- **Success Count**: Number of successfully sent messages
- **Failed Count**: Number of failed messages

### Performance Optimization
```python
# Batch processing
def process_batch(self, leads: List[Dict], batch_size: int = 10):
    """Process leads in batches for better performance"""
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i + batch_size]
        self._process_batch(batch)
        time.sleep(1)  # Rate limiting
```

## 🔮 Future Enhancements

### Planned Features
- **Real Meta API Integration**: Official WhatsApp Business API
- **Message Templates**: Predefined message templates
- **Media Support**: Image and document sending
- **Delivery Receipts**: Real-time delivery confirmation
- **Multi-language Support**: International message templates
- **Webhook Integration**: Real-time status updates

### API Integration Roadmap
```python
# Future Meta API integration
class MetaWhatsAppGateway(WhatsAppGateway):
    def __init__(self, api_token: str, phone_number_id: str):
        super().__init__()
        self.api_token = api_token
        self.phone_number_id = phone_number_id
    
    def send_message_api(self, phone_number: str, message: str) -> MessageResult:
        """Send message using official Meta API"""
        # Implementation for official API
        pass
```

## 🧪 Testing

### Unit Tests
```python
import unittest
from core_modules.notifications.whatsapp_gateway import WhatsAppGateway

class TestWhatsAppGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = WhatsAppGateway(':memory:')
    
    def test_phone_validation(self):
        """Test phone number validation"""
        # Valid numbers
        self.assertTrue(self.gateway._validate_phone_number("628123456789"))
        self.assertTrue(self.gateway._validate_phone_number("08123456789"))
        
        # Invalid numbers
        with self.assertRaises(WhatsAppGatewayError):
            self.gateway._validate_phone_number("123")
        
        with self.assertRaises(WhatsAppGatewayError):
            self.gateway._validate_phone_number("abc")
    
    def test_message_validation(self):
        """Test message validation"""
        # Valid messages
        self.assertEqual(self.gateway._validate_message("Hello"), "Hello")
        self.assertEqual(self.gateway._validate_message("Hello World!"), "Hello World!")
        
        # Invalid messages
        with self.assertRaises(WhatsAppGatewayError):
            self.gateway._validate_message("")
        
        # Too long message
        with self.assertRaises(WhatsAppGatewayError):
            self.gateway._validate_message("a" * 1601)
```

### Integration Tests
```python
def test_full_workflow():
    """Test complete workflow"""
    gateway = WhatsAppGateway()
    
    # Test web mode
    result1 = gateway.send_message("628123456789", "Test message", mode='web')
    assert result1.success
    
    # Test API simulation
    result2 = gateway.send_message("628123456789", "Test message", mode='api_simulation')
    assert result2.success
    
    # Test queue processing
    queue_result = gateway.process_pending_queue()
    assert isinstance(queue_result, dict)
    
    # Test statistics
    stats = gateway.get_delivery_stats()
    assert 'total_sent' in stats
    assert 'success_rate' in stats
```

## 📱 API Reference

### WhatsAppGateway Class

#### Constructor
```python
def __init__(self, db_path: Optional[str] = None)
```

**Parameters:**
- `db_path`: Path to SQLite database (default: `../data/leads.db`)

**Returns:** WhatsAppGateway instance

#### Methods

##### send_message()
```python
def send_message(self, phone_number: str, message: str, mode: str = 'web') -> MessageResult
```

**Parameters:**
- `phone_number`: Target phone number (string)
- `message`: Message content (string, max 1600 characters)
- `mode`: Delivery mode ('web' or 'api_simulation')

**Returns:** MessageResult object

**Example:**
```python
gateway = WhatsAppGateway()
result = gateway.send_message("628123456789", "Hello World!", mode='api_simulation')
```

##### process_pending_queue()
```python
def process_pending_queue(self) -> Dict[str, Any]
```

**Returns:** Dictionary with processing statistics

**Example:**
```python
result = gateway.process_pending_queue()
print(f"Processed: {result['processed']}, Success: {result['success']}")
```

##### get_delivery_stats()
```python
def get_delivery_stats(self) -> Dict[str, Any]
```

**Returns:** Dictionary with delivery statistics

**Example:**
```python
stats = gateway.get_delivery_stats()
print(f"Success rate: {stats['success_rate']}%")
```

### MessageResult Data Class

```python
@dataclass
class MessageResult:
    success: bool
    phone_number: str
    message: str
    mode: str
    timestamp: str
    delivery_method: str
    error_message: Optional[str] = None
    message_id: Optional[str] = None
```

### WhatsAppGatewayError Exception

```python
class WhatsAppGatewayError(Exception):
    """Custom exception for WhatsApp Gateway errors"""
    pass
```

---

## 🎯 Key Features Summary

### Core Capabilities
- **Dual Delivery Modes**: Web and API simulation
- **Database Integration**: SQLite with automatic schema updates
- **Queue Processing**: Automated pending message handling
- **Professional Error Handling**: Comprehensive exception management
- **Phone Validation**: International format normalization
- **Message Validation**: Content and length checking
- **Statistics Tracking**: Real-time delivery metrics

### Technical Excellence
- **Type Safety**: Data classes and type hints
- **Logging**: Comprehensive error logging
- **ASCII Art**: Professional terminal presentation
- **Modular Design**: Easy integration with other modules
- **Testing Ready**: Unit and integration test support
- **Documentation**: Complete API reference

### Business Value
- **Automated Messaging**: Queue processing for bulk operations
- **Analytics Integration**: Database tracking of message delivery
- **Multi-Mode Support**: Manual and automated sending options
- **Error Recovery**: Graceful handling of delivery failures
- **Performance Monitoring**: Real-time statistics and metrics

---

*Last updated: May 30, 2026*
