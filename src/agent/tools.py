import json
from typing import List, Dict, Any
from langchain.tools import tool
from ddgs import DDGS
from .notification_memory import notification_memory
from datetime import datetime


def create_email_content(topic: str, updates: List[Dict], recipient: str = "User") -> Dict[str, str]:
    """Create email subject and body content for notifications.
    
    Args:
        topic: The topic of the updates
        updates: List of update dictionaries with title, url, snippet
        recipient: Name of the email recipient
        
    Returns:
        Dictionary with 'subject' and 'body' keys containing email content
    """
    if not updates:
        return {
            "subject": f"No new updates found for {topic}",
            "body": f"Hello {recipient},\n\nNo new updates were found for the topic '{topic}' at this time.\n\nBest regards,\nEvent Action Agent"
        }
    
    subject = f"🔔 {len(updates)} New Update{'s' if len(updates) > 1 else ''} on {topic.title()}"
    current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    body_parts: List[str] = [
        f"Hello {recipient},",
        "",
        f"We found {len(updates)} new update{'s' if len(updates) > 1 else ''} on '{topic}' as of {current_date}:",
        "",
        "📋 Updates Summary:",
        ""
    ]
    
    for i, update in enumerate(updates, 1):
        title = update.get('title', 'No title available')
        url = update.get('url', 'No URL available')
        snippet = update.get('snippet', 'No description available')
        if len(snippet) > 200:
            snippet = snippet[:200] + "..."
        body_parts.extend([
            f"{i}. {title}",
            f"   Link: {url}",
            f"   Summary: {snippet}",
            ""
        ])
    
    body_parts.extend([
        "---",
        "",
        "This is an automated notification from Event Action Agent.",
        "",
        "Best regards,",
        "Event Action Agent"
    ])
    
    return {
        "subject": subject,
        "body": "\n".join(body_parts)
    }


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for current information about a topic, event, or query.
    
    Args:
        query: The search query to look up on the web
        max_results: Maximum number of search results to return (default: 5)
    
    Returns:
        JSON string containing search results with title, url, and snippet
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href") or r.get("url", ""),
                    "snippet": r.get("body", "")
                })
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})


@tool
def checkIsMailneedtoSend(event_data: str) -> str:
    """Check if an email needs to be sent based on event data by searching the web for updates.
    This function also checks notification memory to prevent duplicate emails.
    
    Args:
        event_data: JSON string containing event information with topic to check for updates
    
    Returns:
        JSON string with decision and reasoning about whether email should be sent
    """
    try:
        # Parse the event data
        event = json.loads(event_data) if isinstance(event_data, str) else event_data
        
        # Extract the topic to search for
        topic = event.get("topic", "")
        if not topic:
            return json.dumps({
                "should_send_email": False,
                "reasoning": "No topic specified for web search",
                "event_analyzed": event
            })
        
        # Search the web for recent updates on the topic
        search_query = f"latest updates {topic} today recent changes"
        try:
            with DDGS() as ddgs:
                search_results = []
                for r in ddgs.text(search_query, max_results=5):
                    search_results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href") or r.get("url", ""),
                        "snippet": r.get("body", "")
                    })
        except Exception as search_error:
            return json.dumps({
                "should_send_email": False,
                "reasoning": f"Web search failed: {str(search_error)}",
                "event_analyzed": event
            })
        
        # Analyze search results to determine if there are relevant updates
        should_send = False
        reasoning = "No relevant updates found"
        relevant_updates = []
        
        # Check if any results contain recent update indicators
        recent_keywords = ["today", "yesterday", "latest", "new", "updated", "announced", "released", "published"]
        date_keywords = ["2024", "2025", "january", "february", "march", "april", "may", "june", 
                        "july", "august", "september", "october", "november", "december"]
        
        for result in search_results:
            title_lower = result["title"].lower()
            snippet_lower = result["snippet"].lower()
            
            # Check for recent update indicators
            has_recent_keywords = any(keyword in title_lower or keyword in snippet_lower 
                                    for keyword in recent_keywords)
            has_date_keywords = any(keyword in title_lower or keyword in snippet_lower 
                                  for keyword in date_keywords)
            
            if has_recent_keywords or has_date_keywords:
                relevant_updates.append(result)
        
        # If we found relevant updates, check notification memory
        if relevant_updates:
            # Filter out updates that were already sent
            new_updates, already_sent_updates = notification_memory.filter_new_updates(topic, relevant_updates)
            
            if new_updates:
                email_content = create_email_content(topic, new_updates)
                notification_data = {
                    "should_send_email": True,
                    "reasoning": f"Found {len(new_updates)} new updates for '{topic}' ({len(already_sent_updates)} already sent)",
                    "topic_searched": topic,
                    "search_query": search_query,
                    "relevant_updates": new_updates,
                    "already_sent_updates": already_sent_updates,
                    "total_search_results": len(search_results),
                    "event_analyzed": event,
                    "email_content": email_content
                }
                should_send = True
                reasoning = f"Found {len(new_updates)} new updates for '{topic}' - notification will be sent"
                notification_memory.mark_notification_sent(topic, notification_data)
            else:
                # All updates were already sent previously
                email_content = create_email_content(topic, already_sent_updates) if already_sent_updates else None
                notification_data = {
                    "should_send_email": False,
                    "reasoning": f"All {len(already_sent_updates)} updates for '{topic}' were already sent previously",
                    "topic_searched": topic,
                    "search_query": search_query,
                    "relevant_updates": [],
                    "already_sent_updates": already_sent_updates,
                    "total_search_results": len(search_results),
                    "event_analyzed": event,
                    "email_content": email_content
                }
        else:
            notification_data = {
                "should_send_email": False,
                "reasoning": reasoning,
                "topic_searched": topic,
                "search_query": search_query,
                "relevant_updates": relevant_updates,
                "already_sent_updates": [],
                "total_search_results": len(search_results),
                "event_analyzed": event,
                "email_content": None
            }
        
        return json.dumps(notification_data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Email check failed: {str(e)}"})
