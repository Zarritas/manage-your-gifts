"""Authentication service."""

import secrets
import json
import hashlib
from datetime import datetime, timedelta
from jose import jwt
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings
from app.models import User, EmailOTP
from app.services.email import EmailService

settings = get_settings()


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.email_service = EmailService()
    
    def _generate_otp(self) -> str:
        """Generate a random 6-digit OTP."""
        if not settings.RESEND_API_KEY:
            return "123456"
        return "".join([str(secrets.randbelow(10)) for _ in range(settings.OTP_LENGTH)])
    
    def _hash_code(self, code: str) -> str:
        """Hash OTP code using SHA256."""
        return hashlib.sha256(code.encode()).hexdigest()
    
    def _verify_code(self, code: str, code_hash: str) -> bool:
        """Verify OTP code against hash."""
        return self._hash_code(code) == code_hash
    
    def _create_token(self, user_id: str) -> str:
        """Create JWT token."""
        expire = datetime.utcnow() + timedelta(hours=settings.SESSION_EXPIRE_HOURS)
        data = {"sub": user_id, "exp": expire}
        return jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    
    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.session.exec(
            select(User).where(User.email == email.lower())
        )
        return result.first()
    
    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        result = await self.session.exec(
            select(User).where(User.id == user_id)
        )
        return result.first()
    
    async def send_login_code(self, email: str) -> tuple[bool, str]:
        """
        Send login OTP code to email.
        
        Steps:
        1. Validate email format (done by Pydantic)
        2. Find or create User by email
        3. Generate 6-digit OTP
        4. Hash OTP
        5. Save EmailOTP (expires in 10 minutes)
        6. Send email with OTP (localized)
        7. Return success
        """
        email = email.lower().strip()
        
        # Find or create user
        user = await self.get_user_by_email(email)
        if not user:
            user = User(email=email)
            self.session.add(user)
            await self.session.flush()
        
        # Generate OTP
        code = self._generate_otp()
        code_hash = self._hash_code(code)
        
        # Create OTP record
        otp = EmailOTP(
            user_id=user.id,
            code_hash=code_hash,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        )
        self.session.add(otp)
        
        # Send email
        sent = await self.email_service.send_otp(email, code, user.language)
        
        if not sent:
            return False, "Failed to send email"
        
        return True, "Code sent"
    
    async def verify_login_code(self, email: str, code: str) -> tuple[bool, str, str | None]:
        """
        Verify login OTP code.
        
        Steps:
        1. Get User by email
        2. Get latest EmailOTP
        3. Validate: not used, not expired, hash matches
        4. Mark OTP as used
        5. Create session token
        6. Return token
        """
        email = email.lower().strip()
        
        # Get user
        user = await self.get_user_by_email(email)
        if not user:
            return False, "Invalid email or code", None
        
        # Get latest OTP
        result = await self.session.exec(
            select(EmailOTP)
            .where(EmailOTP.user_id == user.id)
            .where(EmailOTP.used == False)
            .where(EmailOTP.expires_at > datetime.utcnow())
            .order_by(EmailOTP.created_at.desc())
        )
        otp = result.first()
        
        if not otp:
            return False, "Code expired or invalid", None
        
        # Verify code
        if not self._verify_code(code, otp.code_hash):
            return False, "Invalid code", None
        
        # Mark as used
        otp.used = True
        self.session.add(otp)
        
        # Create token
        token = self._create_token(user.id)
        
        return True, "Login successful", token
    
    async def update_user_language(self, user_id: str, language: str) -> bool:
        """Update user language preference."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        if language not in ["en", "es"]:
            return False
        
        user.language = language
        self.session.add(user)
        return True
    
    async def update_user_stores(self, user_id: str, stores: list[dict]) -> bool:
        """Update user search stores configuration."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.search_stores = json.dumps(stores)
        self.session.add(user)
        return True
