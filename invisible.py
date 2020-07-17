import math
from datetime import datetime, timedelta

import boto3

app_name = 'robinhood'


def login():
    client = boto3.client('logs')
    paginator = client.get_paginator('describe_log_streams')
    response_iterator = paginator.paginate(
        logGroupName=f'/aws/lambda/{app_name}',
    )
    return client, response_iterator


def deletion_date():
    tod = datetime.today() - timedelta(days=7)
    epoch_date = str(math.trunc(tod.timestamp()))
    selected_date = int(epoch_date.ljust(13, '0'))
    return selected_date


def purger():
    n = 0
    print('Deleting log files..')
    for item in response:
        collection = item['logStreams']
        for collected_value in collection:
            if collected_value['creationTime'] < req_date:
                resp = client_.delete_log_stream(
                    logGroupName=f'/aws/lambda/{app_name}',
                    logStreamName=f"{collected_value['logStreamName']}"
                )
                n = n + 1
                if (resp['ResponseMetadata']['HTTPStatusCode']) == 200:
                    pass
                else:
                    print(f"Unable to purge logStream: {collected_value['logStreamName']}")
                    pass
    return n


if __name__ == '__main__':
    client_, response = login()
    req_date = deletion_date()
    print(f'\n{purger()} log streams were purged successfully.')
