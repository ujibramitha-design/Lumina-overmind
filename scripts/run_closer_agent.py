#!/usr/bin/env python3
"""
Lumina OS - Closer Agent Scheduler Script
Automated follow-up message generation and review system

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import argparse

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import core modules
from core_modules.closer_agent.sales_consultant import SalesConsultant
from core_modules.db_manager import DatabaseManager

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.END):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_header():
    """Print scheduler header"""
    print_colored("=" * 80, Colors.BOLD)
    print_colored("🤖 LUMINA OS - CLOSER AGENT SCHEDULER", Colors.BOLD)
    print_colored("   Intelligent Follow-up Message Generation System", Colors.BLUE)
    print_colored("=" * 80, Colors.BOLD)
    print()

def print_agent_status(agent: SalesConsultant):
    """Print agent status information"""
    status = agent.get_agent_status()
    
    print_colored("🔧 AGENT STATUS", Colors.CYAN)
    print("-" * 50)
    print_colored(f"Agent Name: {status['agent_name']}", Colors.END)
    print_colored(f"AI Enabled: {status['ai_enabled']}", Colors.GREEN if status['ai_enabled'] else Colors.YELLOW)
    if status['ai_enabled']:
        print_colored(f"AI Provider: {status['ai_provider']}", Colors.BLUE)
    print_colored(f"Supported Categories: {', '.join(status['supported_categories'])}", Colors.END)
    print_colored(f"Tone Styles: {', '.join(status['tone_styles'])}", Colors.END)
    print_colored(f"Status: {status['status']}", Colors.GREEN)
    print()

def get_pending_leads(db_manager: DatabaseManager) -> List[Dict[str, Any]]:
    """
    Get leads that need follow-up messages
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        List: Leads requiring follow-up
    """
    try:
        # Query leads with status 'New' or 'Follow Up'
        query = """
        SELECT id, nama, no_hp, email, location, pekerjaan, sumber, catatan, 
               skor_akhir, kategori, status, created_at, updated_at,
               catatan_followup
        FROM leads 
        WHERE status IN ('New', 'Follow Up') 
        AND (catatan_followup IS NULL OR catatan_followup = '')
        ORDER BY skor_akhir DESC, created_at ASC
        """
        
        raw_leads = db_manager.execute_query(query)
        
        if not raw_leads:
            print_colored("📭 No pending leads found requiring follow-up messages", Colors.YELLOW)
            return []
        
        # Convert tuples to dictionaries
        leads = []
        for row in raw_leads:
            lead_dict = {
                'id': row[0],
                'nama': row[1],
                'no_hp': row[2],
                'email': row[3],
                'location': row[4],
                'pekerjaan': row[5],
                'sumber': row[6],
                'catatan': row[7],
                'skor_akhir': row[8],
                'kategori': row[9],
                'status': row[10],
                'created_at': row[11],
                'updated_at': row[12],
                'catatan_followup': row[13]
            }
            leads.append(lead_dict)
        
        print_colored(f"📊 Found {len(leads)} leads requiring follow-up messages", Colors.BLUE)
        return leads
        
    except Exception as e:
        print_colored(f"❌ Error fetching pending leads: {str(e)}", Colors.RED)
        return []

def process_single_lead(agent: SalesConsultant, lead: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single lead and generate follow-up message
    
    Args:
        agent: SalesConsultant instance
        lead: Lead data dictionary
        
    Returns:
        Dict: Processing result
    """
    lead_name = lead.get('nama', 'Unknown')
    lead_id = lead.get('id')
    
    print_colored(f"[CLOSER AGENT] Processing lead: {lead_name} (ID: {lead_id})", Colors.CYAN)
    
    # Generate follow-up message
    result = agent.generate_followup_message(lead)
    
    if result['success']:
        message = result['message']
        metadata = result['metadata']
        
        print_colored(f"✅ Message generated successfully!", Colors.GREEN)
        print_colored(f"   Score: {metadata['skor_akhir']} | Category: {metadata['kategori']}", Colors.BLUE)
        print_colored(f"   Tone: {metadata['tone_style']} | Source: {metadata['message_source']}", Colors.BLUE)
        
        # Display the generated message
        print_colored("\n📝 GENERATED MESSAGE:", Colors.YELLOW)
        print_colored("-" * 60, Colors.YELLOW)
        print_colored(message, Colors.END)
        print_colored("-" * 60, Colors.YELLOW)
        
        return {
            'success': True,
            'lead_id': lead_id,
            'lead_name': lead_name,
            'message': message,
            'metadata': metadata
        }
    else:
        print_colored(f"❌ Failed to generate message: {result['error']}", Colors.RED)
        return {
            'success': False,
            'lead_id': lead_id,
            'lead_name': lead_name,
            'error': result['error']
        }

