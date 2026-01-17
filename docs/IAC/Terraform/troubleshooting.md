# Terraform Troubleshooting Guide

Common errors and their solutions.

---

## Initialization Errors

### Error: Provider not found

```
Error: Failed to query available provider packages
```

**Solution:**

```bash
# Check internet connectivity
# Verify provider source in versions.tf
terraform init -upgrade
```

### Error: Backend initialization

```
Error: Failed to get existing workspaces
```

**Solution:**

```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify S3 bucket exists
aws s3 ls s3://your-bucket

# Check DynamoDB table
aws dynamodb describe-table --table-name terraform-locks
```

---

## State Errors

### Error: State lock

```
Error: Error locking state: Error acquiring the state lock
Lock Info:
  ID:        12345678-abcd
  Created:   2024-01-15 10:00:00
```

**Solution:**

```bash
# Check if another process is running
# If safe to unlock:
terraform force-unlock 12345678-abcd
```

### Error: Resource already exists

```
Error: Resource already exists
aws_s3_bucket.example with id "my-bucket" already exists
```

**Solution:**

```bash
# Import existing resource
terraform import aws_s3_bucket.example my-bucket
```

### Error: State out of sync

```
Error: Resource instance not found
```

**Solution:**

```bash
# Refresh state
terraform apply -refresh-only

# Or remove from state
terraform state rm aws_instance.old
```

---

## Configuration Errors

### Error: Invalid variable type

```
Error: Invalid value for variable
```

**Solution:**

```hcl
# Check variable type matches provided value
variable "ports" {
  type = list(number)  # Ensure you're passing numbers, not strings
}
```

### Error: Invalid reference

```
Error: Reference to undeclared resource
```

**Solution:**

- Check resource name spelling
- Verify resource is in same module or properly referenced
- Check for circular dependencies

### Error: Count and for_each conflict

```
Error: count and for_each are mutually exclusive
```

**Solution:**

```hcl
# Use only one:
resource "aws_instance" "web" {
  count = 3  # OR
  # for_each = toset(["a", "b"])  # Not both
}
```

---

## Provider Errors

### Error: No valid credential sources

```
Error: No valid credential sources found for AWS Provider
```

**Solution:**

```bash
# Configure AWS credentials
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx

# Or specify profile
provider "aws" {
  profile = "my-profile"
}
```

### Error: Access Denied

```
Error: AccessDenied: User is not authorized
```

**Solution:**

- Check IAM permissions
- Verify correct AWS account
- Check resource-based policies

---

## Apply Errors

### Error: Resource tainted

```
Resource is tainted, so must be replaced
```

**Solution:**

```bash
# Remove taint if resource is fine
terraform untaint aws_instance.web

# Or let it be replaced
terraform apply
```

### Error: Dependency cycle

```
Error: Cycle: aws_instance.a, aws_instance.b
```

**Solution:**

- Review resource dependencies
- Use `depends_on` carefully
- Break cycles with intermediate resources

### Error: Timeout

```
Error: timeout while waiting for state
```

**Solution:**

```hcl
resource "aws_instance" "web" {
  # Increase timeouts
  timeouts {
    create = "60m"
    delete = "30m"
  }
}
```

---

## Module Errors

### Error: Module not found

```
Error: Module not found
```

**Solution:**

```bash
# Re-initialize to download modules
terraform init -upgrade

# Check source path
module "vpc" {
  source = "./modules/vpc"  # Relative to root
}
```

### Error: Module version conflict

```
Error: Module version requirements are inconsistent
```

**Solution:**

```hcl
# Pin specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"  # Explicit version
}
```

---

## Debugging Tips

### Enable Verbose Logging

```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=/tmp/terraform.log
terraform apply
```

Log levels: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`

### Show Plan Details

```bash
terraform plan -out=tfplan
terraform show tfplan
terraform show -json tfplan > plan.json
```

### Check State

```bash
terraform state list
terraform state show aws_instance.web
terraform state pull > state.json
```

### Validate Without Backend

```bash
terraform init -backend=false
terraform validate
```

---

## Recovery Procedures

### Recover Corrupted State

```bash
# If using S3 versioning
aws s3api list-object-versions \
  --bucket terraform-state \
  --prefix path/to/terraform.tfstate

# Restore specific version
aws s3api get-object \
  --bucket terraform-state \
  --key path/to/terraform.tfstate \
  --version-id VERSION_ID \
  restored.tfstate

terraform state push restored.tfstate
```

### Recreate State from Scratch

```bash
# For each resource, import it
terraform import aws_vpc.main vpc-12345
terraform import aws_subnet.public[0] subnet-12345
# etc.
```

### Move Resources Between States

```bash
# Pull source state
terraform state pull > source.tfstate

# Move resource to target
terraform state mv \
  -state=source.tfstate \
  -state-out=target.tfstate \
  aws_instance.web aws_instance.web
```

---

## SSO/OIDC Authentication Issues

### AWS SSO Expired Credentials

**Problem:**

```
Error: error configuring Terraform AWS Provider: no valid credential sources
```

**Solution:**

```bash
# Re-authenticate with SSO
aws sso login --profile my-sso-profile

# Verify credentials
aws sts get-caller-identity --profile my-sso-profile

