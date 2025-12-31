"""Email service using Resend."""

import resend
from app.config import get_settings

settings = get_settings()


class EmailService:
    """Service for sending emails via Resend."""
    
    def __init__(self):
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY
    
    async def send_otp(self, email: str, code: str, language: str = "en") -> bool:
        """Send OTP code via email."""
        
        # Localized templates
        subjects = {
            "en": "Your login code",
            "es": "Tu código de acceso"
        }
        
        bodies = {
            "en": f"""
            <h2>Your verification code</h2>
            <p>Use this code to log in to Gift Sharing App:</p>
            <h1 style="font-size: 32px; letter-spacing: 4px; color: #4F46E5;">{code}</h1>
            <p>This code expires in 10 minutes.</p>
            <p>If you didn't request this code, you can safely ignore this email.</p>
            """,
            "es": f"""
            <h2>Tu código de verificación</h2>
            <p>Usa este código para iniciar sesión en Gift Sharing App:</p>
            <h1 style="font-size: 32px; letter-spacing: 4px; color: #4F46E5;">{code}</h1>
            <p>Este código expira en 10 minutos.</p>
            <p>Si no solicitaste este código, puedes ignorar este correo.</p>
            """
        }
        
        subject = subjects.get(language, subjects["en"])
        body = bodies.get(language, bodies["en"])
        
        if not settings.RESEND_API_KEY:
            # Dev mode: log to console with very visible output
            print("\n")
            print("*" * 60)
            print("*" + " " * 58 + "*")
            print("*" + "         📧 OTP CODE (DEV MODE)".center(58) + "*")
            print("*" + " " * 58 + "*")
            print("*" + f"   Email: {email}".ljust(58) + "*")
            print("*" + " " * 58 + "*")
            print("*" + f"   CODE:  {code}".ljust(58) + "*")
            print("*" + " " * 58 + "*")
            print("*" * 60)
            print("\n", flush=True)
            return True
        
        try:
            resend.Emails.send({
                "from": settings.EMAIL_FROM,
                "to": email,
                "subject": subject,
                "html": body
            })
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
