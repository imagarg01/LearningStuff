# S3 Static Website with CloudFront

Host a static website on S3 with CloudFront CDN.

## Architecture

```
Users → CloudFront (CDN) → S3 Bucket (Origin)
```

## Files

- `setup.sh` - Creates S3 bucket and CloudFront
- `cleanup.sh` - Deletes all resources
- `template.yaml` - CloudFormation template
- `sample-site/` - Sample HTML files

## Usage

```bash
# Deploy with shell script
./setup.sh my-unique-bucket-name

# Or use CloudFormation
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name static-website \
    --parameter-overrides BucketName=my-unique-bucket-name

# Upload content
aws s3 sync sample-site/ s3://my-unique-bucket-name/

# Get CloudFront URL
aws cloudfront list-distributions --query 'DistributionList.Items[0].DomainName'
```

## Cost

- S3: ~$0.023/GB storage
- CloudFront: ~$0.085/GB data transfer
- **Estimated: ~$1-5/month for small sites**
