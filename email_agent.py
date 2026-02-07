# email_agent.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG, HUGGINGFACE_CONFIG
from classifier import EmailClassifier

class EmailAgent:
    def __init__(self):
        print("🔄 Loading AI model... (this may take a few minutes first time)")
        
        # Using FLAN-T5 - free and excellent for email tasks
        model_name = "google/flan-t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=HUGGINGFACE_CONFIG['token']  # Add token here
        )        
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            token=HUGGINGFACE_CONFIG['token']  # Add token here
        )  
        self.classifier = EmailClassifier()
        print("✅ Model loaded successfully!")
        
        self.email = EMAIL_CONFIG['email']
        self.password = EMAIL_CONFIG['password']
        self.imap_server = EMAIL_CONFIG['imap_server']
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
    
    def classify_email(self, email_content):
        text = f"{email_content['subject']} {email_content['body']}"
        category, scores = self.classifier.classify(text)
        return category
    
    def read_unread_emails(self, max_emails=5):
        """Read unread emails from inbox"""
        print(f"\n📬 Connecting to {self.imap_server}...")
        
        try:
            # Connect to email server
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)
            mail.select('inbox')
            
            # Search for unread emails
            _, message_numbers = mail.search(None, 'UNSEEN')
            
            emails = []
            for num in message_numbers[0].split()[:max_emails]:
                _, msg_data = mail.fetch(num, '(RFC822)')
                email_body = email.message_from_bytes(msg_data[0][1])
                
                # Extract email details
                subject = email_body['subject']
                from_email = email.utils.parseaddr(email_body['from'])[1]
                
                # Get email body
                body = ""
                if email_body.is_multipart():
                    for part in email_body.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_body.get_payload(decode=True).decode()
                
                emails.append({
                    'from': from_email,
                    'subject': subject,
                    'body': body[:500],  # Limit body length
                })
            
            mail.close()
            mail.logout()
            
            print(f"✅ Found {len(emails)} unread email(s)")
            return emails
            
        except Exception as e:
            print(f"❌ Error reading emails: {e}")
            return []
    
    def generate_reply(self, email_content, tone="professional"):
        """Generate AI response to email"""
        print("\n🤖 Generating AI response...")
        
        prompt = f"""Write a {tone} email reply to the following email:

Subject: {email_content['subject']}
From: {email_content['from']}

Email content:
{email_content['body']}

Reply:"""
        
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            max_length=512, 
            truncation=True
        )
        
        outputs = self.model.generate(
            **inputs,
            max_length=200,
            num_beams=4,
            temperature=0.7,
            do_sample=True
        )
        
        reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("✅ Reply generated!")
        return reply
    
    def send_email(self, to_email, subject, body):
        """Send email"""
        print(f"\n📧 Sending email to {to_email}...")
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = f"Re: {subject}"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            print("✅ Email sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def draft_email(self, instruction):
        """Draft a new email from scratch"""
        print("\n✍️ Drafting email...")
        
        prompt = f"Write a professional email: {instruction}"
        
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
        outputs = self.model.generate(**inputs, max_length=200)
        
        draft = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("✅ Draft created!")
        return draft
    
    def summarize_email(self, email_content):
        """Summarize email content"""
        print("\n📝 Summarizing email...")
        
        prompt = f"Summarize this email in one sentence: {email_content['body']}"
        
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(**inputs, max_length=50)
        
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("✅ Summary created!")
        return summary