def save_followup_to_database(db_manager: DatabaseManager, result: Dict[str, Any]) -> bool:
    """
    Save follow-up message to database
    
    Args:
        db_manager: Database manager instance
        result: Processing result with message
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        if not result['success']:
            return False
        
        # Update lead with follow-up message
        update_query = """
        UPDATE leads 
        SET catatan_followup = ?, 
            updated_at = ?,
            status = 'Follow Up'
        WHERE id = ?
        """
        
        message_data = json.dumps({
            'message': result['message'],
            'metadata': result['metadata'],
            'generated_at': result['metadata']['generated_at']
        })
        
        db_manager.execute_update(update_query, (message_data, datetime.now().isoformat(), result['lead_id']))
        
        print_colored(f"💾 Follow-up message saved to database for lead: {result['lead_name']}", Colors.GREEN)
        return True
        
    except Exception as e:
        print_colored(f"❌ Error saving follow-up to database: {str(e)}", Colors.RED)
        return False

def process_all_leads(agent: SalesConsultant, db_manager: DatabaseManager, leads: List[Dict[str, Any]], save_to_db: bool = True) -> Dict[str, Any]:
    """
    Process all pending leads and generate follow-up messages
    
    Args:
        agent: SalesConsultant instance
        db_manager: Database manager instance
        leads: List of leads to process
        save_to_db: Whether to save messages to database
        
    Returns:
        Dict: Processing summary
    """
    results = []
    successful = 0
    failed = 0
    saved = 0
    
    print_colored(f"\n🚀 Processing {len(leads)} leads...", Colors.BOLD)
    print_colored("=" * 60, Colors.BOLD)
    
    for i, lead in enumerate(leads, 1):
        print_colored(f"\n[{i}/{len(leads)}] ===================================", Colors.CYAN)
        
        # Process lead
        result = process_single_lead(agent, lead)
        
        if result['success']:
            successful += 1
            
            # Save to database if requested
            if save_to_db:
                if save_followup_to_database(db_manager, result):
                    saved += 1
            else:
                print_colored("📋 Message generated but NOT saved to database (dry run)", Colors.YELLOW)
        else:
            failed += 1
        
        results.append(result)
        
        # Add delay between leads (if not the last one)
        if i < len(leads):
            print_colored("⏳ Waiting 2 seconds before next lead...", Colors.YELLOW)
            time.sleep(2)
    
    # Return summary
    return {
        'total_processed': len(leads),
        'successful': successful,
        'failed': failed,
        'saved': saved,
        'success_rate': (successful / len(leads)) * 100 if leads else 0,
        'results': results,
        'processed_at': datetime.now().isoformat()
    }

def print_summary(summary: Dict[str, Any]):
    """Print processing summary"""
    print_colored("\n" + "=" * 80, Colors.BOLD)
    print_colored("📊 PROCESSING SUMMARY", Colors.BOLD)
    print_colored("=" * 80, Colors.BOLD)
    
    print_colored(f"Total Leads Processed: {summary['total_processed']}", Colors.END)
    print_colored(f"✅ Successful: {summary['successful']}", Colors.GREEN)
    print_colored(f"❌ Failed: {summary['failed']}", Colors.RED)
    print_colored(f"💾 Saved to Database: {summary['saved']}", Colors.BLUE)
    print_colored(f"📈 Success Rate: {summary['success_rate']:.1f}%", Colors.YELLOW)
    print_colored(f"⏰ Completed: {summary['processed_at']}", Colors.END)
    
    if summary['failed'] > 0:
        print_colored(f"\n⚠️  {summary['failed']} leads failed to process. Check logs for details.", Colors.YELLOW)
    
    print_colored("=" * 80, Colors.BOLD)

def run_scheduler_mode(agent: SalesConsultant, db_manager: DatabaseManager, interval_minutes: int = 30):
    """
    Run scheduler in continuous mode
    
    Args:
        agent: SalesConsultant instance
        db_manager: Database manager instance
        interval_minutes: Interval between runs in minutes
    """
    print_colored(f"🔄 Starting continuous scheduler mode (interval: {interval_minutes} minutes)", Colors.BLUE)
    print_colored("Press Ctrl+C to stop", Colors.YELLOW)
    print()
    
    run_count = 0
    
    try:
        while True:
            run_count += 1
            print_colored(f"\n🕐 Scheduler Run #{run_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.BOLD)
            
            # Get pending leads
            leads = get_pending_leads(db_manager)
            
            if leads:
                # Process all leads
                summary = process_all_leads(agent, db_manager, leads, save_to_db=True)
                print_summary(summary)
            else:
                print_colored("📭 No leads to process in this run", Colors.YELLOW)
            
            print_colored(f"\n⏳ Next run in {interval_minutes} minutes...", Colors.CYAN)
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print_colored(f"\n\n⏹️  Scheduler stopped by user after {run_count} runs", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n\n💥 Scheduler error: {str(e)}", Colors.RED)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Lumina OS Closer Agent Scheduler')
    parser.add_argument('--mode', choices=['single', 'continuous'], default='single',
                        help='Run mode: single (one-time) or continuous (scheduler)')
    parser.add_argument('--interval', type=int, default=30,
                        help='Interval in minutes for continuous mode (default: 30)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Generate messages but don\'t save to database')
    parser.add_argument('--lead-id', type=int,
                        help='Process specific lead ID only')
    
    args = parser.parse_args()
    
    print_header()
    
    # Initialize agent and database
    try:
        print_colored("🔧 Initializing Closer Agent...", Colors.BLUE)
        agent = SalesConsultant()
        db_manager = DatabaseManager()
        
        print_colored("✅ Agent initialized successfully!", Colors.GREEN)
        print_agent_status(agent)
        
    except Exception as e:
        print_colored(f"❌ Failed to initialize agent: {str(e)}", Colors.RED)
        return
    
    # Run based on mode
    if args.mode == 'continuous':
        run_scheduler_mode(agent, db_manager, args.interval)
    else:
        # Single run mode
        if args.lead_id:
            # Process specific lead
            try:
                lead_query = "SELECT * FROM leads WHERE id = ?"
                lead = db_manager.execute_query(lead_query, (args.lead_id,))
                
                if not lead:
                    print_colored(f"❌ Lead with ID {args.lead_id} not found", Colors.RED)
                    return
                
                lead = lead[0]
                print_colored(f"🎯 Processing specific lead: {lead.get('nama', 'Unknown')} (ID: {args.lead_id})", Colors.CYAN)
                
                result = process_single_lead(agent, lead)
                
                if result['success'] and not args.dry_run:
                    save_followup_to_database(db_manager, result)
                elif args.dry_run:
                    print_colored("📋 Dry run mode - message not saved to database", Colors.YELLOW)
                
            except Exception as e:
                print_colored(f"❌ Error processing lead {args.lead_id}: {str(e)}", Colors.RED)
        else:
            # Process all pending leads
            leads = get_pending_leads(db_manager)
            
            if leads:
                summary = process_all_leads(agent, db_manager, leads, save_to_db=not args.dry_run)
                print_summary(summary)
                
                if args.dry_run:
                    print_colored("\n📋 Dry run mode completed - no messages were saved to database", Colors.YELLOW)
            else:
                print_colored("📭 No pending leads found", Colors.YELLOW)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⏹️  Process interrupted by user", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n\n💥 Unexpected error: {str(e)}", Colors.RED)
