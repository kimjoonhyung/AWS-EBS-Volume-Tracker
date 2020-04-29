# AWS-EBS-Volume-Tracker
Record EBS Volume life cycle to DDB on AWS

Some developer usig AWS may have an experience of how many and what volumes was created and deleted, and also their performance during their entire lifecycles. 

You can run this repository with AWS CDK to automate deploy Amazon Cloudwatch Event, Amazon DynomoDB and Lambda functions to read and to record at DDB and Cloudwatch.
