# API Documentation

## Endpoints

### GET /api/v1/events

### Description
Get all events

### Response

```json
{
    "events": [
        {
            "id": 1,
            "name": "Event 1",
            "action": "If any update in tax policy then send email to the user",
            "cron_job": "Every day at 12:00 AM"
        }
    ]
}
```
### GET /api/v1/events/{event_id}

### Description
Get the event with the given event_id

### Response

```json
{
    "event": {
        "id": 1,
        "name": "Event 1",
        "action": "If any update in tax policy then send email to the user",
        "cron_job": "Every day at 12:00 AM"
    }
}
```

<!-- create event with action and cron job -->

### POST /api/v1/events

### Description
Create a new event with the given name, action, and cron job

### Request

```json
{
    "name": "Event 1",
    "action": "If any update in tax policy then send email to the user",
    "cron_job": "Every day at 12:00 AM"
}
```

### Response

```json
{
    "event": {
        "id": 1,
        "name": "Event 1",
        "action": "If any update in tax policy then send email to the user",
        "cron_job": "Every day at 12:00 AM"
    }
}
```

<!-- update event -->   

### PUT /api/v1/events/{event_id}
### Description
Update the event with the given event_id
### Request

```json
{
    "name": "Event 1",
    "action": "If any update in tax policy then send email to the user",
    "cron_job": "Every day at 12:00 AM"
}
```

### Response

```json
{
    "event": {
        "id": 1,
        "name": "Event 1",
        "action": "If any update in tax policy then send email to the user",
        "cron_job": "Every day at 12:00 AM"
    }
}
```     

<!-- delete event -->

### DELETE /api/v1/events/{event_id}

### Description
Delete the event with the given event_id

### Response

```json
{
    "message": "Event deleted successfully",
    "event": {
        "id": 1,
        "name": "Event 1",
        "action": "If any update in tax policy then send email to the user",
        "cron_job": "Every day at 12:00 AM"
    }
}
``` 

