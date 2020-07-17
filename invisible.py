import os

import boto3

client = boto3.client('logs')
app_name = os.getenv('app')

response = client.describe_log_streams(
    logGroupName=f'/aws/lambda/{app_name}',
)

for item in (response['logStreams']):
    resp = client.delete_log_stream(
        logGroupName='/aws/lambda/stock_hawk',
        logStreamName=f"{item['logStreamName']}"
    )
    print(resp)
