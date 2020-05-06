#Record to DDB when the EBS was created

from __future__ import print_function # Python 2/3 compatibility
import json
import boto3
from datetime import datetime
import decimal

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YOUR_DDB_TABLE')


def lambda_handler(event, context):
    #print(event)
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
    
    # Set EBS volume create date which is now.
    createDate = datetime.today().isoformat()

    # Get EBS volmue info from ec2.
    ec2 = boto3.resource('ec2')
    vol = ec2.Volume(id=volumeId)
    size = vol.size
    name = None
    
    # Search 'Name' tag of EBS. If no tag was found, name will be 'None'
    for tag in vol.tags:
	    if tag['Key'] == 'Name':
	        name = tag.get('Value')
    
    # Put item to ddb that contains EBS info.
    ddb_response = table.put_item(
        Item={
            'volumeId': volumeId,
            'createDate' : createDate,
            'Name' : name,
            'Size' : vol.size,
            'Type' : vol.volume_type,
            'IOPS' : vol.iops
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully Done!')
    }