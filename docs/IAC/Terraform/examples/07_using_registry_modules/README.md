# Using Terraform Registry Modules

This example demonstrates the **enterprise pattern** of using pre-built, community-maintained modules from the Terraform Registry instead of writing infrastructure from scratch.

## Why Use Registry Modules?

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Enterprise Module Pattern                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ❌ DON'T: Write everything from scratch                           │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ resource "aws_vpc" "main" { ... }                            │  │
│   │ resource "aws_subnet" "public" { ... }                       │  │
│   │ resource "aws_subnet" "private" { ... }                      │  │
│   │ resource "aws_nat_gateway" "main" { ... }                    │  │
│   │ resource "aws_route_table" "public" { ... }                  │  │
│   │ resource "aws_route_table" "private" { ... }                 │  │
│   │ ... 200+ lines of code                                       │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│   ✅ DO: Use battle-tested modules                                  │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ module "vpc" {                                               │  │
│   │   source  = "terraform-aws-modules/vpc/aws"                  │  │
│   │   version = "5.0.0"                                          │  │
│   │   name    = "my-vpc"                                         │  │
│   │   cidr    = "10.0.0.0/16"                                    │  │
│   │ }                                                            │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Benefits of Registry Modules

| Benefit | Description |
|---------|-------------|
| **Battle-tested** | Used by thousands of companies |
| **Well-documented** | Comprehensive README and examples |
| **Maintained** | Regular updates and security patches |
| **Best practices** | Follows AWS/cloud provider recommendations |
| **Time savings** | Deploy complex infra in minutes |
| **Consistency** | Standard patterns across teams |

## What You'll Learn

- Using modules from the Terraform Registry
- Module versioning and pinning
- Passing variables to modules
- Using module outputs
- Composing multiple modules together

## Modules Used in This Example

| Module | Source | Purpose |
|--------|--------|---------|
| VPC | `terraform-aws-modules/vpc/aws` | Complete VPC with subnets |
| Security Group | `terraform-aws-modules/security-group/aws` | Security group rules |
| ALB | `terraform-aws-modules/alb/aws` | Application Load Balancer |
| RDS | `terraform-aws-modules/rds/aws` | RDS PostgreSQL database |

## Files

| File | Purpose |
|------|---------|
| `main.tf` | Module deployments |
| `variables.tf` | Input variables |
| `outputs.tf` | Output values |
| `versions.tf` | Provider and module requirements |
| `terraform.tfvars.example` | Example variable values |

## Usage

```bash
# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars

# Initialize (downloads modules)
terraform init

# Preview changes
terraform plan

# Apply
terraform apply

# View outputs
terraform output
```

## Finding Modules

1. **Terraform Registry**: [registry.terraform.io](https://registry.terraform.io)
2. **AWS Modules**: [github.com/terraform-aws-modules](https://github.com/terraform-aws-modules)
3. **Azure Modules**: [github.com/Azure](https://github.com/Azure)
4. **Google Modules**: [github.com/terraform-google-modules](https://github.com/terraform-google-modules)

## Module Version Constraints

```hcl
# ✅ Pin exact version (recommended for production)
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
}

# ✅ Allow patch updates only
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0.0"  # 5.0.x
}

# ⚠️ Allow minor updates (test before production)
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"    # 5.x.x
}

# ❌ Never use in production
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  # No version = always latest (dangerous!)
}
```

## Cost Estimate

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| NAT Gateway (2x) | ~$64 |
| ALB | ~$16 |
| RDS db.t3.micro | ~$15 |
| **Total (minimum)** | **~$95/month** |

## Cleanup

```bash
terraform destroy
```
