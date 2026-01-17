#!/bin/bash
# S3 Static Website Setup

set -e

BUCKET_NAME="${1:-my-static-website-$(date +%s)}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"

echo "Creating S3 bucket: $BUCKET_NAME"

# Create bucket
if [ "$REGION" = "us-east-1" ]; then
    aws s3api create-bucket --bucket $BUCKET_NAME
else
    aws s3api create-bucket --bucket $BUCKET_NAME \
        --create-bucket-configuration LocationConstraint=$REGION
fi

# Block public access (we'll use CloudFront)
aws s3api put-public-access-block \
    --bucket $BUCKET_NAME \
    --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Enable static website hosting
aws s3 website s3://$BUCKET_NAME/ --index-document index.html --error-document error.html

# Create CloudFront Origin Access Control
OAC_ID=$(aws cloudfront create-origin-access-control \
    --origin-access-control-config \
        "Name=${BUCKET_NAME}-oac,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3" \
    --query 'OriginAccessControl.Id' --output text)
echo "Created OAC: $OAC_ID"

# Create CloudFront distribution
DIST_CONFIG=$(cat <<EOF
{
    "CallerReference": "$(date +%s)",
    "Comment": "Static website distribution",
    "DefaultRootObject": "index.html",
    "Origins": {
        "Quantity": 1,
        "Items": [{
            "Id": "S3Origin",
            "DomainName": "${BUCKET_NAME}.s3.${REGION}.amazonaws.com",
            "S3OriginConfig": {"OriginAccessIdentity": ""},
            "OriginAccessControlId": "${OAC_ID}"
        }]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3Origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"]},
        "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
        "Compress": true
    },
    "Enabled": true,
    "PriceClass": "PriceClass_100"
}
EOF
)

DIST_ID=$(aws cloudfront create-distribution \
    --distribution-config "$DIST_CONFIG" \
    --query 'Distribution.Id' --output text)
echo "Created CloudFront Distribution: $DIST_ID"

DIST_DOMAIN=$(aws cloudfront get-distribution --id $DIST_ID \
    --query 'Distribution.DomainName' --output text)

# Update S3 bucket policy for CloudFront
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "cloudfront.amazonaws.com"},
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::${BUCKET_NAME}/*",
        "Condition": {
            "StringEquals": {
                "AWS:SourceArn": "arn:aws:cloudfront::${ACCOUNT_ID}:distribution/${DIST_ID}"
            }
        }
    }]
}
EOF
)
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy "$POLICY"

# Create sample content
mkdir -p sample-site
cat > sample-site/index.html <<'EOF'
<!DOCTYPE html>
<html><head><title>My Static Website</title>
<style>
body { font-family: system-ui; max-width: 800px; margin: 0 auto; padding: 20px; }
h1 { color: #333; }
</style></head>
<body>
<h1>🚀 Welcome to My Static Website</h1>
<p>Hosted on S3 with CloudFront CDN.</p>
</body></html>
EOF

cat > sample-site/error.html <<'EOF'
<!DOCTYPE html>
<html><head><title>Error</title></head>
<body><h1>404 - Page Not Found</h1></body></html>
EOF

# Upload content
aws s3 sync sample-site/ s3://$BUCKET_NAME/

# Save IDs
cat > .website-ids <<EOF
BUCKET_NAME=$BUCKET_NAME
DIST_ID=$DIST_ID
OAC_ID=$OAC_ID
EOF

echo ""
echo "=========================================="
echo "Static Website Setup Complete!"
echo "=========================================="
echo "S3 Bucket:    $BUCKET_NAME"
echo "Distribution: $DIST_ID"
echo "Website URL:  https://$DIST_DOMAIN"
echo ""
echo "Note: CloudFront deployment takes 5-10 minutes"
echo "Run ./cleanup.sh to delete all resources"
