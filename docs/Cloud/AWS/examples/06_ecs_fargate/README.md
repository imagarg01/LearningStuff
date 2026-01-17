# ECS Fargate Service

Deploy a containerized application on ECS Fargate.

## Architecture

```
Internet → ALB → ECS Fargate Tasks → Container
                      ↓
                 CloudWatch Logs
```

## Files

- `setup.sh` - Creates ECS cluster, task, and service
- `cleanup.sh` - Deletes all resources
- `Dockerfile` - Sample container image
- `template.yaml` - CloudFormation template

## Prerequisites

- Existing VPC with public subnets
- Docker for building images

## Usage

```bash
# Build and push image to ECR
aws ecr create-repository --repository-name my-app
docker build -t my-app .
docker tag my-app:latest <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker push <account>.dkr.ecr.<region>.amazonaws.com/my-app:latest

# Deploy with CloudFormation
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name ecs-fargate \
    --capabilities CAPABILITY_IAM
```

## Cost

- Fargate: ~$0.04/vCPU/hour + $0.0044/GB/hour
- ALB: ~$0.0225/hour + data
- **Estimated: ~$30-50/month for small service**
