#!/bin/bash
# User data script for web/app servers

# Update system
yum update -y

# Install required packages
yum install -y httpd php php-mysqlnd

# Start Apache
systemctl start httpd
systemctl enable httpd

# Create simple health check page
cat > /var/www/html/health.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Health Check</title></head>
<body><h1>OK</h1></body>
</html>
EOF

# Create info page showing instance details
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
LOCAL_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)

cat > /var/www/html/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Three-Tier App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .info { background: #e8f5e9; padding: 15px; border-radius: 4px; margin: 10px 0; }
        .info-label { font-weight: bold; color: #2e7d32; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Three-Tier Architecture Demo</h1>
        <p>This page is served from an EC2 instance in the web tier.</p>
        <div class="info">
            <p><span class="info-label">Instance ID:</span> ${INSTANCE_ID}</p>
            <p><span class="info-label">Availability Zone:</span> ${AZ}</p>
            <p><span class="info-label">Private IP:</span> ${LOCAL_IP}</p>
            <p><span class="info-label">Hostname:</span> $(hostname)</p>
        </div>
        <p>Refresh the page to see load balancing in action!</p>
    </div>
</body>
</html>
EOF

# Set permissions
chown -R apache:apache /var/www/html/
