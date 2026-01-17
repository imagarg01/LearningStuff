# RDS Database Example

This example demonstrates how to create a managed PostgreSQL database using Amazon RDS.

## What You'll Learn

- Creating RDS instances with Terraform
- Database subnet groups and security groups
- Parameter groups for database configuration
- Secrets management with random passwords
- Multi-AZ deployment options

## Prerequisites

- AWS account with appropriate permissions
- VPC with private subnets (or use the VPC example first)
- Terraform >= 1.6.0

## Files

| File | Purpose |
|------|---------|
| `main.tf` | RDS instance, subnet group, security group |
| `variables.tf` | Input variables |
| `outputs.tf` | Database connection details |
| `versions.tf` | Provider requirements |
| `terraform.tfvars.example` | Example variable values |

## Usage

```bash
# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialize
terraform init

# Preview changes
terraform plan

# Create resources
terraform apply

# Get connection string
terraform output -raw db_connection_string
```

## Cost Estimate

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| db.t3.micro (Single-AZ) | ~$15-20 |
| db.t3.small (Single-AZ) | ~$30-35 |
| db.t3.micro (Multi-AZ) | ~$30-40 |
| Storage (20GB gp3) | ~$2-3 |

> **Note**: Enable `skip_final_snapshot = true` for development to avoid snapshot costs on destroy.

## Cleanup

```bash
terraform destroy

# Verify no snapshots remain (if skip_final_snapshot = false)
aws rds describe-db-snapshots --query 'DBSnapshots[*].DBSnapshotIdentifier'
```

## Security Considerations

- Database is in private subnets (no public access)
- Password generated randomly and stored in state
- For production, use AWS Secrets Manager instead
- Enable deletion protection for production databases
