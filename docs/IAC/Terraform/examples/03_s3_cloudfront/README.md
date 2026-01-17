# Example 03: S3 + CloudFront Static Website

Host a static website on S3 with CloudFront CDN.

## What You'll Learn

- S3 bucket configuration for static hosting
- CloudFront distribution setup
- Origin Access Identity (OAI)
- Bucket policies

## Architecture

```
Internet → CloudFront → S3 Bucket (private)
                ↓
           OAI Access
```

## Usage

```bash
cd examples/03_s3_cloudfront
terraform init
terraform plan
terraform apply

# Upload your website files
aws s3 sync ./website s3://$(terraform output -raw bucket_name)

terraform destroy  # Cleanup when done
```

## Cost Estimate

- S3: ~$0.023/GB storage
- CloudFront: ~$0.085/GB transfer