# Set profile
export AWS_PROFILE=my-sso-profile
```

### GitHub Actions OIDC Failure

**Problem:**

```
Error: Not authorized to perform sts:AssumeRoleWithWebIdentity
```

**Solution:**

Check IAM role trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:org/repo:*"
        }
      }
    }
  ]
}
```

Verify GitHub workflow has correct permissions:

```yaml
permissions:
  id-token: write
  contents: read
```

---

## State Migration Issues

### Backend Migration Failure

**Problem:**

```
Error: Backend configuration changed
```

**Solution:**

```bash
# Force re-initialization with migration
terraform init -migrate-state

# If still failing, reconfigure
terraform init -reconfigure
```

### State Lock Stuck

**Problem:**

```
Error: Error acquiring the state lock
Lock Info:
  ID:        12345-abcd-6789
  Path:      terraform-state/prod/terraform.tfstate
```

**Solution:**

```bash
# Force unlock (use with caution!)
terraform force-unlock 12345-abcd-6789

# Verify no one else is running
aws dynamodb scan --table-name terraform-locks
```

### Partial State Migration

**Problem:** Only some resources migrated.

**Solution:**

```bash
# List resources in old state
cd old-config
terraform state list

# List resources in new state
cd ../new-config
terraform state list

# Import missing resources
terraform import aws_instance.web i-12345678
```

---

## Import Failures

### Resource Already Managed

**Problem:**

```
Error: Resource already managed by Terraform
```

**Solution:**

```bash
# Remove from state first
terraform state rm aws_instance.web

# Then import
terraform import aws_instance.web i-12345678
```

### Resource Not Found

**Problem:**

```
Error: Cannot import non-existent resource
```

**Solution:**

```bash
# Verify resource exists
aws ec2 describe-instances --instance-ids i-12345678

# Check region
export AWS_REGION=us-west-2

# Verify ID format (some resources need ARN)
terraform import aws_iam_role.example arn:aws:iam::123456789:role/example
```

### Import ID Format Unknown

**Problem:** Don't know the correct import ID format.

**Solution:**

```bash
# Check provider documentation
# Common formats:
# EC2 Instance: i-12345678
# S3 Bucket: bucket-name
# IAM Role: role-name
# Security Group Rule: sg-id_type_protocol_from_to_source
# Route Table Association: subnet-id/rtb-id

# Example for security group rule
terraform import aws_security_group_rule.ssh \
  sg-12345678_ingress_tcp_22_22_0.0.0.0/0
```

### Generated Config Incomplete

**Problem:** `terraform plan -generate-config-out` missing required attributes.

**Solution:**

```bash
# View current state for missing values
terraform state show aws_instance.web

# Add required attributes manually
# Common missing: key_name, subnet_id, security groups
```

---

## Module Resolution Errors

### Module Not Found

**Problem:**

```
Error: Failed to download module
```

**Solution:**

```bash
# Clear module cache
rm -rf .terraform/modules

# Re-initialize
terraform init

# Check source path (local modules)
# Use relative path: source = "../modules/vpc"
# Not absolute: source = "/Users/me/modules/vpc"
```

### Module Version Conflict

**Problem:**

```
Error: Module version conflicts
```

**Solution:**

```hcl
# Pin specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"  # Exact version
}

# Or use constraint
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # Any 5.x.x
}
```

```bash
# Update modules
terraform init -upgrade
```

### Private Registry Authentication

**Problem:**

```
Error: Failed to retrieve module
401 Unauthorized
```

**Solution:**

```bash
# Terraform Cloud/Enterprise
terraform login

# Or set token
export TF_TOKEN_app_terraform_io=your-token

# For private Git repos
export GITHUB_TOKEN=your-token
# Or use SSH
module "example" {
  source = "git@github.com:org/terraform-module.git?ref=v1.0.0"
}
```

### Terraform Registry Rate Limiting

**Problem:**

```
Error: Too Many Requests
```

**Solution:**

```bash
# Use Terraform Cloud for registry caching
# Or mirror providers locally
terraform providers mirror /path/to/mirror
```

---

## Debugging Tips

### Enable Verbose Logging

```bash
# All logs
export TF_LOG=TRACE
export TF_LOG_PATH=terraform.log

# Provider logs only
export TF_LOG_PROVIDER=TRACE

# Core logs only
export TF_LOG_CORE=DEBUG
```

### Common Log Patterns

```bash
# Search for errors
grep -i "error" terraform.log

# Search for API calls
grep "http" terraform.log | head -20

# Search for state operations
grep -i "state" terraform.log
```

### Terraform Console

```bash
# Debug expressions
terraform console

> var.environment
"production"

> aws_vpc.main.id
"vpc-12345678"

> length(aws_subnet.public)
3
```

---

## Best Practices to Avoid Issues

1. **Always run `terraform plan` before `apply`**
2. **Use version constraints** for Terraform and providers
3. **Enable state locking** with DynamoDB
4. **Enable state versioning** in S3
5. **Use workspaces or directories** for environment separation
6. **Don't edit state manually** - use `terraform state` commands
7. **Pin module versions** in production
8. **Review CI/CD plans** before auto-applying
9. **Use `terraform fmt` and `terraform validate`** in CI
10. **Enable verbose logging** when debugging
