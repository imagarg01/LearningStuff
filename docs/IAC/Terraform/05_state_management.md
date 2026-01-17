# State Management

State is the backbone of Terraform. Understanding state management is crucial for team collaboration and production deployments.

> [!NOTE]
> **Learning Goal**: Master state files, remote backends, state locking, and state operations.

---

## What is Terraform State?

State is a JSON file that maps your configuration to real-world resources.

```mermaid
graph TB
    subgraph "State as Source of Truth"
        A[main.tf<br/>Desired State] --> C[Terraform Core]
        B[terraform.tfstate<br/>Actual State] --> C
        C --> D{Compare}
        D -->|Differences| E[Create/Update/Delete]
        D -->|Match| F[No Changes Needed]
        E --> G[Update State]
    end
    
    style C fill:#844fba,stroke:#333,color:#fff
```

### State File Contents

```json
{
  "version": 4,
  "terraform_version": "1.6.6",
  "serial": 15,
  "lineage": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "outputs": {
    "vpc_id": {
      "value": "vpc-0123456789abcdef0",
      "type": "string"
    }
  },
  "resources": [
    {
      "mode": "managed",
      "type": "aws_vpc",
      "name": "main",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 1,
          "attributes": {
            "id": "vpc-0123456789abcdef0",
            "cidr_block": "10.0.0.0/16",
            "enable_dns_hostnames": true,
            "tags": {
              "Name": "production-vpc"
            }
          }
        }
      ]
    }
  ]
}
```

### Why State Matters

| Purpose | What It Does |
|---------|--------------|
| **Resource Mapping** | Links config names to real resource IDs |
| **Dependency Tracking** | Knows which resources depend on others |
| **Performance** | Caches attributes to minimize API calls |
| **Change Detection** | Determines what has changed |

---

## Local State (Default)

By default, Terraform stores state locally in `terraform.tfstate`.

```mermaid
graph TD
    subgraph "Local State Problems"
        A[Developer 1<br/>Local State] --> E[AWS]
        B[Developer 2<br/>Local State] --> E
        C[CI/CD<br/>Local State] --> E
        
        A -.->|No Sync| B
        B -.->|No Sync| C
    end
    
    style E fill:#ff9800
```

**Problems with local state:**

- ❌ No team collaboration
- ❌ No state locking (concurrent modifications)
- ❌ No versioning
- ❌ Risk of accidental deletion
- ❌ Secrets stored in plain text locally

---

## Remote State Backends

Remote backends store state in a shared location.

```mermaid
graph TB
    subgraph "Remote State Solution"
        A[Developer 1] --> D[S3 Backend<br/>terraform.tfstate]
        B[Developer 2] --> D
        C[CI/CD Pipeline] --> D
        D --> E[AWS Resources]
        D <--> F[DynamoDB<br/>State Locking]
    end
    
    style D fill:#4CAF50,stroke:#333,color:#fff
```

### AWS S3 Backend (Recommended for AWS)

```hcl
# backend.tf

terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    
    # Enable encryption
    encrypt        = true
    
    # State locking
    dynamodb_table = "terraform-state-lock"
    
    # Optional: Use specific profile
    # profile        = "production"
  }
}
```

### Setting Up S3 Backend

**Step 1: Create S3 bucket** (do this once, manually or with separate Terraform)

```hcl
# backend-setup/main.tf

provider "aws" {
  region = "us-east-1"
}

# S3 bucket for state storage
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-company-terraform-state"
  
  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  tags = {
    Name = "Terraform State Lock Table"
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.terraform_lock.name
}
```

**Step 2: Initialize with backend**

```bash
# First run - initialize with backend
terraform init

# If changing backends, use migrate flag
terraform init -migrate-state
```

### State Locking

State locking prevents concurrent modifications:

