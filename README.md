# job-scheduler

Here's a implementation of a scheduling system using only Python's built-in libraries, without any external dependencies. This example replicates the basic functionality of scheduling and triggering HTTP requests using a custom loop, handling both one-time and recurring jobs.

We'll use a list to manage the jobs and a simple while loop to check for the jobs that are ready to be triggered.

### Code Explanation
1. **Job Registration**:
   - The `create_job` function creates a job with details such as `url`, `method`, `req_payload`, `timestamp`, and whether it is recursive.
   - The job's status is initially set to `REGISTERED`.

2. **Job Scheduler**:
   - The `run_scheduler` function continuously loops to check if any job's scheduled time has been reached.
   - It uses the `check_and_run_jobs` function to trigger jobs whose time has arrived.

3. **Job Execution**:
   - When the time for a job arrives, the `trigger_job` function sends the HTTP request and updates the job's status.
   - If the job is recursive, it automatically reschedules itself for the next run.

4. **Job Status and Logging**:
   - The status of each job changes from `REGISTERED` to `TRIGGERED` and then to either `COMPLETED` or `FAILED`.
   - Execution responses are logged to give feedback on the success or failure of each job.

### Insights:
- **Simplified Workflow**: This code manually handles job scheduling without using external libraries, giving a clear view of the scheduling mechanism.
- **Concurrency Considerations**: This implementation is sequential and may not handle a high volume of jobs efficiently. For a production-level system, you would need to introduce threading or multiprocessing.
- **One-time vs. Recurring**: The code differentiates between one-time and recurring jobs, automatically rescheduling recursive jobs.




