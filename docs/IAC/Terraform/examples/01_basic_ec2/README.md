# Example 01: Basic EC2 Instance

Your first Terraform project - create an EC2 instance on AWS.

## What You'll Learn

- Basic Terraform configuration
- AWS provider setup
- Creating and destroying resources
- Using data sources

## Prerequisites

- Terraform installed
- AWS CLI configured
- AWS account

## Files

| File | Purpose |
|------|---------|
| `main.tf` | EC2 instance resource |
| `variables.tf` | Input variables |
| `outputs.tf` | Output values |
| `versions.tf` | Version constraints |

## Usage

```bash
cd examples/01_basic_ec2
terraform init
terraform plan
terraform apply
terraform destroy  # Cleanup when done
```

## Cost Estimate

- t3.micro: ~$8/month (Free tier eligible for first year)
