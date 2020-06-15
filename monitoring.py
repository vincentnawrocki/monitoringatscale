import boto3

def update_sns_subscriber(file_path:str):
    # update subscribers on all SNS (all regions) for a given CIO based on a file (simple list of emails)

    pass

def deploy_monitoring_in_account():
    # List all regions
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    skynet_socle_account_id = '123'

    account_id = '123'

    cio = 'test'

    # connect to the account on all region
    # TODO
    for region in regions:

        # Open AWS CW client in the appropriate region
        cloudwatch_client = boto3.client('cloudwatch')

        # for each region:
        #   list lambda and save with prefix
        #   for the list, add to create alarm in metrics

        lambda_client = boto3.client('lambda')

        lambda_list = lambda_client.list_functions(
            # Marker='string',
            MaxItems=50
        )

        skynet_lambda = []

        for lambda in lambda_list['Functions']:
            if lambda['FunctionName'].startswith('skynet'):
                skynet_lambda += lambda

        cloudwatch_client.put_metric_alarm(
            AlarmName=f"skynet_alarm_lambda_error_{cio}_{account_id}_{region}",
            AlarmDescription='Send alarm if any Skynet Lambda in the region is in error',
            ActionsEnabled=True,
            OKActions=[
                f"arn:aws:sns:{region}:{skynet_socle_account_id}:sns-topic-name",
            ],
            AlarmActions=[
                f"arn:aws:sns:{region}:{skynet_socle_account_id}:sns-topic-name",
            ],
            EvaluationPeriods=300,
            Threshold=1.0,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            TreatMissingData='notBreaching',
            Metrics=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'string',
                            'MetricName': 'string',
                            'Dimensions': [
                                {
                                    'Name': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                        'Period': 123,
                        'Stat': 'string',
                        'Unit': 'Count'
                    },
                    'Expression': 'SUM(METRICS())',
                    'Label': 'skynet_lambda_error',
                    'ReturnData': True,
                    'Period': 300
                },
            ],
            Tags=[
                {
                    'Key': 'component',
                    'Value': 'skynet'
                },
                {
                    'Key': 'role',
                    'Value': 'monitoring'
                }
            ]
        )

        print(f"Alarm created")

        pass
