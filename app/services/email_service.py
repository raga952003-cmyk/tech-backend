import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send an email using SMTP
    """
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = settings.SMTP_FROM_EMAIL
        message['To'] = to_email
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Connect to SMTP server and send
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_task_completion_email(user_email: str, user_name: str, day_number: int, topic: str, technology: str):
    """
    Send congratulations email when a task is completed
    """
    subject = f"🎉 Great Job! Day {day_number} Completed - {technology}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .badge {{ display: inline-block; background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; margin: 10px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Congratulations, {user_name}!</h1>
            </div>
            <div class="content">
                <h2>You've completed Day {day_number}!</h2>
                <p><strong>Topic:</strong> {topic}</p>
                <p><strong>Technology:</strong> {technology}</p>
                <div class="badge">✓ Task Completed</div>
                <p>You're making excellent progress on your learning journey. Keep up the great work!</p>
                <p>Your dedication to learning is inspiring. Every day completed brings you closer to mastering {technology}.</p>
                <a href="http://localhost:5175/dashboard" class="button">Continue Learning →</a>
            </div>
            <div class="footer">
                <p>TechStudy Tracker - Your Learning Companion</p>
                <p>Sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)

def send_daily_reminder_email(user_email: str, user_name: str, day_number: int, topic: str, technology: str, estimated_duration: str, tasks: list):
    """
    Send daily reminder for incomplete tasks
    """
    subject = f"📅 Daily Reminder: Day {day_number} - {topic}"
    
    tasks_html = "".join([f"<li style='margin: 8px 0;'>{task}</li>" for task in tasks])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #667eea; }}
            .tasks {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; }}
            .tasks ul {{ margin: 10px 0; padding-left: 20px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin-top: 15px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
            .time-badge {{ display: inline-block; background: #f59e0b; color: white; padding: 6px 12px; border-radius: 15px; font-size: 14px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📅 Today's Learning Task</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>You have an incomplete task waiting for you!</p>
                
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #667eea;">Day {day_number}: {topic}</h3>
                    <p><strong>Technology:</strong> {technology}</p>
                    <p><strong>Estimated Time:</strong> <span class="time-badge">⏱️ {estimated_duration}</span></p>
                </div>
                
                <div class="tasks">
                    <h4 style="margin-top: 0;">📝 Today's Tasks:</h4>
                    <ul>
                        {tasks_html}
                    </ul>
                </div>
                
                <p>Take your time and complete these tasks at your own pace. Consistent learning leads to mastery!</p>
                
                <a href="http://localhost:5175/dashboard" class="button">Start Learning →</a>
            </div>
            <div class="footer">
                <p>TechStudy Tracker - Your Learning Companion</p>
                <p>Sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)

def send_missed_task_reminder(user_email: str, user_name: str, days_behind: int, technology: str):
    """
    Send reminder when user has missed multiple days
    """
    subject = f"⚠️ You're {days_behind} days behind - Let's get back on track!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .warning-box {{ background: #fef3c7; padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #f59e0b; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin-top: 15px; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Don't Give Up!</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>We noticed you haven't completed your learning tasks in a while.</p>
                
                <div class="warning-box">
                    <h3 style="margin-top: 0; color: #d97706;">You're {days_behind} days behind on {technology}</h3>
                    <p>But that's okay! It's never too late to get back on track.</p>
                </div>
                
                <p><strong>Remember:</strong></p>
                <ul>
                    <li>Learning is a journey, not a race</li>
                    <li>Small progress is still progress</li>
                    <li>You can always pick up where you left off</li>
                </ul>
                
                <p>We're here to support you. Let's continue your learning journey together!</p>
                
                <a href="http://localhost:5175/dashboard" class="button">Resume Learning →</a>
            </div>
            <div class="footer">
                <p>TechStudy Tracker - Your Learning Companion</p>
                <p>Sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)

def send_password_reset_email(user_email: str, user_name: str, reset_token: str):
    """
    Send password reset email with reset link
    """
    subject = "🔐 Reset Your Password - TechStudy Tracker"
    reset_link = f"http://localhost:5175/reset-password?token={reset_token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #667eea; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; margin-top: 15px; font-weight: 600; }}
            .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 14px; }}
            .warning {{ background: #fef3c7; padding: 15px; border-radius: 8px; margin: 15px 0; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Password Reset Request</h1>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>We received a request to reset your password for your TechStudy Tracker account.</p>
                
                <div class="info-box">
                    <p style="margin: 0;"><strong>Click the button below to reset your password:</strong></p>
                </div>
                
                <div style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </div>
                
                <div class="warning">
                    <p style="margin: 0;"><strong>⚠️ Security Notice:</strong></p>
                    <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                        <li>This link will expire in 1 hour</li>
                        <li>If you didn't request this, please ignore this email</li>
                        <li>Never share this link with anyone</li>
                    </ul>
                </div>
                
                <p style="font-size: 13px; color: #6b7280; margin-top: 20px;">
                    If the button doesn't work, copy and paste this link into your browser:<br>
                    <a href="{reset_link}" style="color: #667eea; word-break: break-all;">{reset_link}</a>
                </p>
            </div>
            <div class="footer">
                <p>TechStudy Tracker - Your Learning Companion</p>
                <p>Sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)
