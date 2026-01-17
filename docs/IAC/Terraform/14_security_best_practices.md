# Security Best Practices

Securing your Terraform infrastructure and workflow is critical for production environments.

> [!NOTE]
> **Learning Goal**: Implement security best practices for secrets management, access control, and policy enforcement.

---

## Security Overview

```mermaid
graph TB
    subgraph "Terraform Security Layers"
        A[Secrets Management] --> Z[Secure Infrastructure]
        B[State File Security] --> Z
        C[Access Control] --> Z
        D[Policy as Code] --> Z
        E[Audit & Compliance] --> Z
    end
    
    style Z fill:#4CAF50,stroke:#333,color:#fff
```

---

## Secrets Management

> [!CAUTION]
> **Never store secrets in plain text!** This includes `.tf` files, `.tfvars` files, and version control.

### What NOT to Do

```hcl
# ❌ NEVER DO THIS
variable "db_password" {
  default = "SuperSecret123!"  # Exposed in code!
}

# ❌ NEVER DO THIS
provider "aws" {
  access_key = "AKIAIOSFODNN7EXAMPLE"      # Exposed!
  secret_key = "wJalrXUtnFEMI/K7MDENG..."  # Exposed!
}
```

### Use Environment Variables

```bash
# AWS credentials
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG..."

# Terraform variables
export TF_VAR_db_password="your-secure-password"
export TF_VAR_api_key="your-api-key"
```

```hcl
# Terraform picks up TF_VAR_* automatically
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Hide in output
}
```

### AWS Secrets Manager

```hcl
# Read secret from Secrets Manager
data "aws_secretsmanager_secret" "db_credentials" {
  name = "prod/database/credentials"
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = data.aws_secretsmanager_secret.db_credentials.id
}

locals {
  db_creds = jsondecode(
    data.aws_secretsmanager_secret_version.db_credentials.secret_string
  )
}

resource "aws_db_instance" "main" {
  engine         = "postgres"
  instance_class = "db.t3.micro"
  
  username = local.db_creds.username
  password = local.db_creds.password
}
```

### AWS SSM Parameter Store

```hcl
# Read from Parameter Store
data "aws_ssm_parameter" "db_password" {
  name            = "/prod/database/password"
  with_decryption = true
}

resource "aws_db_instance" "main" {
  password = data.aws_ssm_parameter.db_password.value
}

# Create a secure parameter
resource "aws_ssm_parameter" "api_key" {
  name        = "/prod/app/api_key"
  description = "API key for external service"
  type        = "SecureString"
  value       = var.api_key  # From environment variable
  
  tags = {
    Environment = "prod"
  }
}
```

### HashiCorp Vault Integration

```hcl
# Configure Vault provider
provider "vault" {
  address = "https://vault.example.com:8200"
  # Token from VAULT_TOKEN env var
}

# Read secret from Vault
data "vault_generic_secret" "database" {
  path = "secret/data/production/database"
}

resource "aws_db_instance" "main" {
  username = data.vault_generic_secret.database.data["username"]
  password = data.vault_generic_secret.database.data["password"]
}

# Dynamic AWS credentials
data "vault_aws_access_credentials" "creds" {
  backend = "aws"
  role    = "terraform-role"
}

provider "aws" {
  access_key = data.vault_aws_access_credentials.creds.access_key
  secret_key = data.vault_aws_access_credentials.creds.secret_key
  token      = data.vault_aws_access_credentials.creds.security_token
}
```

### SOPS (Secrets OPerationS)

Encrypt secrets files that can be committed to Git:

```bash
# Install SOPS
brew install sops

# Create encrypted file
sops --encrypt --kms arn:aws:kms:us-east-1:123456789:key/abc123 \
  secrets.yaml > secrets.enc.yaml
```

```hcl
# Read SOPS-encrypted file
data "sops_file" "secrets" {
  source_file = "${path.module}/secrets.enc.yaml"
}

locals {
  secrets = yamldecode(data.sops_file.secrets.raw)
}
```

---

## State File Security

> [!WARNING]
> State files contain sensitive data in plain text, including passwords, API keys, and resource details.

### Encrypt State at Rest

```hcl
# S3 Backend with encryption
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    
    # Enable encryption
    encrypt        = true
    
    # Use custom KMS key
    kms_key_id     = "arn:aws:kms:us-east-1:123456789:key/abc123"
    
    # Enable locking
    dynamodb_table = "terraform-locks"
  }
}
```

### Restrict State Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "TerraformStateAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::terraform-state/prod/*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalTag/Team": "platform"
        }
      }
    },
    {
      "Sid": "TerraformStateLocking",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:*:table/terraform-locks"
    }
  ]
}
```

### Enable Versioning for Recovery

```hcl
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Block Public Access

