#!/usr/bin/env python3
"""
Email Checker - Check if you've received emails from a specific sender
Supports Gmail, Outlook, Yahoo, and other IMAP-enabled email providers
"""

import imaplib
import email
from email.header import decode_header
import getpass
import sys
import argparse
from datetime import datetime, timedelta
import json
import os

class EmailChecker:
    def __init__(self, email_address, password, server, port=993, use_ssl=True):
        self.email_address = email_address
        self.password = password
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.mail = None
    
    def connect(self):
        """Connect to the email server"""
        try:
            if self.use_ssl:
                self.mail = imaplib.IMAP4_SSL(self.server, self.port)
            else:
                self.mail = imaplib.IMAP4(self.server, self.port)
            
            self.mail.login(self.email_address, self.password)
            print(f"✅ Successfully connected to {self.email_address}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the email server"""
        if self.mail:
            self.mail.close()
            self.mail.logout()
    
    def search_emails_from_sender(self, sender_email, days_back=30, mailbox="INBOX"):
        """Search for emails from a specific sender"""
        if not self.mail:
            print("❌ Not connected to email server")
            return []
        
        try:
            # Select the mailbox
            self.mail.select(mailbox)
            
            # Calculate date range
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            # Search for emails from the sender
            search_criteria = f'(FROM "{sender_email}" SINCE "{since_date}")'
            status, messages = self.mail.search(None, search_criteria)
            
            if status != 'OK':
                print(f"❌ Search failed: {status}")
                return []
            
            email_ids = messages[0].split()
            found_emails = []
            
            print(f"🔍 Found {len(email_ids)} emails from {sender_email} in the last {days_back} days")
            
            for email_id in email_ids:
                try:
                    # Fetch the email
                    status, msg_data = self.mail.fetch(email_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    # Parse the email
                    email_message = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract email details
                    subject = self.decode_header_value(email_message.get("Subject", ""))
                    from_addr = self.decode_header_value(email_message.get("From", ""))
                    date_str = email_message.get("Date", "")
                    
                    # Parse date
                    try:
                        email_date = email.utils.parsedate_to_datetime(date_str)
                        formatted_date = email_date.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        formatted_date = date_str
                    
                    found_emails.append({
                        'id': email_id.decode(),
                        'subject': subject,
                        'from': from_addr,
                        'date': formatted_date,
                        'raw_date': date_str
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error processing email {email_id}: {str(e)}")
                    continue
            
            return found_emails
            
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def decode_header_value(self, header_value):
        """Decode email header values"""
        if not header_value:
            return ""
        
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(encoding or 'utf-8')
                except:
                    decoded_string += part.decode('utf-8', errors='ignore')
            else:
                decoded_string += part
        
        return decoded_string

def get_email_server_config(email_address):
    """Get IMAP server configuration based on email provider"""
    domain = email_address.split('@')[1].lower()
    
    server_configs = {
        'gmail.com': {'server': 'imap.gmail.com', 'port': 993},
        'outlook.com': {'server': 'outlook.office365.com', 'port': 993},
        'hotmail.com': {'server': 'outlook.office365.com', 'port': 993},
        'live.com': {'server': 'outlook.office365.com', 'port': 993},
        'yahoo.com': {'server': 'imap.mail.yahoo.com', 'port': 993},
        'icloud.com': {'server': 'imap.mail.me.com', 'port': 993},
        'aol.com': {'server': 'imap.aol.com', 'port': 993},
    }
    
    return server_configs.get(domain, {'server': f'imap.{domain}', 'port': 993})

def load_config():
    """Load configuration from config.json if it exists"""
    config_file = '/workspace/email_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading config: {str(e)}")
    return {}

def save_config(config):
    """Save configuration to config.json"""
    config_file = '/workspace/email_config.json'
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"💾 Configuration saved to {config_file}")
    except Exception as e:
        print(f"⚠️ Error saving config: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Check if you have received emails from a specific sender')
    parser.add_argument('sender_email', help='Email address to search for (e.g., user@missive.com)')
    parser.add_argument('--email', '-e', help='Your email address')
    parser.add_argument('--password', '-p', help='Your email password or app password')
    parser.add_argument('--server', '-s', help='IMAP server address')
    parser.add_argument('--port', type=int, default=993, help='IMAP server port (default: 993)')
    parser.add_argument('--days', '-d', type=int, default=30, help='Number of days to search back (default: 30)')
    parser.add_argument('--mailbox', '-m', default='INBOX', help='Mailbox to search (default: INBOX)')
    parser.add_argument('--save-config', action='store_true', help='Save email configuration for future use')
    parser.add_argument('--no-ssl', action='store_true', help='Disable SSL connection')
    
    args = parser.parse_args()
    
    # Load existing config
    config = load_config()
    
    # Get email credentials
    email_address = args.email or config.get('email_address')
    if not email_address:
        email_address = input("Enter your email address: ")
    
    password = args.password or config.get('password')
    if not password:
        password = getpass.getpass("Enter your email password (or app password): ")
    
    # Get server configuration
    if args.server:
        server = args.server
        port = args.port
    else:
        server_config = get_email_server_config(email_address)
        server = config.get('server', server_config['server'])
        port = config.get('port', server_config['port'])
    
    # Save configuration if requested
    if args.save_config:
        new_config = {
            'email_address': email_address,
            'server': server,
            'port': port
        }
        # Don't save password for security
        save_config(new_config)
    
    print(f"🔍 Searching for emails from: {args.sender_email}")
    print(f"📧 Using account: {email_address}")
    print(f"🌐 Server: {server}:{port}")
    print(f"📅 Searching last {args.days} days")
    print("-" * 50)
    
    # Create email checker instance
    checker = EmailChecker(email_address, password, server, port, not args.no_ssl)
    
    try:
        # Connect to email server
        if not checker.connect():
            sys.exit(1)
        
        # Search for emails
        emails = checker.search_emails_from_sender(args.sender_email, args.days, args.mailbox)
        
        if emails:
            print(f"\n✅ Found {len(emails)} email(s) from {args.sender_email}:")
            print("=" * 80)
            
            for i, email_info in enumerate(emails, 1):
                print(f"\n📧 Email #{i}")
                print(f"   Subject: {email_info['subject']}")
                print(f"   From: {email_info['from']}")
                print(f"   Date: {email_info['date']}")
                print("-" * 40)
        else:
            print(f"\n❌ No emails found from {args.sender_email} in the last {args.days} days")
    
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    finally:
        checker.disconnect()

if __name__ == "__main__":
    main()