# Royal Caribbean Ticket Monitor - Setup Guide

## Overview
This automated system checks Royal Caribbean every 5 minutes for your cruise availability and emails you immediately when tickets are found.

**Your Cruise:**
- Ship: Navigator of the Seas
- Destination: Mexico (Cabo San Lucas)
- Departure: February 7, 2026
- Duration: 7 nights
- Guests: 2

**Email:** linglingsan@gmail.com

---

## Setup Steps

### 1. Set Up Mailgun (Email Service)

1. Go to [mailgun.com](https://www.mailgun.com) and sign up (free tier: 5,000 emails/month)
2. Verify your email address
3. In the Mailgun dashboard:
   - Go to **Sending** → **Domain settings**
   - Note your **Domain name** (e.g., `sandbox123abc.mailgun.org`)
   - Go to **Settings** → **API Keys**
   - Copy your **Private API key** (starts with `key-...`)

### 2. Set Up GitHub Actions

1. **Create a GitHub repository:**
   - Go to [github.com](https://github.com) and create a new repository
   - Name it something like `cruise-ticket-monitor`
   - Can be private or public

2. **Upload these files to your repository:**
   - `cruise_monitor.py`
   - `requirements.txt`
   - `.github/workflows/cruise-monitor.yml`

   You can do this via:
   - GitHub web interface (Add file → Upload files)
   - Or git commands:
     ```bash
     git init
     git add cruise_monitor.py requirements.txt .github/
     git commit -m "Initial cruise monitor setup"
     git remote add origin https://github.com/YOUR_USERNAME/cruise-ticket-monitor.git
     git push -u origin main
     ```

3. **Add secrets to GitHub:**
   - In your GitHub repository, go to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret** and add these three secrets:

   | Secret Name | Value |
   |-------------|-------|
   | `MAILGUN_API_KEY` | Your Mailgun private API key (e.g., `key-abc123...`) |
   | `MAILGUN_DOMAIN` | Your Mailgun domain (e.g., `sandbox123abc.mailgun.org`) |
   | `RECIPIENT_EMAIL` | `linglingsan@gmail.com` |

4. **Enable GitHub Actions:**
   - Go to **Actions** tab in your repository
   - Click "I understand my workflows, go ahead and enable them"
   - You should see "Royal Caribbean Ticket Monitor" workflow

5. **Test it manually:**
   - In the Actions tab, click on "Royal Caribbean Ticket Monitor"
   - Click "Run workflow" → "Run workflow"
   - Wait ~30 seconds and check the run logs

---

## How It Works

- **Automatic checks:** GitHub Actions runs the monitor every 5 minutes
- **When tickets found:**
  - You receive an email at linglingsan@gmail.com
  - Email contains direct link to book
  - Monitoring continues running
- **Cost:** Completely free (GitHub: 2,000 minutes/month, Mailgun: 5,000 emails/month)

---

## Troubleshooting

### Not receiving emails?

1. **Check Mailgun sandbox domain:**
   - Mailgun sandbox domains require authorized recipients
   - Go to Mailgun dashboard → **Sending** → **Authorized Recipients**
   - Add `linglingsan@gmail.com` and verify it
   - OR upgrade to a custom domain (free, but requires DNS setup)

2. **Check spam folder:** First emails from Mailgun might go to spam

3. **Check GitHub Actions logs:**
   - Go to Actions tab → latest run → check for errors

### Workflow not running?

- GitHub Actions requires at least one commit after adding workflow
- Check Actions tab → make sure workflows are enabled
- Scheduled workflows may take 5-10 minutes to first trigger

### Want to change cruise parameters?

Edit `cruise_monitor.py` and change these values:
```python
SHIP_NAME = "Navigator of the Seas"
DESTINATION = "Mexico"
DEPARTURE_DATE = "2026-02-07"
DURATION = 7
NUM_GUESTS = 2
```

Then commit and push changes.

---

## Stopping Monitoring

To stop the automated checks:
1. Go to your GitHub repository
2. Go to **Actions** tab
3. Click on "Royal Caribbean Ticket Monitor" workflow
4. Click "..." (three dots) → "Disable workflow"

Or delete `.github/workflows/cruise-monitor.yml` from your repository.

---

## Testing Locally

Before deploying to GitHub, you can test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MAILGUN_API_KEY="your-key-here"
export MAILGUN_DOMAIN="your-domain-here"
export RECIPIENT_EMAIL="linglingsan@gmail.com"

# Run the monitor
python cruise_monitor.py
```

---

## Questions?

Common adjustments:
- **Check more/less frequently:** Edit `.github/workflows/cruise-monitor.yml` cron schedule
- **Monitor multiple cruises:** Create separate workflow files or add parameters
- **Different email provider:** Replace Mailgun code with SendGrid, AWS SES, etc.

Good luck finding your cruise! 🚢