```hcl
resource "aws_s3_bucket_public_access_block" "state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

---

## Least-Privilege IAM

### Terraform IAM Role

```hcl
# IAM Role for Terraform
resource "aws_iam_role" "terraform" {
  name = "terraform-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::${var.admin_account_id}:root"
      }
      Condition = {
        StringEquals = {
          "sts:ExternalId" = var.external_id
        }
      }
    }]
  })
}

# Attach specific policies instead of AdministratorAccess
resource "aws_iam_role_policy_attachment" "terraform_vpc" {
  role       = aws_iam_role.terraform.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
}

resource "aws_iam_role_policy_attachment" "terraform_ec2" {
  role       = aws_iam_role.terraform.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}
```

### Custom Least-Privilege Policy

```hcl
data "aws_iam_policy_document" "terraform_limited" {
  # VPC permissions
  statement {
    sid    = "VPCManagement"
    effect = "Allow"
    actions = [
      "ec2:CreateVpc",
      "ec2:DeleteVpc",
      "ec2:DescribeVpcs",
      "ec2:ModifyVpcAttribute",
      "ec2:CreateSubnet",
      "ec2:DeleteSubnet",
      "ec2:DescribeSubnets",
    ]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "aws:RequestTag/ManagedBy"
      values   = ["Terraform"]
    }
  }
  
  # State management
  statement {
    sid    = "StateManagement"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::terraform-state/*"
    ]
  }
  
  # Deny dangerous actions
  statement {
    sid    = "DenyDangerous"
    effect = "Deny"
    actions = [
      "iam:CreateUser",
      "iam:DeleteUser",
      "organizations:*",
    ]
    resources = ["*"]
  }
}
```

### Use IAM Roles Instead of Access Keys

```hcl
# For EC2 instances running Terraform
resource "aws_iam_instance_profile" "terraform_runner" {
  name = "terraform-runner"
  role = aws_iam_role.terraform.name
}

# For CI/CD (GitHub Actions OIDC)
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_actions" {
  name = "github-actions-terraform"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:myorg/myrepo:*"
        }
      }
    }]
  })
}
```

---

## Policy as Code

### Checkov

Static analysis for Terraform:

```bash
# Install
pip install checkov

# Run scan
checkov -d .

# Skip specific checks
checkov -d . --skip-check CKV_AWS_79,CKV_AWS_88

# Custom policy
checkov -d . --external-checks-dir ./custom-policies
```

**Custom Checkov policy:**

```python
# custom-policies/RequireEncryption.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class S3BucketEncryption(BaseResourceCheck):
    def __init__(self):
        name = "Ensure S3 bucket has encryption enabled"
        id = "CUSTOM_S3_001"
        supported_resources = ['aws_s3_bucket']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, 
                         supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        # Check for encryption configuration
        if 'server_side_encryption_configuration' in conf:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = S3BucketEncryption()
```

### tfsec

Security scanner for Terraform:

```bash
# Install
brew install tfsec

# Run scan
tfsec .

# Ignore specific checks
tfsec . --exclude aws-s3-enable-versioning

# Output as SARIF for GitHub
tfsec . --format sarif > results.sarif
```

**Inline ignores:**

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "my-logs-bucket"
  
  #tfsec:ignore:aws-s3-enable-versioning
  # Logs don't need versioning
}
```

### OPA (Open Policy Agent)

```rego
# policies/terraform.rego

package terraform

# Deny public S3 buckets
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    resource.change.after.acl == "public-read"
    msg := sprintf("S3 bucket '%s' cannot be public", [resource.name])
}

# Require tags
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not resource.change.after.tags.Environment
    msg := sprintf("Instance '%s' must have Environment tag", [resource.name])
}

# Limit instance types
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not startswith(resource.change.after.instance_type, "t3.")
    msg := sprintf("Instance '%s' must use t3.* family", [resource.name])
}
```

```bash
# Generate plan JSON
terraform plan -out=tfplan
terraform show -json tfplan > plan.json

# Evaluate with OPA
opa eval --data policies/ --input plan.json "data.terraform.deny"
```

### Sentinel (Terraform Enterprise/Cloud)

```hcl
# policies/require-tags.sentinel

import "tfplan/v2" as tfplan

mandatory_tags = ["Environment", "Owner", "CostCenter"]

# Get all resources
resources = filter tfplan.resource_changes as _, rc {
    rc.mode is "managed" and
    (rc.change.actions contains "create" or 
     rc.change.actions contains "update")
}

# Check tags
denied_resources = filter resources as _, r {
    tags = r.change.after.tags else {}
    missing = filter mandatory_tags as t {
        not (t in tags)
    }
    length(missing) > 0
}

main = rule {
    length(denied_resources) is 0
}
```

---

## Resource Security Patterns

### S3 Bucket Security

```hcl
resource "aws_s3_bucket" "secure" {
  bucket = "my-secure-bucket"
}

# Enable versioning
resource "aws_s3_bucket_versioning" "secure" {
  bucket = aws_s3_bucket.secure.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable logging
resource "aws_s3_bucket_logging" "secure" {
  bucket        = aws_s3_bucket.secure.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access-logs/"
}
```

### RDS Security

```hcl
resource "aws_db_instance" "secure" {
  identifier = "secure-database"
  
  engine         = "postgres"
  engine_version = "14"
  instance_class = "db.t3.micro"
  
  # Encryption
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn
  
  # Network isolation
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.private.name
  vpc_security_group_ids = [aws_security_group.database.id]
  
  # Enhanced monitoring
  monitoring_interval             = 60
  monitoring_role_arn             = aws_iam_role.rds_monitoring.arn
  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.rds.arn
  
  # Backup and protection
  backup_retention_period = 7
  deletion_protection     = true
  skip_final_snapshot     = false
  
  # Use Secrets Manager for credentials
  manage_master_user_password   = true
  master_user_secret_kms_key_id = aws_kms_key.rds.arn
  
  # Enable IAM authentication
  iam_database_authentication_enabled = true
}
```

### EC2 Security

```hcl
resource "aws_instance" "secure" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  
  # Network
  subnet_id                   = aws_subnet.private.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = false
  
  # Use IAM role instead of keys
  iam_instance_profile = aws_iam_instance_profile.app.name
  
  # IMDSv2 required
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # Require IMDSv2
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "disabled"
  }
  
  # Encrypted root volume
  root_block_device {
    encrypted   = true
    kms_key_id  = aws_kms_key.ec2.arn
    volume_type = "gp3"
  }
  
  # Enable detailed monitoring
  monitoring = true
  
  tags = {
    Name = "secure-instance"
  }
}
```

---

## Audit and Compliance

### CloudTrail for API Logging

```hcl
resource "aws_cloudtrail" "terraform" {
  name                          = "terraform-audit"
  s3_bucket_name                = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  
  kms_key_id = aws_kms_key.cloudtrail.arn
  
  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
}
```

### Resource Tagging for Governance

```hcl
# Enforce tags using provider default_tags
provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Environment = var.environment
      Owner       = var.owner
      CostCenter  = var.cost_center
      Project     = var.project
    }
  }
}

# Validate required tags
variable "owner" {
  type = string
  
  validation {
    condition     = can(regex("^[a-z.]+@company\\.com$", var.owner))
    error_message = "Owner must be a valid company email."
  }
}

variable "cost_center" {
  type = string
  
  validation {
    condition     = can(regex("^CC-[0-9]{4}$", var.cost_center))
    error_message = "Cost center must be in format CC-XXXX."
  }
}
```

---

## CI/CD Security

### GitHub Actions with OIDC

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:

permissions:
  id-token: write    # Required for OIDC
  contents: read
  pull-requests: write

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      # No access keys needed!
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-terraform
          aws-region: us-east-1
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
      
      - name: Terraform Init
        run: terraform init
      
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform
      
      - name: Terraform Plan
        run: terraform plan -no-color
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
      - id: terraform_checkov
        args:
          - --args=--skip-check CKV_AWS_79
```

---

## Security Checklist

### Before Production

- [ ] No secrets in code or `.tfvars`
- [ ] State file encrypted and access-controlled
- [ ] S3 bucket for state has versioning enabled
- [ ] State locking enabled (DynamoDB)
- [ ] IAM follows least privilege
- [ ] Using IAM roles, not access keys
- [ ] All S3 buckets block public access
- [ ] All RDS instances encrypted and in private subnets
- [ ] EC2 instances use IMDSv2
- [ ] CloudTrail logging enabled
- [ ] Required tags enforced
- [ ] Security scanning (Checkov/tfsec) in CI/CD
- [ ] Code review required for all changes
- [ ] Sensitive variables marked as `sensitive = true`

---

## Next Steps

Continue to **[15_terraform_cloud_enterprise.md](./15_terraform_cloud_enterprise.md)** to learn about team collaboration features, remote execution, and enterprise governance.

**→ [15_terraform_cloud_enterprise.md](./15_terraform_cloud_enterprise.md)**
