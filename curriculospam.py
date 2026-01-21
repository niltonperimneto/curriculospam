import imaplib
import smtplib
import email
import datetime
import getpass
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr
from typing import List, Set

# --- CONFIGURATION ---
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Note: IMAP search is often case-insensitive but can be sensitive to accents
# Note: IMAP search is often case-insensitive but can be sensitive to accents
SEARCH_KEYWORDS = ["curriculo", "Curriculo", "currículo", "Currículo"]
DAYS_BACK = 90
SENT_FOLDER = '"[Gmail]/Sent Mail"'  # Adjust for your provider (e.g., "Sent", "Sent Items")

SUBJECT_LINE = "Follow-up: Candidatura Professor de História - Nilton Perim Neto"
BODY_TEMPLATE = """
Olá,

Gostaria de confirmar o recebimento do meu currículo enviado anteriormente e reiterar meu interesse na vaga.
Permaneço à disposição para uma entrevista.

Atenciosamente,
Nilton Perim Neto
"""

def build_or_query(keywords: List[str]) -> str:
    """Recursively builds an IMAP OR query for multiple keywords."""
    # Base case: if only one keyword, just return the TEXT search criterion
    if len(keywords) == 1:
        return f'TEXT "{keywords[0]}"'
    
    # Recursive case: (OR TEXT "kw1" (OR TEXT "kw2" ...))
    return f'(OR TEXT "{keywords[0]}" {build_or_query(keywords[1:])})'

def get_recent_targets(email_user: str, email_pass: str) -> List[str]:
    """Scans Sent folder for keyword in the last X days and returns unique email addresses."""
    targets: Set[str] = set()
    
    try:
        # Context manager handles logout automatically
        with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
            mail.login(email_user, email_pass)
            
            status, _ = mail.select(SENT_FOLDER)
            if status != 'OK':
                print(f"Error: Could not select folder {SENT_FOLDER}. Check folder name.")
                return []

            date_cutoff = (datetime.date.today() - datetime.timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
            print(f"[*] Scanning '{SENT_FOLDER}' since {date_cutoff} for keywords: {SEARCH_KEYWORDS}...")

            # Build the recursive OR query
            keyword_query = build_or_query(SEARCH_KEYWORDS)
            full_query = f'(SINCE "{date_cutoff}" {keyword_query})'
            
            # Search query
            typ, data = mail.search(None, full_query)
            
            if not data[0]:
                print("[-] No emails found matching criteria.")
                return []

            email_ids = data[0].split()
            print(f"[*] Found {len(email_ids)} matching emails. Parsing recipients...")

            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        to_header = msg.get("To")
                        if to_header:
                            # Robust decoding and extraction
                            decoded_header = str(make_header(decode_header(to_header)))
                            # parseaddr extracts 'user@domain.com' from 'Name <user@domain.com>'
                            _, email_address = parseaddr(decoded_header)
                            
                            if email_address:
                                targets.add(email_address)

        return list(targets)

    except Exception as e:
        print(f"Error checking IMAP: {e}")
        return []

def send_followup(recipients: List[str], email_user: str, email_pass: str) -> None:
    """Sends the follow-up emails via SMTP."""
    if not recipients:
        return

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(email_user, email_pass)

            for recipient in recipients:
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = recipient
                msg['Subject'] = SUBJECT_LINE
                msg.attach(MIMEText(BODY_TEMPLATE, 'plain'))

                server.sendmail(email_user, recipient, msg.as_string())
                print(f"[+] Email sent to: {recipient}")

        print("[*] Batch complete.")

    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    try:
        u_email = input("Enter your email: ")
        u_pass = getpass.getpass("Enter your App Password: ")
    except KeyboardInterrupt:
        print("\nInput cancelled.")
        exit(0)

    # 1. Gather Targets
    targets = get_recent_targets(u_email, u_pass)
    
    print("\n" + "="*30)
    print(f"DRY RUN RESULTS: Found {len(targets)} unique recipients.")
    print("="*30)
    
    for r in targets:
        print(f"- {r}")

    # 2. Safety Gate
    if targets:
        print("\nWARNING: Review the list above carefully.")
        confirm = input("Do you want to send emails to these people NOW? (yes/no): ")
        
        if confirm.lower() == "yes":
            send_followup(targets, u_email, u_pass)
        else:
            print("Operation cancelled. No emails sent.")
    else:
        print("No targets found via search.")