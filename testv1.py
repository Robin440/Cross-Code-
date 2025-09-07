from services.email.email_service import EmailService


email_service = EmailService()

try:
    email_service.send_email(
        subject="Test Email from Django",
        template_name="custom_email.html",
        recipients=["robinrajan440@gmail.com"],
        context={"username": "TestUser", "message": "This is a test email sent from Django."}
    )
except Exception as e:
    print(f"Failed to send test email: {e}")       

print("Test email sent.")

