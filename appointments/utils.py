import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Set the OAuth scope required to add events to primary calendar profiles
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_auth_flow():
    """Builds the OAuth flow initialization client target wrapper."""
    # Note: You will download client_secret.json from your Google Cloud Console 
    # and place it directly inside your main project root directory.
    return Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri='http://127.0.0.1:8000/appointments/oauth2callback/'
    )

def add_appointment_to_google_calendar(access_token, refresh_token, slot_instance, event_summary):
    """Uses authorized user OAuth credentials to inject standard calendar events."""
    try:
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get("GOOGLE_CLIENT_ID"),       # Optional: read from env
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET") # Optional: read from env
        )
        
        # Build the actual API client connection layer
        service = build('calendar', 'v3', credentials=credentials)
        
        # Format strings safely to comply with mandatory ISO 8601 formatting rules
        start_datetime = f"{slot_instance.date}T{slot_instance.start_time.isoformat()}"
        end_datetime = f"{slot_instance.date}T{slot_instance.end_time.isoformat()}"
        
        event_body = {
            'summary': event_summary,
            'description': 'Automated verification booking managed securely via Hospital Platform.',
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'UTC',
            },
        }
        
        # Dispatch insertion requests straight to user targets
        service.events().insert(calendarId='primary', body=event_body).execute()
        print(f"[GOOGLE CALENDAR API] Event successfully injected: {event_summary}")
        
    except Exception as e:
        print(f"[GOOGLE CALENDAR ERROR] Bypassing calendar scheduling exception: {e}")