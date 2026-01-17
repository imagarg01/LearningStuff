#!/bin/bash
# Lambda API Setup

set -e

FUNCTION_NAME="demo-api"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Setting up Lambda API..."

# Create IAM role for Lambda
ROLE_NAME="${FUNCTION_NAME}-role"
TRUST_POLICY='{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}'

ROLE_ARN=$(aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document "$TRUST_POLICY" \
    --query 'Role.Arn' --output text 2>/dev/null || \
    aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
echo "IAM Role: $ROLE_ARN"

# Attach basic execution policy
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 2>/dev/null || true

# Wait for role to propagate
sleep 10

# Package function
cd function
zip -r ../function.zip .
cd ..

# Create Lambda function
LAMBDA_ARN=$(aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --runtime nodejs18.x \
    --handler index.handler \
    --role $ROLE_ARN \
    --zip-file fileb://function.zip \
    --query 'FunctionArn' --output text 2>/dev/null || \
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://function.zip \
        --query 'FunctionArn' --output text)
echo "Lambda Function: $LAMBDA_ARN"

# Create HTTP API
API_ID=$(aws apigatewayv2 create-api \
    --name "${FUNCTION_NAME}-api" \
    --protocol-type HTTP \
    --query 'ApiId' --output text)
echo "API Gateway: $API_ID"

# Create integration
INTEGRATION_ID=$(aws apigatewayv2 create-integration \
    --api-id $API_ID \
    --integration-type AWS_PROXY \
    --integration-uri $LAMBDA_ARN \
    --payload-format-version 2.0 \
    --query 'IntegrationId' --output text)

# Create routes
aws apigatewayv2 create-route \
    --api-id $API_ID \
    --route-key "GET /hello" \
    --target "integrations/$INTEGRATION_ID" > /dev/null

aws apigatewayv2 create-route \
    --api-id $API_ID \
    --route-key "GET /users" \
    --target "integrations/$INTEGRATION_ID" > /dev/null

aws apigatewayv2 create-route \
    --api-id $API_ID \
    --route-key "POST /users" \
    --target "integrations/$INTEGRATION_ID" > /dev/null

# Create stage
aws apigatewayv2 create-stage \
    --api-id $API_ID \
    --stage-name prod \
    --auto-deploy > /dev/null

# Add permission for API Gateway to invoke Lambda
aws lambda add-permission \
    --function-name $FUNCTION_NAME \
    --statement-id apigateway-invoke \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${API_ID}/*" 2>/dev/null || true

# Get API endpoint
API_ENDPOINT="https://${API_ID}.execute-api.${REGION}.amazonaws.com/prod"

# Save IDs
cat > .lambda-ids <<EOF
FUNCTION_NAME=$FUNCTION_NAME
ROLE_NAME=$ROLE_NAME
API_ID=$API_ID
EOF

# Clean up
rm -f function.zip

echo ""
echo "=========================================="
echo "Lambda API Setup Complete!"
echo "=========================================="
echo "API Endpoint: $API_ENDPOINT"
echo ""
echo "Test endpoints:"
echo "  curl $API_ENDPOINT/hello"
echo "  curl $API_ENDPOINT/users"
echo "  curl -X POST $API_ENDPOINT/users -d '{\"name\":\"Alice\"}'"
echo ""
echo "Run ./cleanup.sh to delete all resources"