```mermaid
sequenceDiagram
    participant Dev1 as Developer 1
    participant DDB as DynamoDB
    participant S3 as S3 State
    participant Dev2 as Developer 2
    
    Dev1->>DDB: Request Lock
    DDB-->>Dev1: Lock Granted ✓
    Dev1->>S3: Read State
    
    Dev2->>DDB: Request Lock
    DDB-->>Dev2: Lock Denied ✗ (Wait)
    
    Dev1->>S3: Write State
    Dev1->>DDB: Release Lock
    
    Dev2->>DDB: Request Lock
    DDB-->>Dev2: Lock Granted ✓
```

**Force unlock** (use with caution):

```bash
# If lock is stuck (e.g., crash during apply)
terraform force-unlock LOCK_ID
```

---

## Other Backend Types

### Terraform Cloud

```hcl
terraform {
  cloud {
    organization = "my-org"
    
    workspaces {
      name = "my-workspace"
    }
  }
}
```

### Azure (azurerm)

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### GCP (gcs)

```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "terraform/state"
  }
}
```

### PostgreSQL

```hcl
terraform {
  backend "pg" {
    conn_str = "postgres://user:pass@db.example.com/terraform_state"
  }
}
```

---

## State Operations

### terraform state list

List all resources in state:

```bash
terraform state list

# Output:
# aws_vpc.main
# aws_subnet.public[0]
# aws_subnet.public[1]
# aws_instance.web
```

### terraform state show

Show details of a specific resource:

```bash
terraform state show aws_instance.web

# Output:
# resource "aws_instance" "web" {
#     ami                          = "ami-0123456789abcdef0"
#     instance_type                = "t3.micro"
#     id                           = "i-0123456789abcdef0"
#     public_ip                    = "54.123.45.67"
#     ...
# }
```

### terraform state mv

Move or rename resources in state:

```hcl
# Rename resource in config from:
resource "aws_instance" "web" { }

# To:
resource "aws_instance" "web_server" { }
```

```bash
# Update state to match new name (avoids destroy/recreate)
terraform state mv aws_instance.web aws_instance.web_server
```

Move resource into a module:

```bash
terraform state mv aws_instance.web module.compute.aws_instance.web
```

### terraform state rm

