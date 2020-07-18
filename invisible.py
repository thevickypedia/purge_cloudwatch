from datetime import datetime, timedelta

import boto3

app_name = 'purge_logs'


def login():
    client = boto3.client('logs')
    paginator = client.get_paginator('describe_log_streams')
    response_iterator = paginator.paginate(
        logGroupName=f'/aws/lambda/{app_name}'
    )
    return client, response_iterator


def deletion_date():
    tod = datetime.today() - timedelta(days=7)
    h_date = tod.strftime('%B %d, %Y')
    print(f'Due Date: {h_date}')
    epoch_date = str(int(tod.timestamp()))
    selected_date = int(epoch_date.ljust(13, '0'))
    return selected_date, h_date


def purger():
    n = 0
    app_memory = 0
    print('Attempting to delete log files..')
    try:
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
                        app_memory += round(float(collected_value['storedBytes'] / 1000), 2)
                    else:
                        print(f"Unable to purge logStream: {collected_value['logStreamName']}")
                        pass
        if n == 0:
            return f'No logs were found before {due_date}'
        elif n == 1:
            return f"{n} log stream was purged for the function {app_name}. Memory released: {app_memory} KB"
        else:
            return f"{n} log streams were purged for the function {app_name}. Memory released: {app_memory} KB"
    except Exception:
        return f"Unable to find the lambda function. Make sure the function name '{app_name}' is correct and exists!!"


if __name__ == '__main__':
    client_, response = login()
    req_date, due_date = deletion_date()
    print(purger())
