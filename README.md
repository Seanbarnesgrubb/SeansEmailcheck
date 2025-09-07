(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/README_email_checker.md b/README_email_checker.md
--- a/README_email_checker.md
+++ b/README_email_checker.md
@@ -0,0 +1,177 @@
+# Email Checker
+
+A Python script that checks if you've received emails from a specific sender (like "missive" or any email address). It supports Gmail, Outlook, Yahoo, and other IMAP-enabled email providers.
+
+## Features
+
+- ✅ Search for emails from specific senders
+- 📅 Configurable date range (default: last 30 days)
+- 🔐 Secure password input (hidden when typing)
+- 💾 Save email configuration for future use
+- 🌐 Auto-detects server settings for popular email providers
+- 📧 Works with Gmail, Outlook, Yahoo, iCloud, AOL, and custom IMAP servers
+
+## Quick Start
+
+### Basic Usage
+```bash
+python email_checker.py user@missive.com
+```
+
+### With your email address
+```bash
+python email_checker.py user@missive.com --email your.email@gmail.com
+```
+
+### Search last 7 days only
+```bash
+python email_checker.py user@missive.com --days 7
+```
+
+## Setup Instructions
+
+### 1. Prerequisites
+- Python 3.6 or higher (uses only standard library)
+- Email account with IMAP access enabled
+
+### 2. Email Provider Setup
+
+#### Gmail
+1. Enable 2-factor authentication
+2. Generate an "App Password":
+   - Go to Google Account settings
+   - Security → 2-Step Verification → App passwords
+   - Generate password for "Mail"
+3. Use the app password when prompted
+
+#### Outlook/Hotmail
+1. Enable 2-factor authentication (recommended)
+2. Generate an app password or use your regular password
+3. Ensure IMAP is enabled in Outlook settings
+
+#### Yahoo
+1. Enable 2-factor authentication
+2. Generate an app password:
+   - Account Security → Generate app password
+3. Use the app password when prompted
+
+### 3. Running the Script
+
+```bash
+# Make the script executable
+chmod +x email_checker.py
+
+# Run with basic search
+python email_checker.py sender@example.com
+
+# Run with all options
+python email_checker.py sender@example.com \
+  --email your.email@gmail.com \
+  --days 14 \
+  --mailbox INBOX \
+  --save-config
+```
+
+## Command Line Options
+
+| Option | Short | Description | Default |
+|--------|-------|-------------|---------|
+| `sender_email` | - | Email address to search for | Required |
+| `--email` | `-e` | Your email address | Prompted if not provided |
+| `--password` | `-p` | Your email password | Prompted securely if not provided |
+| `--server` | `-s` | IMAP server address | Auto-detected |
+| `--port` | - | IMAP server port | 993 |
+| `--days` | `-d` | Days to search back | 30 |
+| `--mailbox` | `-m` | Mailbox to search | INBOX |
+| `--save-config` | - | Save configuration for future use | False |
+| `--no-ssl` | - | Disable SSL connection | False (SSL enabled) |
+
+## Configuration
+
+The script can save your email configuration (excluding password) for convenience:
+
+```bash
+python email_checker.py sender@example.com --save-config
+```
+
+This creates `email_config.json` with your email settings.
+
+## Example Output
+
+```
+🔍 Searching for emails from: user@missive.com
+📧 Using account: your.email@gmail.com
+🌐 Server: imap.gmail.com:993
+📅 Searching last 30 days
+--------------------------------------------------
+✅ Successfully connected to your.email@gmail.com
+🔍 Found 3 emails from user@missive.com in the last 30 days
+
+✅ Found 3 email(s) from user@missive.com:
+================================================================================
+
+📧 Email #1
+   Subject: Welcome to Missive!
+   From: "Missive Team" <user@missive.com>
+   Date: 2024-01-15 10:30:00
+----------------------------------------
+
+📧 Email #2
+   Subject: Your team collaboration update
+   From: user@missive.com
+   Date: 2024-01-10 14:22:15
+----------------------------------------
+
+📧 Email #3
+   Subject: New features available
+   From: "Missive" <user@missive.com>
+   Date: 2024-01-05 09:15:30
+----------------------------------------
+```
+
+## Troubleshooting
+
+### Common Issues
+
+1. **Authentication Failed**
+   - Use app passwords for Gmail, Yahoo, Outlook
+   - Enable 2-factor authentication first
+   - Check if IMAP is enabled
+
+2. **Connection Timeout**
+   - Check your internet connection
+   - Verify server settings
+   - Try with `--no-ssl` for some servers
+
+3. **No Emails Found**
+   - Check the sender email address spelling
+   - Try increasing `--days` parameter
+   - Verify the sender actually sent emails
+
+### Server Settings for Other Providers
+
+If auto-detection doesn't work, use manual server settings:
+
+```bash
+# Custom IMAP server
+python email_checker.py sender@example.com \
+  --server imap.yourprovider.com \
+  --port 993
+```
+
+Common IMAP servers:
+- Gmail: `imap.gmail.com:993`
+- Outlook: `outlook.office365.com:993`
+- Yahoo: `imap.mail.yahoo.com:993`
+- iCloud: `imap.mail.me.com:993`
+
+## Security Notes
+
+- Passwords are never stored in configuration files
+- Use app passwords instead of main account passwords
+- The script uses secure IMAP SSL connections by default
+- Consider using environment variables for automation
+
+## License
+
+This project is open source and available under the MIT License.
EOF
)
