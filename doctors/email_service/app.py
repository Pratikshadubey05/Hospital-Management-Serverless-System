import json
from flask import Flask, request, jsonify
# Import the exact handler code you wrote in step 3
from handler import send_email_notification 

app = Flask(__name__)

@app.route('/dev/notify', methods=['POST'])
def local_trigger():
    # 1. Transform the incoming Flask request into a mock AWS Lambda Event structure
    mock_aws_event = {
        "body": json.dumps(request.json)
    }
    
    # 2. Execute your exact handler function directly
    response = send_email_notification(mock_aws_event, None)
    
    # 3. Return the result format
    return jsonify(json.loads(response["body"])), response["statusCode"]

if __name__ == '__main__':
    print("*" * 60)
    print("🚀 PYTHON SERVERLESS-OFFLINE SIMULATOR RUNNING")
    print("Listening on: http://localhost:3000/dev/notify")
    print("*" * 60)
    app.run(port=3000)