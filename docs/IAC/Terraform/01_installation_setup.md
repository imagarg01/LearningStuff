# Installation & AWS Setup

This guide walks you through installing Terraform and configuring AWS credentials for your learning journey.

> [!NOTE]
> **Time Required**: ~15 minutes
> **Prerequisites**: macOS, Linux, or Windows with admin access

---

## Installing Terraform

### macOS (Recommended: Homebrew)

```bash
# Install HashiCorp tap
brew tap hashicorp/tap

# Install Terraform
brew install hashicorp/tap/terraform

# Verify installation
terraform -version
```

**Expected output:**

```
Terraform v1.6.x
on darwin_arm64
```

### macOS/Linux (Manual Install)

```bash
# Download (replace VERSION and ARCH as needed)
# Visit: https://releases.hashicorp.com/terraform/

# Example for macOS ARM64 (M1/M2)
curl -LO https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_darwin_arm64.zip

# Unzip
unzip terraform_1.6.6_darwin_arm64.zip

# Move to PATH
sudo mv terraform /usr/local/bin/

# Verify
terraform -version
```

### Linux (apt-based distributions)

```bash
# Install HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list

# Update and install
sudo apt update && sudo apt install terraform

# Verify
terraform -version
```

### Windows

```powershell
# Option 1: Chocolatey
choco install terraform

# Option 2: Scoop
scoop install terraform

# Verify
terraform -version
```

---

## Version Management with tfenv (Recommended)

Different projects may require different Terraform versions. **tfenv** helps manage multiple versions.

```mermaid
graph LR
    subgraph "tfenv Version Management"
        A[Project A<br/>Terraform 1.5.x] --> B[tfenv]
        C[Project B<br/>Terraform 1.6.x] --> B
        D[Project C<br/>Terraform 1.4.x] --> B
        B --> E[Automatic Version Switching]
    end
```

### Installing tfenv

```bash
# macOS
brew install tfenv

# Linux/macOS (manual)
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Using tfenv

```bash
# List available versions
tfenv list-remote

# Install a specific version
tfenv install 1.6.6

# Use a specific version globally
tfenv use 1.6.6

# Pin version for a project (creates .terraform-version file)
echo "1.6.6" > .terraform-version

# List installed versions
tfenv list
```

> [!TIP]
> Always create a `.terraform-version` file in your project root to ensure consistent Terraform versions across team members.

---

## Installing AWS CLI

Terraform communicates with AWS using your AWS credentials. The AWS CLI provides an easy way to configure them.

### macOS

```bash
# Using Homebrew
brew install awscli

# Verify
aws --version
```

### Linux

```bash
# Download and install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

### Windows

```powershell
# Download MSI installer from:
# https://awscli.amazonaws.com/AWSCLIV2.msi

# Or using Chocolatey
choco install awscli

# Verify
aws --version
```

---

## AWS Account Setup

### Creating an IAM User for Terraform

> [!CAUTION]
> **Never use your AWS root account for Terraform!** Create a dedicated IAM user with appropriate permissions.

```mermaid
flowchart TD
    subgraph "AWS IAM Setup"
        A[AWS Console] --> B[IAM Service]
        B --> C[Create User: terraform-user]
        C --> D[Attach Policy:<br/>AdministratorAccess]
        D --> E[Create Access Keys]
        E --> F[Download Credentials]
    end
    
    style F fill:#f66,stroke:#333
```

### Step-by-Step IAM User Creation

1. **Login to AWS Console** → Navigate to **IAM**
2. **Users** → **Create User**
3. **User name**: `terraform-user`
4. **Permissions**: Attach `AdministratorAccess` policy (for learning)

> [!WARNING]
> `AdministratorAccess` grants full access to your AWS account. For production, create a custom policy with only necessary permissions.

1. **Security Credentials** → **Create Access Key**
2. **Use case**: Select "Command Line Interface (CLI)"
3. **Download** the `.csv` file with your credentials

### Configuring AWS Credentials

```bash
# Run AWS configure
aws configure

# Enter your credentials when prompted:
# AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name [None]: us-east-1
# Default output format [None]: json
```

This creates two files:

- `~/.aws/credentials` - Your access keys
- `~/.aws/config` - Region and output settings

### Verify AWS Configuration

```bash
# Test your credentials
aws sts get-caller-identity
```

**Expected output:**

```json
{
    "UserId": "AIDAIOSFODNN7EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/terraform-user"
}
```

---

## AWS Named Profiles (Optional but Recommended)

For managing multiple AWS accounts or roles:

```bash
# Create a profile for Terraform learning
aws configure --profile terraform-learning

# Use profile in commands
aws s3 ls --profile terraform-learning

# Export for current session
export AWS_PROFILE=terraform-learning
```

In Terraform, specify the profile:

```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "terraform-learning"
}
```

---

## Editor Setup

A good editor makes Terraform development much easier.

### VS Code (Recommended)

Install the **HashiCorp Terraform** extension:

```mermaid
graph LR
    A[VS Code] --> B[Extensions]
    B --> C[Search: HashiCorp Terraform]
    C --> D[Install]
    D --> E[Features]
    E --> F[Syntax Highlighting]
    E --> G[Auto-completion]
    E --> H[Formatting]
    E --> I[Validation]
```

