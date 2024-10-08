import time
import requests
from datetime import datetime, timedelta

# In-memory job list to simulate a job store
jobs_store = []

# Function to create a job and register it in the job store
def create_job(url, method, req_payload, timestamp, is_recursive):
    job_id = len(jobs_store) + 1  # Generate a unique ID for each job
    job = {
        'id': job_id,
        'url': url,
        'method': method,
        'req_payload': req_payload,
        'timestamp': datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ'),
        'is_recursive': is_recursive,
        'status': 'REGISTERED'
    }
    jobs_store.append(job)
    print(f"Job {job_id} registered to run at {timestamp}.")

# Function to check and trigger the jobs when their scheduled time is reached
def check_and_run_jobs():
    current_time = datetime.now()
    for job in jobs_store:
        if job['status'] == 'REGISTERED' and current_time >= job['timestamp']:
            trigger_job(job)

# Function to trigger a job execution
def trigger_job(job):
    print(f"Triggering job {job['id']} at {datetime.now()}...")
    job['status'] = 'TRIGGERED'  # Update the job status to TRIGGERED

    try:
        # Make the HTTP request
        response = requests.request(method=job['method'], url=job['url'], json=job['req_payload'])
        log_response(job['id'], response)
        print(f"Job {job['id']} executed successfully with status code: {response.status_code}")
        job['status'] = 'COMPLETED'  # Mark job as COMPLETED after successful execution

        # If the job is recursive, schedule the next execution
        if job['is_recursive']:
            job['status'] = 'REGISTERED'
            job['timestamp'] = datetime.now() + timedelta(minutes=1)  # Re-schedule to run in the next minute
            print(f"Job {job['id']} re-scheduled to run again at {job['timestamp']}.")

    except Exception as e:
        job['status'] = 'FAILED'
        log_response(job['id'], f"Error: {str(e)}")
        print(f"Job {job['id']} failed with error: {str(e)}")

# Function to log the response from the job execution
def log_response(job_id, response):
    log_message = f"Job ID: {job_id} | Response: {response}"
    print(log_message)  # For demonstration, printing the log

# Function to run the scheduler continuously and check jobs at regular intervals
def run_scheduler():
    while True:
        check_and_run_jobs()  # Check if there are jobs ready to be triggered
        time.sleep(1)  # Wait for a second before checking again to avoid busy-waiting

# Example usage
if __name__ == "__main__":
    # Create a one-time job
    create_job(
        url="https://example.com/api",
        method="POST",
        req_payload={"data": "example payload"},
        timestamp=(datetime.now() + timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        is_recursive=False
    )

    # Create a recurring job
    create_job(
        url="https://example.com/api",
        method="POST",
        req_payload={"data": "recurring payload"},
        timestamp=(datetime.now() + timedelta(seconds=15)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        is_recursive=True
    )

    # Start the scheduler loop
    run_scheduler()
