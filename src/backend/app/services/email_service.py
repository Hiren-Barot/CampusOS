import logging
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:

    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM_ADDRESS or settings.SMTP_USER
        self.from_name = settings.EMAIL_FROM_NAME

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:

        if not self.username or not self.password:
            logger.warning("SMTP credentials not configured — email not sent")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            if text_content:
                msg.attach(MIMEText(text_content, "plain"))

            msg.attach(MIMEText(html_content, "html"))

            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=True,
                timeout=10,
            )

            logger.info(f"Email sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    async def send_welcome_email(
        self,
        to_email: str,
        full_name: str,
        role: str,
        temp_password: str,
        login_url: str = "http://localhost:5173/login",
    ) -> bool:

        subject = f"Welcome to CampusOS — Your {role.title()} Account"

        html_content = self._welcome_html(
            full_name=full_name,
            email=to_email,
            role=role,
            temp_password=temp_password,
            login_url=login_url,
        )

        text_content = f"""
Hello {full_name},

Welcome to CampusOS!

Your account has been created with the role: {role.title()}

Login Credentials:
  Email:    {to_email}
  Password: {temp_password}

Login URL: {login_url}

Please log in and change your password immediately for security.

Regards,
CampusOS Team
        """.strip()

        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )

    async def send_password_reset_email(
        self,
        to_email: str,
        full_name: str,
        reset_url: str,
        expires_minutes: int = 30,
    ) -> bool:
        subject = "Reset your CampusOS password"

        html_content = self._reset_password_html(
            full_name=full_name,
            email=to_email,
            reset_url=reset_url,
            expires_minutes=expires_minutes,
        )

        text_content = f"""
Hello {full_name},

We received a request to reset your CampusOS password.

Reset Link: {reset_url}

This link will expire in {expires_minutes} minutes.

If you did not request this, you can safely ignore this email.

Regards,
CampusOS Team
        """.strip()

        if not self.username or not self.password:
            logger.warning("=" * 70)
            logger.warning("SMTP not configured — printing reset link to console")
            logger.warning(f"  To      : {to_email}")
            logger.warning(f"  Reset   : {reset_url}")
            logger.warning(f"  Expires : {expires_minutes} minutes")
            logger.warning("=" * 70)
            return False

        return await self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )

    def _welcome_html(
        self,
        full_name: str,
        email: str,
        role: str,
        temp_password: str,
        login_url: str,
    ) -> str:
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to CampusOS</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f5f5f0; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f5f0; padding: 30px 15px;">
        <tr>
            <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <tr>
                        <td style="background-color: #1a2430; padding: 30px 40px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 26px; font-weight: bold; letter-spacing: 0.5px;">
                                Campus<span style="color: #c4432b;">OS</span>
                            </h1>
                            <p style="margin: 8px 0 0 0; color: #a0a8b0; font-size: 12px; letter-spacing: 1px;">
                                CENTRALIZED ACADEMIC PLATFORM
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 35px 40px 15px 40px;">
                            <h2 style="margin: 0 0 10px 0; color: #1a2430; font-size: 22px;">
                                Hello, {full_name} 👋
                            </h2>
                            <p style="margin: 0; color: #5c6b7a; font-size: 15px;">
                                Welcome to CampusOS! Your account has been created successfully.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td style="background-color: #c4432b; color: #ffffff; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                                        ROLE: {role.upper()}
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 25px 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f6f2; border: 1px solid #e4dfd4; border-radius: 6px;">
                                <tr>
                                    <td style="padding: 20px 25px;">
                                        <p style="margin: 0 0 5px 0; color: #5c6b7a; font-size: 11px; letter-spacing: 1px; font-weight: 600;">
                                            YOUR LOGIN CREDENTIALS
                                        </p>
                                        <p style="margin: 12px 0 5px 0; color: #5c6b7a; font-size: 12px;">Email:</p>
                                        <p style="margin: 0; color: #1a2430; font-size: 15px; font-family: 'Courier New', monospace; font-weight: 600;">
                                            {email}
                                        </p>
                                        <p style="margin: 12px 0 5px 0; color: #5c6b7a; font-size: 12px;">Temporary Password:</p>
                                        <p style="margin: 0; color: #c4432b; font-size: 18px; font-family: 'Courier New', monospace; font-weight: 700; letter-spacing: 1px;">
                                            {temp_password}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 10px 40px 25px 40px;">
                            <a href="{login_url}" style="display: inline-block; background-color: #1a2430; color: #ffffff; text-decoration: none; padding: 12px 32px; border-radius: 4px; font-size: 14px; font-weight: 600; letter-spacing: 0.5px;">
                                Log In to CampusOS →
                            </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 40px 25px 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #fef5f3; border-left: 3px solid #c4432b; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 15px 18px;">
                                        <p style="margin: 0; color: #8a2a1a; font-size: 13px;">
                                            <strong>⚠️ Security Notice:</strong> Please change your password immediately after your first login. Do not share these credentials with anyone.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8f6f2; padding: 20px 40px; text-align: center; border-top: 1px solid #e4dfd4;">
                            <p style="margin: 0 0 5px 0; color: #5c6b7a; font-size: 12px;">
                                This email was sent by CampusOS.
                            </p>
                            <p style="margin: 0; color: #a0a8b0; font-size: 11px;">
                                If you did not request this account, please contact your department faculty.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """.strip()

    def _reset_password_html(
        self,
        full_name: str,
        email: str,
        reset_url: str,
        expires_minutes: int,
    ) -> str:
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset your CampusOS password</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f5f5f0; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f5f0; padding: 30px 15px;">
        <tr>
            <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <tr>
                        <td style="background-color: #1a2430; padding: 30px 40px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 26px; font-weight: bold; letter-spacing: 0.5px;">
                                Campus<span style="color: #c4432b;">OS</span>
                            </h1>
                            <p style="margin: 8px 0 0 0; color: #a0a8b0; font-size: 12px; letter-spacing: 1px;">
                                CENTRALIZED ACADEMIC PLATFORM
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 35px 40px 15px 40px;">
                            <h2 style="margin: 0 0 10px 0; color: #1a2430; font-size: 22px;">
                                Hello, {full_name} 👋
                            </h2>
                            <p style="margin: 0; color: #5c6b7a; font-size: 15px;">
                                We received a request to reset your CampusOS password.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td style="background-color: #c4432b; color: #ffffff; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                                        PASSWORD RESET REQUEST
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 25px 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f6f2; border: 1px solid #e4dfd4; border-radius: 6px;">
                                <tr>
                                    <td style="padding: 20px 25px;">
                                        <p style="margin: 0 0 5px 0; color: #5c6b7a; font-size: 11px; letter-spacing: 1px; font-weight: 600;">
                                            YOUR ACCOUNT
                                        </p>
                                        <p style="margin: 12px 0 5px 0; color: #5c6b7a; font-size: 12px;">Email:</p>
                                        <p style="margin: 0; color: #1a2430; font-size: 15px; font-family: 'Courier New', monospace; font-weight: 600;">
                                            {email}
                                        </p>
                                        <p style="margin: 12px 0 5px 0; color: #5c6b7a; font-size: 12px;">Link expires in:</p>
                                        <p style="margin: 0; color: #c4432b; font-size: 18px; font-family: 'Courier New', monospace; font-weight: 700; letter-spacing: 1px;">
                                            {expires_minutes} MINUTES
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 10px 40px 25px 40px;">
                            <a href="{reset_url}" style="display: inline-block; background-color: #1a2430; color: #ffffff; text-decoration: none; padding: 12px 32px; border-radius: 4px; font-size: 14px; font-weight: 600; letter-spacing: 0.5px;">
                                Reset Password →
                            </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 40px 25px 40px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #fef5f3; border-left: 3px solid #c4432b; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 15px 18px;">
                                        <p style="margin: 0; color: #8a2a1a; font-size: 13px;">
                                            <strong>⚠️ Didn't request this?</strong> You can safely ignore this email — your password won't change unless you click the link above and set a new one.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8f6f2; padding: 20px 40px; text-align: center; border-top: 1px solid #e4dfd4;">
                            <p style="margin: 0 0 5px 0; color: #5c6b7a; font-size: 12px;">
                                This email was sent by CampusOS.
                            </p>
                            <p style="margin: 0; color: #a0a8b0; font-size: 11px;">
                                If you need help, contact your department faculty.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """.strip()


email_service = EmailService()