**Extension ID**: `hashicorp.terraform`

**Features:**

- Syntax highlighting for `.tf` files
- IntelliSense for resources and attributes
- Auto-formatting with `terraform fmt`
- Built-in validation
- Go to definition

### VS Code Settings for Terraform

Add to your `settings.json`:

```json
{
  "[terraform]": {
    "editor.defaultFormatter": "hashicorp.terraform",
    "editor.formatOnSave": true,
    "editor.formatOnSaveMode": "file"
  },
  "[terraform-vars]": {
    "editor.defaultFormatter": "hashicorp.terraform",
    "editor.formatOnSave": true
  }
}
```

### Other Editors

| Editor | Plugin/Extension |
|--------|-----------------|
| JetBrains IDEs | Terraform and HCL plugin |
| Vim/Neovim | vim-terraform |
| Emacs | terraform-mode |
| Sublime Text | Terraform package |

---

## Your First Terraform Project

Let's verify everything works by creating a simple project.

### Step 1: Create Project Directory

```bash
# Create directory
mkdir -p ~/terraform-learning/hello-terraform
cd ~/terraform-learning/hello-terraform
```

### Step 2: Create Configuration

Create `main.tf`:

```hcl
# Terraform configuration
terraform {
  required_version = ">= 1.0.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# AWS Provider
provider "aws" {
  region = "us-east-1"
}

# A simple data source to verify connectivity
data "aws_caller_identity" "current" {}

# Output to display
output "account_id" {
  value       = data.aws_caller_identity.current.account_id
  description = "Your AWS Account ID"
}

output "caller_arn" {
  value       = data.aws_caller_identity.current.arn
  description = "ARN of the calling identity"
}
```

### Step 3: Initialize Terraform

```bash
terraform init
```

**Expected Output:**

```
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.x.x...
- Installed hashicorp/aws v5.x.x (signed by HashiCorp)

Terraform has been successfully initialized!
```

```mermaid
graph TD
    subgraph "What terraform init does"
        A[terraform init] --> B[Creates .terraform directory]
        A --> C[Downloads providers]
        A --> D[Creates .terraform.lock.hcl]
        B --> E[Stores provider binaries]
        D --> F[Locks provider versions]
    end
```

### Step 4: Plan and Apply

```bash
# Preview what will happen
terraform plan

# Apply (this only reads data, creates nothing)
terraform apply
```

Type `yes` when prompted. You should see:

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

account_id = "123456789012"
caller_arn = "arn:aws:iam::123456789012:user/terraform-user"
```

🎉 **Congratulations!** Your Terraform + AWS setup is complete!

---

## Understanding the Generated Files

After running `terraform init` and `terraform apply`, you'll have:

```
hello-terraform/
├── main.tf                    # Your configuration
├── .terraform/                # Provider binaries (gitignore this)
│   └── providers/
│       └── registry.terraform.io/
│           └── hashicorp/
│               └── aws/
├── .terraform.lock.hcl        # Dependency lock file (commit this)
└── terraform.tfstate          # State file (manage carefully!)
```

| File/Directory | Purpose | Git |
|----------------|---------|-----|
| `.terraform/` | Downloaded providers | ❌ Ignore |
| `.terraform.lock.hcl` | Locks provider versions | ✅ Commit |
| `terraform.tfstate` | Tracks deployed resources | ⚠️ Never commit locally |
| `*.tf` | Your configuration | ✅ Commit |

### Recommended .gitignore

Create `.gitignore`:

```gitignore
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Exclude all .tfvars files, which are likely to contain sensitive data
*.tfvars
*.tfvars.json

# Ignore override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Ignore CLI configuration files
.terraformrc
terraform.rc
```

---

## Troubleshooting

### Common Issues

#### "Error: No valid credential sources found"

```bash
# Check AWS credentials
aws sts get-caller-identity

# If it fails, reconfigure
aws configure
```

#### "Error: Incompatible provider version"

```bash
# Remove cached providers and reinitialize
rm -rf .terraform
terraform init -upgrade
```

#### "Error: Provider produced inconsistent result"

This usually means the provider has a bug. Try:

```bash
# Upgrade to latest provider version
terraform init -upgrade
```

#### Terraform command not found

```bash
# Check if terraform is in PATH
which terraform

# If not, check your installation:
# - Homebrew: brew list terraform
# - Manual: Check /usr/local/bin/
```

---

## Best Practices Checklist

Before moving on, ensure you have:

- [ ] Terraform installed and working (`terraform -version`)
- [ ] AWS CLI installed (`aws --version`)
- [ ] IAM user created with appropriate permissions
- [ ] AWS credentials configured (`aws sts get-caller-identity` works)
- [ ] VS Code with Terraform extension (or equivalent)
- [ ] First project runs successfully (`terraform apply` shows outputs)
- [ ] `.gitignore` file created

---

## Next Steps

You're all set! Continue to **[02_core_concepts.md](./02_core_concepts.md)** to learn about:

- Providers and how they connect to cloud platforms
- Resources as the building blocks of infrastructure
- State files and why they're critical
- The complete Terraform workflow

**→ [02_core_concepts.md](./02_core_concepts.md)**
