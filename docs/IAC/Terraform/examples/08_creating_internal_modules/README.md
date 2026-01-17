# Creating and Using Internal Modules

This example demonstrates the **enterprise pattern** of creating reusable internal modules that can be shared across teams and projects.

## Enterprise Module Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Internal Module Library                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   modules/                  ← Shared module library                  │
│   ├── networking/                                                    │
│   │   └── vpc/             ← Standardized VPC module                 │
│   ├── compute/                                                       │
│   │   ├── ec2-instance/    ← Approved EC2 patterns                   │
│   │   └── asg/             ← Auto Scaling patterns                   │
│   ├── database/                                                      │
│   │   └── rds-postgres/    ← Database standards                      │
│   └── security/                                                      │
│       └── security-group/  ← Security-approved configs               │
│                                                                      │
│   environments/             ← Environment configurations              │
│   ├── dev/                                                           │
│   │   └── main.tf          ← Uses modules from library               │
│   ├── staging/                                                       │
│   │   └── main.tf                                                    │
│   └── prod/                                                          │
│       └── main.tf                                                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Why Internal Modules?

| Benefit | Description |
|---------|-------------|
| **Standardization** | All teams use approved patterns |
| **Security** | Security team pre-approves modules |
| **Compliance** | Built-in compliance controls |
| **Governance** | Enforce tagging, naming, encryption |
| **Reusability** | Write once, use everywhere |
| **Maintainability** | Update module, all consumers get fix |

## Module Structure

```
08_creating_internal_modules/
├── modules/                      ← Internal module library
│   ├── vpc/                      ← VPC module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── ec2-web-server/          ← EC2 module with standards
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── rds-postgres/            ← RDS module with compliance
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── main.tf                       ← Root module using internal modules
├── variables.tf
├── outputs.tf
└── versions.tf
```

## What You'll Learn

- Creating reusable modules
- Module input validation
- Module output composition
- Calling modules from root
- Module best practices

## Usage

```bash
# Initialize
terraform init

# Preview
terraform plan

# Apply
terraform apply

# Access the web server
terraform output web_url
```

## Cost Estimate

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| VPC + NAT Gateway | ~$32 |
| EC2 t3.micro | ~$8 |
| RDS db.t3.micro | ~$15 |
| **Total** | **~$55/month** |

## Cleanup

```bash
terraform destroy
```

## Publishing Modules

### Git Repository (Recommended for teams)

```hcl
module "vpc" {
  source = "git::https://github.com/myorg/terraform-modules.git//vpc?ref=v1.0.0"
}
```

### Private Registry (Terraform Cloud/Enterprise)

```hcl
module "vpc" {
  source  = "app.terraform.io/myorg/vpc/aws"
  version = "1.0.0"
}
```

### S3 Bucket

```hcl
module "vpc" {
  source = "s3::https://s3-us-east-1.amazonaws.com/my-modules/vpc.zip"
}
```