Remove a resource from state (doesn't destroy it):

```bash
# Remove from Terraform management
terraform state rm aws_instance.legacy

# Use case: Stop managing a resource without destroying it
```

### terraform import

Import existing infrastructure into state:

```bash
# Syntax: terraform import RESOURCE_ADDRESS RESOURCE_ID
terraform import aws_instance.web i-0123456789abcdef0
```

**Example workflow for importing:**

```hcl
# 1. Write the resource configuration (empty or partial)
resource "aws_instance" "existing" {
  # Will be populated after import
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
}
```

```bash
# 2. Import the resource
terraform import aws_instance.existing i-0123456789abcdef0

# 3. View the imported state
terraform state show aws_instance.existing

# 4. Update your configuration to match the imported resource
# 5. Run plan to verify no changes
terraform plan
```

### terraform refresh (deprecated)

Update state to match real infrastructure:

```bash
# Old way (deprecated)
terraform refresh

# New way (Terraform 1.5+)
terraform apply -refresh-only
```

---

## State File Organization

### Monolithic State

All resources in one state file:

```
project/
├── main.tf
├── variables.tf
└── terraform.tfstate  # Everything here
```

**Pros:** Simple, no cross-state references needed
**Cons:** Slow for large infrastructures, blast radius is entire project

### State Per Environment

Separate state for each environment:

```mermaid
graph TD
    subgraph "State Per Environment"
        A[S3 Bucket] --> B["dev/terraform.tfstate"]
        A --> C["staging/terraform.tfstate"]
        A --> D["prod/terraform.tfstate"]
    end
```

Using backend configuration:

```hcl
# dev/backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
  }
}

# prod/backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### State Per Component

Separate state for network, compute, database:

```mermaid
graph TD
    subgraph "State Per Component"
        A[S3 Bucket] --> B["network/terraform.tfstate"]
        A --> C["compute/terraform.tfstate"]
        A --> D["database/terraform.tfstate"]
        
        B -->|outputs| C
        C -->|outputs| D
    end
```

**Pros:** Smaller blast radius, faster plans, team isolation
**Cons:** More complex, requires data sources for cross-state references

---

## Reading Remote State

Access outputs from another state file:

```hcl
# In compute project, reference network state
data "terraform_remote_state" "network" {
  backend = "s3"
  
  config = {
    bucket = "terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use the outputs
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  
  # Reference VPC ID from network state
  subnet_id = data.terraform_remote_state.network.outputs.public_subnet_ids[0]
  
  vpc_security_group_ids = [
    data.terraform_remote_state.network.outputs.web_sg_id
  ]
}
```

```mermaid
graph LR
    subgraph "Cross-State References"
        A[Network State] -->|outputs| B[terraform_remote_state]
        B -->|data source| C[Compute Config]
        C --> D[EC2 Instances]
    end
```

---

## State Migration

### Migrating from Local to Remote

```bash
# 1. Configure backend in backend.tf
# 2. Run init with migrate flag
terraform init -migrate-state

# Terraform will ask to copy existing state to new backend
# Do you want to copy existing state to the new backend?
# Type "yes"
```

### Migrating Between Remote Backends

```bash
# 1. Update backend configuration
# 2. Run init with reconfigure
terraform init -migrate-state
```

### Backend Configuration Changes

```bash
# After changing backend config
terraform init -reconfigure
```

---

## State Security

> [!CAUTION]
> State files contain sensitive data! They may include database passwords, API keys, and private keys in plaintext.

### Best Practices

```mermaid
graph TD
    subgraph "State Security Checklist"
        A[Encrypt at Rest] --> B[S3 SSE / KMS]
        C[Encrypt in Transit] --> D[HTTPS / TLS]
        E[Access Control] --> F[IAM Policies]
        G[Enable Versioning] --> H[S3 Versioning]
        I[Enable Logging] --> J[S3 Access Logs]
    end
```

**IAM Policy for State Access:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::terraform-state"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::terraform-state/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:*:table/terraform-state-lock"
    }
  ]
}
```

---

## State Troubleshooting

### State Lock Stuck

```bash
# Check who holds the lock (from error message)
# Error: Error locking state: ...
# Lock Info:
#   ID:        12345678-abcd-1234-abcd-123456789012
#   ...

# Force unlock (only if you're sure no one is running)
terraform force-unlock 12345678-abcd-1234-abcd-123456789012
```

### State Out of Sync

```bash
# Refresh state to match real infrastructure
terraform apply -refresh-only

# Review and approve the refresh
```

### Recovering from Corrupted State

```bash
# If using S3 versioning, restore previous version
aws s3api list-object-versions \
  --bucket terraform-state \
  --prefix prod/terraform.tfstate

# Download specific version
aws s3api get-object \
  --bucket terraform-state \
  --key prod/terraform.tfstate \
  --version-id VERSION_ID \
  restored-state.tfstate

# Replace current state (after backing up)
terraform state push restored-state.tfstate
```

---

## Best Practices Summary

| Practice | Why |
|----------|-----|
| **Use remote backend** | Team collaboration, safety |
| **Enable state locking** | Prevent corruption |
| **Enable versioning** | Recovery from mistakes |
| **Encrypt state** | Protect sensitive data |
| **Limit access** | IAM policies, least privilege |
| **Separate state per environment** | Reduce blast radius |
| **Never commit state to git** | Contains secrets |
| **Use workspaces sparingly** | Can be confusing at scale |

---

## Next Steps

Continue to **[06_modules.md](./06_modules.md)** to learn:

- Creating reusable modules
- Module structure and conventions
- Using public modules from Registry
- Module versioning and composition

**→ [06_modules.md](./06_modules.md)**
