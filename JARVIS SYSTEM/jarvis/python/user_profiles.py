"""
JARVIS User Profiles Module
==========================

Database schema and management for user profiles including:
- Interaction count for relationship evolution
- Persona preferences
- Communication preferences
"""

import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserProfileManager:
    """
    Manager for user profiles and interaction tracking.
    """
    
    def __init__(self, db_path: str = './jarvis/data/user_profiles.db'):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """
        Initialize the user profiles database.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create user profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    phone_number TEXT,
                    telegram_id TEXT,
                    interaction_count INTEGER DEFAULT 0,
                    first_interaction DATETIME,
                    last_interaction DATETIME,
                    persona TEXT DEFAULT 'formal',
                    communication_preferences TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create interaction history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interaction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    message_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_interaction_history_user_id 
                ON interaction_history(user_id)
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("✅ User profiles database initialized")
        
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
            raise
    
    def get_or_create_user(self, user_id: str, platform: str, **kwargs) -> Dict[str, Any]:
        """
        Get existing user or create new user profile.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Try to get existing user
            cursor.execute('''
                SELECT user_id, platform, phone_number, telegram_id, 
                       interaction_count, first_interaction, last_interaction, 
                       persona, communication_preferences
                FROM user_profiles
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            
            if row:
                # User exists, return profile
                profile = {
                    'user_id': row[0],
                    'platform': row[1],
                    'phone_number': row[2],
                    'telegram_id': row[3],
                    'interaction_count': row[4],
                    'first_interaction': row[5],
                    'last_interaction': row[6],
                    'persona': row[7],
                    'communication_preferences': row[8],
                }
                
                # Update last interaction time
                cursor.execute('''
                    UPDATE user_profiles
                    SET last_interaction = ?, updated_at = ?
                    WHERE user_id = ?
                ''', (datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), user_id))
                
                conn.commit()
                conn.close()
                
                return profile
            else:
                # Create new user
                cursor.execute('''
                    INSERT INTO user_profiles (
                        user_id, platform, phone_number, telegram_id,
                        interaction_count, first_interaction, last_interaction,
                        persona
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    platform,
                    kwargs.get('phone_number'),
                    kwargs.get('telegram_id'),
                    0,  # interaction_count
                    datetime.utcnow().isoformat(),  # first_interaction
                    datetime.utcnow().isoformat(),  # last_interaction
                    'formal',  # persona
                ))
                
                conn.commit()
                conn.close()
                
                logger.info(f"✅ Created new user profile: {user_id}")
                
                return {
                    'user_id': user_id,
                    'platform': platform,
                    'phone_number': kwargs.get('phone_number'),
                    'telegram_id': kwargs.get('telegram_id'),
                    'interaction_count': 0,
                    'first_interaction': datetime.utcnow().isoformat(),
                    'last_interaction': datetime.utcnow().isoformat(),
                    'persona': 'formal',
                    'communication_preferences': None,
                }
        
        except Exception as e:
            logger.error(f"❌ Error getting/creating user: {e}")
            raise
    
    def increment_interaction_count(self, user_id: str) -> int:
        """
        Increment interaction count for a user.
        Returns the new count.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Increment interaction count
            cursor.execute('''
                UPDATE user_profiles
                SET interaction_count = interaction_count + 1,
                    last_interaction = ?,
                    updated_at = ?
                WHERE user_id = ?
            ''', (datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), user_id))
            
            # Get new count
            cursor.execute('''
                SELECT interaction_count FROM user_profiles WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            new_count = row[0] if row else 0
            
            # Update persona based on count
            new_persona = self._get_persona_from_count(new_count)
            cursor.execute('''
                UPDATE user_profiles
                SET persona = ?
                WHERE user_id = ?
            ''', (new_persona, user_id))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Incremented interaction count for {user_id}: {new_count}")
            
            return new_count
        
        except Exception as e:
            logger.error(f"❌ Error incrementing interaction count: {e}")
            return 0
    
    def get_interaction_count(self, user_id: str) -> int:
        """
        Get interaction count for a user.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT interaction_count FROM user_profiles WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            count = row[0] if row else 0
            
            conn.close()
            
            return count
        
        except Exception as e:
            logger.error(f"❌ Error getting interaction count: {e}")
            return 0
    
    def get_persona(self, user_id: str) -> str:
        """
        Get current persona for a user.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT persona FROM user_profiles WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            persona = row[0] if row else 'formal'
            
            conn.close()
            
            return persona
        
        except Exception as e:
            logger.error(f"❌ Error getting persona: {e}")
            return 'formal'
    
    def _get_persona_from_count(self, count: int) -> str:
        """
        Determine persona based on interaction count.
        """
        if count < 100:
            return 'formal'  # Strictly formal
        elif count < 500:
            return 'casual'  # More casual
        else:
            return 'friendly'  # Close, trusted colleague
    
    def log_interaction(self, user_id: str, platform: str, message_type: str = 'text'):
        """
        Log an interaction to the history table.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO interaction_history (user_id, platform, message_type)
                VALUES (?, ?, ?)
            ''', (user_id, platform, message_type))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logger.error(f"❌ Error logging interaction: {e}")
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics for a user.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get profile
            cursor.execute('''
                SELECT interaction_count, first_interaction, last_interaction, persona
                FROM user_profiles
                WHERE user_id = ?
            ''', (user_id,))
            
            profile_row = cursor.fetchone()
            
            if not profile_row:
                return {}
            
            # Get interaction history count
            cursor.execute('''
                SELECT COUNT(*) FROM interaction_history WHERE user_id = ?
            ''', (user_id,))
            
            history_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'interaction_count': profile_row[0],
                'first_interaction': profile_row[1],
                'last_interaction': profile_row[2],
                'persona': profile_row[3],
                'total_interactions_logged': history_count,
            }
        
        except Exception as e:
            logger.error(f"❌ Error getting user stats: {e}")
            return {}

# Singleton instance
user_profile_manager: Optional[UserProfileManager] = None

def get_user_profile_manager(db_path: str = None) -> UserProfileManager:
    """Get or create user profile manager singleton"""
    global user_profile_manager
    
    if user_profile_manager is None:
        if db_path is None:
            db_path = './jarvis/data/user_profiles.db'
        user_profile_manager = UserProfileManager(db_path)
    
    return user_profile_manager
