# Terraform Cheat Sheet

Quick reference for common Terraform commands and patterns.

---

## CLI Commands

### Basic Workflow

```bash
terraform init              # Initialize working directory
terraform plan              # Preview changes
terraform apply             # Apply changes
terraform destroy           # Destroy all resources
```

### Planning Options

```bash
terraform plan -out=tfplan           # Save plan to file
terraform plan -var="key=value"      # Pass variable
terraform plan -var-file=prod.tfvars # Use variable file
terraform plan -target=aws_instance.web  # Plan specific resource
terraform plan -refresh=false        # Skip state refresh
```

### Apply Options

```bash
terraform apply -auto-approve        # Skip confirmation
terraform apply tfplan               # Apply saved plan
terraform apply -target=aws_instance.web  # Apply specific resource
terraform apply -parallelism=10      # Increase parallelism
```

### State Commands

```bash
terraform state list                 # List all resources
terraform state show RESOURCE        # Show resource details
terraform state mv OLD NEW           # Rename resource
terraform state rm RESOURCE          # Remove from state
terraform state pull                 # Download state
terraform state push                 # Upload state
terraform import RESOURCE ID         # Import existing resource
```

### Other Commands

```bash
terraform fmt                        # Format code
terraform fmt -check                 # Check formatting
terraform validate                   # Validate configuration
terraform output                     # Show outputs
terraform output -json               # JSON format
terraform refresh                    # Update state (deprecated: use apply -refresh-only)
terraform workspace list             # List workspaces
terraform workspace new NAME         # Create workspace
terraform workspace select NAME      # Switch workspace
terraform graph | dot -Tpng > graph.png  # Visualize dependencies
```

---

## Configuration Syntax

### Provider Configuration

```hcl
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "my-profile"
}
```

### Resource

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
  }
}
```

### Variable

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
  
  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Must be t2 or t3 family."
  }
}
```

### Output

```hcl
output "public_ip" {
  description = "Public IP address"
  value       = aws_instance.web.public_ip
  sensitive   = false
}
```

### Local

```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project = var.project
    Environment = var.environment
  }
}
```

### Data Source

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}
```

### Module

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

---

## Common Patterns

### Conditional Resource

```hcl
resource "aws_eip" "web" {
  count = var.create_eip ? 1 : 0
  instance = aws_instance.web.id
}
```

### for_each with Map

```hcl
resource "aws_instance" "servers" {
  for_each = var.instances
  ami           = each.value.ami
  instance_type = each.value.type
  tags = { Name = each.key }
}
```

### Dynamic Block

```hcl
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port = ingress.value.port
    to_port   = ingress.value.port
    protocol  = "tcp"
  }
}
```

### For Expression

```hcl
# List
upper_names = [for n in var.names : upper(n)]

# Map
name_map = { for n in var.names : n => upper(n) }

# With filter
filtered = [for n in var.names : n if length(n) > 3]
```

### Lifecycle

```hcl
lifecycle {
  create_before_destroy = true
  prevent_destroy       = true
  ignore_changes        = [tags["LastModified"]]
}
```

---

## Common Functions

| Function | Example | Result |
|----------|---------|--------|
| `format` | `format("Hello %s", "World")` | "Hello World" |
| `join` | `join(",", ["a","b"])` | "a,b" |
| `split` | `split(",", "a,b")` | ["a","b"] |
| `length` | `length(["a","b"])` | 2 |
| `lookup` | `lookup(map, "key", "default")` | value or default |
| `merge` | `merge(map1, map2)` | combined map |
| `coalesce` | `coalesce(null, "default")` | "default" |
| `try` | `try(var.x, "fallback")` | x or "fallback" |
| `cidrsubnet` | `cidrsubnet("10.0.0.0/16", 8, 1)` | "10.0.1.0/24" |

---

## File Structure

```
project/
├── main.tf           # Primary resources
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── versions.tf       # Version constraints
├── providers.tf      # Provider config
├── backend.tf        # State backend
├── locals.tf         # Local values
├── data.tf           # Data sources
├── terraform.tfvars  # Variable values
└── modules/
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## .gitignore

