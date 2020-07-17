import math
from datetime import datetime, timedelta

import boto3

client = boto3.client('logs')
app_name = 'robinhood'

paginator = client.get_paginator('describe_log_streams')
response_iterator = paginator.paginate(
    logGroupName=f'/aws/lambda/{app_name}',
)
for a in response_iterator:
    b = a['logStreams']
    for c in b:
        print(c['logStreamName'])


# tod = datetime.today() - timedelta(days=65)
# epoch_date = str(math.trunc(tod.timestamp()))
# deletion_date = int(epoch_date.ljust(13, '0'))

# for item in (response['logStreams']):
#     if item['creationTime'] < deletion_date:
#         resp = client.delete_log_stream(
#             logGroupName=f'/aws/lambda/{app_name}',
#             logStreamName=f"{item['logStreamName']}"
#         )
#         print(resp)
