# Three-Tier Architecture Example

This example demonstrates a complete production-ready three-tier AWS architecture with web, application, and database tiers.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                              Internet                                │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Application Load        │
                    │       Balancer (ALB)       │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼─────────┐ ┌───────▼───────┐ ┌────────▼────────┐
    │   Web Server 1    │ │ Web Server 2  │ │  Web Server N   │
    │   (Public Subnet) │ │(Public Subnet)│ │ (Public Subnet) │
    └─────────┬─────────┘ └───────┬───────┘ └────────┬────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
    ┌─────────────────────────────▼─────────────────────────────┐
    │                    Internal Load Balancer                  │
    └─────────────────────────────┬─────────────────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼─────────┐ ┌───────▼───────┐ ┌────────▼────────┐
    │   App Server 1    │ │ App Server 2  │ │  App Server N   │
    │ (Private Subnet)  │ │(Private Subnet│ │ (Private Subnet)│
    └─────────┬─────────┘ └───────┬───────┘ └────────┬────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │      RDS Database         │
                    │    (Private Subnet)       │
                    │       Multi-AZ            │
                    └───────────────────────────┘
```

## What You'll Learn

- Complete VPC with public and private subnets
- Application Load Balancer with health checks
- Auto Scaling Groups for web and app tiers
- RDS PostgreSQL with Multi-AZ option
- Security groups with least-privilege access
- NAT Gateway for private subnet internet access

## Prerequisites

- AWS account with appropriate permissions
- Terraform >= 1.6.0
- SSH key pair in AWS (for EC2 access)

## Files

| File | Purpose |
|------|---------|
| `main.tf` | All infrastructure resources |
| `variables.tf` | Input variables |
| `outputs.tf` | Important resource details |
| `versions.tf` | Provider requirements |
| `user_data.sh` | EC2 bootstrap script |
| `terraform.tfvars.example` | Example variable values |

## Usage

```bash
# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Set database password
export TF_VAR_db_password="YourSecurePassword123!"

# Initialize
terraform init

# Preview changes
terraform plan

# Create resources (takes 15-20 minutes)
terraform apply

# Get ALB URL
terraform output alb_dns_name
```

## Cost Estimate

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| NAT Gateway (2x) | ~$64 |
| ALB | ~$16 + data transfer |
| EC2 t3.micro (4x) | ~$30 |
| RDS db.t3.micro | ~$15 |
| EBS Storage | ~$5 |
| **Total (minimum)** | **~$130/month** |

> **⚠️ Warning**: Production configurations with larger instances and Multi-AZ will cost significantly more.

## Cleanup

```bash
# Destroy all resources
terraform destroy

# Verify cleanup
aws ec2 describe-instances --filters "Name=tag:Project,Values=three-tier-app"
aws rds describe-db-instances
```

## Security Considerations

- Database is in private subnets (no public access)
- Application tier only accessible from web tier
- Web tier only accessible from ALB
- All security groups follow least-privilege
- Use AWS Secrets Manager for database credentials in production
- Enable deletion protection for production RDS
