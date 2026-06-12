#!/usr/bin/env python3
"""
Google Sheets Connector - Dashboard Bridge Module

This module provides integration between HUNTER_AGENT_AI_MARKETING_DIGITAL and Google Sheets
for real-time data synchronization and dashboard functionality.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL Team
Version: 2.0.0
"""

import os
import json
import logging
import time
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import gspread
from gspread.exceptions import SpreadsheetNotFound, APIError, NoValidUrlKey
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging with colored output for warnings/errors
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for warnings and errors"""
    
    COLORS = {
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[91m', # Red
        'INFO': '\033[94m',    # Blue
        'DEBUG': '\033[92m',   # Green
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to the entire message
        return f"{log_color}{formatted}{reset_color}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_logs/sheets_connector.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Apply colored formatter to console handler
for handler in logging.root.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)

class GoogleSheetsConnector:
    """
    Google Sheets integration for real-time data synchronization
    
    This class provides comprehensive integration with Google Sheets API for
    lead management, analytics synchronization, and dashboard functionality.
    """
    
    def __init__(self):
        """
        Initialize Google Sheets Connector with Pre-check System
        
        Performs pre-check for credentials file existence and loads configuration.
        Uses service account authentication for secure API access.
        """
        self.logger = logging.getLogger(__name__)
        
        # Load configuration from environment variables
        self.credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'config/google_sheets_credentials.json')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID', '')
        self.spreadsheet_url = os.getenv('GOOGLE_SHEETS_URL', '')
        
        # API scopes for Google Sheets and Drive access
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Initialize connection variables
        self.creds = None
        self.client = None
        self.spreadsheet = None
        self.last_connection_time = None
        self.connection_retry_count = 0
        self.max_retry_attempts = 3
        
        # Rate limiting configuration
        self.rate_limit_delay = 1.0  # seconds between API calls
        self.last_api_call_time = 0
        
        # Module status flag
        self.module_active = True
        
        # PRE-CHECK: Verify credentials file exists
        if not self._precheck_credentials():
            self.module_active = False
            return
        
        # Initialize connection
        self._load_credentials()
        self.logger.info("Google Sheets Connector initialized successfully")
    
    def _precheck_credentials(self) -> bool:
        """
        Pre-check system for credentials file existence
        
        Returns:
            bool: True if credentials file exists, False otherwise
        """
        try:
            # Check if credentials file exists
            if not os.path.exists(self.credentials_path):
                # Display colored warning message
                warning_msg = f"[WARNING] Kredensial Google Sheets tidak ditemukan di: {self.credentials_path}"
                self.logger.warning(warning_msg)
                
                # Additional helpful information
                info_msg = "[INFO] Modul Google Sheets Connector dinonaktifkan sementara."
                self.logger.info(info_msg)
                
                setup_msg = "[INFO] Untuk mengaktifkan modul ini:"
                self.logger.info(setup_msg)
                self.logger.info(f"[INFO] 1. Buat file kredensial JSON dari Google Cloud Console")
                self.logger.info(f"[INFO] 2. Simpan sebagai: {self.credentials_path}")
                self.logger.info(f"[INFO] 3. Pastikan environment variable GOOGLE_SHEETS_CREDENTIALS sudah di-set")
                
                return False
            
            # Check if file is readable
            try:
                with open(self.credentials_path, 'r') as f:
                    # Try to parse as JSON to verify it's valid
                    json.load(f)
                
                success_msg = f"[SUCCESS] Kredensial Google Sheets ditemukan dan valid: {self.credentials_path}"
                self.logger.info(success_msg)
                return True
                
            except json.JSONDecodeError:
                error_msg = f"[ERROR] File kredensial tidak valid (bukan format JSON): {self.credentials_path}"
                self.logger.error(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"[ERROR] Error saat mengecek kredensial: {e}"
            self.logger.error(error_msg)
            return False
    
    def _load_credentials(self) -> bool:
        """
        Load Google Sheets credentials from JSON file
        
        Returns:
            bool: True if credentials loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.credentials_path):
                self.logger.error(f"Credentials file not found: {self.credentials_path}")
                return False
            
            # Load service account credentials
            self.creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.scopes
            )
            
            self.logger.info(f"Credentials loaded successfully from: {self.credentials_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading credentials: {e}")
            self.creds = None
            return False
    
    def _rate_limit_check(self):
        """
        Implement rate limiting to avoid API quota exhaustion
        
        Adds delay between API calls to respect Google Sheets API limits.
        """
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call_time
        
        if time_since_last_call < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_call
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_api_call_time = time.time()
    
    def connect(self) -> bool:
        """
        Authenticate and connect to Google Sheets
        
        Establishes connection to Google Sheets API using service account credentials.
        Handles connection errors and implements retry logic.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Check if module is active
            if not self.module_active:
                self.logger.warning("[DISABLED] Google Sheets Connector module tidak aktif. Silakan setup kredensial terlebih dahulu.")
                return False
            
            if not self.creds:
                self.logger.error("No credentials available for connection")
                return False
            
            # Implement rate limiting
            self._rate_limit_check()
            
            # Authorize and create client
            self.client = gspread.authorize(self.creds)
            
            # Open spreadsheet by ID or URL
            if self.spreadsheet_id:
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                self.logger.info(f"Connected to spreadsheet by ID: {self.spreadsheet_id}")
            elif self.spreadsheet_url:
                self.spreadsheet = self.client.open_by_url(self.spreadsheet_url)
                self.logger.info(f"Connected to spreadsheet by URL: {self.spreadsheet_url}")
            else:
                self.logger.error("No spreadsheet ID or URL provided in environment variables")
                return False
            
            self.last_connection_time = datetime.now()
            self.connection_retry_count = 0
            
            # Test connection by getting spreadsheet title
            title = self.spreadsheet.title
            self.logger.info(f"Successfully connected to spreadsheet: {title}")
            
            return True
            
        except NoValidUrlKey:
            self.logger.error("Invalid spreadsheet URL provided")
            return False
        except SpreadsheetNotFound:
            self.logger.error("Spreadsheet not found. Check ID/URL and permissions.")
            return False
        except APIError as e:
            self.logger.error(f"Google Sheets API error: {e}")
            return self._handle_connection_error(e)
        except RefreshError as e:
            self.logger.error(f"Token refresh error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during connection: {e}")
            return self._handle_connection_error(e)
    
    def _handle_connection_error(self, error: Exception) -> bool:
        """
        Handle connection errors with retry logic
        
        Args:
            error: The exception that occurred
            
        Returns:
            bool: True if retry should be attempted, False otherwise
        """
        self.connection_retry_count += 1
        
        if self.connection_retry_count <= self.max_retry_attempts:
            wait_time = 2 ** self.connection_retry_count  # Exponential backoff
            self.logger.warning(f"Connection attempt {self.connection_retry_count} failed. Retrying in {wait_time} seconds...")
            self.logger.debug(f"Error details: {error}")
            
            time.sleep(wait_time)
            return self.connect()
        else:
            self.logger.error(f"Max retry attempts ({self.max_retry_attempts}) exceeded. Connection failed.")
            return False
    
    def _get_or_create_worksheet(self, worksheet_name: str, headers: List[str]) -> Optional[Any]:
        """
        Get existing worksheet or create new one with headers
        
        Args:
            worksheet_name: Name of the worksheet
            headers: List of column headers
            
        Returns:
            Worksheet object or None if failed
        """
        try:
            if not self.spreadsheet:
                self.logger.error("No spreadsheet connected")
                return None
            
            # Implement rate limiting
            self._rate_limit_check()
            
            try:
                # Try to get existing worksheet
                worksheet = self.spreadsheet.worksheet(worksheet_name)
                self.logger.debug(f"Found existing worksheet: {worksheet_name}")
                return worksheet
            except gspread.exceptions.WorksheetNotFound:
                # Create new worksheet
                worksheet = self.spreadsheet.add_worksheet(
                    title=worksheet_name,
                    rows="1000",
                    cols=len(headers)
                )
                
                # Add headers
                header_range = f"A1:{chr(ord('A') + len(headers) - 1)}1"
                worksheet.update(header_range, [headers])
                
                # Format headers
                worksheet.format(header_range, {
                    'textFormat': {
                        'bold': True,
                        'fontSize': 12,
                        'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                    },
                    'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
                })
                
                self.logger.info(f"Created new worksheet: {worksheet_name} with headers: {headers}")
                return worksheet
                
        except Exception as e:
            self.logger.error(f"Error getting/creating worksheet {worksheet_name}: {e}")
            return None
    
    def push_new_lead(self, lead_data: Dict) -> bool:
        """
        Insert a new lead row into the Leads worksheet
        
        Args:
            lead_data: Dictionary containing lead information with keys:
                - nama: Lead name (required)
                - no_hp: Phone number (required)
                - skor_ai: AI score (optional)
                - status: Lead status (optional)
                - sumber: Lead source (optional)
                - lokasi: Location (optional)
                - catatan: Notes (optional)
        
        Returns:
            bool: True if lead inserted successfully, False otherwise
        """
        try:
            # Check if module is active
            if not self.module_active:
                self.logger.warning("[DISABLED] Google Sheets Connector tidak aktif. Lead tidak disimpan ke Google Sheets.")
                return False
            
            if not self.connect():
                return False
            
            # Define worksheet configuration
            worksheet_name = "Leads"
            headers = ["Timestamp", "Nama", "No HP", "Skor AI", "Status", "Sumber", "Lokasi", "Catatan"]
            
            # Get or create worksheet
            worksheet = self._get_or_create_worksheet(worksheet_name, headers)
            if not worksheet:
                return False
            
            # Prepare lead data with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [
                timestamp,
                lead_data.get('nama', ''),
                lead_data.get('no_hp', ''),
                lead_data.get('skor_ai', 0),
                lead_data.get('status', 'New'),
                lead_data.get('sumber', 'Manual'),
                lead_data.get('lokasi', ''),
                lead_data.get('catatan', '')
            ]
            
            # Find next empty row
            try:
                next_row = len(worksheet.get_all_values()) + 1
            except:
                next_row = 2  # Start after headers
            
            # Insert new row
            cell_range = f"A{next_row}:{chr(ord('A') + len(row_data) - 1)}{next_row}"
            worksheet.update(cell_range, [row_data])
            
            self.logger.info(f"Successfully inserted new lead: {lead_data.get('nama', 'Unknown')} in row {next_row}")
            return True
            
        except APIError as e:
            self.logger.error(f"Google Sheets API error while inserting lead: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inserting new lead: {e}")
            return False
    
    def sync_all_from_sqlite(self, db_path: str) -> bool:
        """
        Sync all leads from SQLite database to Google Sheets
        
        Args:
            db_path: Path to SQLite database file
            
        Returns:
            bool: True if sync successful, False otherwise
        """
        try:
            # Check if module is active
            if not self.module_active:
                self.logger.warning("[DISABLED] Google Sheets Connector tidak aktif. Sync ke Google Sheets dibatalkan.")
                return False
            
            if not self.connect():
                return False
            
            # Connect to SQLite database
            try:
                conn = # SQLite connection removed
                cursor = conn.cursor()
                
                # Get all leads from database
                # cursor.execute() removed"""
                    SELECT id, url, title, content_snippet, score, source, timestamp, 
                           status, contact_info, urgency_score, potential_value, 
                           data_quality_score, location, lead_type, query_used
                    FROM leads 
                    ORDER BY timestamp DESC
                """)
                
                leads = cursor.fetchall()
                # conn.close() removed
                
                self.logger.info(f"Retrieved {len(leads)} leads from SQLite database")
                
            except sqlite3.Error as e:
                self.logger.error(f"SQLite error: {e}")
                return False
            
            if not leads:
                self.logger.info("No leads found in database")
                return True
            
            # Prepare worksheet
            worksheet_name = "All Leads"
            headers = [
                "ID", "URL", "Title", "Content", "Score", "Source", "Timestamp",
                "Status", "Contact Info", "Urgency", "Value", "Quality",
                "Location", "Type", "Query Used"
            ]
            
            worksheet = self._get_or_create_worksheet(worksheet_name, headers)
            if not worksheet:
                return False
            
            # Clear existing data (except headers)
            try:
                worksheet.delete_rows(2, worksheet.row_count)
            except:
                pass  # Worksheet might be empty
            
            # Prepare data for batch upload
            rows_data = []
            for lead in leads:
                row = [
                    lead[0],  # id
                    lead[1],  # url
                    lead[2],  # title
                    lead[3],  # content_snippet
                    lead[4],  # score
                    lead[5],  # source
                    lead[6],  # timestamp
                    lead[7],  # status
                    lead[8],  # contact_info
                    lead[9],  # urgency_score
                    lead[10], # potential_value
                    lead[11], # data_quality_score
                    lead[12], # location
                    lead[13], # lead_type
                    lead[14]  # query_used
                ]
                rows_data.append(row)
            
            # Batch upload with rate limiting
            batch_size = 100  # Process in batches to avoid rate limits
            total_uploaded = 0
            
            for i in range(0, len(rows_data), batch_size):
                batch = rows_data[i:i + batch_size]
                
                # Implement rate limiting between batches
                self._rate_limit_check()
                
                # Calculate range for this batch
                start_row = i + 2  # +2 for headers and 1-based indexing
                end_row = start_row + len(batch) - 1
                cell_range = f"A{start_row}:{chr(ord('A') + len(headers) - 1)}{end_row}"
                
                # Upload batch
                worksheet.update(cell_range, batch)
                total_uploaded += len(batch)
                
                self.logger.info(f"Uploaded batch {i//batch_size + 1}: {len(batch)} leads (total: {total_uploaded})")
                
                # Add small delay between batches
                time.sleep(0.5)
            
            self.logger.info(f"Successfully synced {total_uploaded} leads from SQLite to Google Sheets")
            return True
            
        except APIError as e:
            self.logger.error(f"Google Sheets API error during sync: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error syncing from SQLite: {e}")
            return False
    
    def get_worksheet_data(self, worksheet_name: str) -> List[Dict]:
        """
        Get all data from a specific worksheet
        
        Args:
            worksheet_name: Name of the worksheet
            
        Returns:
            List of dictionaries containing row data
        """
        try:
            if not self.connect():
                return []
            
            worksheet = self.spreadsheet.worksheet(worksheet_name)
            all_data = worksheet.get_all_records()
            
            self.logger.info(f"Retrieved {len(all_data)} records from worksheet: {worksheet_name}")
            return all_data
            
        except Exception as e:
            self.logger.error(f"Error getting data from worksheet {worksheet_name}: {e}")
            return []
    
    def update_cell(self, worksheet_name: str, cell_range: str, value: Any) -> bool:
        """
        Update a specific cell in a worksheet
        
        Args:
            worksheet_name: Name of the worksheet
            cell_range: Cell range (e.g., "A1", "B5")
            value: Value to set
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            if not self.connect():
                return False
            
            worksheet = self.spreadsheet.worksheet(worksheet_name)
            worksheet.update(cell_range, value)
            
            self.logger.info(f"Updated cell {cell_range} in worksheet {worksheet_name} with value: {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating cell {cell_range}: {e}")
            return False
    
    def get_connection_status(self) -> Dict:
        """
        Get current connection status and statistics
        
        Returns:
            Dictionary containing connection status information
        """
        status = {
            'connected': self.spreadsheet is not None,
            'last_connection': self.last_connection_time.isoformat() if self.last_connection_time else None,
            'retry_count': self.connection_retry_count,
            'credentials_loaded': self.creds is not None,
            'spreadsheet_title': None,
            'worksheet_count': 0
        }
        
        if self.spreadsheet:
            try:
                status['spreadsheet_title'] = self.spreadsheet.title
                status['worksheet_count'] = len(self.spreadsheet.worksheets())
            except:
                pass
        
        return status