```gitignore
# Terraform
**/.terraform/*
*.tfstate
*.tfstate.*
crash.log
*.tfvars
!*.tfvars.example
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraformrc
terraform.rc
.terraform.lock.hcl
```

---

## S3 Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

---

## Moved Blocks

Refactor resources without destroying:

```hcl
# Rename resource
moved {
  from = aws_instance.web
  to   = aws_instance.app
}

# Move into module
moved {
  from = aws_vpc.main
  to   = module.network.aws_vpc.main
}

# Move resource within for_each
moved {
  from = aws_instance.servers["old-key"]
  to   = aws_instance.servers["new-key"]
}
```

---

## Import Blocks

Declarative imports (Terraform 1.5+):

```hcl
import {
  to = aws_instance.web
  id = "i-0123456789abcdef0"
}

import {
  to = aws_vpc.main
  id = "vpc-12345678"
}
```

```bash
# Generate config for imports
terraform plan -generate-config-out=generated.tf
```

---

## terraform test

```bash
# Run tests
terraform test

# Run specific test file
terraform test -filter=tests/main.tftest.hcl

# Verbose output
terraform test -verbose
```

Test file structure:

```hcl
# tests/main.tftest.hcl

variables {
  environment = "test"
}

run "validate_vpc" {
  command = plan

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR is incorrect"
  }
}

run "create_resources" {
  command = apply

  assert {
    condition     = length(aws_subnet.public) == 3
    error_message = "Should create 3 subnets"
  }
}
```

---

## Additional Functions

### Collection Functions

```hcl
# one() - extract single element
one(aws_instance.web[*].id)

# alltrue() / anytrue()
alltrue([true, true, true])  # true
anytrue([false, true, false])  # true

# sum() / min() / max()
sum([1, 2, 3])  # 6
min(5, 2, 8)    # 2
max(5, 2, 8)    # 8

# range()
range(3)      # [0, 1, 2]
range(1, 4)   # [1, 2, 3]
```

### String Functions

```hcl
# startswith() / endswith()
startswith("hello", "he")  # true
endswith("hello.txt", ".txt")  # true

# trim variants
trimprefix("helloworld", "hello")  # "world"
trimsuffix("hello.txt", ".txt")    # "hello"
trimspace("  hello  ")             # "hello"

# strcontains()
strcontains("hello world", "world")  # true
```

### Type Functions

```hcl
# type()
type("hello")  # string
type(42)       # number

# can() - check if expression is valid
can(regex("^[a-z]+$", var.input))

# try() - return first successful expression
try(var.complex.nested.value, "default")

# sensitive() / nonsensitive()
sensitive(var.password)
nonsensitive(data.aws_ssm_parameter.secret.value)
```

### Date/Time Functions

```hcl
# timestamp()
timestamp()  # "2024-01-15T12:00:00Z"

# formatdate()
formatdate("YYYY-MM-DD", timestamp())

# timeadd()
timeadd(timestamp(), "24h")
timeadd(timestamp(), "-1h30m")

# timecmp()
timecmp(timestamp(), "2024-01-01T00:00:00Z")  # 1 (greater), 0 (equal), -1 (less)
```

---

## Check Blocks

Continuous validation (Terraform 1.5+):

```hcl
check "certificate_valid" {
  data "aws_acm_certificate" "main" {
    domain = "example.com"
  }

  assert {
    condition     = data.aws_acm_certificate.main.status == "ISSUED"
    error_message = "Certificate is not valid!"
  }
}
```

---

## Preconditions & Postconditions

```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = var.environment == "prod" ? var.instance_type != "t3.micro" : true
      error_message = "Production cannot use t3.micro"
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have public IP"
    }
  }
}
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy infrastructure |
| `terraform fmt` | Format code |
| `terraform validate` | Validate configuration |
| `terraform output` | Show outputs |
| `terraform state list` | List resources in state |
| `terraform state show <resource>` | Show resource details |
| `terraform import <addr> <id>` | Import existing resource |
| `terraform test` | Run tests |
| `terraform console` | Interactive console |
