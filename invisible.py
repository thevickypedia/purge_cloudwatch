import math
from datetime import datetime, timedelta

import boto3

client = boto3.client('logs')
app_name = 'stock_hawk'

response = client.describe_log_streams(
    logGroupName=f'/aws/lambda/{app_name}',
)

tod = datetime.today() - timedelta(days=65)
epoch_date = str(math.trunc(tod.timestamp()))
deletion_date = int(epoch_date.ljust(13, '0'))

for item in (response['logStreams']):
    if item['creationTime'] < deletion_date:
        resp = client.delete_log_stream(
            logGroupName=f'/aws/lambda/{app_name}',
            logStreamName=f"{item['logStreamName']}"
        )
        print(resp)
