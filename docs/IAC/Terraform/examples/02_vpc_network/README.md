# Example 02: VPC Networking

Create a complete VPC with public and private subnets.

## What You'll Learn

- VPC architecture
- Multi-AZ subnets
- Internet Gateway and NAT Gateway
- Route tables

## Architecture

```
VPC (10.0.0.0/16)
├── Public Subnet 1 (10.0.1.0/24) - us-east-1a
├── Public Subnet 2 (10.0.2.0/24) - us-east-1b
├── Private Subnet 1 (10.0.11.0/24) - us-east-1a
├── Private Subnet 2 (10.0.12.0/24) - us-east-1b
├── Internet Gateway
└── NAT Gateway
```

## Usage

```bash
cd examples/02_vpc_network
terraform init
terraform plan
terraform apply
terraform destroy  # Cleanup when done
```

## Cost Estimate

- NAT Gateway: ~$32/month + data transfer
