#!/bin/bash
# Cleanup S3 Static Website

set -e

if [ ! -f .website-ids ]; then
    echo "No .website-ids file found."
    exit 0
fi

source .website-ids

echo "Cleaning up static website resources..."

# Disable CloudFront distribution first
echo "Disabling CloudFront distribution: $DIST_ID"
ETAG=$(aws cloudfront get-distribution-config --id $DIST_ID --query 'ETag' --output text)
CONFIG=$(aws cloudfront get-distribution-config --id $DIST_ID --query 'DistributionConfig')
DISABLED_CONFIG=$(echo $CONFIG | jq '.Enabled = false')
aws cloudfront update-distribution --id $DIST_ID --if-match $ETAG --distribution-config "$DISABLED_CONFIG" 2>/dev/null || true

echo "Waiting for distribution to be disabled (this may take several minutes)..."
aws cloudfront wait distribution-deployed --id $DIST_ID 2>/dev/null || true

# Delete CloudFront distribution
echo "Deleting CloudFront distribution..."
ETAG=$(aws cloudfront get-distribution-config --id $DIST_ID --query 'ETag' --output text)
aws cloudfront delete-distribution --id $DIST_ID --if-match $ETAG 2>/dev/null || true

# Delete OAC
echo "Deleting Origin Access Control: $OAC_ID"
ETAG=$(aws cloudfront get-origin-access-control --id $OAC_ID --query 'ETag' --output text 2>/dev/null || echo "")
if [ -n "$ETAG" ]; then
    aws cloudfront delete-origin-access-control --id $OAC_ID --if-match $ETAG 2>/dev/null || true
fi

# Empty and delete S3 bucket
echo "Emptying S3 bucket: $BUCKET_NAME"
aws s3 rm s3://$BUCKET_NAME --recursive 2>/dev/null || true

echo "Deleting S3 bucket: $BUCKET_NAME"
aws s3api delete-bucket --bucket $BUCKET_NAME 2>/dev/null || true

rm -f .website-ids
rm -rf sample-site

echo "Cleanup complete!"
