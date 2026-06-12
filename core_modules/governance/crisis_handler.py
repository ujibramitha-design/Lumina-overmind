#!/usr/bin/env python3
"""
Crisis Handler Module - Governance System
Advanced crisis management and negative sentiment detection system

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import json
import logging
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ANSI Color Codes for hacker-style logging
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
BOLD = '\033[1m'
BLINK = '\033[5m'
END = '\033[0m'

class CrisisLevel(Enum):
    """Crisis severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class IssueStatus(Enum):
    """Issue status tracking"""
    DETECTED = "detected"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    MONITORING = "monitoring"

@dataclass
class CrisisIssue:
    """Data class for crisis issue tracking"""
    issue_id: str
    issue_type: str
    severity: CrisisLevel
    source: str
    message: str
    detected_at: str
    escalated_at: Optional[str]
    resolved_at: Optional[str]
    assigned_to: Optional[str]
    status: IssueStatus
    sentiment_score: float  # 0-100 (negative sentiment intensity)
    keywords_found: List[str]
    raw_message: str
    metadata: Dict[str, Any]
    resolution_notes: Optional[str]

class CrisisManagementSystem:
    """
    Advanced crisis management system for negative sentiment detection and escalation
    
    This class provides comprehensive crisis detection, automated escalation,
    and issue tracking for maintaining system integrity and customer satisfaction.
    """
    
    def __init__(self):
        """Initialize CrisisManagementSystem with configuration"""
        self.logger = logging.getLogger(__name__)
        
        # Critical keywords for negative sentiment detection
        self.critical_keywords = {
            'severe': [
                'penipuan', 'kecewa', 'bocor', 'jelek', 'sampah', 'buruk',
                'menipu', 'penipu', 'hoax', 'palsu', 'tipu', 'bohong',
                'gagal', 'rusak', 'hancur', 'curi', 'maling', 'korupsi',
                'teroris', 'ancaman', 'kekerasan', 'pelecehan', 'diskriminasi'
            ],
            'moderate': [
                'lambat', 'sulit', 'masalah', 'kendala', 'error', 'bug',
                'gagal', 'terlambat', 'tidak bisa', 'bermasalah', 'kecewaan',
                'kecewa', 'kecewaan', 'kecewaan', 'kecewaan', 'kecewaan'
            ],
            'mild': [
                'kurang', 'perlu perbaiki', 'tidak sesuai', 'butuh perhatian',
                'masukan', 'saran', 'feedback', 'komentar', 'ulasan'
            ]
        }
        
        # Escalation thresholds
        self.escalation_thresholds = {
            'severe': 3,  # 3 severe keywords -> CRITICAL
            'moderate': 5,  # 5 moderate keywords -> HIGH
            'mild': 8     # 8 mild keywords -> MEDIUM
        }
        
        # Notification channels
        self.notification_channels = {
            'terminal': True,
            'database': True,
            'email': False,  # Can be enabled with email configuration
            'telegram': False  # Can be enabled with Telegram configuration
        }
        
        # Database configuration
        self.db_path = 'logs/crisis_logs.db (SQLite - removed)
        
        # Initialize database
        self._initialize_database()
        
        # Initialize notification system
        self._initialize_notifications()
        
        self.logger.info("🛡️ CrisisManagementSystem initialized with advanced threat detection")
    
    def _initialize_database(self) -> None:
        """Initialize crisis logs database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create crisis logs table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS crisis_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_id TEXT UNIQUE NOT NULL,
                    issue_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    source TEXT NOT NULL,
                    message TEXT NOT NULL,
                    sentiment_score REAL DEFAULT 0.0,
                    keywords_found TEXT,
                    raw_message TEXT NOT NULL,
                    metadata TEXT,
                    status TEXT DEFAULT 'detected',
                    detected_at TEXT NOT NULL,
                    escalated_at TEXT,
                    resolved_at TEXT,
                    assigned_to TEXT,
                    resolution_notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_crisis_severity ON crisis_logs(severity)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_crisis_status ON crisis_logs(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_crisis_detected_at ON crisis_logs(detected_at)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("🛡️ Crisis database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize crisis database: {e}")
    
    def _initialize_notifications(self) -> None:
        """Initialize notification system"""
        try:
            # Check for notification modules
            self.has_telegram = self._check_telegram_availability()
            self.has_email = self._check_email_availability()
            
            if self.has_telegram:
                self.notification_channels['telegram'] = True
                self.logger.info("📱 Telegram notifications enabled")
            
            if self.has_email:
                self.notification_channels['email'] = True
                self.logger.info("📧 Email notifications enabled")
            
            self.logger.info("🔔 Notification system initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize notifications: {e}")
    
    def _check_telegram_availability(self) -> bool:
        """Check if Telegram notification system is available"""
        try:
            # Try to import telegram module
            from core_modules.notifications.alert_manager import AlertManager
            alert_manager = AlertManager()
            return alert_manager.is_configured
        except ImportError:
            return False
        except Exception:
            return False
    
    def _check_email_availability(self) -> bool:
        """Check if email notification system is available"""
        # Placeholder for future email integration
        return False
    
    def detect_negative_sentiment(self, message: str) -> Dict[str, Any]:
        """
        Detect negative sentiment in message using advanced pattern matching
        
        Args:
            message: Input message to analyze
            
        Returns:
            Dictionary containing detection results
        """
        print(f"{GREEN}🔍 SENTIMENT ANALYSIS INITIATED{END}")
        print(f"{CYAN}├── Message Length: {len(message)} characters{END}")
        print(f"{CYAN}├── Analysis Engine: Advanced Pattern Recognition{END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        try:
            # Preprocess message
            processed_message = self._preprocess_message(message)
            
            # Detect keywords
            detected_keywords = self._detect_keywords(processed_message)
            
            # Calculate sentiment score
            sentiment_score = self._calculate_sentiment_score(detected_keywords)
            
            # Determine severity
            severity = self._determine_severity(detected_keywords)
            
            # Create detection result
            result = {
                'has_negative_sentiment': len(detected_keywords) > 0,
                'sentiment_score': sentiment_score,
                'severity': severity.value if severity else 'low',
                'keywords_found': detected_keywords,
                'message_length': len(message),
                'analysis_timestamp': datetime.now().isoformat(),
                'processed_message': processed_message[:200] + '...' if len(processed_message) > 200 else processed_message
            }
            
            # Print analysis results
            self._print_sentiment_analysis_results(result, message)
            
            return result
            
        except Exception as e:
            print(f"{RED}❌ SENTIMENT ANALYSIS ERROR: {e}{END}")
            self.logger.error(f"Error analyzing sentiment: {e}")
            
            return {
                'has_negative_sentiment': False,
                'sentiment_score': 0.0,
                'severity': 'low',
                'keywords_found': [],
                'error': str(e)
            }
    
    def _preprocess_message(self, message: str) -> str:
        """Preprocess message for analysis"""
        # Convert to lowercase
        processed = message.lower()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed)
        
        # Remove special characters except spaces and basic punctuation
        processed = re.sub(r'[^\w\s.,!?-]', '', processed)
        
        return processed.strip()
    
    def _detect_keywords(self, message: str) -> List[str]:
        """Detect negative keywords in message"""
        detected = []
        
        for category, keywords in self.critical_keywords.items():
            for keyword in keywords:
                # Use word boundaries for exact matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, message):
                    detected.append(keyword)
        
        return detected
    
    def _calculate_sentiment_score(self, keywords: List[str]) -> float:
        """Calculate sentiment score based on detected keywords"""
        if not keywords:
            return 0.0
        
        score = 0.0
        for keyword in keywords:
            if keyword in self.critical_keywords['severe']:
                score += 30  # 30 points per severe keyword
            elif keyword in self.critical_keywords['moderate']:
                score += 20  # 20 points per moderate keyword
            elif keyword in self.critical_keywords['mild']:
                score += 10  # 10 points per mild keyword
        
        # Cap at 100
        return min(score, 100.0)
    
    def _determine_severity(self, keywords: List[str]) -> Optional[CrisisLevel]:
        """Determine crisis severity based on detected keywords"""
        if not keywords:
            return None
        
        severe_count = len([k for k in keywords if k in self.critical_keywords['severe']])
        moderate_count = len([k for k in keywords if k in self.critical_keywords['moderate']])
        mild_count = len([k for k in keywords if k in self.critical_keywords['mild']])
        
        if severe_count >= self.escalation_thresholds['severe']:
            return CrisisLevel.CRITICAL
        elif moderate_count >= self.escalation_thresholds['moderate']:
            return CrisisLevel.HIGH
        elif mild_count >= self.escalation_thresholds['mild']:
            return CrisisLevel.MEDIUM
        else:
            return CrisisLevel.LOW
    
    def escalate_issue(self, issue_data: Dict[str, Any]) -> CrisisIssue:
        """
        Escalate detected issue to appropriate channels
        
        Args:
            issue_data: Dictionary containing issue information
            
        Returns:
            CrisisIssue object with escalation details
        """
        print(f"{RED}🚨 CRISIS ESCALATION INITIATED{END}")
        print(f"{MAGENTA}├── Issue Type: {issue_data.get('issue_type', 'Unknown')}{END}")
        print(f"{MAGENTA}├── Severity: {issue_data.get('severity', 'Unknown')}{END}")
        print(f"{MAGENTA}├── Source: {issue_data.get('source', 'Unknown')}{END}")
        print(f"{MAGENTA}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        try:
            # Generate unique issue ID
            issue_id = f"CRISIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(issue_data.get('message', ''))}"
            
            # Create crisis issue
            crisis_issue = CrisisIssue(
                issue_id=issue_id,
                issue_type=issue_data.get('issue_type', 'negative_sentiment'),
                severity=CrisisLevel(issue_data.get('severity', 'medium')),
                source=issue_data.get('source', 'unknown'),
                message=issue_data.get('message', ''),
                detected_at=datetime.now().isoformat(),
                escalated_at=datetime.now().isoformat(),
                resolved_at=None,
                assigned_to='crisis_manager',
                status=IssueStatus.ESCALATED,
                sentiment_score=issue_data.get('sentiment_score', 0.0),
                keywords_found=issue_data.get('keywords_found', []),
                raw_message=issue_data.get('raw_message', ''),
                metadata=issue_data.get('metadata', {}),
                resolution_notes=None
            )
            
            # Save to database
            self._save_issue_to_database(crisis_issue)
            
            # Send notifications
            self._send_escalation_notifications(crisis_issue)
            
            # Print escalation results
            self._print_escalation_results(crisis_issue)
            
            return crisis_issue
            
        except Exception as e:
            print(f"{RED}❌ ESCALATION ERROR: {e}{END}")
            self.logger.error(f"Error escalating issue: {e}")
            
            # Return basic crisis issue on error
            return CrisisIssue(
                issue_id=f"CRISIS_ERROR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                issue_type='escalation_error',
                severity=CrisisLevel.HIGH,
                source='system',
                message='Error during escalation process',
                detected_at=datetime.now().isoformat(),
                escalated_at=datetime.now().isoformat(),
                resolved_at=None,
                assigned_to='system',
                status=IssueStatus.ESCALATED,
                sentiment_score=0.0,
                keywords_found=[],
                raw_message=str(e),
                metadata={'error': True},
                resolution_notes=f"Escalation failed: {e}"
            )
    
    def _save_issue_to_database(self, crisis_issue: CrisisIssue) -> None:
        """Save crisis issue to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO crisis_logs 
                (issue_id, issue_type, severity, source, message, 
                 sentiment_score, keywords_found, raw_message, metadata, 
                 status, detected_at, escalated_at, resolved_at, 
                 assigned_to, resolution_notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                crisis_issue.issue_id,
                crisis_issue.issue_type,
                crisis_issue.severity.value,
                crisis_issue.source,
                crisis_issue.message,
                crisis_issue.sentiment_score,
                json.dumps(crisis_issue.keywords_found),
                crisis_issue.raw_message,
                json.dumps(crisis_issue.metadata),
                crisis_issue.status.value,
                crisis_issue.detected_at,
                crisis_issue.escalated_at,
                crisis_issue.resolved_at,
                crisis_issue.assigned_to,
                crisis_issue.resolution_notes,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Crisis issue {crisis_issue.issue_id} saved to database")
            
        except Exception as e:
            self.logger.error(f"Failed to save crisis issue to database: {e}")
    
    def _send_escalation_notifications(self, crisis_issue: CrisisIssue) -> None:
        """Send escalation notifications through available channels"""
        try:
            # Terminal notification (always available)
            if self.notification_channels['terminal']:
                self._send_terminal_notification(crisis_issue)
            
            # Database notification (always available)
            if self.notification_channels['database']:
                self._save_issue_to_database(crisis_issue)
            
            # Telegram notification (if available)
            if self.notification_channels['telegram']:
                self._send_telegram_notification(crisis_issue)
            
            # Email notification (if available)
            if self.notification_channels['email']:
                self._send_email_notification(crisis_issue)
                
        except Exception as e:
            self.logger.error(f"Failed to send notifications: {e}")
    
    def _send_terminal_notification(self, crisis_issue: CrisisIssue) -> None:
        """Send terminal notification with blinking effect"""
        severity_colors = {
            CrisisLevel.CRITICAL: f"{RED}{BLINK}",
            CrisisLevel.HIGH: f"{RED}",
            CrisisLevel.MEDIUM: f"{YELLOW}",
            CrisisLevel.LOW: f"{CYAN}",
            CrisisLevel.EMERGENCY: f"{MAGENTA}{BLINK}"
        }
        
        color = severity_colors.get(crisis_issue.severity, f"{WHITE}")
        
        print(f"{color}🚨 CRITICAL ALERT: Negative sentiment detected! Escalating to Human Manager immediately!{END}")
        print(f"{color}├── Issue ID: {crisis_issue.issue_id}{END}")
        print(f"{color}├── Severity: {crisis_issue.severity.value.upper()}{END}")
        print(f"{color}├── Source: {crisis_issue.source}{END}")
        print(f"{color}├── Keywords: {', '.join(crisis_issue.keywords_found)}{END}")
        print(f"{color}├── Sentiment Score: {crisis_issue.sentiment_score:.1f}/100{END}")
        print(f"{color}├── Assigned to: {crisis_issue.assigned_to}{END}")
        print(f"{color}└── Escalated at: {crisis_issue.escalated_at}{END}")
        print(f"{color}🛡️ Defense Protocol: ACTIVATED - Issue tracking and monitoring enabled{END}")
        print(f"{GREEN}└── Crisis Management System: Issue logged and escalation process initiated{END}")
    
    def _send_telegram_notification(self, crisis_issue: CrisisIssue) -> None:
        """Send Telegram notification for crisis escalation"""
        try:
            from core_modules.notifications.alert_manager import AlertManager
            
            alert_manager = AlertManager()
            
            message = f"""
🚨 CRITICAL ALERT - Crisis Management System

Issue ID: {crisis_issue.issue_id}
Severity: {crisis_issue.severity.value.upper()}
Source: {crisis_issue.source}
Detected: {crisis_issue.detected_at}

Message: {crisis_issue.message[:200]}{'...' if len(crisis_issue.message) > 200 else ''}

Keywords: {', '.join(crisis_issue.keywords_found)}
Sentiment Score: {crisis_issue.sentiment_score:.1f}/100

Action Required: IMMEDIATE ATTENTION
Assigned to: {crisis_issue.assigned_to}
            """
            
            success = alert_manager.send_telegram_alert({
                'title': f"🚨 CRISIS ALERT - {crisis_issue.severity.value.upper()}",
                'message': message,
                'priority': 'high'
            })
            
            if success:
                self.logger.info(f"Telegram notification sent for crisis {crisis_issue.issue_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
    
    def _send_email_notification(self, crisis_issue: CrisisIssue) -> None:
        """Send email notification for crisis escalation"""
        # Placeholder for future email integration
        self.logger.info(f"Email notification would be sent for crisis {crisis_issue.issue_id}")
    
    def _print_sentiment_analysis_results(self, result: Dict[str, Any], original_message: str) -> None:
        """Print sentiment analysis results"""
        if result['has_negative_sentiment']:
            print(f"{GREEN}✅ SENTIMENT ANALYSIS COMPLETE{END}")
            print(f"{CYAN}├── Negative Sentiment: DETECTED{END}")
            print(f"{CYAN}├── Sentiment Score: {result['sentiment_score']:.1f}/100{END}")
            print(f"{CYAN}├── Severity Level: {result['severity'].upper()}{END}")
            print(f"{CYAN}├── Keywords Found: {len(result['keywords_found'])}{END}")
            
            if result['keywords_found']:
                print(f"{CYAN}├── Keywords: {', '.join(result['keywords_found'])}{END}")
            
            print(f"{YELLOW}🧠 Behavioral Model: User intent indicates strong negative sentiment requiring immediate attention{END}")
        else:
            print(f"{GREEN}✅ SENTIMENT ANALYSIS COMPLETE{END}")
            print(f"{CYAN}├── Negative Sentiment: NOT DETECTED{END}")
            print(f"{CYAN}├── Sentiment Score: {result['sentiment_score']:.1f}/100{END}")
            print(f"{CYAN}├── Severity Level: {result['severity'].upper()}{END}")
            print(f"{GREEN}└── Message sentiment is neutral or positive{END}")
        
        print(f"{CYAN}└── Analysis completed in {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
    
    def _print_escalation_results(self, crisis_issue: CrisisIssue) -> None:
        """Print escalation results"""
        print(f"{GREEN}✅ CRISIS ESCALATION COMPLETE{END}")
        print(f"{CYAN}├── Issue ID: {crisis_issue.issue_id}{END}")
        print(f"{CYAN}├── Status: {crisis_issue.status.value.upper()}{END}")
        print(f"{CYAN}├── Assigned to: {crisis_issue.assigned_to}{END}")
        print(f"{CYAN}├── Database: Logged in crisis_logs.db{END}")
        print(f"{CYAN}├── Notifications: Sent to available channels{END}")
        print(f"{GREEN}└── Crisis Management System: Issue tracking and monitoring enabled{END}")
    
    def monitor_crisis_dashboard(self, hours: int = 24) -> Dict[str, Any]:
        """
        Monitor crisis dashboard with comprehensive statistics
        
        Args:
            hours: Number of hours to look back for dashboard
            
        Returns:
            Dictionary with dashboard statistics
        """
        print(f"{GREEN}📊 CRISIS DASHBOARD MONITORING{END}")
        print(f"{CYAN}├── Time Range: Last {hours} hours{END}")
        print(f"{CYAN}├── Analysis Engine: Crisis Tracking System{END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        try:
            # Get statistics from database
            stats = self._get_crisis_statistics(hours)
            
            print(f"{GREEN}✅ DASHBOARD ANALYSIS COMPLETE{END}")
            print(f"{CYAN}├── Total Issues: {stats['total_issues']}{END}")
            print(f"{CYAN}├── Critical Issues: {stats['critical_issues']}{END}")
            print(f"{CYAN}├── High Issues: {stats['high_issues']}{END}")
            print(f"{CYAN}├── Medium Issues: {stats['medium_issues']}{END}")
            print(f"{CYAN}├── Low Issues: {stats['low_issues']}{END}")
            print(f"{CYAN}├── Resolved Issues: {stats['resolved_issues']}{END}")
            print(f"{CYAN}├── Active Issues: {stats['active_issues']}{END}")
            print(f"{CYAN}├── Average Resolution Time: {stats['avg_resolution_time']:.1f} hours{END}")
            print(f"{GREEN}└── Dashboard updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
            
            return stats
            
        except Exception as e:
            print(f"{RED}❌ DASHBOARD ERROR: {e}{END}")
            self.logger.error(f"Error generating crisis dashboard: {e}")
            
            return {
                'error': str(e),
                'total_issues': 0,
                'critical_issues': 0,
                'high_issues': 0,
                'medium_issues': 0,
                'low_issues': 0,
                'resolved_issues': 0,
                'active_issues': 0,
                'avg_resolution_time': 0.0
            }
    
    def _get_crisis_statistics(self, hours: int) -> Dict[str, Any]:
        """Get crisis statistics from database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Calculate time threshold
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            # Get total issues
            # cursor.execute() removed"SELECT COUNT(*) FROM crisis_logs WHERE detected_at >= ?", (time_threshold.isoformat(),))
            total_issues = cursor.fetchone()[0]
            
            # Get issues by severity
            # cursor.execute() removed"""
                SELECT severity, COUNT(*) 
                FROM crisis_logs 
                WHERE detected_at >= ?
                GROUP BY severity
            """, (time_threshold.isoformat(),))
            
            severity_counts = dict(cursor.fetchall())
            
            # Get resolved issues
            # cursor.execute() removed"SELECT COUNT(*) FROM crisis_logs WHERE status = 'resolved' AND detected_at >= ?", (time_threshold.isoformat(),))
            resolved_issues = cursor.fetchone()[0]
            
            # Calculate average resolution time
            # cursor.execute() removed"""
                SELECT AVG(
                    julianday(strftime('%s', 'resolved_at')) - julianday(strftime('%s', 'detected_at'))
                ) AS avg_resolution_time
                FROM crisis_logs 
                WHERE status = 'resolved' AND detected_at >= ?
            """, (time_threshold.isoformat(),))
            
            avg_resolution_result = cursor.fetchone()
            avg_resolution_time = avg_resolution_result[0] if avg_resolution_result[0] else 0.0
            
            # conn.close() removed
            
            return {
                'total_issues': total_issues,
                'critical_issues': severity_counts.get('critical', 0),
                'high_issues': severity_counts.get('high', 0),
                'medium_issues': severity_counts.get('medium', 0),
                'low_issues': severity_counts.get('low', 0),
                'resolved_issues': resolved_issues,
                'active_issues': total_issues - resolved_issues,
                'avg_resolution_time': avg_resolution_time,
                'time_range_hours': hours,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting crisis statistics: {e}")
            return {
                'error': str(e),
                'total_issues': 0,
                'critical_issues': 0,
                'high_issues': 0,
                'medium_issues': 0,
                'low_issues': 0,
                'resolved_issues': 0,
                'active_issues': 0,
                'avg_resolution_time': 0.0
            }

def main():
    """
    Main function to demonstrate CrisisManagementSystem
    """
    print("🛡️ CRISIS HANDLER - GOVERNANCE SYSTEM")
    print("=" * 60)
    print("🔐 Advanced crisis management and negative sentiment detection")
    print("=" * 60)
    
    # Initialize crisis management system
    cms = CrisisManagementSystem()
    
    # Test sentiment detection
    print("\n📊 Testing negative sentiment detection...")
    
    # Test cases
    test_messages = [
        "Produk ini sangat buruk dan penipu, saya sangat kecewa dengan pelayanan yang lambat",
        "Sistem ini bagus, tapi perlu perbaiki beberapa fitur",
        "Saya sangat puas dengan produk ini, terima kasih!",
        "Customer service sangat jelek dan tidak membantu sama sekali"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📊 Testing message {i}/{len(test_messages)}...")
        result = cms.detect_negative_sentiment(message)
        
        if result['has_negative_sentiment']:
            # Escalate the issue
            issue_data = {
                'issue_type': 'negative_sentiment',
                'severity': result['severity'],
                'source': 'customer_feedback',
                'message': message,
                'sentiment_score': result['sentiment_score'],
                'keywords_found': result['keywords_found'],
                'raw_message': message,
                'metadata': {'test_case': i}
            }
            
            crisis_issue = cms.escalate_issue(issue_data)
    
    # Test crisis dashboard
    print("\n📊 Monitoring crisis dashboard...")
    dashboard = cms.monitor_crisis_dashboard(24)
    
    print("\n" + "=" * 60)
    print("✅ CRISIS HANDLER DEMO COMPLETE")
    print("🛡️ Advanced crisis management system ready for production")
    print("=" * 60)

if __name__ == "__main__":
    main()
