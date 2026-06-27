
#### Hospital Management System (HMS)

A multi-role medical portal featuring a monolithic Django core backend paired with a decoupled Serverless asynchronous email notification microservice layout.

---

## ## Setup and Run

### 🖥️ 1. Notification Microservice (Terminal 1)
bash

# cd email-service
npm install -g serverless
npm install serverless-offline --save-dev
serverless offline start --port 3000
2. Django Web Application (Terminal 2)
Bash
python -m venv venv
venv\Scripts\activate  # Mac/Linux: source venv/bin/activate
pip install django requests google-auth google-auth-oauthlib google-auth-httplib2
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
URL Interface: http://127.0.0.1:8000/

## System Architecture
Plaintext
[Patient Browser UI] ──(Clicks Book Now)──> [Django Core Backend (Port 8000)]
                                                       │
                                            (Atomic Database Row Update)
                                                       │
                                            (Pushes JSON HTTP POST)
                                                       ▼
                                        [Serverless Offline Service (Port 3000)]
Data Flow: When a patient claims a slot, Django handles the transactional database commit locally and instantly hands off a JSON payload across local socket boundaries to http://127.0.0.1:3000/send-email.

Data Models: Employs an isolated One-to-One Profile mapping extension to lock down User Roles (doctor vs patient). The AvailabilitySlot table model enforces timing ranges paired with an atomic is_booked status parameter to structurally block race-condition scheduling.

Access Control: Enforced natively via Django @login_required metadata decorators coupled with dynamic template-level logic forks to securely restrict view modifications.

Google Calendar: Hooks into the native client authentication library layer to register events for both users upon booking verification.

## The Design Decision
Monolithic Internal SMTP Engine vs. Decoupled Microservice Messaging API Backend
Decision: Selected an independent serverless architecture microservice pattern running on port 3000 over a standard monolithic application setup.

Justification: Synchronous internal email delivery routines introduce immediate layout latency bottlenecks if an external mail server lags. Moving notifications to an independent service layer ensures that even if notification services experience network drops, the primary web database remains operational, catching exceptions cleanly without freezing the user interface.

## Limitations
Hardcoded Endpoints: Network connection string parameters use fixed loopback destination mapping pointers (127.0.0.1). These should be changed to parse dynamically from hidden environment configuration files (.env).

Synchronous Requests: The requests.post API call executes within the main application execution thread block. For live cloud production tracking, this must be assigned to an independent asynchronous background event worker routine like Celery paired with a Redis data cache broker.


