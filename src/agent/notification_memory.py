#!/usr/bin/env python3
"""
Notification Memory Management System

This module provides functionality to track sent notifications and prevent duplicates.
Uses SQLite database to store notification history with idempotency keys.
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os


class NotificationMemory:
    """Memory system for tracking sent notifications to prevent duplicates."""
    
    def __init__(self, db_path: str = "notification_memory.db"):
        """Initialize the notification memory system.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sent_notifications (
                    idempotency_key TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    notification_hash TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notification_data TEXT,
                    recipient TEXT DEFAULT 'default'
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS notification_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    notification_hash TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notification_data TEXT,
                    recipient TEXT DEFAULT 'default'
                )
            ''')
            
            # Track individual updates that have been sent (prevents partial duplicates)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sent_updates (
                    update_hash TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    recipient TEXT DEFAULT 'default',
                    full_content TEXT
                )
            ''')
            
            conn.commit()
    
    def _generate_idempotency_key(self, topic: str, notification_data: Dict) -> str:
        """Generate a unique idempotency key for a notification.
        
        Args:
            topic: The topic of the notification
            notification_data: The notification data
            
        Returns:
            Unique idempotency key
        """
        # Create a more stable hash based on topic and key content
        relevant_updates = notification_data.get('relevant_updates', [])
        
        # Extract key information from updates (title and URL are more stable than snippets)
        key_info = []
        for update in relevant_updates:
            key_info.append({
                'title': update.get('title', ''),
                'url': update.get('url', '')
            })
        
        # Sort for consistency
        key_info.sort(key=lambda x: x['title'])
        
        # Create hash from topic and key info
        data_str = f"{topic}:{json.dumps(key_info, sort_keys=True)}"
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _generate_notification_hash(self, notification_data: Dict) -> str:
        """Generate a hash for the notification content.
        
        Args:
            notification_data: The notification data
            
        Returns:
            Hash of the notification content
        """
        # Create a more stable hash from the relevant updates
        relevant_updates = notification_data.get('relevant_updates', [])
        
        # Extract stable content (title and URL)
        stable_content = []
        for update in relevant_updates:
            stable_content.append({
                'title': update.get('title', ''),
                'url': update.get('url', '')
            })
        
        # Sort for consistency
        stable_content.sort(key=lambda x: x['title'])
        content_str = json.dumps(stable_content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _generate_update_hash(self, update: Dict) -> str:
        """Generate a unique hash for an individual update (title + url)."""
        title = update.get('title', '').strip()
        url = update.get('url', '').strip()
        content_str = f"{title}|{url}"
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def filter_new_updates(self, topic: str, updates: List[Dict], time_window_hours: int = 24) -> Tuple[List[Dict], List[Dict]]:
        """Split updates into new vs already sent within the time window."""
        if not updates:
            return [], []
        new_updates: List[Dict] = []
        already_sent_updates: List[Dict] = []
        with sqlite3.connect(self.db_path) as conn:
            for update in updates:
                update_hash = self._generate_update_hash(update)
                cursor = conn.execute('''
                    SELECT 1 FROM sent_updates 
                    WHERE update_hash = ? AND topic = ? AND sent_at >= datetime('now', '-{} hours')
                    LIMIT 1
                '''.format(time_window_hours), (update_hash, topic))
                if cursor.fetchone() is not None:
                    already_sent_updates.append(update)
                else:
                    new_updates.append(update)
        return new_updates, already_sent_updates
    
    def is_notification_sent(self, topic: str, notification_data: Dict, time_window_hours: int = 24) -> bool:
        """Return True only if all relevant updates were already sent in the window."""
        relevant_updates = notification_data.get('relevant_updates', [])
        if not relevant_updates:
            return False
        new_updates, _ = self.filter_new_updates(topic, relevant_updates, time_window_hours)
        return len(new_updates) == 0
    
    def mark_notification_sent(self, topic: str, notification_data: Dict, recipient: str = "default") -> str:
        """Mark a notification as sent.
        
        Args:
            topic: The topic of the notification
            notification_data: The notification data
            recipient: The recipient of the notification
            
        Returns:
            The idempotency key used
        """
        idempotency_key = self._generate_idempotency_key(topic, notification_data)
        notification_hash = self._generate_notification_hash(notification_data)
        
        with sqlite3.connect(self.db_path) as conn:
            # Insert into sent_notifications (for idempotency)
            conn.execute('''
                INSERT OR IGNORE INTO sent_notifications 
                (idempotency_key, topic, notification_hash, notification_data, recipient)
                VALUES (?, ?, ?, ?, ?)
            ''', (idempotency_key, topic, notification_hash, json.dumps(notification_data), recipient))
            
            # Insert into notification_history (for tracking)
            conn.execute('''
                INSERT INTO notification_history 
                (topic, notification_hash, notification_data, recipient)
                VALUES (?, ?, ?, ?)
            ''', (topic, notification_hash, json.dumps(notification_data), recipient))
            
            # Track individual updates (for partial duplicate prevention)
            relevant_updates = notification_data.get('relevant_updates', [])
            for update in relevant_updates:
                update_hash = self._generate_update_hash(update)
                conn.execute('''
                    INSERT OR IGNORE INTO sent_updates 
                    (update_hash, topic, title, url, recipient, full_content)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    update_hash,
                    topic,
                    update.get('title', ''),
                    update.get('url', ''),
                    recipient,
                    json.dumps(update)
                ))
            
            conn.commit()
        
        return idempotency_key
    
    def get_recent_notifications(self, topic: str, days: int = 7) -> List[Dict]:
        """Get recent notifications for a topic.
        
        Args:
            topic: The topic to get notifications for
            days: Number of days to look back
            
        Returns:
            List of recent notifications
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT notification_data, sent_at, recipient
                FROM notification_history 
                WHERE topic = ? AND sent_at >= datetime('now', '-{} days')
                ORDER BY sent_at DESC
            '''.format(days), (topic,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'notification_data': json.loads(row[0]),
                    'sent_at': row[1],
                    'recipient': row[2]
                })
            
            return results
    
    def get_sent_updates(self, topic: str, days: int = 7) -> List[Dict]:
        """Get individual sent updates for a topic within a time range."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT title, url, sent_at, recipient, full_content
                FROM sent_updates 
                WHERE topic = ? AND sent_at >= datetime('now', '-{} days')
                ORDER BY sent_at DESC
            '''.format(days), (topic,))
            results: List[Dict] = []
            for row in cursor.fetchall():
                results.append({
                    'title': row[0],
                    'url': row[1],
                    'sent_at': row[2],
                    'recipient': row[3],
                    'content': json.loads(row[4]) if row[4] else {}
                })
            return results
    
    def get_notification_stats(self) -> Dict:
        """Get statistics about sent notifications.
        
        Returns:
            Dictionary with notification statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            # Total notifications
            total = conn.execute('SELECT COUNT(*) FROM notification_history').fetchone()[0]
            # Total individual updates
            try:
                total_updates = conn.execute('SELECT COUNT(*) FROM sent_updates').fetchone()[0]
            except Exception:
                total_updates = 0
            
            # Notifications by topic
            topics = conn.execute('''
                SELECT topic, COUNT(*) as count 
                FROM notification_history 
                GROUP BY topic
            ''').fetchall()
            
            # Recent notifications (last 7 days)
            recent = conn.execute('''
                SELECT COUNT(*) 
                FROM notification_history 
                WHERE sent_at >= datetime('now', '-7 days')
            ''').fetchone()[0]
            
            return {
                'total_notifications': total,
                'total_individual_updates': total_updates,
                'recent_notifications': recent,
                'notifications_by_topic': dict(topics)
            }
    
    def cleanup_old_notifications(self, days: int = 30):
        """Clean up old notifications from the history table.
        
        Args:
            days: Number of days to keep in history
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM notification_history 
                WHERE sent_at < datetime('now', '-{} days')
            '''.format(days))
            conn.execute('''
                DELETE FROM sent_updates 
                WHERE sent_at < datetime('now', '-{} days')
            '''.format(days))
            conn.commit()
    
    def reset_memory(self):
        """Reset all notification memory (for testing purposes)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM sent_notifications')
            conn.execute('DELETE FROM notification_history')
            try:
                conn.execute('DELETE FROM sent_updates')
            except Exception:
                pass
            conn.commit()


# Global instance for easy access
notification_memory = NotificationMemory()
