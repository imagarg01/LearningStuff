exports.handler = async (event) => {
    console.log('Event:', JSON.stringify(event, null, 2));

    const httpMethod = event.httpMethod || event.requestContext?.http?.method;
    const path = event.path || event.requestContext?.http?.path;

    // Route handling
    if (path === '/hello' || path === '/prod/hello') {
        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify({
                message: 'Hello from Lambda!',
                timestamp: new Date().toISOString(),
                path: path,
                method: httpMethod
            })
        };
    }

    if (path === '/users' || path === '/prod/users') {
        if (httpMethod === 'GET') {
            return {
                statusCode: 200,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    users: [
                        { id: 1, name: 'Alice' },
                        { id: 2, name: 'Bob' }
                    ]
                })
            };
        }

        if (httpMethod === 'POST') {
            const body = JSON.parse(event.body || '{}');
            return {
                statusCode: 201,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: 'User created',
                    user: body
                })
            };
        }
    }

    return {
        statusCode: 404,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Not Found' })
    };
};
