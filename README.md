# AWS-EBS-Volume-Tracker
Record EBS Volume Creation and Deletion to DDB on AWS

Some developer usig AWS may have an experience of need to to track how many and what volumes was created and deleted, and also their performance during their entire lifecycles. 

You can run this repository with Amazon Cloudwatch Event, Amazon DynomoDB and Lambda functions to read and to records to DDB and Cloudwatch.
