import json
import urllib.request
import os
import boto3
from datetime import datetime as dt

def lambda_handler(event, context):
    # TODO implement
    return create_meeting(event)
    
def create_meeting(event):
    url = "https://api.zoom.us/v2/users/"+os.environ['user_id']+"/meetings"

    s3_get = boto3.client('s3')
    bucket_name = 'zoom-data-shu'
    objkey = 'body.json'
    obj = s3_get.get_object(Bucket=bucket_name, Key=objkey)
    body = obj['Body'].read()
    bodystr = body.decode('utf-8')
    jwt = event['jwt']
    headers = {
    'content-type': "application/json",
    'authorization': "Bearer " + jwt
    }
    print(headers)
    request = urllib.request.Request(
        url, 
        data=bodystr.encode('utf-8'),
        headers = headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            res = json.loads(response_body)
            meeting_url = res['join_url']
            meeting_id = res['id']
            tdatetime = dt.now()
            tstr = tdatetime.strftime('%Y/%m/%d')

            dynamodb = boto3.resource('dynamodb')
            table    = dynamodb.Table('meetings')
            table.put_item(
                Item = {
                    "date" : tstr,
                    "meeting_id" : meeting_id,
                    "meeting_url" : meeting_url
                }
            )
            return {"Result" : True}
    except urllib.error.HTTPError as error:
        print(str(error.code) + error.reason)
        return {"Result" : False}
    else:
        return {"Result" : False}

    