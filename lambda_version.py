import boto3

from datetime import datetime, timedelta


def lambda_handler(event, context):
    tod = datetime.today() - timedelta(days=7)
    epoch_date = str(int(tod.timestamp()))
    req_date = int(epoch_date.ljust(13, '0'))

    app_names = ['function_1', 'function_2', 'function_3']
    app1 = app_names[0]
    app2 = app_names[1]
    app3 = app_names[2]
    n1 = 0
    n2 = 0
    n3 = 0
    app1_m = 0
    app2_m = 0
    app3_m = 0
    for app_name in app_names:
        client = boto3.client('logs')
        paginator = client.get_paginator('describe_log_streams')
        response_iterator = paginator.paginate(
            logGroupName=f'/aws/lambda/{app_name}',
        )

        for item in response_iterator:
            collection = item['logStreams']
            for collected_value in collection:
                if collected_value['creationTime'] < req_date:
                    client.delete_log_stream(
                        logGroupName=f'/aws/lambda/{app_name}',
                        logStreamName=f"{collected_value['logStreamName']}"
                    )
                    if app_name == app1:
                        n1 = n1 + 1
                        app1_m += round(float(collected_value['storedBytes'] / 1000), 2)
                    elif app_name == app2:
                        n2 = n2 + 1
                        app2_m += round(float(collected_value['storedBytes'] / 1000), 2)
                    elif app_name == app3:
                        n3 = n3 + 1
                        app3_m += round(float(collected_value['storedBytes'] / 1000), 2)

    data = f"Number of logs purged for {app1}: {n1} Memory released: {round(float(app1_m), 2)} KB\n" \
           f"Number of logs purged for {app2}: {n2} Memory released: {round(float(app2_m), 2)} KB\n" \
           f"Number of logs purged for {app3}: {n3} Memory released: {round(float(app3_m), 2)} KB\n"

    print(data)
