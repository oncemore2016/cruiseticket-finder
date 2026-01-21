#!/usr/bin/env python3
"""
Royal Caribbean Cruise Ticket Monitor
Checks availability and sends email notifications via Mailgun
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Configuration - set these as environment variables
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'linglingsan@gmail.com')

# Cruise search parameters
SHIP_NAME = "Navigator of the Seas"
DESTINATION = "Mexico"
DEPARTURE_DATE = "2026-02-07"
DURATION = 7
NUM_GUESTS = 2


def check_availability():
    """Check Royal Caribbean website for cruise availability"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking availability...")

    base_url = "https://www.royalcaribbean.com/cruises"
    params = {
        "ship": SHIP_NAME.lower().replace(" ", "-"),
        "destination": DESTINATION.lower(),
        "duration": f"{DURATION}-nights",
        "departureDate": DEPARTURE_DATE,
        "numGuests": NUM_GUESTS
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for availability indicators
        text_lower = response.text.lower()

        if "sold out" in text_lower or "not available" in text_lower:
            status = "not_available"
            message = "No availability"
        elif "book now" in text_lower or "select" in text_lower:
            status = "available"
            message = "Tickets available!"
        else:
            status = "unclear"
            message = "Status unclear - manual check recommended"

        # Extract cruise links
        cruise_details = []
        cruise_links = soup.find_all('a', href=re.compile(r'/cruises/'))
        for link in cruise_links[:5]:
            title = link.get_text(strip=True)
            if title:
                url = link['href']
                if url.startswith('/'):
                    url = f"https://www.royalcaribbean.com{url}"
                cruise_details.append({"title": title[:100], "url": url})

        print(f"Status: {message}")

        return {
            "status": status,
            "message": message,
            "search_url": response.url,
            "cruises": cruise_details,
            "checked_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error checking availability: {str(e)}")
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "checked_at": datetime.now().isoformat()
        }


def send_mailgun_email(subject, body_text, body_html):
    """Send email notification via Mailgun"""

    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("❌ Mailgun credentials not configured")
        print("Set MAILGUN_API_KEY and MAILGUN_DOMAIN environment variables")
        return False

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Cruise Monitor <monitor@{MAILGUN_DOMAIN}>",
                "to": RECIPIENT_EMAIL,
                "subject": subject,
                "text": body_text,
                "html": body_html
            },
            timeout=10
        )

        if response.status_code == 200:
            print(f"✅ Email sent to {RECIPIENT_EMAIL}")
            return True
        else:
            print(f"❌ Email failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False


def send_notification(result):
    """Send email notification about availability"""

    available = result["status"] == "available"

    if available:
        subject = "🎉 TICKETS AVAILABLE - Royal Caribbean Navigator!"
    else:
        subject = "Royal Caribbean Monitor - No Availability Yet"

    # Plain text email
    body_text = f"""
Royal Caribbean Cruise Ticket Alert

Status: {result['message']}

Cruise Details:
- Ship: {SHIP_NAME}
- Destination: {DESTINATION} (Cabo San Lucas)
- Departure Date: {DEPARTURE_DATE}
- Duration: {DURATION} nights
- Guests: {NUM_GUESTS}

Checked at: {result['checked_at']}

View on Royal Caribbean: {result.get('search_url', 'N/A')}

---
Automated notification from your cruise ticket monitor
"""

    # HTML email
    cruises_html = ""
    if result.get('cruises'):
        cruises_html = "<h3>Available Cruises:</h3><ul>"
        for cruise in result['cruises']:
            cruises_html += f'<li><a href="{cruise["url"]}">{cruise["title"]}</a></li>'
        cruises_html += "</ul>"

    body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background: {'#28a745' if available else '#6c757d'}; color: white; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">{result['message']}</h1>
    </div>

    <div style="padding: 20px; background: #f8f9fa;">
        <h2>Cruise Details</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Ship:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{SHIP_NAME}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Destination:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{DESTINATION} (Cabo San Lucas)</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Departure:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{DEPARTURE_DATE}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Duration:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{DURATION} nights</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Guests:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{NUM_GUESTS}</td></tr>
        </table>
    </div>

    {cruises_html}

    <div style="padding: 20px; text-align: center;">
        <a href="{result.get('search_url', '#')}" style="background-color: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">View on Royal Caribbean</a>
    </div>

    <div style="padding: 20px; background: #f8f9fa; text-align: center; font-size: 12px; color: #666;">
        <p>Checked at: {result['checked_at']}</p>
        <p>Automated notification from your cruise ticket monitor</p>
    </div>
</body>
</html>
"""

    return send_mailgun_email(subject, body_text, body_html)


def main():
    """Main monitoring function"""
    print("=" * 60)
    print("Royal Caribbean Cruise Ticket Monitor")
    print("=" * 60)
    print(f"Ship: {SHIP_NAME}")
    print(f"Destination: {DESTINATION}")
    print(f"Departure: {DEPARTURE_DATE}")
    print(f"Duration: {DURATION} nights")
    print(f"Notification email: {RECIPIENT_EMAIL}")
    print("=" * 60)

    # Check availability
    result = check_availability()

    # Send notification if tickets are available
    if result["status"] == "available":
        print("\n🎉 TICKETS FOUND! Sending notification...")
        send_notification(result)
        sys.exit(0)  # Success - tickets found
    else:
        print(f"\n{result['message']}")
        # Optionally send periodic updates (commented out to avoid spam)
        # send_notification(result)
        sys.exit(1)  # No tickets yet


if __name__ == "__main__":
    main()
