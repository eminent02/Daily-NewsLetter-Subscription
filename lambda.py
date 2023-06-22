import json
import urllib.parse
import boto3
import io
import pandas as pd
import datetime


def send_ses(message, subject,dest_email):
    try:
        client = boto3.client('ses',region_name='us-east-1')
        result = client.send_email(
        Destination={
            'ToAddresses': [
                dest_email
        ],
    },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': message,
                },
                # 'Text': {
                #     'Charset': 'UTF-8',
                #     'Data': 'This is the message body in text format.',
                # },
            },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': subject
        },
    },
        # ReplyToAddresses=[
        # ],
        # ReturnPath='',
        # ReturnPathArn='',
        Source='swaraj1ga17cs163@gmail.com',
        SourceArn='arn:aws:ses:us-east-1:143602348576:identity/swaraj1ga17cs163@gmail.com',
    )
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification send successfully..!!!")
            return True
    except Exception as e:
        print("Error occured while publish notifications and error is : ", e)
        return True

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(key)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        # print(io.BytesIO(response['Body'].read()).read().decode())
        df = pd.read_csv(io.BytesIO(response['Body'].read()),header=0, delimiter=",", low_memory=False)
        print(df)
        msg = "<html> <head> </head> <body>"
        for i in range(len(df)):
            #print(df.iloc[i])
            msg += "<p> <div> "
            msg += df.iloc[i]['pubDate']
            msg+= "<br>"
            msg += "<strong>"
            msg+= df.iloc[i]['title']
            msg += "</strong>"
            msg+="<br>"
            msg+= "<a href=\"" + df.iloc[i]['link'] + "\">See More</a>"
            msg+="<br>"
            msg += " </div> </p> "
        message = msg
        # ist = convert_to_ist()
        dt_India = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        subject = key.split('/')[1].split('.')[0] + " IST"
        dest_email = key.split('/')[0]
        ses_result = send_ses(message,subject,dest_email)
        if ses_result:
            print("News sent successfully")
            return ses_result
        else:
            return "Failed"
        # return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e