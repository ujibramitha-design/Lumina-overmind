"""
JARVIS Memory Pruning Module
============================

Nightly cron job for memory pruning and summarization.
Prevents token exhaustion by summarizing chat logs and clearing raw buffers.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import sqlite3
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MemoryPruner:
    """
    Manages memory pruning and summarization for JARVIS.
    Runs nightly to prevent token exhaustion.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Database path
        self.db_path = config.get('db_path', './jarvis/data/jarvis_memory.db')
        
        # Retention settings
        self.raw_log_retention_days = config.get('raw_log_retention_days', 7)
        self.summary_retention_days = config.get('summary_retention_days', 90)
        
        # LLM settings for summarization
        self.llm_config = config.get('llm', {
            'model': 'gpt-4',
            'max_tokens': 1000,
            'temperature': 0.3,
        })
        
        # Pruning schedule
        self.prune_time = config.get('prune_time', '02:00')  # 2:00 AM
        
        # Statistics
        self.stats = {
            'last_prune': None,
            'messages_pruned': 0,
            'summaries_created': 0,
            'facts_extracted': 0,
            'tokens_saved': 0,
        }
    
    async def initialize(self):
        """Initialize database schema"""
        await self._create_tables()
        logger.info("✅ Memory Pruner initialized")
    
    async def _create_tables(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table (raw chat logs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Conversation summaries table (LLM-generated summaries)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                date DATE NOT NULL,
                summary TEXT NOT NULL,
                key_points TEXT,
                token_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(platform, user_id, date)
            )
        ''')
        
        # Key facts table (extracted facts from summaries)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                fact TEXT NOT NULL,
                category TEXT,
                confidence REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversations_timestamp 
            ON conversations(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_summaries_date 
            ON conversation_summaries(date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_facts_category 
            ON key_facts(category)
        ''')
        
        conn.commit()
        conn.close()
    
    async def run_pruning(self):
        """Run the memory pruning process"""
        logger.info("🧹 Starting memory pruning process")
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Get conversations to prune
            conversations_to_prune = await self._get_conversations_to_prune()
            logger.info(f"Found {len(conversations_to_prune)} conversations to prune")
            
            # Step 2: Group by platform and user
            grouped_conversations = self._group_conversations(conversations_to_prune)
            
            # Step 3: Generate summaries for each group
            summaries_created = 0
            facts_extracted = 0
            tokens_saved = 0
            
            for (platform, user_id), convs in grouped_conversations.items():
                # Generate summary
                summary = await self._generate_summary(convs)
                
                # Extract key facts
                facts = await self._extract_facts(summary)
                
                # Save to database
                await self._save_summary(platform, user_id, summary, facts)
                
                summaries_created += 1
                facts_extracted += len(facts)
                tokens_saved += self._calculate_token_savings(convs, summary)
            
            # Step 4: Delete raw conversations
            await self._delete_raw_conversations(conversations_to_prune)
            
            # Step 5: Update statistics
            self.stats.update({
                'last_prune': datetime.utcnow().isoformat(),
                'messages_pruned': len(conversations_to_prune),
                'summaries_created': summaries_created,
                'facts_extracted': facts_extracted,
                'tokens_saved': tokens_saved,
            })
            
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Pruning completed in {elapsed:.2f}s")
            logger.info(f"📊 Pruned {len(conversations_to_prune)} messages")
            logger.info(f"📊 Created {summaries_created} summaries")
            logger.info(f"📊 Extracted {facts_extracted} facts")
            logger.info(f"📊 Saved ~{tokens_saved} tokens")
            
        except Exception as e:
            logger.error(f"❌ Pruning failed: {e}")
            raise
    
    async def _get_conversations_to_prune(self) -> List[Dict[str, Any]]:
        """Get conversations that need pruning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.utcnow() - timedelta(days=self.raw_log_retention_days)
        
        cursor.execute('''
            SELECT id, platform, user_id, message, response, timestamp
            FROM conversations
            WHERE timestamp < ?
            ORDER BY timestamp ASC
        ''', (cutoff_date.isoformat(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'platform': row[1],
                'user_id': row[2],
                'message': row[3],
                'response': row[4],
                'timestamp': row[5],
            }
            for row in rows
        ]
    
    def _group_conversations(self, conversations: List[Dict[str, Any]]) -> Dict[tuple, List[Dict[str, Any]]]:
        """Group conversations by platform and user"""
        grouped = {}
        
        for conv in conversations:
            key = (conv['platform'], conv['user_id'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(conv)
        
        return grouped
    
    async def _generate_summary(self, conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary using LLM"""
        # Prepare conversation text
        conversation_text = "\n".join([
            f"User: {conv['message']}\nJARVIS: {conv['response']}"
            for conv in conversations
        ])
        
        # In production, this would call the actual LLM
        # For now, we'll create a mock summary
        summary = {
            'summary': f"Summary of {len(conversations)} conversations from {conversations[0]['timestamp']} to {conversations[-1]['timestamp']}.",
            'key_points': [
                "User asked about system status multiple times",
                "JARVIS provided metrics and health reports",
                "User requested code explanations",
            ],
            'token_count': len(conversation_text.split()),
        }
        
        return summary
    
    async def _extract_facts(self, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key facts from summary"""
        # In production, this would use NLP to extract facts
        # For now, we'll extract from key_points
        facts = []
        
        for point in summary.get('key_points', []):
            facts.append({
                'fact': point,
                'category': 'general',
                'confidence': 0.9,
            })
        
        return facts
    
    async def _save_summary(self, platform: str, user_id: str, summary: Dict[str, Any], facts: List[Dict[str, Any]]):
        """Save summary and facts to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Save summary
        date = datetime.utcnow().date()
        cursor.execute('''
            INSERT OR REPLACE INTO conversation_summaries
            (platform, user_id, date, summary, key_points, token_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            platform,
            user_id,
            date.isoformat(),
            summary['summary'],
            json.dumps(summary['key_points']),
            summary['token_count'],
        ))
        
        # Save facts
        for fact in facts:
            cursor.execute('''
                INSERT INTO key_facts
                (platform, user_id, fact, category, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                platform,
                user_id,
                fact['fact'],
                fact['category'],
                fact['confidence'],
            ))
        
        conn.commit()
        conn.close()
    
    async def _delete_raw_conversations(self, conversations: List[Dict[str, Any]]):
        """Delete raw conversations from database"""
        if not conversations:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        ids_to_delete = [conv['id'] for conv in conversations]
        placeholders = ','.join(['?'] * len(ids_to_delete))
        
        cursor.execute(f'''
            DELETE FROM conversations
            WHERE id IN ({placeholders})
        ''', ids_to_delete)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"🗑️ Deleted {deleted_count} raw conversations")
    
    def _calculate_token_savings(self, conversations: List[Dict[str, Any]], summary: Dict[str, Any]) -> int:
        """Calculate token savings from pruning"""
        # Estimate tokens in raw conversations
        raw_tokens = sum(
            len(conv['message'].split()) + len(conv['response'].split())
            for conv in conversations
        )
        
        # Estimate tokens in summary
        summary_tokens = summary['token_count']
        
        return raw_tokens - summary_tokens
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count raw conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        raw_count = cursor.fetchone()[0]
        
        # Count summaries
        cursor.execute('SELECT COUNT(*) FROM conversation_summaries')
        summary_count = cursor.fetchone()[0]
        
        # Count facts
        cursor.execute('SELECT COUNT(*) FROM key_facts')
        fact_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'raw_conversations': raw_count,
            'summaries': summary_count,
            'facts': fact_count,
            'pruning_stats': self.stats,
        }
    
    async def search_memory(self, query: str, platform: str = None, user_id: str = None) -> List[Dict[str, Any]]:
        """Search memory for relevant information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search in summaries
        if platform and user_id:
            cursor.execute('''
                SELECT id, platform, user_id, date, summary, key_points
                FROM conversation_summaries
                WHERE platform = ? AND user_id = ?
                AND (summary LIKE ? OR key_points LIKE ?)
                ORDER BY date DESC
                LIMIT 10
            ''', (platform, user_id, f'%{query}%', f'%{query}%'))
        else:
            cursor.execute('''
                SELECT id, platform, user_id, date, summary, key_points
                FROM conversation_summaries
                WHERE summary LIKE ? OR key_points LIKE ?
                ORDER BY date DESC
                LIMIT 10
            ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'platform': row[1],
                'user_id': row[2],
                'date': row[3],
                'summary': row[4],
                'key_points': json.loads(row[5]) if row[5] else [],
            }
            for row in rows
        ]

# Singleton instance
memory_pruner: Optional[MemoryPruner] = None

def get_memory_pruner(config: Dict[str, Any] = None) -> MemoryPruner:
    """Get or create memory pruner singleton"""
    global memory_pruner
    
    if memory_pruner is None:
        if config is None:
            config = {}
        memory_pruner = MemoryPruner(config)
    
    return memory_pruner
