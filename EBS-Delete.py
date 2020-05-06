#Record to DDB when the EBS was terminated

from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from datetime import datetime
import decimal

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YOUR_DDB_TABLE')
period = 300


def lambda_handler(event, context):
    # Get volume ARN from event. 
    volumeARN = event['resources'][0]
    
    # Get the end of the ARN
    volumeId_end = len(volumeARN)
    
    # volume starts with 'vol-'. 
    volumeId_start = volumeARN.find("vol-")
    
    # Get the volume-id from ARN using start and end positions. 
    volumeId = volumeARN[volumeId_start:volumeId_end]
    #print(volumeId)
    
    # Get event pattern from event that derived from Cloudwatch Event
    eventPattern = event['detail']['event']
    #print(eventPattern)
    
    # Get data of the EBS volume from DDB
    ddb_response = table.get_item(
        Key={
            'volumeId': volumeId
        }
    )
 
    # Get create time from DDB item
    startTime = ddb_response['Item']['createDate']
    #print("startTime"+startTime)
    
    # Set terminate time which is now
    endTime=datetime.today().isoformat()
    
    # Get Cloudwatch metric of the EBS volume. from its start time to end time. Metrics are Average, Minimum, Maximum.
    cloudwatch = boto3.client('cloudwatch')

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='VolumeWriteOps',
        Dimensions=[
            {
                'Name': 'VolumeId',
                'Value': volumeId
            },
        ],
        StartTime = startTime,
        EndTime=endTime,
        Period=period,
        Statistics=[
            'Average','Minimum','Maximum'
        ],
        Unit='Count'
    )
    
    # Set initial values of Average, Minimum, Maximum from Cloudwatch response
    values = {'avg':0, 'min':1000000, 'max':0}
    values = setValues(response, values)
    

    # Put values for the EBS volume to DDB
    ddb_response = table.update_item(
        Key={
            'volumeId': volumeId
        },
        UpdateExpression='SET deleteDate = :val1, avgIOPS = :val2, minIOPS = :val3, maxIOPS = :val4',
        ExpressionAttributeValues={
            ':val1':endTime,
            ':val2':int(values['avg']/period),
            ':val3':int(values['min']/period),
            ':val4':int(values['max']/period)
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully Done!')
    }

def setValues(response, values):
    # If there are several metric values, loop and set values.
    for i in response['Datapoints']:
        if i['Average'] > values['avg']:
            values['avg'] = i['Average']
        if i['Minimum'] < values['min']:
            values['min'] = i['Minimum']
        if i['Maximum'] > values['max']:
            values['max'] = i['Maximum']
    return values

