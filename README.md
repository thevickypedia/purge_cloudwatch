# Purge Logs
Script to delete cloudwatch logs.

This script requires aws cli setup which enables the user to login to the aws account to purge the cloudwatch logs.

Lambda script for a scheduled cleanup: [lambda_version.py](https://github.com/thevickypedia/purge_cloudwatch/blob/master/lambda_version.py)

[AWS CLI setup](https://docs.aws.amazon.com/polly/latest/dg/setup-aws-cli.html)

[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html)