import math
from datetime import datetime, timedelta

import boto3

client = boto3.client('logs')
app_name = 'stock_hawk'

response = client.describe_log_streams(
    logGroupName=f'/aws/lambda/{app_name}',
)

tod = datetime.today() - timedelta(days=2)
epoch_date = math.trunc(tod.timestamp())
epoch_date = str(epoch_date)
deletion_date = epoch_date.ljust(13, '0')
deletion_date = int(deletion_date)

for item in (response['logStreams']):
    if item['creationTime'] < deletion_date:
        resp = client.delete_log_stream(
            logGroupName=f'/aws/lambda/{app_name}',
            logStreamName=f"{item['logStreamName']}"
        )
        print(resp)
