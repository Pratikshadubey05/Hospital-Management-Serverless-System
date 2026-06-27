import json

def send_email_notification(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        trigger_type = body.get("trigger")  # 'SIGNUP_WELCOME' or 'BOOKING_CONFIRMATION'
        recipient_email = body.get("email")
        
        if not trigger_type or not recipient_email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing parameters: 'trigger' and 'email' are required."})
            }
        
        if trigger_type == "SIGNUP_WELCOME":
            subject = "Welcome to Hospital Portal!"
            message_content = "Thank you for registering. Your profile dashboard is now fully active."
        elif trigger_type == "BOOKING_CONFIRMATION":
            subject = "Appointment Confirmation"
            message_content = "Your appointment slot has been successfully booked and secured in our system."
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Unsupported trigger type: {trigger_type}"})
            }
            
        # Clear visibility console verification logs
        print("\n" + "="*50)
        print(f"[SERVERLESS MOCK TRIGGER ACTIVE]")
        print(f"Trigger Context: {trigger_type}")
        print(f"Recipient:       {recipient_email}")
        print(f"Subject:         {subject}")
        print(f"Body:            {message_content}")
        print("="*50 + "\n")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success", 
                "message": f"Notification sequence executed for {trigger_type}"
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }