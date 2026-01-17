#!/bin/bash
# Cleanup Lambda API

set -e

if [ ! -f .lambda-ids ]; then
    echo "No .lambda-ids file found."
    exit 0
fi

source .lambda-ids

echo "Cleaning up Lambda API resources..."

# Delete API Gateway
echo "Deleting API Gateway: $API_ID"
aws apigatewayv2 delete-api --api-id $API_ID 2>/dev/null || true

# Delete Lambda function
echo "Deleting Lambda function: $FUNCTION_NAME"
aws lambda delete-function --function-name $FUNCTION_NAME 2>/dev/null || true

# Detach policies and delete role
echo "Deleting IAM role: $ROLE_NAME"
aws iam detach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 2>/dev/null || true
aws iam delete-role --role-name $ROLE_NAME 2>/dev/null || true

rm -f .lambda-ids function.zip

echo "Cleanup complete!"
