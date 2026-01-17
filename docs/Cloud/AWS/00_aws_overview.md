# AWS Overview

A comprehensive introduction to Amazon Web Services (AWS), the world's leading cloud platform.

---

## What is AWS?

Amazon Web Services (AWS) is a comprehensive cloud computing platform offering over **200 services** across computing, storage, networking, databases, analytics, machine learning, and more.

```mermaid
graph TB
    subgraph "AWS Global Infrastructure"
        subgraph "Region: us-east-1"
            AZ1["Availability Zone 1a"]
            AZ2["Availability Zone 1b"]
            AZ3["Availability Zone 1c"]
        end
        
        subgraph "Region: eu-west-1"
            AZ4["Availability Zone 1a"]
            AZ5["Availability Zone 1b"]
        end
        
        Edge["Edge Locations (400+)"]
    end
    
    User["Users"] --> Edge
    Edge --> AZ1
    Edge --> AZ4
```

---

## Global Infrastructure

### Regions

A **Region** is a geographical area containing multiple, isolated data centers.

| Component | Description | Example |
|-----------|-------------|---------|
| **Region** | Geographic area (33+ worldwide) | `us-east-1` (N. Virginia) |
| **Availability Zone** | Isolated data center(s) in a region | `us-east-1a`, `us-east-1b` |
| **Local Zone** | Extension of a region closer to users | `us-east-1-bos-1a` (Boston) |
| **Wavelength Zone** | Ultra-low latency at 5G edge | Embedded in telecom networks |
| **Edge Location** | CDN endpoints (400+ worldwide) | CloudFront, Route 53 |

### Choosing a Region

Consider these factors when selecting a region:

1. **Compliance** - Data residency requirements
2. **Latency** - Proximity to users
3. **Service availability** - Not all services in all regions
4. **Pricing** - Costs vary by region

```bash
# List all regions
aws ec2 describe-regions --query 'Regions[*].RegionName' --output table

# List availability zones in current region
aws ec2 describe-availability-zones --query 'AvailabilityZones[*].ZoneName'
```

---

## Core Service Categories

```mermaid
mindmap
  root((AWS Services))
    Compute
      EC2
      Lambda
      ECS/EKS
      Fargate
    Storage
      S3
      EBS
      EFS
      Glacier
    Database
      RDS
      DynamoDB
      Aurora
      ElastiCache
    Networking
      VPC
      Route 53
      CloudFront
      Direct Connect
    Security
      IAM
      KMS
      WAF
      Shield
    Management
      CloudWatch
      CloudFormation
      Systems Manager
```

### Compute Services

| Service | Use Case | Pricing Model |
|---------|----------|---------------|
| **EC2** | Virtual servers | Per-hour/second |
| **Lambda** | Serverless functions | Per-invocation |
| **ECS** | Container orchestration | Per-resource |
| **EKS** | Managed Kubernetes | $0.10/hr + resources |
| **Fargate** | Serverless containers | Per-vCPU/memory |

### Storage Services

| Service | Type | Durability | Use Case |
|---------|------|------------|----------|
| **S3** | Object | 99.999999999% | Files, backups, static assets |
| **EBS** | Block | 99.999% | EC2 disk volumes |
| **EFS** | File | 99.999999999% | Shared file storage |
| **Glacier** | Archive | 99.999999999% | Long-term archival |

### Database Services

| Service | Type | Engine | Use Case |
|---------|------|--------|----------|
| **RDS** | Relational | MySQL, PostgreSQL, etc. | Traditional apps |
| **Aurora** | Relational | MySQL/PostgreSQL compatible | High performance |
| **DynamoDB** | NoSQL | Key-value | Serverless, high scale |
| **ElastiCache** | In-memory | Redis, Memcached | Caching |

---

## AWS CLI Setup

### Installation

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows (PowerShell)
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify installation
aws --version
```

### Configuration

```bash
# Configure with access keys
aws configure

# Enter when prompted:
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name: us-east-1
# Default output format: json
```

### Named Profiles

```bash
# Configure additional profiles
aws configure --profile production

