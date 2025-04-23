import smtplib
import ssl
import certifi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import secrets

class AccountActivationManager(PasswordResetTokenGenerator):
    def token_generator(self):
        token = secrets.randbelow(1000000)
        return token

    def send_email(self, subject, body, recipient_email):
        # Your email credentials
        sender_email = "parampatel6844@gmail.com"
        sender_password = "zldv dsnu ebzz sjuw"  # Replace with your application-specific password

        # Compose the email
        message = f"Subject: {subject}\n\n{body}"

        # Set up the SMTP server with SSL context
        context = ssl.create_default_context(cafile=certifi.where())

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)  # Secure the connection
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

