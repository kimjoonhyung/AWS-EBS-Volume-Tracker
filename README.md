# AWS-EBS-Volume-Tracker
Record EBS Volume Creation and Deletion to DDB on AWS

Some developer usig AWS may have an experience of need to to track how many and what volumes was created and deleted, and also their performance during their entire lifecycles. 

You can run this repository with Amazon Cloudwatch Event, Amazon DynomoDB and Lambda functions to read and to records to DDB and Cloudwatch.

You can easily deploy EBS Volume Tracker as follwing.
1. Download 2 files EBS_Create.py and EBS_Delete.py, then create lambda functions. 
2. Both lambda functions should have IAM Role which allow DDB, EC2, CloudWatch Event actions.
3. Go Cloudwatch Event, and create new rules for EBS Creation and Deletion.
4. To create rule, select 'Event Pattern', 'EC2', 'EBS Volume Notification' and specify event. For EBS creation choose 'createVolume' and for EBS deletion choose 'deleteVolume'. Then, select a proper lambda function that you created.
5. Create DynamoDB table. Use string typed 'volumeId' as a primary key.
6. Create your EC2 or EMR. Use 'Name' tag to track your record at DDB more easily.

When EBS was deleted, its information such as size, type, write IOPS(avg, min, max) will be recored in the DDB table. 

You can analyze this information with Amazon ES and Kibana dashboard. 