# Use a specific profile
aws s3 ls --profile production

# Set default profile
export AWS_PROFILE=production
```

### Configuration Files

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[production]
aws_access_key_id = AKIAI44QH8DHBEXAMPLE
aws_secret_access_key = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
```

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile production]
region = us-west-2
output = table
```

---

## AWS Console Navigation

```mermaid
graph LR
    Console["AWS Console"] --> Services["Services Menu"]
    Services --> Favorites["★ Favorites"]
    Services --> Recent["Recently Visited"]
    Services --> Search["Search Bar"]
    
    Console --> Region["Region Selector"]
    Console --> Account["Account Menu"]
    Account --> Billing["Billing"]
    Account --> Security["Security Credentials"]
    Account --> Organizations["Organizations"]
```

### Key Console Features

1. **Resource Groups** - Organize resources by tags
2. **CloudShell** - Browser-based CLI (free)
3. **Tag Editor** - Bulk tag management
4. **Service Health Dashboard** - AWS status

---

## Cost Management

### AWS Free Tier

| Category | Free Allowance | Duration |
|----------|----------------|----------|
| EC2 | 750 hours/month t2.micro | 12 months |
| S3 | 5 GB storage | 12 months |
| RDS | 750 hours/month db.t2.micro | 12 months |
| Lambda | 1M requests/month | Always free |
| DynamoDB | 25 GB storage | Always free |

### Cost Tools

```bash
# Enable Cost Explorer (Console)
# Billing → Cost Explorer → Enable

# Get current spend (requires Cost Explorer API access)
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics "BlendedCost"
```

### Cost Optimization Tips

1. **Right-size instances** - Use appropriate instance types
2. **Reserved Instances** - Up to 72% savings for 1-3 year commits
3. **Spot Instances** - Up to 90% savings for interruptible workloads
4. **S3 Lifecycle** - Move old data to cheaper storage classes
5. **Stop idle resources** - Shut down dev/test environments
6. **Use budgets** - Set alerts before overspending

```bash
# Create a monthly budget alert
aws budgets create-budget \
    --account-id 123456789012 \
    --budget file://budget.json \
    --notifications-with-subscribers file://notifications.json
```

---

## Essential CLI Commands

### Account & Identity

```bash
# Who am I?
aws sts get-caller-identity

# List account aliases
aws iam list-account-aliases
```

### Common Operations

```bash
# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# S3
aws s3 ls
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./folder s3://my-bucket/folder

# Lambda
aws lambda list-functions
aws lambda invoke --function-name my-function output.json
```

### Output Formatting

```bash
# Table format (human-readable)
aws ec2 describe-instances --output table

# JSON with jq filtering
aws ec2 describe-instances | jq '.Reservations[].Instances[].InstanceId'

# Query parameter (built-in filtering)
aws ec2 describe-instances \
    --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]' \
    --output table
```

---

## Best Practices for Beginners

> [!TIP]
> Start with these practices from day one to avoid bad habits.

### Security

1. **Never use root account** for daily tasks
2. **Enable MFA** on all accounts
3. **Use IAM roles** instead of access keys when possible
4. **Rotate credentials** regularly

### Cost Control

1. **Set up billing alerts** immediately
2. **Tag all resources** for cost tracking
3. **Review Cost Explorer** weekly
4. **Delete unused resources** promptly

### Architecture

1. **Use multiple AZs** for high availability
2. **Keep data in same region** as compute
3. **Use managed services** when possible
4. **Automate everything** with IaC

---

## Learning Path

```mermaid
graph LR
    A[AWS Overview] --> B[IAM & Security]
    B --> C[Networking VPC]
    C --> D[Compute EC2]
    D --> E[Storage S3]
    E --> F[Databases]
    F --> G[Serverless]
    G --> H[Well-Architected]
    
    style A fill:#e1f5fe
    style C fill:#fff3e0
    style H fill:#e8f5e9
```

---

## Next Steps

- **[IAM & Security](01_iam_security.md)** - Identity and access management fundamentals
