# ZoomMeetingNotification

## **This is the notification service which notifies us Zoom meeting URLs.**

**It's structed on AWS and  all of functions  are made by managed service, e.g. lambda,DynamoDB,S3.**

## The target range of this repository is Zoom meeting notification functions.

## *Create Zoom Meetings*

A source code is 'create_meeting.py'.
At first, it calls Create Meeting API delivered by Zoom.<br>
If you want to understand details of API, **[read a official document.](https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/meetingcreate)** The JSON of request body is stored in S3 bucket, so this function get it and send it as payload.<br>
When API execution is succeed, A Zoom Meeting ID is responsed.
An ID is stored in DynamoDB.Result of this function is notified to Step Functions.

## *Notify Zoom Meeting*

A source code is 'notify_meeting.py'. If creaton of Meetings is succeed, Step Functins calls a next function posts a Meeting URL to a Slack channenl.
At first, the function get a Zoom Meeting ID of today from DynamoDB.
<br>And next, it post a URL to Incoming Webhook which behave as Slack BOT. Please **[read a official document](https://api.slack.com/messaging/webhooks)** to understand details.

## *Notify failure*

A source code is 'notify_failure.py'.If creaton of Meetings is failed, Step Functins notifies SNS a message of failure.<br>
When a message is published to SNS, SNS call a lambda function which post the message to Slack.

## *Note of AWS Resources*

### DynamoDB

- Create a table
  
```sh
aws dynamodb create-table --table-name 'meetings'
--attribute-definitions '[{"AttributeName":"date","AttributeType": "S"}]'
--key-schema '[{"AttributeName":"date","KeyType": "HASH"}]'
--provisioned-throughput '{"ReadCapacityUnits": 5,"WriteCapacityUnits": 5}'
```

### S3

- Create a bucket

```sh
aws s3 mb s3//{bucket name}/{object key}
```

- Transfer local files

```sh
aws s3 cp {file path} s3//{bucket name}/{object key}
```

