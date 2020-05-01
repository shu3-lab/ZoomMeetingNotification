from __future__ import print_function

import json
import os
import urllib.request

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    return post_slack(message)

def post_slack(message):

    send_data = {
	"username": "Zoom Notification BOT",
	"icon_emoji": ":cry:",
    "attachments": [
        {
            "color": "#36a64f",
            "pretext": "Failure!!",
            "author_name": "Owner",
            "text": message
        }
    ]
}
    
    send_text = "payload=" + json.dumps(send_data)
    headers = {"Content-Type" : "application/json"}
    request = urllib.request.Request(
        os.environ["slack_url"], 
        data=send_text.encode('utf-8'),
        method="POST"
    )
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    except urllib.error.HTTPError as error:
        print(str(error.code) + error.reason)
    else:
        return response_body
