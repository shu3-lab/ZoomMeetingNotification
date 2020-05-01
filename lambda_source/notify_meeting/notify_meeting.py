import json
import urllib.request
import os
import boto3
from datetime import datetime as dt

def lambda_handler(event, context):
    result = post_slack()
    if 'ok' in json.dumps(result):
        body = json.dumps(result)
    else:
        body = 'NG!'
        
    return {
        'statusCode': 200,
        'body': "slack result is " + body
    }
    
def post_slack():
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('meetings')

    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y/%m/%d')
    
    items = table.get_item(
        Key={
            "date":tstr
        }
    )
    zoom_url = items['Item']['meeting_url']

    send_data = {
	"username": "Zoom Notification BOT",
	"icon_emoji": ":laughing:",
    "attachments": [
        {
            "color": "#36a64f",
            "pretext": "Daily Zoom Meeting is created!",
            "author_name": "Owner",
            "title": "Zoom Meeting URL is here!",
            "title_link": zoom_url,
            "text": "Let' join us!"
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
