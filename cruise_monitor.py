#!/usr/bin/env python3
"""
Royal Caribbean Cruise Ticket Monitor
Checks availability and sends email notifications via Gmail
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration - set these as environment variables
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')  # Your Gmail address
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # Gmail app password
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


def send_gmail_email(subject, body_text, body_html):
    """Send email notification via Gmail"""

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("❌ Gmail credentials not configured")
        print("Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables")
        return False

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL

        # Attach both plain text and HTML versions
        part1 = MIMEText(body_text, 'plain')
        part2 = MIMEText(body_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {RECIPIENT_EMAIL}")
        return True

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

    return send_gmail_email(subject, body_text, body_html)


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
