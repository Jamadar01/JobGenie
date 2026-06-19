# services/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from services.jobscraping import JobScrapingService

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
job_genie = JobScrapingService()

def daily_pipeline():
    print("Running daily pipeline...")
    job_genie.run_cleanup()
    job_genie.job_storing()

def start_scheduler():
    print("Starting scheduler...")
    scheduler.add_job(
        daily_pipeline,
        CronTrigger(day_of_week="mon", hour=0, minute=1),
        # IntervalTrigger(seconds=6),
        id="daily_pipeline",
        replace_existing=True,
    )
    scheduler.start()

def stop_scheduler():
    print("Stopping scheduler...")
    scheduler.shutdown()