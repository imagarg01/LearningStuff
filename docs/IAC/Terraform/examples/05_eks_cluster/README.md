# EKS Cluster Example

This example demonstrates how to create a managed Kubernetes cluster using Amazon EKS.

## What You'll Learn

- Creating EKS clusters with Terraform
- Node groups and scaling configuration
- IAM roles for EKS (cluster and node roles)
- VPC configuration for Kubernetes
- kubectl configuration

## Prerequisites

- AWS account with appropriate permissions
- Terraform >= 1.6.0
- kubectl installed
- aws-iam-authenticator (or AWS CLI v2+)

## Files

| File | Purpose |
|------|---------|
| `main.tf` | EKS cluster, node groups, IAM roles |
| `variables.tf` | Input variables |
| `outputs.tf` | Cluster details and kubeconfig |
| `versions.tf` | Provider requirements |
| `terraform.tfvars.example` | Example variable values |

## Usage

```bash
# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialize
terraform init

# Preview changes
terraform plan

# Create resources (takes 10-15 minutes)
terraform apply

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster

# Verify cluster
kubectl get nodes
kubectl get pods -A
```

## Cost Estimate

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| EKS Control Plane | ~$72 |
| t3.medium nodes (2x) | ~$60 |
| NAT Gateway | ~$32 |
| **Total (minimum)** | **~$164/month** |

> **⚠️ Warning**: EKS is expensive! Remember to destroy when not in use.

## Cleanup

```bash
# Important: Delete any LoadBalancer services first
kubectl delete svc --all -A

# Wait for load balancers to be deleted
sleep 60

# Destroy infrastructure
terraform destroy

# Verify cleanup
aws eks list-clusters
```

## Common Issues

### kubectl connection fails

```bash
# Refresh kubeconfig
aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster
```

### Nodes not joining

```bash
# Check node group status
aws eks describe-nodegroup --cluster-name my-eks-cluster --nodegroup-name main
```

## Security Considerations

- Cluster endpoint is public by default (configure private access for production)
- Node groups run in private subnets
- Use IRSA (IAM Roles for Service Accounts) for pod permissions
- Enable envelope encryption for secrets
