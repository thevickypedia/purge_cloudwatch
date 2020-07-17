import math
from datetime import datetime, timedelta

import boto3

app_name = 'robinhood'

client = boto3.client('logs')
paginator = client.get_paginator('describe_log_streams')
response_iterator = paginator.paginate(
    logGroupName=f'/aws/lambda/{app_name}',
)


def deletion_date():
    tod = datetime.today() - timedelta(days=20)
    epoch_date = str(math.trunc(tod.timestamp()))
    selected_date = int(epoch_date.ljust(13, '0'))
    return selected_date


print('Deleting log files..')

for response in response_iterator:
    collection = response['logStreams']
    for collected_value in collection:
        if collected_value['creationTime'] < deletion_date():
            resp = client.delete_log_stream(
                logGroupName=f'/aws/lambda/{app_name}',
                logStreamName=f"{collected_value['logStreamName']}"
            )
            if (resp['ResponseMetadata']['HTTPStatusCode']) == 200:
                pass
            else:
                print(f"Unable to purge logStream: {collected_value['logStreamName']}")
