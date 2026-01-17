# Basic VPC Setup

Creates a simple VPC with public subnets.

## Architecture

```
┌─────────────────────────────────────────┐
│ VPC: 10.0.0.0/16                        │
│                                         │
│  ┌─────────────┐  ┌─────────────┐      │
│  │ Public 1a   │  │ Public 1b   │      │
│  │ 10.0.1.0/24 │  │ 10.0.2.0/24 │      │
│  └──────┬──────┘  └──────┬──────┘      │
│         │                │              │
│         └────────┬───────┘              │
│                  │                      │
│         ┌───────┴───────┐              │
│         │ Internet GW   │              │
│         └───────────────┘              │
└─────────────────────────────────────────┘
```

## Files

- `setup.sh` - Creates all resources
- `cleanup.sh` - Deletes all resources
- `template.yaml` - CloudFormation template

## Usage

### Option 1: Shell Script

```bash
# Create VPC
./setup.sh

# Clean up
./cleanup.sh
```

### Option 2: CloudFormation

```bash
# Deploy
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name basic-vpc

# Delete
aws cloudformation delete-stack --stack-name basic-vpc
```

## Cost

- VPC: Free
- Internet Gateway: Free
- **Estimated: $0/month**
