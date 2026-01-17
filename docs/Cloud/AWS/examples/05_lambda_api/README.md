# Lambda + API Gateway

Serverless API with Lambda and API Gateway.

## Architecture

```
Client → API Gateway → Lambda → DynamoDB (optional)
```

## Files

- `setup.sh` - Creates Lambda and API Gateway
- `cleanup.sh` - Deletes all resources
- `function/` - Lambda function code
- `template.yaml` - SAM template

## Usage

```bash
# Deploy with shell script
./setup.sh

# Or use SAM
cd function
sam build
sam deploy --guided

# Test the API
curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello
```

## Lambda Function

```javascript
// function/index.js
exports.handler = async (event) => {
    return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Hello from Lambda!" })
    };
};
```

## Cost

- Lambda: 1M requests/month free
- API Gateway: 1M requests/month free
- **Estimated: Free tier for small APIs**
