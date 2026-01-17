# AWS Cheat Sheet

Quick reference for common AWS CLI commands.

---

## Configuration

```bash
# Configure default profile
aws configure

# Configure named profile
aws configure --profile myprofile

# Set default region
export AWS_DEFAULT_REGION=us-east-1

# Set profile
export AWS_PROFILE=myprofile

# Who am I?
aws sts get-caller-identity
```

---

## EC2

```bash
# List instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress]' --output table

# Start/Stop/Terminate
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx

# Launch instance
aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro --key-name mykey --security-group-ids sg-xxx --subnet-id subnet-xxx

# Get console output
aws ec2 get-console-output --instance-id i-xxx

# Create AMI
aws ec2 create-image --instance-id i-xxx --name "MyAMI"
```

---

## S3

```bash
# List buckets
aws s3 ls

# List objects
aws s3 ls s3://bucket-name/

# Upload/Download
aws s3 cp file.txt s3://bucket-name/
aws s3 cp s3://bucket-name/file.txt ./

# Sync folder
aws s3 sync ./folder s3://bucket-name/folder/

# Delete
aws s3 rm s3://bucket-name/file.txt
aws s3 rm s3://bucket-name/folder/ --recursive

# Presigned URL
aws s3 presign s3://bucket-name/file.txt --expires-in 3600
```

---

## IAM

```bash
# List users/roles
aws iam list-users
aws iam list-roles

# Create user
aws iam create-user --user-name john

# Create access key
aws iam create-access-key --user-name john

# Attach policy
aws iam attach-user-policy --user-name john --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Assume role
aws sts assume-role --role-arn arn:aws:iam::xxx:role/MyRole --role-session-name mysession
```

---

## VPC

```bash
# List VPCs
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' --output table

# List subnets
aws ec2 describe-subnets --query 'Subnets[*].[SubnetId,VpcId,CidrBlock,AvailabilityZone]' --output table

# List security groups
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,VpcId]' --output table
```

---

## RDS

```bash
# List instances
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,Engine,DBInstanceStatus]' --output table

# Create snapshot
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot

# Get endpoint
aws rds describe-db-instances --db-instance-identifier mydb --query 'DBInstances[0].Endpoint.Address' --output text
```

---

## Lambda

```bash
# List functions
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime,MemorySize]' --output table

# Invoke function
aws lambda invoke --function-name myfunction --payload '{}' output.json

# Update code
aws lambda update-function-code --function-name myfunction --zip-file fileb://function.zip

# View logs
aws logs tail /aws/lambda/myfunction --follow
```

---

## ECS

```bash
# List clusters
aws ecs list-clusters

# List services
aws ecs list-services --cluster mycluster

# Update service
aws ecs update-service --cluster mycluster --service myservice --force-new-deployment

# Run task
aws ecs run-task --cluster mycluster --task-definition mytask
```

---

## CloudWatch

```bash
# List log groups
aws logs describe-log-groups

# Tail logs
aws logs tail /aws/lambda/myfunction --follow

# Get metric
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-xxx --start-time 2024-01-01T00:00:00Z --end-time 2024-01-01T01:00:00Z --period 300 --statistics Average
```

---

## Useful Flags

```bash
--query      # JMESPath query for filtering
--output     # table, json, text
--profile    # Use named profile
--region     # Override region
--dry-run    # Check permissions without executing
--no-paginate # Return all results
```

---

## Common Filters

```bash
# Filter by tag
--filters "Name=tag:Name,Values=myinstance"

# Filter by state
--filters "Name=instance-state-name,Values=running"

# Filter by VPC
--filters "Name=vpc-id,Values=vpc-xxx"
```

---

## Output Formatting

```bash
# Table format
aws ec2 describe-instances --output table

# Query specific fields
aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --output text

# JSON with jq
aws ec2 describe-instances | jq '.Reservations[].Instances[].InstanceId'
```

---

## Service Limits

| Service | Default Limit |
|---------|---------------|
| VPCs per region | 5 |
| Subnets per VPC | 200 |
| Security groups per VPC | 2,500 |
| EC2 instances | Varies by type |
| EBS volumes per region | 10,000 |
| S3 buckets per account | 100 |
| Lambda concurrent executions | 1,000 |
| RDS instances per region | 40 |

Check limits: `aws service-quotas list-service-quotas --service-code ec2`

---

## Cost Management

```bash
# Get current spend
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics BlendedCost

# List reserved instances
aws ec2 describe-reserved-instances

# List savings plans
aws savingsplans describe-savings-plans
```

---

## Quick Troubleshooting

```bash
# Check instance status
aws ec2 describe-instance-status --instance-ids i-xxx

# Check RDS events
aws rds describe-events --source-identifier mydb --source-type db-instance

# Check Lambda errors
aws logs filter-log-events --log-group-name /aws/lambda/myfunction --filter-pattern ERROR

# Check CloudTrail
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=StopInstances
```
