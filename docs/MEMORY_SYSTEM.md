# Notification Memory System

## Overview

The Notification Memory System prevents duplicate email notifications by tracking sent notifications in a SQLite database. This ensures that users only receive notifications about new updates and not repeated information.

## Features

### 🔄 **Duplicate Prevention**
- Uses idempotency keys to prevent duplicate notifications
- Tracks notification history with timestamps
- Prevents spam by checking if similar updates were already sent

### 📊 **Memory Management**
- SQLite database for persistent storage
- Notification statistics and history tracking
- Automatic cleanup of old notifications

### 🛠️ **CLI Management**
- View notification statistics
- Reset memory for testing
- View recent notifications by topic

## How It Works

### 1. **Idempotency Key Generation**
When a notification is processed, the system generates a unique idempotency key based on:
- Topic (e.g., "tax policy")
- Key content from relevant updates (title and URL)
- Sorted for consistency

### 2. **Duplicate Detection**
Before sending a notification, the system:
1. Generates an idempotency key for the current notification
2. Checks if this key exists in the database
3. If found, skips sending the notification
4. If not found, sends the notification and records the key

### 3. **Database Schema**
```sql
-- For idempotency (prevents duplicates)
CREATE TABLE sent_notifications (
    idempotency_key TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    notification_hash TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notification_data TEXT,
    recipient TEXT DEFAULT 'default'
);

-- For history tracking
CREATE TABLE notification_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    notification_hash TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notification_data TEXT,
    recipient TEXT DEFAULT 'default'
);
```

## Usage

### CLI Commands

```bash
# View notification memory status
python main.py --memory

# View recent notifications
python main.py --recent

# View recent notifications for specific topic
python main.py --recent "tax policy"

# View recent notifications for last N days
python main.py --recent "tax policy" 14

# Reset notification memory (for testing)
python main.py --reset-memory
```

### Programmatic Usage

```python
from notification_memory import notification_memory

# Check if notification was already sent
is_sent = notification_memory.is_notification_sent(topic, notification_data)

# Mark notification as sent
key = notification_memory.mark_notification_sent(topic, notification_data)

# Get notification statistics
stats = notification_memory.get_notification_stats()

# Get recent notifications
recent = notification_memory.get_recent_notifications("tax policy", days=7)
```

## Integration with Agent

The memory system is automatically integrated with the `checkIsMailneedtoSend` tool:

1. **Web Search**: Agent searches for updates on the specified topic
2. **Update Analysis**: System analyzes search results for recent updates
3. **Memory Check**: System checks if similar notification was already sent
4. **Decision**: 
   - If duplicate found: `should_send_email: false`
   - If new updates: `should_send_email: true` and mark as sent

## Example Output

### First Run (New Updates Found)
```json
{
  "should_send_email": true,
  "reasoning": "Found 4 relevant updates for 'tax policy' - notification will be sent",
  "topic_searched": "tax policy",
  "relevant_updates": [...],
  "total_search_results": 5
}
```

### Second Run (Duplicate Detection)
```json
{
  "should_send_email": false,
  "reasoning": "Notification already sent for these 4 updates on 'tax policy'",
  "topic_searched": "tax policy",
  "relevant_updates": [...],
  "total_search_results": 5
}
```

## Configuration

### Database Location
- Default: `notification_memory.db` in the project root
- Can be customized by passing `db_path` to `NotificationMemory()`

### Cleanup
- Automatic cleanup of old notifications (configurable)
- Default retention: 30 days for history table
- Idempotency table keeps all records for duplicate prevention

## Testing

### Run Memory System Tests
```bash
# Test memory system functionality
python test_memory_system.py

# Test with controlled data
python test_memory_simple.py

# Test complete system integration
python test_complete_system.py
```

### Expected Behavior
1. **First call**: Should send email (new updates found)
2. **Second call**: Should NOT send email (duplicate detected)
3. **Different topic**: Should send email (new topic)
4. **Different updates**: Should send email (new content)

## Benefits

### ✅ **Prevents Spam**
- No duplicate notifications for the same updates
- Users only receive notifications about new information

### ✅ **Efficient Resource Usage**
- Avoids unnecessary email sending
- Reduces API calls and processing time

### ✅ **Audit Trail**
- Complete history of sent notifications
- Statistics and reporting capabilities

### ✅ **Scalable**
- SQLite database for persistence
- Can handle multiple topics and recipients
- Automatic cleanup prevents database bloat

## Future Enhancements

- **Email Integration**: Direct email sending with SMTP
- **Multiple Recipients**: Support for different notification lists
- **Advanced Filtering**: More sophisticated duplicate detection
- **Web Interface**: Dashboard for notification management
- **Scheduled Cleanup**: Automatic database maintenance
