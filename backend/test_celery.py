"""
Quick test — run this to verify Celery can receive and execute tasks.
Usage: python test_celery.py
"""
import sys
import time

# Test 1: Config loads correctly
print("=== Test 1: Config ===")
from app.config import get_settings
s = get_settings()
print(f"DB URL: {s.DATABASE_URL_SYNC}")
print(f"Redis:  {s.REDIS_URL}")

# Test 2: DB connection works
print("\n=== Test 2: Database ===")
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(s.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM scans"))
        count = result.scalar()
        print(f"✓ DB connected — {count} scans in database")
    engine.dispose()
except Exception as e:
    print(f"✗ DB FAILED: {e}")
    sys.exit(1)

# Test 3: Redis connection works
print("\n=== Test 3: Redis ===")
try:
    import redis
    r = redis.from_url(s.REDIS_URL)
    r.ping()
    print("✓ Redis connected")
    r.close()
except Exception as e:
    print(f"✗ Redis FAILED: {e}")
    sys.exit(1)

# Test 4: Celery task can be sent
print("\n=== Test 4: Celery Task ===")
try:
    from app.workers.celery_app import celery_app
    from app.workers.tasks import run_scan_task

    # Get a real scan ID from DB to test with
    from sqlalchemy.orm import Session
    from app.models.scan import Scan, ScanStatus
    sync_engine = create_engine(s.DATABASE_URL_SYNC)
    with Session(sync_engine) as session:
        scan = session.query(Scan).filter(
            Scan.status == ScanStatus.VERIFYING
        ).first()
        if scan:
            scan_id = str(scan.id)
            print(f"Found stuck scan: {scan_id} — sending to Celery...")
            task = run_scan_task.apply_async(args=[scan_id], queue="default")
            print(f"✓ Task sent! Task ID: {task.id}")
            print("Watch your Celery worker terminal for output.")
        else:
            print("No stuck scans found. Start a new scan from the UI.")
    sync_engine.dispose()
except Exception as e:
    print(f"✗ Celery FAILED: {e}")
    import traceback
    traceback.print_exc()
