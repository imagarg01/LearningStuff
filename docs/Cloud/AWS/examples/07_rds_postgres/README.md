# RDS PostgreSQL

Create an RDS PostgreSQL instance with best practices.

## Architecture

```
┌─────────────────────────────────────────┐
│ VPC                                     │
│                                         │
│  ┌─────────────┐  ┌─────────────┐      │
│  │ Private 1a  │  │ Private 1b  │      │
│  │   (RDS)     │  │ (Standby)   │      │
│  └──────┬──────┘  └──────┬──────┘      │
│         │                │              │
│         └────────┬───────┘              │
│                  │                      │
│         ┌───────┴───────┐              │
│         │ RDS Multi-AZ  │              │
│         └───────────────┘              │
└─────────────────────────────────────────┘
```

## Files

- `setup.sh` - Creates RDS instance
- `cleanup.sh` - Deletes all resources
- `template.yaml` - CloudFormation template

## Usage

```bash
# Deploy
./setup.sh

# Or with CloudFormation
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name rds-postgres \
    --parameter-overrides \
        VpcId=vpc-xxx \
        SubnetIds=subnet-aaa,subnet-bbb \
        MasterPassword=YourSecurePassword123!

# Connect
psql -h <endpoint> -U admin -d mydb
```

## Security Features

- Encrypted at rest
- Private subnets only
- Security group restricted
- Automated backups

## Cost

- db.t3.micro: ~$15/month
- db.t3.small: ~$30/month
- Multi-AZ doubles cost
- **Estimated: $15-60/month**
