#!/bin/bash
# Basic VPC Setup Script
# Creates a VPC with public subnets

set -e

# Configuration
VPC_CIDR="10.0.0.0/16"
PUBLIC_SUBNET_1_CIDR="10.0.1.0/24"
PUBLIC_SUBNET_2_CIDR="10.0.2.0/24"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
NAME_PREFIX="demo"

echo "Creating VPC in $REGION..."

# Create VPC
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block $VPC_CIDR \
    --query 'Vpc.VpcId' \
    --output text)
echo "Created VPC: $VPC_ID"

# Enable DNS hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-support

# Tag VPC
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=${NAME_PREFIX}-vpc

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --query 'InternetGateway.InternetGatewayId' \
    --output text)
echo "Created Internet Gateway: $IGW_ID"

aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
aws ec2 create-tags --resources $IGW_ID --tags Key=Name,Value=${NAME_PREFIX}-igw

# Get availability zones
AZ1=$(aws ec2 describe-availability-zones \
    --query 'AvailabilityZones[0].ZoneName' \
    --output text)
AZ2=$(aws ec2 describe-availability-zones \
    --query 'AvailabilityZones[1].ZoneName' \
    --output text)

# Create public subnet 1
SUBNET_1_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $PUBLIC_SUBNET_1_CIDR \
    --availability-zone $AZ1 \
    --query 'Subnet.SubnetId' \
    --output text)
echo "Created Subnet 1: $SUBNET_1_ID in $AZ1"

aws ec2 modify-subnet-attribute --subnet-id $SUBNET_1_ID --map-public-ip-on-launch
aws ec2 create-tags --resources $SUBNET_1_ID --tags Key=Name,Value=${NAME_PREFIX}-public-1

# Create public subnet 2
SUBNET_2_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $PUBLIC_SUBNET_2_CIDR \
    --availability-zone $AZ2 \
    --query 'Subnet.SubnetId' \
    --output text)
echo "Created Subnet 2: $SUBNET_2_ID in $AZ2"

aws ec2 modify-subnet-attribute --subnet-id $SUBNET_2_ID --map-public-ip-on-launch
aws ec2 create-tags --resources $SUBNET_2_ID --tags Key=Name,Value=${NAME_PREFIX}-public-2

# Create route table
RTB_ID=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --query 'RouteTable.RouteTableId' \
    --output text)
echo "Created Route Table: $RTB_ID"

aws ec2 create-tags --resources $RTB_ID --tags Key=Name,Value=${NAME_PREFIX}-public-rt

# Add route to internet
aws ec2 create-route \
    --route-table-id $RTB_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associate subnets with route table
aws ec2 associate-route-table --route-table-id $RTB_ID --subnet-id $SUBNET_1_ID
aws ec2 associate-route-table --route-table-id $RTB_ID --subnet-id $SUBNET_2_ID

# Save IDs for cleanup
cat > .vpc-ids <<EOF
VPC_ID=$VPC_ID
IGW_ID=$IGW_ID
SUBNET_1_ID=$SUBNET_1_ID
SUBNET_2_ID=$SUBNET_2_ID
RTB_ID=$RTB_ID
EOF

echo ""
echo "=========================================="
echo "VPC Setup Complete!"
echo "=========================================="
echo "VPC ID:        $VPC_ID"
echo "IGW ID:        $IGW_ID"
echo "Subnet 1:      $SUBNET_1_ID ($AZ1)"
echo "Subnet 2:      $SUBNET_2_ID ($AZ2)"
echo "Route Table:   $RTB_ID"
echo ""
echo "Run ./cleanup.sh to delete all resources"
