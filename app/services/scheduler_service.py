from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, LearningPath, Progress
from app.services.email_service import send_daily_reminder_email, send_missed_task_reminder
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def check_and_send_daily_reminders():
    """
    Check all users for incomplete tasks and send reminders
    This runs daily at the configured time (default: 9:00 AM)
    """
    if not settings.ENABLE_EMAIL_NOTIFICATIONS:
        logger.info("Email notifications are disabled")
        return
    
    db: Session = SessionLocal()
    try:
        logger.info("Starting daily reminder check...")
        
        # Get all users
        users = db.query(User).all()
        
        for user in users:
            # Get all learning paths for this user
            learning_paths = db.query(LearningPath).filter(
                LearningPath.user_id == user.id
            ).all()
            
            for path in learning_paths:
                # Get progress for this path
                progress_records = db.query(Progress).filter(
                    Progress.learning_path_id == path.id
                ).all()
                
                # Find the first incomplete day
                completed_days = {p.day_number for p in progress_records if p.completed}
                
                if not path.daily_plan:
                    continue
                
                # Find first incomplete day
                incomplete_day = None
                for day in path.daily_plan:
                    if day['day'] not in completed_days:
                        incomplete_day = day
                        break
                
                if incomplete_day:
                    # Calculate days behind
                    expected_day = len(completed_days) + 1
                    days_behind = incomplete_day['day'] - expected_day
                    
                    # Send appropriate email
                    if days_behind > 3:
                        # User is significantly behind
                        send_missed_task_reminder(
                            user.email,
                            user.full_name,
                            days_behind,
                            path.technology
                        )
                        logger.info(f"Sent missed task reminder to {user.email} for {path.technology}")
                    else:
                        # Send regular daily reminder
                        send_daily_reminder_email(
                            user.email,
                            user.full_name,
                            incomplete_day['day'],
                            incomplete_day['topic'],
                            path.technology,
                            incomplete_day.get('estimated_duration', '2-3 hours'),
                            incomplete_day['tasks']
                        )
                        logger.info(f"Sent daily reminder to {user.email} for Day {incomplete_day['day']}")
        
        logger.info("Daily reminder check completed")
    except Exception as e:
        logger.error(f"Error in daily reminder check: {str(e)}")
    finally:
        db.close()

# Initialize scheduler
scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Start the background scheduler for email notifications
    """
    if not settings.ENABLE_EMAIL_NOTIFICATIONS:
        logger.info("Email notifications disabled - scheduler not started")
        return
    
    # Parse the reminder time
    hour, minute = map(int, settings.DAILY_REMINDER_TIME.split(':'))
    
    # Schedule daily reminder check
    scheduler.add_job(
        check_and_send_daily_reminders,
        CronTrigger(hour=hour, minute=minute),
        id='daily_reminder',
        name='Send daily learning reminders',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started - Daily reminders will be sent at {settings.DAILY_REMINDER_TIME}")

def stop_scheduler():
    """
    Stop the background scheduler
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
