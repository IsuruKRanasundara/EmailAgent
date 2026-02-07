# main.py
from email_agent import EmailAgent
import time

def print_menu():
    print("\n" + "="*50)
    print("📧 EMAIL AGENT - Main Menu")
    print("="*50)
    print("1. Check unread emails")
    print("2. Generate reply to email")
    print("3. Draft new email")
    print("4. Summarize email")
    print("5. Auto-reply to unread emails")
    print("6. Exit")
    print("="*50)

def main():
    print("🚀 Starting Email Agent...")
    agent = EmailAgent()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            # Check unread emails
            emails = agent.read_unread_emails()
            
            if emails:
                for i, email_data in enumerate(emails, 1):
                    print(f"\n--- Email {i} ---")
                    print(f"From: {email_data['from']}")
                    print(f"Subject: {email_data['subject']}")
                    print(f"Body preview: {email_data['body'][:200]}...")
            else:
                print("\n📭 No unread emails found!")
        
        elif choice == '2':
            # Generate reply
            emails = agent.read_unread_emails(max_emails=1)
            
            if emails:
                email_data = emails[0]
                print(f"\n📧 Email from: {email_data['from']}")
                print(f"Subject: {email_data['subject']}")
                print(f"Body: {email_data['body'][:300]}...")
                
                tone = input("\nChoose tone (professional/friendly/formal): ").strip() or "professional"
                reply = agent.generate_reply(email_data, tone=tone)
                
                print(f"\n📝 Generated Reply:\n{reply}")
                
                send = input("\nSend this reply? (yes/no): ").strip().lower()
                if send == 'yes':
                    agent.send_email(email_data['from'], email_data['subject'], reply)
            else:
                print("\n📭 No emails to reply to!")
        
        elif choice == '3':
            # Draft new email
            instruction = input("\nDescribe the email you want to write: ").strip()
            draft = agent.draft_email(instruction)
            
            print(f"\n📝 Draft:\n{draft}")
            
            send = input("\nWant to send this? Enter recipient email (or 'no'): ").strip()
            if send != 'no' and '@' in send:
                subject = input("Email subject: ").strip()
                agent.send_email(send, subject, draft)
        
        elif choice == '4':
            # Summarize email
            emails = agent.read_unread_emails(max_emails=1)
            
            if emails:
                summary = agent.summarize_email(emails[0])
                print(f"\n📊 Summary: {summary}")
            else:
                print("\n📭 No emails to summarize!")
        
        elif choice == '5':
            # Auto-reply
            emails = agent.read_unread_emails()
            
            if emails:
                print(f"\n🤖 Auto-replying to {len(emails)} email(s)...")
                
                for email_data in emails:
                    print(f"\nProcessing email from {email_data['from']}...")
                    reply = agent.generate_reply(email_data)
                    agent.send_email(email_data['from'], email_data['subject'], reply)
                    time.sleep(2)  # Avoid rate limits
                
                print("\n✅ All emails processed!")
            else:
                print("\n📭 No emails to process!")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()