# ZoomMeetingNotification

## **This is the notification service which notifies us Zoom meeting URLs.**

**It's structed on AWS and  all of functions  are made by managed service, e.g. lambda,DynamoDB,S3.**<br>
The whole architecture is the below image.

<img src=https://user-images.githubusercontent.com/56756975/80899475-7ef0df00-8d4b-11ea-86c7-a255551eb341.png width=70%>

<br>

#### The target range of this repository is Zoom meeting notification functions.(The range is a red frame in the above figure)

## *Create Zoom Meetings*

A source code is 'create_meeting.py'.
At first, it calls Create Meeting API delivered by Zoom.<br>
If you want to understand details of API, **[read a official document.](https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/meetingcreate)** The JSON of request body is stored in S3 bucket, so this function get it and send it as payload.<br>
When API execution is succeed, A Zoom Meeting ID is responsed.
The ID is stored in DynamoDB.Result of this function is notified to Step Functions.

## *Notify Zoom Meeting*

A source code is 'notify_meeting.py'. If creaton of Meetings is succeed, Step Functins calls a next function posts a Meeting URL to a Slack channenl.
At first, the function get a Zoom Meeting ID of today from DynamoDB.
<br>And next, it post a URL to Incoming Webhook which behave as Slack BOT. Please **[read a official document](https://api.slack.com/messaging/webhooks)** to understand details.<br>
<img width="324" alt="Meeting Notice" src="https://user-images.githubusercontent.com/56756975/80901335-bf9d2800-8d4c-11ea-9371-c9c959d5d178.png">

## *Notify failure*

A source code is 'notify_failure.py'.If creaton of Meetings is failed, Step Functins notifies SNS a message of failure.<br>
When a message is published to SNS, SNS call a lambda function which post the message to Slack.<br>
<img width="329" alt="Failure Notice" src="https://user-images.githubusercontent.com/56756975/80901417-c5930900-8d4c-11ea-9a92-70f025754a16.png">


## *Notes of AWS Resources*

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
aws s3 mb s3://{bucket name}/{object key}
```

- Transfer local files

```sh
aws s3 cp {file path} s3://{bucket name}/{object key}
```

### Step Functions

The State Machine is the below figure.<br>
![stepfunctions_graph](https://user-images.githubusercontent.com/56756975/80899545-384fb480-8d4c-11ea-9ff5-ad1b60c23bbb.png)

## I've written about this application on my BLOG!
The URL is https://qiita.com/Shu3/items/edacbfbea4b1b6aaf877 .(It' written in Japanese.)