def sync_leads_to_sheets_mock(db_path: str = 'data/database/leads.db (SQLite - removed)) -> bool:
    """
    Mock simulation function for Google Sheets sync
    Simulates API calls with local database operations and hacker-style logging
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        True if mock sync successful, False otherwise
    """
    # ANSI Color Codes for hacker-style logging
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    try:
        print(f"{GREEN}🚀 GOOGLE SHEETS SYNC INITIATED{END}")
        print(f"{CYAN}├── Mode: MOCK SIMULATION{END}")
        print(f"{CYAN}├── Database: {db_path}{END}")
        print(f"{CYAN}├── Target: Google Sheets{END}")
        
        # Ensure database directory exists
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to SQLite database
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Create leads table if not exists (for demo)
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT,
                contact TEXT,
                phone TEXT,
                email TEXT,
                score REAL,
                status TEXT,
                source TEXT,
                location TEXT,
                date_found TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data if table is empty
        # cursor.execute() removed"SELECT COUNT(*) FROM leads")
        lead_count = cursor.fetchone()[0]
        
        if lead_count == 0:
            print(f"{YELLOW}├── No leads found. Inserting sample data...{END}")
            sample_leads = [
                ('PT. Maju Jaya Properti', 'Budi Santoso', '08123456789', 'budi@maju.com', 8.5, 'hot', 'web_scraping', 'Jakarta', '2024-05-28'),
                ('CV. Sejahtera Bersama', 'Andi Wijaya', '08123456790', 'andi@sejahtera.com', 7.2, 'warm', 'referral', 'Tangerang', '2024-05-28'),
                ('PT. Prima Property', 'Cahyo Prabowo', '08123456791', 'cahyo@prima.com', 6.8, 'cold', 'social_media', 'Bekasi', '2024-05-28'),
                ('CV. Mitra Properti', 'Diana Putri', '08123456792', 'diana@mitra.com', 9.1, 'hot', 'web_scraping', 'Depok', '2024-05-28'),
                ('PT. Harapan Baru', 'Eko Kusumo', '08123456793', 'eko@harapan.com', 5.5, 'cold', 'walk_in', 'Bogor', '2024-05-28'),
                ('CV. Sukses Mandiri', 'Rina Susanti', '08123456794', 'rina@sukses.com', 7.8, 'warm', 'referral', 'Bandung', '2024-05-28'),
                ('PT. Karya Bersama', 'Ahmad Fauzi', '08123456795', 'ahmad@karya.com', 8.2, 'hot', 'web_scraping', 'Semarang', '2024-05-28'),
                ('CV. Jaya Abadi', 'Siti Nurhaliza', '08123456796', 'siti@jaya.com', 6.5, 'cold', 'social_media', 'Surabaya', '2024-05-28'),
                ('PT. Berkah Property', 'Muhammad Rizki', '08123456797', 'rizki@berkah.com', 7.9, 'warm', 'referral', 'Yogyakarta', '2024-05-28'),
                ('CV. Sukses Mandiri', 'Rina Susanti', '08123456794', 'rina@sukses.com', 7.8, 'warm', 'referral', 'Bandung', '2024-05-28')
            ]
            
            cursor.executemany('''
                INSERT INTO leads (business_name, contact, phone, email, score, status, source, location, date_found)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_leads)
            
            # conn.commit() removed
            print(f"{GREEN}├── Sample data inserted: {len(sample_leads)} leads{self.END}")
        
        # Get all leads from database
        # cursor.execute() removed'''
            SELECT business_name, contact, phone, email, score, status, source, location, date_found
            FROM leads 
            ORDER BY score DESC
        ''')
        
        leads = cursor.fetchall()
        # conn.close() removed
        
        if not leads:
            print(f"{YELLOW}└── No leads to sync{self.END}")
            return True
        
        # Format data for Google Sheets (array of arrays)
        headers = ['Business Name', 'Contact', 'Phone', 'Email', 'Score', 'Status', 'Source', 'Location', 'Date Found']
        sheets_data = [headers]
        
        for lead in leads:
            row = list(lead)
            sheets_data.append(row)
        
        # Mock sync to Google Sheets
        print(f"{CYAN}├── Processing {len(leads)} leads...{self.END}")
        print(f"{CYAN}├── Formatting data for Sheets API...{self.END}")
        
        # Simulate API call delay
        import time
        time.sleep(1)
        
        # Mock success response
        mock_url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        print(f"{GREEN}✅ {len(leads)} Leads successfully synced to Google Sheets: {mock_url}{self.END}")
        print(f"{CYAN}├── Sheet URL: {mock_url}{self.END}")
        print(f"{CYAN}├── Range: A1:{chr(ord('A') + len(headers) - 1)}{len(leads) + 1}{self.END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.END}")
        print(f"{YELLOW}└── Status: MOCK COMPLETED{self.END}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"{RED}❌ DATABASE ERROR: {e}{END}")
        return False
    except Exception as e:
        print(f"{RED}❌ SYNC ERROR: {e}{END}")
        return False

def main():
    """
    Main function for testing Google Sheets Connector
    """
    print("=" * 60)
    print("📊 GOOGLE SHEETS CONNECTOR - DASHBOARD BRIDGE")
    print("=" * 60)
    
    # Test mock sync first
    print("\n🔄 Testing mock sync...")
    mock_success = sync_leads_to_sheets_mock()
    if mock_success:
        print("✅ Mock sync test successful")
    else:
        print("❌ Mock sync test failed")
    
    # Initialize connector
    connector = GoogleSheetsConnector()
    
    # Test connection
    print("\n🔐 Testing Google Sheets connection...")
    status = connector.get_connection_status()
    
    if status['connected']:
        print("✅ Google Sheets connection successful")
        print(f"📋 Spreadsheet: {status['spreadsheet_title']}")
        print(f"📊 Worksheets: {status['worksheet_count']}")
        
        # Test inserting a new lead
        print("\n📝 Testing new lead insertion...")
        test_lead = {
            'nama': 'Test Lead',
            'no_hp': '0812-3456-7890',
            'skor_ai': 8.5,
            'status': 'Test',
            'sumber': 'Manual Test',
            'lokasi': 'Serang',
            'catatan': 'This is a test lead from connector'
        }
        
        lead_success = connector.push_new_lead(test_lead)
        if lead_success:
            print("✅ Test lead inserted successfully")
        else:
            print("❌ Failed to insert test lead")
        
        # Test SQLite sync (if database exists)
        db_path = "data/leads.db (SQLite - removed)
        if os.path.exists(db_path):
            print("\n🔄 Testing SQLite sync...")
            sync_success = connector.sync_all_from_sqlite(db_path)
            if sync_success:
                print("✅ SQLite sync successful")
            else:
                print("❌ Failed to sync from SQLite")
        else:
            print(f"\n📁 SQLite database not found at: {db_path}")
        
    else:
        print("❌ Google Sheets connection failed")
        print("📝 Please check:")
        print("   - GOOGLE_SHEETS_CREDENTIALS environment variable")
        print("   - GOOGLE_SHEETS_SPREADSHEET_ID or GOOGLE_SHEETS_URL environment variable")
        print("   - Service account permissions for the spreadsheet")
    
    print("\n" + "=" * 60)
    print("✅ GOOGLE SHEETS CONNECTOR TEST COMPLETE")
    print("🔐 Mock sync test completed successfully")
    print("=" * 60)

if __name__ == "__main__":
    main()
