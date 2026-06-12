#!/usr/bin/env python3
"""
Follow Up Manager - Closer Agent
Automated follow-up system for lead nurturing and deal tracking
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeadStatus(Enum):
    """Lead status tracking"""
    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    FOLLOW_UP_SCHEDULED = "follow_up_scheduled"

class FollowUpPriority(Enum):
    """Follow-up priority levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class FollowUpTask:
    """Follow-up task structure"""
    lead_id: str
    task_type: str
    scheduled_date: datetime
    priority: FollowUpPriority
    message_template: str
    status: str = "pending"
    completed_date: Optional[datetime] = None
    notes: str = ""

class FollowUpManager:
    """Automated follow-up management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/follow_up.db (SQLite - removed)
        self._init_database()
        
        # Follow-up templates
        self.message_templates = {
            'initial_contact': {
                'high': "Halo {name}, saya melihat Anda tertarik dengan properti di {location}. Saya bisa bantu informasi lebih lanjut.",
                'medium': "Halo {name}, terima kasih sudah menghubungi kami. Ada yang bisa saya bantu untuk properti di {location}?",
                'low': "Halo {name}, kami punya beberapa pilihan properti menarik di {location}. Mau saya kirim info?"
            },
            'follow_up_3_days': {
                'high': "Halo {name}, apakah Anda sudah sempat melihat properti yang kita diskusikan? Saya bisa bantu jadwalkan survey.",
                'medium': "Halo {name}, bagaimana proses pencarian properti Anda? Ada yang perlu saya bantu?",
                'low': "Halo {name}, kami punya promo baru untuk properti di {location}. Mau saya info?"
            },
            'follow_up_7_days': {
                'high': "Halo {name}, saya follow up karena properti yang Anda minati sedang banyak diminati. Ada baiknya segera diproses.",
                'medium': "Halo {name}, apakah Anda masih mencari properti? Kami ada beberapa unit baru di {location}.",
                'low': "Halo {name}, kami ada update harga terbaru untuk properti di {location}. Mau saya kirim?"
            },
            'negotiation_reminder': {
                'high': "Halo {name}, untuk negosiasi kemarin, apakah ada perkembangan? Saya bisa bantu proses lebih lanjut.",
                'medium': "Halo {name}, bagaimana proses negosiasi properti? Ada yang perlu saya bantu?",
                'low': "Halo {name}, apakah Anda masih tertarik dengan properti yang kita diskusikan?"
            }
        }
        
        # Follow-up schedule rules
        self.schedule_rules = {
            LeadStatus.NEW: [
                {'days': 0, 'template': 'initial_contact', 'priority': 'high'},
                {'days': 3, 'template': 'follow_up_3_days', 'priority': 'medium'},
                {'days': 7, 'template': 'follow_up_7_days', 'priority': 'low'}
            ],
            LeadStatus.CONTACTED: [
                {'days': 3, 'template': 'follow_up_3_days', 'priority': 'medium'},
                {'days': 7, 'template': 'follow_up_7_days', 'priority': 'low'}
            ],
            LeadStatus.INTERESTED: [
                {'days': 2, 'template': 'negotiation_reminder', 'priority': 'high'},
                {'days': 5, 'template': 'follow_up_3_days', 'priority': 'medium'}
            ],
            LeadStatus.NEGOTIATION: [
                {'days': 1, 'template': 'negotiation_reminder', 'priority': 'high'},
                {'days': 3, 'template': 'negotiation_reminder', 'priority': 'medium'}
            ]
        }
    
    def _init_database(self):
        """Initialize follow-up database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create follow-up tasks table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS follow_up_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    scheduled_date TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    message_template TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    completed_date TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create lead status history table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS lead_status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id TEXT NOT NULL,
                    old_status TEXT,
                    new_status TEXT NOT NULL,
                    changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_follow_up_lead_id ON follow_up_tasks(lead_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_follow_up_status ON follow_up_tasks(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_follow_up_date ON follow_up_tasks(scheduled_date)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_status_history_lead_id ON lead_status_history(lead_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Follow-up database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing follow-up database: {e}")
            raise
    
    def add_lead_from_search(self, lead_data: Dict) -> str:
        """Add lead from search results and create initial follow-up tasks"""
        try:
            lead_id = lead_data.get('id', f"lead_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Determine initial priority based on lead data
            priority = self._determine_lead_priority(lead_data)
            
            # Create initial follow-up tasks
            tasks_created = self._create_follow_up_tasks(lead_id, LeadStatus.NEW, priority)
            
            self.logger.info(f"Added lead {lead_id} with {tasks_created} follow-up tasks")
            return lead_id
            
        except Exception as e:
            self.logger.error(f"Error adding lead {lead_data.get('id', 'unknown')}: {e}")
            return ""
    
    def _determine_lead_priority(self, lead_data: Dict) -> FollowUpPriority:
        """Determine lead priority based on lead characteristics"""
        score = 0
        
        # Check for contact info
        if lead_data.get('contact_info', {}).get('phone'):
            score += 3
        if lead_data.get('contact_info', {}).get('email'):
            score += 2
        
        # Check for urgency indicators in content
        content = lead_data.get('content_snippet', '').lower()
        urgency_keywords = ['urgent', 'segera', 'butuh', 'cari', 'dijual', 'nego']
        for keyword in urgency_keywords:
            if keyword in content:
                score += 1
        
        # Check for price information
        if 'juta' in content or 'miliar' in content or 'rp' in content:
            score += 1
        
        # Determine priority
        if score >= 5:
            return FollowUpPriority.HIGH
        elif score >= 3:
            return FollowUpPriority.MEDIUM
        else:
            return FollowUpPriority.LOW
    
    def _create_follow_up_tasks(self, lead_id: str, status: LeadStatus, priority: FollowUpPriority) -> int:
        """Create follow-up tasks based on lead status and priority"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            tasks_created = 0
            rules = self.schedule_rules.get(status, [])
            
            for rule in rules:
                scheduled_date = datetime.now() + timedelta(days=rule['days'])
                
                # Adjust priority based on rule and lead priority
                task_priority = rule['priority'] if rule['priority'] != 'medium' else priority.value
                
                # Get message template
                template_category = self.message_templates.get(rule['template'], {})
                message_template = template_category.get(task_priority, template_category.get('medium', ''))
                
                # cursor.execute() removed'''
                    INSERT INTO follow_up_tasks 
                    (lead_id, task_type, scheduled_date, priority, message_template)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    lead_id,
                    rule['template'],
                    scheduled_date.isoformat(),
                    task_priority,
                    message_template
                ))
                
                tasks_created += 1
            
            # conn.commit() removed
            # conn.close() removed
            
            return tasks_created
            
        except Exception as e:
            self.logger.error(f"Error creating follow-up tasks for lead {lead_id}: {e}")
            return 0
    
    def get_pending_follow_ups(self, days_ahead: int = 1) -> List[Dict]:
        """Get pending follow-up tasks for the next N days"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            end_date = datetime.now() + timedelta(days=days_ahead)
            
            # cursor.execute() removed'''
                SELECT * FROM follow_up_tasks 
                WHERE status = 'pending' 
                AND scheduled_date <= ?
                ORDER BY priority DESC, scheduled_date ASC
            ''', (end_date.isoformat(),))
            
            columns = [desc[0] for desc in cursor.description]
            tasks = []
            
            for row in cursor.fetchall():
                task = dict(zip(columns, row))
                tasks.append(task)
            
            # conn.close() removed
            
            self.logger.info(f"Found {len(tasks)} pending follow-up tasks")
            return tasks
            
        except Exception as e:
            self.logger.error(f"Error getting pending follow-ups: {e}")
            return []
    
    def complete_follow_up(self, task_id: int, result: str, notes: str = "") -> bool:
        """Mark follow-up task as completed"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                UPDATE follow_up_tasks 
                SET status = 'completed', 
                    completed_date = ?,
                    notes = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), notes, task_id))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Completed follow-up task {task_id} with result: {result}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error completing follow-up task {task_id}: {e}")
            return False
    
    def update_lead_status(self, lead_id: str, new_status: LeadStatus, notes: str = "") -> bool:
        """Update lead status and create new follow-up tasks"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get current status
            # cursor.execute() removed'SELECT new_status FROM lead_status_history WHERE lead_id = ? ORDER BY changed_at DESC LIMIT 1', (lead_id,))
            result = cursor.fetchone()
            old_status = result[0] if result else None
            
            # Record status change
            # cursor.execute() removed'''
                INSERT INTO lead_status_history (lead_id, old_status, new_status, notes)
                VALUES (?, ?, ?, ?)
            ''', (lead_id, old_status, new_status.value, notes))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Cancel pending tasks for old status
            self._cancel_pending_tasks(lead_id)
            
            # Create new follow-up tasks for new status
            priority = self._get_lead_current_priority(lead_id)
            tasks_created = self._create_follow_up_tasks(lead_id, new_status, priority)
            
            self.logger.info(f"Updated lead {lead_id} status to {new_status.value} with {tasks_created} new tasks")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating lead {lead_id} status: {e}")
            return False
    
    def _cancel_pending_tasks(self, lead_id: str):
        """Cancel pending follow-up tasks for a lead"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                UPDATE follow_up_tasks 
                SET status = 'cancelled' 
                WHERE lead_id = ? AND status = 'pending'
            ''', (lead_id,))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error cancelling tasks for lead {lead_id}: {e}")
    
    def _get_lead_current_priority(self, lead_id: str) -> FollowUpPriority:
        """Get current priority for a lead"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                SELECT priority FROM follow_up_tasks 
                WHERE lead_id = ? AND status = 'pending'
                ORDER BY created_at DESC LIMIT 1
            ''', (lead_id,))
            
            result = cursor.fetchone()
            # conn.close() removed
            
            if result:
                return FollowUpPriority(result[0])
            else:
                return FollowUpPriority.MEDIUM
                
        except Exception as e:
            self.logger.error(f"Error getting priority for lead {lead_id}: {e}")
            return FollowUpPriority.MEDIUM
    
    def generate_follow_up_report(self) -> Dict:
        """Generate comprehensive follow-up report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get task statistics
            # cursor.execute() removed'SELECT status, COUNT(*) FROM follow_up_tasks GROUP BY status')
            task_stats = dict(cursor.fetchall())
            
            # Get upcoming tasks
            # cursor.execute() removed'''
                SELECT COUNT(*) FROM follow_up_tasks 
                WHERE status = 'pending' 
                AND scheduled_date <= ?
            ''', ((datetime.now() + timedelta(days=7)).isoformat(),))
            upcoming_tasks = cursor.fetchone()[0]
            
            # Get overdue tasks
            # cursor.execute() removed'''
                SELECT COUNT(*) FROM follow_up_tasks 
                WHERE status = 'pending' 
                AND scheduled_date < ?
            ''', (datetime.now().isoformat(),))
            overdue_tasks = cursor.fetchone()[0]
            
            # Get lead status distribution
            # cursor.execute() removed'SELECT new_status, COUNT(*) FROM lead_status_history GROUP BY new_status')
            status_dist = dict(cursor.fetchall())
            
            # conn.close() removed
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'task_statistics': task_stats,
                'upcoming_tasks_7_days': upcoming_tasks,
                'overdue_tasks': overdue_tasks,
                'lead_status_distribution': status_dist,
                'total_leads': len(status_dist),
                'completion_rate': (task_stats.get('completed', 0) / max(sum(task_stats.values()), 1)) * 100
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating follow-up report: {e}")
            return {}
    
    def import_leads_from_search_results(self, leads_file: str) -> int:
        """Import leads from search results and create follow-up tasks"""
        try:
            with open(leads_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            leads = data.get('leads', [])
            imported_count = 0
            
            for lead in leads:
                lead_id = self.add_lead_from_search(lead)
                if lead_id:
                    imported_count += 1
            
            self.logger.info(f"Imported {imported_count} leads from {leads_file}")
            return imported_count
            
        except Exception as e:
            self.logger.error(f"Error importing leads from {leads_file}: {e}")
            return 0

def main():
    """Main function to demonstrate follow-up manager"""
    print("=" * 60)
    print("🔄 FOLLOW UP MANAGER - CLOSER AGENT")
    print("=" * 60)
    
    # Initialize follow-up manager
    follow_up_manager = FollowUpManager()
    
    # Import leads from test results
    print("📥 Importing leads from search results...")
    imported = follow_up_manager.import_leads_from_search_results('test_leads_results.json')
    print(f"✅ Imported {imported} leads")
    
    # Get pending follow-ups
    print("\n📋 Getting pending follow-ups...")
    pending_tasks = follow_up_manager.get_pending_follow_ups(7)
    
    if pending_tasks:
        print(f"📊 Found {len(pending_tasks)} pending follow-up tasks:")
        for i, task in enumerate(pending_tasks[:5]):  # Show first 5
            print(f"  {i+1}. Lead {task['lead_id']} - {task['task_type']} ({task['priority']})")
            print(f"     Scheduled: {task['scheduled_date']}")
            print(f"     Message: {task['message_template'][:80]}...")
            print("")
    else:
        print("📭 No pending follow-up tasks found")
    
    # Generate report
    print("\n📈 Generating follow-up report...")
    report = follow_up_manager.generate_follow_up_report()
    
    if report:
        print("📊 Follow-Up Statistics:")
        print(f"  - Total Leads: {report.get('total_leads', 0)}")
        print(f"  - Completion Rate: {report.get('completion_rate', 0):.1f}%")
        print(f"  - Upcoming Tasks (7 days): {report.get('upcoming_tasks_7_days', 0)}")
        print(f"  - Overdue Tasks: {report.get('overdue_tasks', 0)}")
        print(f"  - Task Status: {report.get('task_statistics', {})}")
    
    # Save report
    report_file = 'follow_up_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ FOLLOW UP MANAGER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
