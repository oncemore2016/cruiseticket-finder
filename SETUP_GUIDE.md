# Royal Caribbean Ticket Monitor - Setup Guide (Gmail Version)

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

### 1. Set Up Gmail App Password

Gmail requires an "App Password" for automated scripts (not your regular password).

1. **Enable 2-Step Verification** (required first):
   - Go to [myaccount.google.com/security](https://myaccount.google.com/security)
   - Scroll to "How you sign in to Google"
   - Click "2-Step Verification" and follow setup

2. **Create App Password**:
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select app: "Mail"
   - Select device: "Other" (type "Cruise Monitor")
   - Click "Generate"
   - Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)
   - **Important:** Save this password - you can't view it again!

### 2. Set Up GitHub Actions

1. **Create a GitHub repository:**
   - Go to [github.com](https://github.com) and create a new repository
   - Name it something like `cruise-ticket-monitor`
   - Can be private or public

2. **Upload these files to your repository:**
   - `cruise_monitor.py`
   - `requirements.txt`
   - `.github/workflows/cruise-monitor.yml`

   **Via GitHub web interface:**
   - Click "Add file" → "Upload files"
   - Drag and drop all three files
   - Commit changes

   **Or via git commands:**
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

   | Secret Name | Value | Example |
   |-------------|-------|---------|
   | `GMAIL_ADDRESS` | Your Gmail address | `your.email@gmail.com` |
   | `GMAIL_APP_PASSWORD` | The 16-char app password from step 1 | `abcdefghijklmnop` (no spaces) |
   | `RECIPIENT_EMAIL` | Email to receive alerts | `linglingsan@gmail.com` |

4. **Enable GitHub Actions:**
   - Go to **Actions** tab in your repository
   - Click "I understand my workflows, go ahead and enable them"
   - You should see "Royal Caribbean Ticket Monitor" workflow

5. **Test it manually:**
   - In the Actions tab, click on "Royal Caribbean Ticket Monitor"
   - Click "Run workflow" → "Run workflow"
   - Wait ~30 seconds and check the run logs
   - You should see "Checking availability..." in the logs

---

## How It Works

- **Automatic checks:** GitHub Actions runs the monitor every 5 minutes
- **When tickets found:**
  - Email sent from your Gmail to linglingsan@gmail.com
  - Email contains direct link to book
  - Monitoring continues running
- **Cost:** Completely free
  - GitHub: 2,000 minutes/month free
  - Gmail: Unlimited emails

---

## Troubleshooting

### Authentication Error?

**"Username and Password not accepted":**
- Make sure you created an **App Password**, not using your regular Gmail password
- App password must be 16 characters, no spaces
- 2-Step Verification must be enabled first

**"Less secure app access":**
- This is old advice - ignore it
- Use App Passwords (the modern secure method)

### Not receiving emails?

1. **Check spam folder:** First automated emails might go to spam
2. **Verify GMAIL_ADDRESS:** Should be your full Gmail address
3. **Test email manually:**
   ```bash
   python cruise_monitor.py
   ```
   Check the output for email errors

### Workflow not running?

- GitHub Actions requires at least one commit after adding workflow file
- Check Actions tab → make sure workflows are enabled
- Scheduled workflows may take 5-10 minutes to first trigger
- Free GitHub accounts: workflows disabled after 60 days of repo inactivity

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

**Option 1: Disable workflow**
1. Go to your GitHub repository
2. Go to **Actions** tab
3. Click on "Royal Caribbean Ticket Monitor" workflow
4. Click "..." (three dots) → "Disable workflow"

**Option 2: Delete workflow file**
- Delete `.github/workflows/cruise-monitor.yml` from your repository

---

## Testing Locally

Before deploying to GitHub, you can test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (Mac/Linux)
export GMAIL_ADDRESS="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your-16-char-app-password"
export RECIPIENT_EMAIL="linglingsan@gmail.com"

# Windows PowerShell
$env:GMAIL_ADDRESS="your.email@gmail.com"
$env:GMAIL_APP_PASSWORD="your-16-char-app-password"
$env:RECIPIENT_EMAIL="linglingsan@gmail.com"

# Run the monitor
python cruise_monitor.py
```

---

## Security Notes

✅ **Safe:**
- App passwords are designed for this use case
- Limited to mail access only (can't access other Google services)
- Can be revoked anytime at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

✅ **GitHub Secrets are encrypted:**
- Only visible to you
- Not exposed in logs
- Can't be read by others even in public repos

⚠️ **Keep private:**
- Never commit app password to code
- Always use GitHub Secrets
- Don't share app password

---

## Questions?

**Check frequency:**
- Default: every 5 minutes
- To change: edit `.github/workflows/cruise-monitor.yml` cron schedule
- Example for every 10 min: `*/10 * * * *`

**Monitor multiple cruises:**
- Create separate workflow files, or
- Duplicate the script with different parameters

**Different sender email:**
- Change `GMAIL_ADDRESS` secret
- Generate new app password for that account

**Notification preferences:**
- Current: only notifies when tickets found
- To get periodic updates: uncomment line 226 in cruise_monitor.py

Good luck finding your cruise! 🚢
