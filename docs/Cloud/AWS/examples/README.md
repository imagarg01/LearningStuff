# AWS Practical Examples

Hands-on examples for common AWS architectures.

## Examples Overview

| # | Example | Services | Difficulty |
|---|---------|----------|------------|
| 01 | [Basic VPC](01_basic_vpc/) | VPC, Subnets, IGW | Beginner |
| 02 | [Multi-Tier VPC](02_multi_tier_vpc/) | VPC, NAT, Route Tables | Intermediate |
| 03 | [EC2 with Auto Scaling](03_ec2_autoscaling/) | EC2, ALB, ASG | Intermediate |
| 04 | [S3 Static Website](04_s3_static_website/) | S3, CloudFront | Beginner |
| 05 | [Lambda + API Gateway](05_lambda_api/) | Lambda, API Gateway | Intermediate |
| 06 | [ECS Fargate](06_ecs_fargate/) | ECS, Fargate, ALB | Advanced |
| 07 | [RDS PostgreSQL](07_rds_postgres/) | RDS, Security Groups | Intermediate |
| 08 | [Transit Gateway](08_transit_gateway/) | TGW, VPC Peering | Advanced |

## How to Use

1. Navigate to example directory
2. Review the README for prerequisites
3. Run the setup script or deploy CloudFormation
4. Clean up when done to avoid charges

## Prerequisites

- AWS CLI configured (`aws configure`)
- Appropriate IAM permissions
- For CloudFormation: ability to create stacks

## Cost Warning

> ⚠️ These examples create real AWS resources that incur charges. Always clean up resources when done!
